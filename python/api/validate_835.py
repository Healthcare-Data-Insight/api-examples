from pathlib import Path

import env
from edi_model.all_classes import ValidationIssue
from ediconvert_sdk import EdiConverterClient

"""
Validate an 835 EDI file using both validation endpoints.

This example intentionally uses the same EDI input twice so the difference
between the endpoints is easy to see:

- /edi/validate returns structured JSON that can be parsed into
  ValidationIssue objects.
- /edi/validate/text returns a human-readable text report that is convenient
  for logs, support tickets, or command-line output.

Run from this directory:

    python validate_835.py
"""

# The examples in this folder are normally run from python/api, so this path is
# written relative to that working directory. Keeping the file path visible near
# the top makes it easy to swap in another 835 file while experimenting.
EDI_FILE = Path("../../edi_files/835/835-validation-issues.edi")


def validate_as_json(client: EdiConverterClient) -> list[ValidationIssue]:
    """
    Call /edi/validate and convert the JSON response into SDK model objects.

    The endpoint returns an array of validation issue JSON objects. Parsing
    those dictionaries into ValidationIssue gives the rest of the script typed
    attributes such as issue_type, message, segment, and loop instead of
    ad-hoc dictionary lookups.
    """

    response = client.validation.to_json_file(EDI_FILE)
    return [ValidationIssue.model_validate(issue) for issue in response.json()]


def print_json_validation_issues(issues: list[ValidationIssue]) -> None:
    """
    Print a compact summary from the structured validation response.

    Applications usually use the JSON endpoint when they need to filter,
    group, store, or display validation findings in their own UI.
    """

    print("Structured validation issues from /edi/validate:")
    print(f"Found {len(issues)} issue(s).")

    for index, issue in enumerate(issues, start=1):
        # model_dump(exclude_none=True) keeps the example resilient as the
        # ValidationIssue model evolves: it prints every populated field without
        # requiring this script to know all optional field names up front.
        populated_fields = issue.model_dump(exclude_none=True)
        issue_type = populated_fields.get("issue_type", "UNKNOWN")
        message = populated_fields.get("message", "")
        segment = populated_fields.get("segment")
        loop = populated_fields.get("loop")

        location_parts = []
        if segment:
            location_parts.append(f"segment={segment}")
        if loop:
            location_parts.append(f"loop={loop}")
        location = f" ({', '.join(location_parts)})" if location_parts else ""

        print(f"{index}. {issue_type}{location}: {message}")


def validate_as_text(client: EdiConverterClient) -> str:
    """
    Call /edi/validate/text and return the text validation report.

    The optional issue_string_prefix is prepended by the API to each reported
    issue. Prefixes are handy when the text report will be mixed with other
    command-line output.
    """

    response = client.validation.to_text_file(
        EDI_FILE,
        issue_string_prefix="835 validation issue: ",
    )
    return response.text


def main() -> None:
    if not EDI_FILE.exists():
        raise FileNotFoundError(f"Sample EDI file not found: {EDI_FILE}")

    # env.api_url points at the local Docker/API instance by default:
    # http://localhost:5080/api. The SDK also supports EDICONVERT_BASE_URL and
    # EDICONVERT_API_KEY for public API usage, but this example keeps the local
    # configuration explicit like the other python/api scripts.
    client = EdiConverterClient(base_url=env.api_url)

    # First exercise /edi/validate, the structured JSON validation endpoint.
    issues = validate_as_json(client)
    print_json_validation_issues(issues)

    print()
    print("Text validation report from /edi/validate/text:")

    # Then exercise /edi/validate/text with the same file. This endpoint is
    # useful when callers want a ready-to-display report instead of structured
    # data.
    text_report = validate_as_text(client)
    print(text_report)


if __name__ == "__main__":
    main()
