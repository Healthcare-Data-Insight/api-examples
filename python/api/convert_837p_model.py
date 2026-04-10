import json
import edi_converter
from edi_converter import ObjectType
from model.prof_claim import ProfClaim
"""
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
response = edi_converter.convert_file(file_to_convert, False)
# Serialize the response into an array of objects
# Note: this requires large memory size for large files; consider a streaming parser instead
claims = response.json()
for claim_json in claims:
    # can have parser warnings in the same array
    object_type = ObjectType(claim_json['objectType'])
    if object_type in {ObjectType.ERROR, ObjectType.WARNING}:
        edi_converter.handle_warning_error(claim_json)
        continue
    pcn = claim_json['patientControlNumber']
    charge = claim_json['chargeAmount']
    billing_npi = claim_json['billingProvider']['identifier']

    print(f'Claim {pcn} from {billing_npi} for the amount {charge}')
    claim = ProfClaim.model_validate(claim_json)
    print(json.dumps(claim.model_dump(by_alias=True), indent=2))
