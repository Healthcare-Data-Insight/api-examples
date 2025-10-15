import json
import edi_converter

"""
Converts 837 files using multipart request.
The response is an array of JSON objects or a line-delimited JSON (ndjson)
This example uses ndjson as it is more convenient for streaming.
If you want to use well-formed JSON, make sure that your logic can handle large arrays if you have large EDI files.
API documentation:
https://datainsight.health/docs/ediconvert-api/reference/#tag/EDI-to-JSON
Schemas:
https://datainsight.health/docs/schemas/837p/
"""

edi_837_dir = '../../edi_files/837'

# Convert multiple files using multipart request to NDJSON
# 837p and 837i have similar response schemas (claim object)
file_names_to_convert = ['837P-all-fields.dat', '837I-all-fields.dat']
files_to_convert = [edi_837_dir + '/' + file_name for file_name in file_names_to_convert]
print('** Converting files:')
print(*files_to_convert)
response = edi_converter.convert_files_with_multipart(files_to_convert, True)
for claim_str in response.iter_lines():
    # each line is a claim object or could be an error/warning
    claim = json.loads(claim_str)
    if edi_converter.handle_warning_error(claim):
        continue
    # is this an institutional claim?
    is_inst = claim['transaction']['transactionType'] == 'INST'
    file_name = claim['transaction']['fileInfo']['name']
    pcn = claim['patientControlNumber']
    charge = claim['chargeAmount']
    billing_npi = claim['billingProvider']['identifier']
    facility_code = claim['facilityCode']['code']
    subscriber = claim['subscriber']
    payer = subscriber['payer']
    insured_person = subscriber['person']
    print(
        f'** Claim {pcn} from {billing_npi} for the amount {charge}. Facility code: {facility_code}. File {file_name}')
    print(f"Patient: {insured_person['identifier']} {insured_person['lastNameOrOrgName']}")
    print(f"Payer: {payer['identifier']} {payer['lastNameOrOrgName']}")
    for diag in claim['diags']:
        present_on_adm = ''
        if is_inst:
            present_on_adm = " POA: " + diag.get('presentOnAdmissionIndicator', 'N')
        print(f"Diagnosis: {diag['code']} {diag.get('desc')} {present_on_adm}")
    if is_inst:
        # examples of institutional codes
        if drg := claim.get('drg'):
            print(f"Billed DRG code: {drg['code']}")
        occurrences = claim.get('occurrences', [])
        for occurrence in occurrences:
            print(f"Occurrence: {occurrence['code']} {occurrence.get('desc')} {occurrence['occurrenceDate']}")
    for i, line in enumerate(claim.get('serviceLines', [])):
        line_control_number = line.get('sourceLineId', i + 1)
        line_charge = line['chargeAmount']
        procedure = line.get('procedure', {'code': None})
        rev_code = line.get('revenueCode', {'code': None})
        print(
            f"Line: {line_control_number} Billed: {line_charge} Service dates: {line.get('serviceDateFrom')} - {line.get('serviceDateTo')}")
        if procedure:
            print(f"Procedure: {procedure['code']} Quantity: {line['unitCount']}")
        if rev_code:
            print(f"Revenue code: {rev_code['code']} {rev_code.get('desc')}")

# Convert a single file by posting its content
file_to_convert = edi_837_dir + '/prof-encounter.dat'
print('** Converting ' + file_to_convert)
response = edi_converter.convert_file(file_to_convert, True)
for claim_str in response.iter_lines():
    # each line is a claim object or could be an error/warning
    claim = json.loads(claim_str)
    if edi_converter.handle_warning_error(claim):
        continue
    pcn = claim['patientControlNumber']
    charge = claim['chargeAmount']
    billing_npi = claim['billingProvider']['identifier']

    print(f'Claim {pcn} from {billing_npi} for the amount {charge}')