import env
from ediconvert_sdk import EdiConverterClient, handle_warning_error

"""
This example does not use the object model, it relies on the raw JSON response and Python dictionaries.
Use it only if you want to avoid dependency on the object model and want to build your own logic.
See convert_837_single_file.py for an example that uses the object model.

Converts an 837 file by posting the file's content.
The response is an array of JSON objects.
API documentation:
https://datainsight.health/docs/ediconvert-api/reference/#tag/EDI-to-JSON
Schemas:
https://datainsight.health/docs/schemas/837p/
"""

edi_837_dir = '../../edi_files/837'

# Convert a single file by posting its content
file_to_convert = edi_837_dir + '/837P-all-fields.dat'
print('** Converting ' + file_to_convert)
client = EdiConverterClient(base_url=env.api_url)
response = client.conversion.to_json_file(file_to_convert, ndjson=False, validate=True)
# Serialize the response into an array of objects
# Note: this requires large memory size for large files; consider a streaming parser instead
claims = response.json()
for claim in claims:
    if handle_warning_error(claim):
        continue
    pcn = claim['patientControlNumber']
    charge = claim['chargeAmount']
    billing_npi = claim['billingProvider']['identifier']

    print(f'Claim {pcn} from {billing_npi} for the amount {charge}')
    # See "convert_837_json" for more details on how to parse other fields
