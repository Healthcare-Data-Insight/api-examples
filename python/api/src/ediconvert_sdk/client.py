"""Client interfaces for the Healthcare Data Insight EDI Converter API.

The main entry point is ``EdiConverterClient``. It exposes grouped clients
for conversion, generation, validation, and application-information endpoints.
"""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator
from urllib.parse import urlsplit

import requests
from edi_model.all_classes import (
    AppInfo,
    EdiGenClaimRequest,
    EdiGenPaymentRequest,
    ValidationIssue,
)
from edi_model.enums import ObjectType
from requests import Response, Session

DEFAULT_BASE_URL = "http://localhost:5080/api"
DEFAULT_API_KEY_ENV = "EDICONVERT_API_KEY"
DEFAULT_BASE_URL_ENV = "EDICONVERT_BASE_URL"

PathLike = str | os.PathLike[str]


class EdiConverterError(Exception):
    """Base class for errors raised by the EDI Converter SDK."""


class EdiConverterApiError(EdiConverterError):
    """Error raised when the API returns an unexpected HTTP status.

    Attributes:
        response: Original response returned by the API.
        status_code: HTTP status code from the response.
        body: Response body decoded as text.
    """

    def __init__(self, response: Response, message: str | None = None):
        self.response = response
        self.status_code = response.status_code
        self.body = response.text
        super().__init__(
            message
            or f"EDI Converter API request failed with status {response.status_code}: {response.text}"
        )


class EdiGenerationValidationError(EdiConverterApiError):
    """Error raised when validation prevents EDI generation.

    This exception is raised by ``GenerationClient.generate_835`` and
    ``GenerationClient.generate_837`` when ``fail_on_validation_errors`` is
    enabled and the API returns HTTP 417.

    Attributes:
        validation_issues: Validation issues returned by the API as typed
            ``edi_model.all_classes.ValidationIssue`` objects.
    """

    def __init__(self, response: Response):
        self.validation_issues = _parse_validation_issues(response)
        super().__init__(
            response,
            "EDI generation failed validation. See validation_issues for details.",
        )


