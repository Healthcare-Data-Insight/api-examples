from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator
from urllib.parse import urlsplit

import requests
from requests import Response, Session

from edi_model.all_classes import (
    AppInfo,
    EdiGenClaimRequest,
    EdiGenPaymentRequest,
    ValidationIssue,
)

DEFAULT_BASE_URL = "http://localhost:5080/api"
DEFAULT_API_KEY_ENV = "EDICONVERT_API_KEY"
DEFAULT_BASE_URL_ENV = "EDICONVERT_BASE_URL"

PathLike = str | os.PathLike[str]


class EdiConverterError(Exception):
    """Base exception for SDK errors."""


class EdiConverterApiError(EdiConverterError):
    """Raised when the API returns an unexpected HTTP status."""

    def __init__(self, response: Response, message: str | None = None):
        self.response = response
        self.status_code = response.status_code
        self.body = response.text
        super().__init__(
            message
            or f"EDI Converter API request failed with status {response.status_code}: {response.text}"
        )


class EdiGenerationValidationError(EdiConverterApiError):
    """Raised when generation fails because validation issues were found."""

    def __init__(self, response: Response):
        self.validation_issues = _parse_validation_issues(response)
        super().__init__(
            response,
            "EDI generation failed validation. See validation_issues for details.",
        )


class EdiConverterClient:
    """
    Client for the EDI Converter API.

    base_url can point either at the API root, such as
    http://localhost:5080/api, or the server root, such as
    http://localhost:5080. Public API calls can pass api_key or set
    EDICONVERT_API_KEY.
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
        if self._owns_session:
            self.session.close()

    def __enter__(self) -> EdiConverterClient:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        self.close()

    def get(self, path: str, *, expected_statuses: set[int] | None = None) -> Response:
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
    """EDI conversion endpoints."""

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
        file_path = Path(file_path)
        kwargs.setdefault("edi_file_name", str(file_path))
        with file_path.open("rb") as file_obj:
            return self.to_json(file_obj, **kwargs)

    def to_json_files(self, file_paths: Iterable[PathLike], **kwargs: Any) -> Response:
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
        file_path = Path(file_path)
        kwargs.setdefault("edi_file_name", str(file_path))
        with file_path.open("rb") as file_obj:
            return self.to_csv(file_obj, **kwargs)

    def to_csv_files(self, file_paths: Iterable[PathLike], **kwargs: Any) -> Response:
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
    """EDI generation endpoints."""

    def __init__(self, client: EdiConverterClient):
        self._client = client

    def generate_837(
        self,
        request: EdiGenClaimRequest | dict[str, Any],
        *,
        fail_on_validation_errors: bool | None = None,
        file_name: str | None = None,
    ) -> str:
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
        response = self._client.post(
            "/edi/gen/835/validate",
            json=_request_json(request),
            params={"fileName": file_name},
        )
        return _parse_validation_issues(response)


class ValidationClient:
    """EDI validation endpoints."""

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
        file_path = Path(file_path)
        kwargs.setdefault("file_name", str(file_path))
        with file_path.open("rb") as file_obj:
            return self.to_json(file_obj, **kwargs)

    def to_json_files(self, file_paths: Iterable[PathLike], **kwargs: Any) -> Response:
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
        return self._client.post(
            "/edi/validate/text",
            data=edi_text,
            headers={"Content-Type": "text/plain"},
            params={"issueStringPrefix": issue_string_prefix},
            stream=stream,
        )

    def to_text_file(self, file_path: PathLike, **kwargs: Any) -> Response:
        file_path = Path(file_path)
        with file_path.open("rb") as file_obj:
            return self.to_text(file_obj, **kwargs)

    def to_text_files(self, file_paths: Iterable[PathLike], **kwargs: Any) -> Response:
        with _multipart_files(file_paths) as files:
            return self._client.post(
                "/edi/validate/text",
                files=files,
                params={"issueStringPrefix": kwargs.get("issue_string_prefix")},
                stream=kwargs.get("stream", True),
            )


class AboutClient:
    """Application information endpoint."""

    def __init__(self, client: EdiConverterClient):
        self._client = client

    def get(self) -> AppInfo:
        return AppInfo.model_validate(self._client.get("/about").json())


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
