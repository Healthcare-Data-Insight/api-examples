# EDI Generator Examples

This directory contains request and response examples for the EDI Generator API. The generator accepts structured JSON data and returns a complete X12 EDI document.

- `POST /api/edi/gen/835` generates an 835 Health Care Claim Payment/Advice transaction.
- `POST /api/edi/gen/837` generates an 837 Health Care Claim transaction. The examples in this directory generate professional claims (837P).

The [`request`](request/) directory contains JSON request bodies that can be submitted to the API. The [`response`](response/) directory contains the corresponding EDI text returned by the API. Minimal examples demonstrate the required data and API defaults, while all-fields examples demonstrate a more complete request model.

## 835 Payment Generation

Submit these requests to `POST /api/edi/gen/835`.

| Example | JSON Request | EDI Response |
| --- | --- | --- |
| Minimal | [835-minimal.json](request/835-minimal.json) | [835-minimal.edi](response/835-minimal.edi) |
| All fields | [835-all-fields.json](request/835-all-fields.json) | [835-all-fields.edi](response/835-all-fields.edi) |

## 837P Claim Generation

Submit these requests to `POST /api/edi/gen/837`.

| Example | JSON Request | EDI Response |
| --- | --- | --- |
| Minimal | [837p-minimal.json](request/837p-minimal.json) | [837p-minimal.edi](response/837p-minimal.edi) |
| All fields | [837p-all-fields.json](request/837p-all-fields.json) | [837p-all-fields.edi](response/837p-all-fields.edi) |

## Python Examples

The Python examples build generator requests using the generated EDI object model, submit them through the shared API helper, handle validation responses, and verify the returned EDI:

- [`generate_835_edi.py`](../python/api/generate_835_edi.py) generates an 835 payment EDI document.
- [`generate_837p_edi.py`](../python/api/generate_837p_edi.py) generates an 837 professional claim EDI document.

Run the examples from the `python/api` directory. They use the API base URL configured in [`env.py`](../python/api/env.py), which defaults to `http://localhost:5080/api`.