class EdiConverterClient:
    """Client for the EDI Converter API.

    The client groups operations under ``conversion``, ``generation``,
    ``validation``, and ``about``. It can be used as a context manager
    so an internally created HTTP session is closed automatically.

    Example usage:

    ```python
    with EdiConverterClient("http://localhost:5080/api") as client:
        response = client.conversion.to_json_file(
            "claim.edi",
            ndjson=True,
            validate=True,
        )
        for line in response.iter_lines():
            process(line)
    ```

    Args:
        base_url: API root or server root. Both ``http://localhost:5080/api``
            and ``http://localhost:5080`` are accepted. When omitted, the client
            uses ``EDICONVERT_BASE_URL`` and then ``DEFAULT_BASE_URL``.
        api_key: API key sent in the ``X-API-Key`` header. Public API calls
            require a key; local API installations normally do not. When
            omitted, the client uses ``EDICONVERT_API_KEY`` if it is set.
        timeout: Request timeout passed to ``requests``. A number applies to
            both connection and response reads; a ``(connect, read)`` tuple
            configures them separately.
        session: Optional preconfigured ``requests.Session``. The caller owns a
            supplied session and remains responsible for closing it.
        headers: Additional headers applied to the session. The API-key header,
            when configured, is applied after these values.

    Attributes:
        base_url: Normalized base URL used for requests.
        timeout: Configured request timeout.
        session: HTTP session used by all grouped clients.
        conversion: EDI-to-JSON and EDI-to-CSV operations.
        generation: 835 and 837 generation and request-validation operations.
        validation: EDI validation operations returning JSON or annotated text.
        about: Application version and license information operation.
    """

    def __init__(
        self,
        base_url: str | None = None,
        *,
        api_key: str | None = None,
        timeout: float | tuple[float, float] = 30,
        session: Session | None = None,
        headers: dict[str, str] | None = None,
    ):
        self.base_url = (base_url or os.getenv(DEFAULT_BASE_URL_ENV) or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.session = session or requests.Session()
        self._owns_session = session is None

        if headers:
            self.session.headers.update(headers)
        api_key = api_key or os.getenv(DEFAULT_API_KEY_ENV)
        if api_key:
            self.session.headers.update({"X-API-Key": api_key})

        self.conversion = ConversionClient(self)
        self.generation = GenerationClient(self)
        self.validation = ValidationClient(self)
        self.about = AboutClient(self)

    def close(self) -> None:
        """Close the internally created HTTP session.

        A session supplied through the constructor is not closed because it is
        owned by the caller. Calling this method more than once is safe.
        """
        if self._owns_session:
            self.session.close()

    def __enter__(self) -> EdiConverterClient:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    def get(self, path: str, *, expected_statuses: set[int] | None = None) -> Response:
        """Send a low-level GET request to an API-relative path.

        Most users should prefer the grouped endpoint clients. This method is
        available for API operations that do not yet have a dedicated wrapper.

        Args:
            path: Endpoint path relative to the API root, with or without a
                leading slash.
            expected_statuses: Status codes treated as successful. Defaults to
                ``{200}``.

        Returns:
            The original ``requests.Response``.

        Raises:
            EdiConverterApiError: If the response status is not expected.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        response = self.session.get(self._url(path), timeout=self.timeout)
        self._raise_for_unexpected_status(response, expected_statuses or {200})
        return response

    def post(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        files: Any = None,
        headers: dict[str, str] | None = None,
        stream: bool = False,
        expected_statuses: set[int] | None = None,
    ) -> Response:
        """Send a low-level POST request to an API-relative path.

        Most users should prefer the grouped endpoint clients. Parameters with
        a value of ``None`` are omitted, and boolean query parameters are sent
        as lowercase ``true`` or ``false`` strings.

        Args:
            path: Endpoint path relative to the API root, with or without a
                leading slash.
            params: Query parameters.
            data: Raw request body accepted by ``requests.Session.post``.
            json: JSON-serializable request body.
            files: Multipart file data accepted by ``requests``.
            headers: Request-specific headers.
            stream: Whether response content should be downloaded lazily.
            expected_statuses: Status codes treated as successful. Defaults to
                ``{200}``.

        Returns:
            The original ``requests.Response``. When ``stream`` is true, consume
            the response body or close the response to release the connection.

        Raises:
            EdiConverterApiError: If the response status is not expected.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        response = self.session.post(
            self._url(path),
            params=_clean_params(params),
            data=data,
            json=json,
            files=files,
            headers=headers,
            stream=stream,
            timeout=self.timeout,
        )
        self._raise_for_unexpected_status(response, expected_statuses or {200})
        return response

    def _url(self, endpoint_path: str) -> str:
        path = endpoint_path if endpoint_path.startswith("/") else f"/{endpoint_path}"
        if _base_url_already_points_to_api(self.base_url):
            return f"{self.base_url}{path}"
        return f"{self.base_url}/api{path}"

    @staticmethod
    def _raise_for_unexpected_status(response: Response, expected_statuses: set[int]) -> None:
        if response.status_code in expected_statuses:
            return
        raise EdiConverterApiError(response)


class ConversionClient:
    """EDI-to-JSON and EDI-to-CSV operations.

    Instances are available through ``EdiConverterClient.conversion``.
    Conversion responses can be streamed and may contain an error after the API
    has already returned HTTP 200. JSON consumers should inspect ``objectType``;
    CSV consumers should check for lines beginning with ``ERROR:``.
    """

    def __init__(self, client: EdiConverterClient):
        self._client = client

    def to_json(
        self,
        edi_text: str | bytes,
        *,
        validate: bool | None = None,
        ndjson: bool | None = None,
        descriptions: bool | None = None,
        convert_control_segments: bool | None = None,
        transaction_top_level: bool | None = None,
        convert_to_segments: str | None = None,
        edi_file_name: str | None = None,
        chunk_size: int | None = None,
        warnings_in_response: bool | None = None,
        max_warnings: int | None = None,
        split_tran: bool | None = None,
        stream: bool = True,
    ) -> Response:
        """Convert EDI text to JSON or newline-delimited JSON.

        Args:
            edi_text: X12 EDI content as text or bytes.
            validate: Run full EDI validation and include ``VALIDATION`` objects
                in the response stream.
            ndjson: Return newline-delimited JSON instead of a JSON array. This
                is recommended for large inputs and streaming workflows.
            descriptions: Include descriptions for healthcare and EDI codes.
            convert_control_segments: Include ``INTERCHANGE_CONTROL`` and
                ``FUNCTIONAL_GROUP`` objects for ISA and GS segments.
            transaction_top_level: Emit transactions as separate top-level
                ``TRANSACTION`` objects instead of repeating transaction data in
                each business object.
            convert_to_segments: Convert to an EDI loop and segment tree instead
                of claims, payments, members, and other business objects.
            edi_file_name: Logical source name propagated to response file
                metadata. This parameter applies only to text-body requests.
            chunk_size: Number of transactions or business objects parsed and
                converted per chunk. Larger values may improve throughput while
                using more memory.
            warnings_in_response: Include parsing warnings in the response.
                Deprecated since API 2.15; use ``validate`` instead.
            max_warnings: Maximum parsing warnings allowed before processing
                stops. Deprecated since API 2.15.
            split_tran: Split 835, 837, and 834 transactions by business object.
                Deprecated because the API now selects this automatically.
            stream: Download the response body lazily. Leave enabled for large
                responses and consume or close the returned response.

        Returns:
            A ``requests.Response`` containing JSON or NDJSON conversion output.

        Raises:
            EdiConverterApiError: If the API immediately returns an unexpected
                HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        return self._client.post(
            "/edi/json",
            data=edi_text,
            headers={"Content-Type": "text/plain"},
            params={
                "validate": validate,
                "ndjson": ndjson,
                "descriptions": descriptions,
                "convertControlSegments": convert_control_segments,
                "transactionTopLevel": transaction_top_level,
                "convertToSegments": convert_to_segments,
                "ediFileName": edi_file_name,
                "chunkSize": chunk_size,
                "warningsInResponse": warnings_in_response,
                "maxWarnings": max_warnings,
                "splitTran": split_tran,
            },
            stream=stream,
        )

    def to_json_file(self, file_path: PathLike, **kwargs: Any) -> Response:
        """Convert one EDI file to JSON or NDJSON.

        Args:
            file_path: Path to the EDI file. Its path is used as
                ``edi_file_name`` unless that argument is provided explicitly.
            **kwargs: Options accepted by ``to_json``.

        Returns:
            A ``requests.Response`` containing JSON or NDJSON conversion output.

        Raises:
            OSError: If the input file cannot be opened.
            EdiConverterApiError: If the API returns an unexpected HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        file_path = Path(file_path)
        kwargs.setdefault("edi_file_name", str(file_path))
        with file_path.open("rb") as file_obj:
            return self.to_json(file_obj, **kwargs)

    def to_json_files(self, file_paths: Iterable[PathLike], **kwargs: Any) -> Response:
        """Upload and convert multiple EDI files to JSON or NDJSON.

        Files are sent as a ``multipart/form-data`` request using the ``files``
        field. Each input file should have a unique name.

        Args:
            file_paths: Paths to EDI files to upload.
            **kwargs: Conversion options accepted by ``to_json``, except
                ``edi_file_name``, which the API ignores for multipart uploads.

        Returns:
            A ``requests.Response`` containing combined conversion output.

        Raises:
            OSError: If an input file cannot be opened.
            EdiConverterApiError: If the API returns an unexpected HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        with _multipart_files(file_paths) as files:
            return self._client.post(
                "/edi/json",
                files=files,
                params={
                    "validate": kwargs.get("validate"),
                    "ndjson": kwargs.get("ndjson"),
                    "descriptions": kwargs.get("descriptions"),
                    "convertControlSegments": kwargs.get("convert_control_segments"),
                    "transactionTopLevel": kwargs.get("transaction_top_level"),
                    "convertToSegments": kwargs.get("convert_to_segments"),
                    "chunkSize": kwargs.get("chunk_size"),
                    "warningsInResponse": kwargs.get("warnings_in_response"),
                    "maxWarnings": kwargs.get("max_warnings"),
                    "splitTran": kwargs.get("split_tran"),
                },
                stream=kwargs.get("stream", True),
            )

    def to_csv(
        self,
        edi_text: str | bytes,
        *,
        schema_file_name: str | None = None,
        schema_name: str | None = None,
        edi_file_name: str | None = None,
        chunk_size: int | None = None,
        warnings_in_response: bool | None = None,
        max_warnings: int | None = None,
        stream: bool = True,
    ) -> Response:
        """Convert EDI text to CSV.

        Args:
            edi_text: X12 EDI content as text or bytes.
            schema_file_name: Name of the API-side CSV schema configuration
                file. The API default is ``csv_conversion.yaml``.
            schema_name: Schema within the CSV configuration file. The API
                default is ``lines-with-header-repeat-first-row``.
            edi_file_name: Logical source name propagated to the ``fileName``
                CSV column. This parameter applies only to text-body requests.
            chunk_size: Number of claims, payments, or members parsed at once.
                Larger values may improve throughput while using more memory.
            warnings_in_response: Write warnings into the first CSV column with
                a ``WARNING:`` prefix. Deprecated; use EDI text validation.
            max_warnings: Maximum parsing warnings allowed before processing
                stops. This API parameter is deprecated.
            stream: Download the response body lazily. Leave enabled for large
                responses and consume or close the returned response.

        Returns:
            A ``requests.Response`` containing streamed CSV text.

        Raises:
            EdiConverterApiError: If the API immediately returns an unexpected
                HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        return self._client.post(
            "/edi/csv",
            data=edi_text,
            headers={"Content-Type": "text/plain"},
            params={
                "schemaFileName": schema_file_name,
                "schemaName": schema_name,
                "ediFileName": edi_file_name,
                "chunkSize": chunk_size,
                "warningsInResponse": warnings_in_response,
                "maxWarnings": max_warnings,
            },
            stream=stream,
        )

    def to_csv_file(self, file_path: PathLike, **kwargs: Any) -> Response:
        """Convert one EDI file to CSV.

        Args:
            file_path: Path to the EDI file. Its path is used as
                ``edi_file_name`` unless that argument is provided explicitly.
            **kwargs: Options accepted by ``to_csv``.

        Returns:
            A ``requests.Response`` containing streamed CSV text.

        Raises:
            OSError: If the input file cannot be opened.
            EdiConverterApiError: If the API returns an unexpected HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        file_path = Path(file_path)
        kwargs.setdefault("edi_file_name", str(file_path))
        with file_path.open("rb") as file_obj:
            return self.to_csv(file_obj, **kwargs)

    def to_csv_files(self, file_paths: Iterable[PathLike], **kwargs: Any) -> Response:
        """Upload and convert multiple EDI files to CSV.

        Files are sent as a ``multipart/form-data`` request using the ``files``
        field. Each input file should have a unique name.

        Args:
            file_paths: Paths to EDI files to upload.
            **kwargs: Conversion options accepted by ``to_csv``, except
                ``edi_file_name``, which the API ignores for multipart uploads.

        Returns:
            A ``requests.Response`` containing combined CSV output.

        Raises:
            OSError: If an input file cannot be opened.
            EdiConverterApiError: If the API returns an unexpected HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        with _multipart_files(file_paths) as files:
            return self._client.post(
                "/edi/csv",
                files=files,
                params={
                    "schemaFileName": kwargs.get("schema_file_name"),
                    "schemaName": kwargs.get("schema_name"),
                    "chunkSize": kwargs.get("chunk_size"),
                    "warningsInResponse": kwargs.get("warnings_in_response"),
                    "maxWarnings": kwargs.get("max_warnings"),
                },
                stream=kwargs.get("stream", True),
            )


class GenerationClient:
    """835 and 837 EDI generation operations.

    Instances are available through ``EdiConverterClient.generation``.
    Request bodies may be SDK Pydantic models or dictionaries that match the
    corresponding API request schema.
    """

    def __init__(self, client: EdiConverterClient):
        self._client = client

    def generate_837(
        self,
        request: EdiGenClaimRequest | dict[str, Any],
        *,
        fail_on_validation_errors: bool | None = None,
        file_name: str | None = None,
    ) -> str:
        """Generate an X12 837P or 837I document.

        Args:
            request: Claim-generation request as an ``EdiGenClaimRequest`` or a
                dictionary matching that model.
            fail_on_validation_errors: Ask the API to return HTTP 417 instead of
                EDI when validation issues are found.
            file_name: Logical file name used in validation issues and errors.
                The API generates a random name when this is omitted.

        Returns:
            Generated 837 EDI text.

        Raises:
            EdiGenerationValidationError: If validation prevents generation.
            EdiConverterApiError: If the API returns another unexpected status.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        response = self.generate_837_response(
            request,
            fail_on_validation_errors=fail_on_validation_errors,
            file_name=file_name,
        )
        if response.status_code == 417:
            raise EdiGenerationValidationError(response)
        return response.text

    def generate_837_response(
        self,
        request: EdiGenClaimRequest | dict[str, Any],
        *,
        fail_on_validation_errors: bool | None = None,
        file_name: str | None = None,
    ) -> Response:
        """Generate an X12 837 document and return the complete HTTP response.

        Unlike ``generate_837``, this method does not raise
        ``EdiGenerationValidationError`` for HTTP 417. Callers can inspect
        ``response.status_code`` and parse validation issues from the response.

        Args:
            request: Claim-generation request as an ``EdiGenClaimRequest`` or a
                dictionary matching that model.
            fail_on_validation_errors: Ask the API to return HTTP 417 instead of
                EDI when validation issues are found.
            file_name: Logical file name used in validation issues and errors.

        Returns:
            A ``requests.Response`` with EDI text for HTTP 200 or validation
            issue JSON for HTTP 417.

        Raises:
            EdiConverterApiError: If the API returns a status other than 200 or
                417.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        return self._client.post(
            "/edi/gen/837",
            json=_request_json(request),
            params={
                "failOnValidationErrors": fail_on_validation_errors,
                "fileName": file_name,
            },
            expected_statuses={200, 417},
        )

    def validate_837(
        self,
        request: EdiGenClaimRequest | dict[str, Any],
        *,
        file_name: str | None = None,
    ) -> list[ValidationIssue]:
        """Validate an 837 generation request without generating EDI.

        Args:
            request: Claim-generation request as an ``EdiGenClaimRequest`` or a
                dictionary matching that model.
            file_name: Logical file name used in validation issues and errors.

        Returns:
            Typed validation issues. The list is empty when no issues are found.

        Raises:
            EdiConverterApiError: If the API returns an unexpected HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
            pydantic.ValidationError: If a returned validation issue does not
                match the SDK model.
        """
        response = self._client.post(
            "/edi/gen/837/validate",
            json=_request_json(request),
            params={"fileName": file_name},
        )
        return _parse_validation_issues(response)

    def generate_835(
        self,
        request: EdiGenPaymentRequest | dict[str, Any],
        *,
        fail_on_validation_errors: bool | None = None,
        file_name: str | None = None,
    ) -> str:
        """Generate an X12 835 document.

        Args:
            request: Payment-generation request as an
                ``EdiGenPaymentRequest`` or a dictionary matching that model.
            fail_on_validation_errors: Ask the API to return HTTP 417 instead of
                EDI when validation issues are found.
            file_name: Logical file name used in validation issues and errors.
                The API generates a random name when this is omitted.

        Returns:
            Generated 835 EDI text.

        Raises:
            EdiGenerationValidationError: If validation prevents generation.
            EdiConverterApiError: If the API returns another unexpected status.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        response = self.generate_835_response(
            request,
            fail_on_validation_errors=fail_on_validation_errors,
            file_name=file_name,
        )
        if response.status_code == 417:
            raise EdiGenerationValidationError(response)
        return response.text

    def generate_835_response(
        self,
        request: EdiGenPaymentRequest | dict[str, Any],
        *,
        fail_on_validation_errors: bool | None = None,
        file_name: str | None = None,
    ) -> Response:
        """Generate an X12 835 document and return the complete HTTP response.

        Unlike ``generate_835``, this method does not raise
        ``EdiGenerationValidationError`` for HTTP 417. Callers can inspect
        ``response.status_code`` and parse validation issues from the response.

        Args:
            request: Payment-generation request as an
                ``EdiGenPaymentRequest`` or a dictionary matching that model.
            fail_on_validation_errors: Ask the API to return HTTP 417 instead of
                EDI when validation issues are found.
            file_name: Logical file name used in validation issues and errors.

        Returns:
            A ``requests.Response`` with EDI text for HTTP 200 or validation
            issue JSON for HTTP 417.

        Raises:
            EdiConverterApiError: If the API returns a status other than 200 or
                417.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        return self._client.post(
            "/edi/gen/835",
            json=_request_json(request),
            params={
                "failOnValidationErrors": fail_on_validation_errors,
                "fileName": file_name,
            },
            expected_statuses={200, 417},
        )

    def validate_835(
        self,
        request: EdiGenPaymentRequest | dict[str, Any],
        *,
        file_name: str | None = None,
    ) -> list[ValidationIssue]:
        """Validate an 835 generation request without generating EDI.

        Args:
            request: Payment-generation request as an
                ``EdiGenPaymentRequest`` or a dictionary matching that model.
            file_name: Logical file name used in validation issues and errors.

        Returns:
            Typed validation issues. The list is empty when no issues are found.

        Raises:
            EdiConverterApiError: If the API returns an unexpected HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
            pydantic.ValidationError: If a returned validation issue does not
                match the SDK model.
        """
        response = self._client.post(
            "/edi/gen/835/validate",
            json=_request_json(request),
            params={"fileName": file_name},
        )
        return _parse_validation_issues(response)


class ValidationClient:
    """EDI validation operations.

    Instances are available through ``EdiConverterClient.validation``.
    Validation can return structured issue objects as JSON/NDJSON or the
    original EDI text annotated with issue lines.
    """

    def __init__(self, client: EdiConverterClient):
        self._client = client

    def to_json(
        self,
        edi_text: str | bytes,
        *,
        file_name: str | None = None,
        ndjson: bool | None = None,
        chunk_size: int | None = None,
        stream: bool = False,
    ) -> Response:
        """Validate EDI text and return validation issues as JSON or NDJSON.

        Args:
            edi_text: X12 EDI content as text or bytes.
            file_name: Logical file name used in validation issues and errors.
                The API generates a random name when this is omitted.
            ndjson: Return one JSON issue per line instead of a JSON array. This
                is recommended for large inputs and streaming workflows.
            chunk_size: Number of transactions or business objects validated per
                chunk. Larger values may improve throughput while using more
                memory.
            stream: Download the response body lazily. Consume or close a
                streamed response to release the connection.

        Returns:
            A ``requests.Response`` containing a JSON array or NDJSON stream of
            validation issues. A valid document produces an empty result.

        Raises:
            EdiConverterApiError: If the API returns an unexpected HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        return self._client.post(
            "/edi/validate",
            data=edi_text,
            headers={"Content-Type": "text/plain"},
            params={
                "fileName": file_name,
                "ndjson": ndjson,
                "chunkSize": chunk_size,
            },
            stream=stream,
        )

    def to_json_file(self, file_path: PathLike, **kwargs: Any) -> Response:
        """Validate one EDI file and return issues as JSON or NDJSON.

        Args:
            file_path: Path to the EDI file. Its path is used as ``file_name``
                unless that argument is provided explicitly.
            **kwargs: Options accepted by ``to_json``.

        Returns:
            A ``requests.Response`` containing validation issues.

        Raises:
            OSError: If the input file cannot be opened.
            EdiConverterApiError: If the API returns an unexpected HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        file_path = Path(file_path)
        kwargs.setdefault("file_name", str(file_path))
        with file_path.open("rb") as file_obj:
            return self.to_json(file_obj, **kwargs)

    def to_json_files(self, file_paths: Iterable[PathLike], **kwargs: Any) -> Response:
        """Upload and validate multiple EDI files as JSON or NDJSON.

        Files are sent as a ``multipart/form-data`` request using the ``files``
        field. Each input file should have a unique name.

        Args:
            file_paths: Paths to EDI files to upload.
            **kwargs: Validation options accepted by ``to_json``, except
                ``file_name``, which is not used for multipart uploads.

        Returns:
            A ``requests.Response`` containing combined validation issues.

        Raises:
            OSError: If an input file cannot be opened.
            EdiConverterApiError: If the API returns an unexpected HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        with _multipart_files(file_paths) as files:
            return self._client.post(
                "/edi/validate",
                files=files,
                params={
                    "ndjson": kwargs.get("ndjson"),
                    "chunkSize": kwargs.get("chunk_size"),
                },
                stream=kwargs.get("stream", False),
            )

    def to_text(
        self,
        edi_text: str | bytes,
        *,
        issue_string_prefix: str | None = None,
        stream: bool = True,
    ) -> Response:
        """Validate EDI text and return an annotated EDI document.

        The response contains the submitted EDI with validation messages placed
        below the affected segments.

        Args:
            edi_text: X12 EDI content as text or bytes.
            issue_string_prefix: Prefix for validation-message lines. The API
                default is ``!!``.
            stream: Download the response body lazily. Consume or close a
                streamed response to release the connection.

        Returns:
            A ``requests.Response`` containing annotated EDI text.

        Raises:
            EdiConverterApiError: If the API returns an unexpected HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        return self._client.post(
            "/edi/validate/text",
            data=edi_text,
            headers={"Content-Type": "text/plain"},
            params={"issueStringPrefix": issue_string_prefix},
            stream=stream,
        )

    def to_text_file(self, file_path: PathLike, **kwargs: Any) -> Response:
        """Validate one EDI file and return annotated EDI text.

        Args:
            file_path: Path to the EDI file.
            **kwargs: Options accepted by ``to_text``.

        Returns:
            A ``requests.Response`` containing annotated EDI text.

        Raises:
            OSError: If the input file cannot be opened.
            EdiConverterApiError: If the API returns an unexpected HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        file_path = Path(file_path)
        with file_path.open("rb") as file_obj:
            return self.to_text(file_obj, **kwargs)

    def to_text_files(self, file_paths: Iterable[PathLike], **kwargs: Any) -> Response:
        """Upload and validate multiple EDI files as annotated text.

        Files are sent as a ``multipart/form-data`` request using the ``files``
        field. Each input file should have a unique name.

        Args:
            file_paths: Paths to EDI files to upload.
            **kwargs: Options accepted by ``to_text``.

        Returns:
            A ``requests.Response`` containing combined annotated EDI text.

        Raises:
            OSError: If an input file cannot be opened.
            EdiConverterApiError: If the API returns an unexpected HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
        """
        with _multipart_files(file_paths) as files:
            return self._client.post(
                "/edi/validate/text",
                files=files,
                params={"issueStringPrefix": kwargs.get("issue_string_prefix")},
                stream=kwargs.get("stream", True),
            )


class AboutClient:
    """Application version and license-information operation.

    Instances are available through ``EdiConverterClient.about``.
    """

    def __init__(self, client: EdiConverterClient):
        self._client = client

    def get(self) -> AppInfo:
        """Return information about the API server and its license.

        Returns:
            Application information parsed into an ``AppInfo`` model.

        Raises:
            EdiConverterApiError: If the API returns an unexpected HTTP status.
            requests.RequestException: If the HTTP request cannot be completed.
            pydantic.ValidationError: If the response does not match ``AppInfo``.
        """
        return AppInfo.model_validate(self._client.get("/about").json())


def handle_warning_error(obj: dict[str, Any]) -> bool | None:
    """Handle a warning, validation issue, or parsing error response object.

    This helper is intended for objects read from JSON or NDJSON conversion
    streams. Warnings and validation issues are printed and marked as handled;
    parsing errors raise an SDK exception. Business objects are left untouched.

    Args:
        obj: Decoded conversion object containing an ``objectType`` field.

    Returns:
        ``True`` when a warning or validation issue was handled, otherwise
        ``None`` for a normal business object.

    Raises:
        EdiConverterError: If ``objectType`` is ``ERROR``.
        KeyError: If a required response field is missing.
        ValueError: If ``objectType`` is not recognized by the SDK enum.
    """
    object_type = ObjectType(obj["objectType"])
    if object_type == ObjectType.ERROR:
        raise EdiConverterError(f"Error parsing EDI; Error: {obj}")
    if object_type == ObjectType.WARNING:
        file_name = obj["fileName"]
        message = obj["message"]
        print(f"Encountered parsing issue with file {file_name}. Warning: {message}")
        return True
    if object_type == ObjectType.VALIDATION:
        print(obj)
        return True
    return None


def _base_url_already_points_to_api(base_url: str) -> bool:
    return urlsplit(base_url).path.rstrip("/").endswith("/api")


def _clean_params(params: dict[str, Any] | None) -> dict[str, Any] | None:
    if not params:
        return None
    cleaned: dict[str, Any] = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, bool):
            cleaned[key] = "true" if value else "false"
        else:
            cleaned[key] = value
    return cleaned or None


def _request_json(request: Any) -> Any:
    if hasattr(request, "model_dump"):
        return request.model_dump(by_alias=True, exclude_none=True, mode="json")
    return request


def _parse_validation_issues(response: Response) -> list[ValidationIssue]:
    return [ValidationIssue.model_validate(issue) for issue in response.json()]


@contextmanager
def _multipart_files(file_paths: Iterable[PathLike]) -> Iterator[list[tuple[str, Any]]]:
    opened_files = []
    try:
        for file_path in file_paths:
            opened_files.append(Path(file_path).open("rb"))
        yield [("files", file_obj) for file_obj in opened_files]
    finally:
        for file_obj in opened_files:
            file_obj.close()