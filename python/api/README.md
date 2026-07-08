# Python API Examples

This directory contains Python examples for working with the EDI Converter API and the Viewer-style search/upload endpoints exposed by a local API instance.

The scripts are intentionally simple. They show how to:

- post EDI files directly to conversion endpoints
- upload multiple files with multipart requests
- stream large JSON or CSV responses
- inspect parsed claims, payments, eligibility, claim status, and enrollment data
- work with generated Python object model classes instead of raw JSON dictionaries
- generate EDI from object model instances

## Project Layout

- `src/ediconvert_sdk/`: reusable SDK client package for conversion, generation, validation, and application-info endpoints.
- `env.py`: local API base URL configuration.
- `convert_*.py`: object model examples for converting or parsing EDI files.
- `convert_*_dict.py`: raw JSON dictionary versions of selected conversion examples.
- `src/edi_model/`: generated Pydantic object model classes used by the model-based examples.
- `out/`: output directory used by CSV streaming examples.

## Prerequisites

These examples assume:

- Python 3.10+.
- A local EDI Converter API is running and reachable at `http://localhost:5080/api`.
- Sample EDI files from this repository are available under `../../edi_files` relative to this folder.

The code imports these packages:

- `requests`
- `pandas`
- `requests-toolbelt`
- `pydantic`

Create a virtual environment and install them:

```bash
python -m venv .venv
source .venv/bin/activate
pip install requests pandas requests-toolbelt pydantic
```

## Configuration

The API URL is defined in `env.py`:

```python
api_url = 'http://localhost:5080/api'
```

Update that value if your API is running elsewhere.

New code should create an SDK client explicitly:

```python
from ediconvert_sdk import EdiConverterClient

client = EdiConverterClient(base_url="http://localhost:5080/api")
response = client.conversion.to_json_files(["../../edi_files/837/837P-all-fields.dat"], ndjson=True)
edi_text = client.generation.generate_835(payment_request)
```

## Important Runtime Assumptions

Most scripts use relative paths such as `../../edi_files/837/...`, so run them from `python/api`:

```bash
python convert_837.py
```

If you run a script from a different working directory, the sample file paths will likely fail.

## Object Model vs Raw JSON Dictionaries

The main conversion examples use generated Pydantic classes from `src/edi_model/`.
They still receive JSON from the API, but immediately validate it into typed objects such as `ProfClaim`, `InstClaim`, `Payment`, and `MemberCoverage`.

Examples without a suffix use the object model:

- `convert_837.py`
- `convert_837_single_file.py`
- `convert_835.py`
- `convert_834.py`
- `generate_837p_edi.py`
- `transform_837p.py`

Some examples also have a raw JSON dictionary variant with a `_dict` suffix:

- `convert_837_dict.py`
- `convert_837_dict_single_file.py`
- `convert_835_dict.py`
- `convert_834_dict.py`

Use the object model examples first. Use the `_dict` examples only when you specifically want to inspect the API response as plain Python dictionaries or build your own mapping layer.

## Example Categories

### Object Model JSON Conversion

- `convert_837.py`: converts multiple 837P/837I files to NDJSON and validates claims as `ProfClaim` or `InstClaim` objects.
- `convert_837_single_file.py`: converts one 837 file and validates the response as a `ProfClaim` object.
- `convert_835.py`: converts 835 files to NDJSON and validates claim payments and provider-level adjustments as object model classes.
- `convert_834.py`: converts 834 enrollment files and validates member coverage objects.
- `generate_837p_edi.py`: builds an `EdiGenClaimRequest` with object model classes and generates 837P EDI.
- `transform_837p.py`: converts an existing 837P claim into an object model request and posts it back to the generator endpoint.

These scripts use `/edi/json` and demonstrate:

- multipart upload for multiple files
- direct streaming of a single file
- NDJSON processing with `response.iter_lines()`
- object model validation with generated Pydantic classes
- parser warning/error handling via `objectType`

### Raw JSON Dictionary Conversion

- `convert_837_dict.py`: raw dictionary version of `convert_837.py`.
- `convert_837_dict_single_file.py`: raw dictionary version of `convert_837_single_file.py`.
- `convert_835_dict.py`: raw dictionary version of `convert_835.py`.
- `convert_834_dict.py`: raw dictionary version of `convert_834.py`.

These scripts use the same API endpoints as the object model examples, but leave the response as plain dictionaries from `json.loads(...)`.

### CSV Conversion

- `convert_835_csv.py`: converts 835 files to CSV, reads them with `csv` and `pandas`, and shows how to stream large responses to disk.
- `convert_835_csv_error.py`: a troubleshooting-oriented example for reading CSV output that contains parsing errors.

These scripts use `/edi/csv` and demonstrate:

- all-fields conversion
- named schema selection such as `key-fields`
- streaming response bodies to `./out/*.csv`
- row-level error/warning inspection

### Raw Parse Examples

- `convert_271.py`: parses a 271 eligibility response into hierarchical segment JSON.
- `convert_277.py`: parses a 277 claim status response and walks payer/provider/patient status loops.
- `parse_in_mem_837.py`: calls the deprecated `/edi/parse` endpoint for a small 837 file.
- `parse_edi_277_from_users.py`: older `/edi/parse` example against a user-supplied 277 sample.

Use these as segment-tree traversal examples. For large files, the conversion endpoints are the better fit.

### Claim Insight/EDI Viewer API Examples

The `viewer/` directory shows how to work with stored data after files have been ingested:

- `upload_delete_files.py`: uploads files to `/files`, triggers analytics rebuild, fetches claims, then deletes the files.
- `get_files.py`: lists recently loaded files and fetches claims for each file.
- `search_claims.py`: paginated claim search using `/claims`.
- `get_claim.py`: fetches a claim by business keys and then by internal ID.
- `search_payments.py`: paginated payment search using `/payments`.
- `get_payment.py`: fetches payments by payer control number or patient control number plus payee ID.
- `analytics_top_codes.py`: retrieves top procedure and diagnosis codes by charge amount.

These examples assume the API has indexed data available, typically after files were uploaded through the `/files` endpoint.

## Typical Usage

Run a conversion example:

```bash
python convert_837.py
python convert_835.py
python convert_834.py
```

Run a CSV example:

```bash
python convert_835_csv.py
```
Generate 837P EDI from object model classes:

```bash
python generate_837p_edi.py
```

Build, install, and test the SDK locally:

```bash
./build_and_test_sdk.sh
```

## Notes and Caveats

- `env.py` is a hardcoded local configuration file for examples. The SDK client also accepts a `base_url` argument and the `EDICONVERT_BASE_URL` environment variable.
- Public API calls can pass `api_key` to `EdiConverterClient` or set the `EDICONVERT_API_KEY` environment variable. Local API calls do not require an API key.
- Several scripts print results directly and are meant as examples, not reusable library code.
- `parse_in_mem_837.py` and `parse_edi_277_from_users.py` use the deprecated `/edi/parse` endpoint.
- `convert_835_csv_error.py` includes a hardcoded file path outside this project and is best treated as a reference/debug script.
- `_dict` examples intentionally use raw Python dictionaries; the same examples without `_dict` are the preferred object model versions.
- Some viewer scripts use fixed search parameters or IDs that may not match your local dataset.

## Recommended Starting Points

If you are new to this folder, start with:

1. `convert_837.py` for streamed NDJSON claim conversion with object model classes.
2. `convert_835_csv.py` for CSV export and streaming-to-disk patterns.
3. `generate_837p_edi.py` if you want to generate 837P EDI from object model classes.
