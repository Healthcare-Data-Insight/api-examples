import json

import env
from edi_model.all_classes import Code, InstClaim, ProfClaim, Transaction837
from ediconvert_sdk import EdiConverterClient, handle_warning_error

"""
Converts 837 files using multipart request.
The response is an array of JSON objects or a line-delimited JSON (ndjson).
This example uses ndjson as it is more convenient for streaming.
We use the 837 claim objects to deserialize the response.

API documentation:
https://datainsight.health/docs/ediconvert-api/reference/#tag/EDI-to-JSON
Schemas:
https://datainsight.health/docs/schemas/837p/
"""

edi_837_dir = '../../edi_files/837'

# Convert multiple files using multipart request to NDJSON
# 837p and 837i have similar response schemas (claim object)
file_names_to_convert = ['837P-all-fields.dat', '837I-all-fields.dat', '837P-validation-issues.edi']
files_to_convert = [edi_837_dir + '/' + file_name for file_name in file_names_to_convert]
print('** Converting files:')
print(*files_to_convert)
client = EdiConverterClient(base_url=env.api_url)
response = client.conversion.to_json_files(files_to_convert, ndjson=True, validate=True)
for claim_str in response.iter_lines():
    # each line is a claim object or could be an error/warning
    claim_json = json.loads(claim_str)
    if handle_warning_error(claim_json):
        continue
    # You can skip this if you know your claim type
    transaction_json = claim_json.get('transaction', {})
    # is this an institutional claim?
    is_inst = transaction_json.get('transactionType') == 'INST'
    if is_inst:
        claim = InstClaim.model_validate(claim_json)
    else:
        claim = ProfClaim.model_validate(claim_json)
    # print validation issues for this claim
    if claim.validation_issues:
        print(f'Validation issues for claim {claim.patient_control_number}:')
        for issue in claim.validation_issues:
            print(issue)
    transaction = claim.transaction or Transaction837()
    file_name = transaction.file_info.name if transaction.file_info else None
    pcn = claim.patient_control_number
    charge = claim.charge_amount
    billing_npi = claim.billing_provider.identifier
    facility_code = claim.facility_code.code
    subscriber = claim.subscriber
    payer = subscriber.payer
    insured_person = subscriber.person
    print(
        f'** Claim {pcn} from {billing_npi} for the amount {charge}. Facility code: {facility_code}. File {file_name}')
    print(f"Patient: {insured_person.identifier} {insured_person.last_name_or_org_name}")
    print(f"Payer: {payer.identifier} {payer.last_name_or_org_name}")
    for diag in claim.diags:
        present_on_adm = ''
        if is_inst:
            present_on_adm = " POA: " + (diag.present_on_admission_indicator or 'N')
        print(f"Diagnosis: {diag.code} {diag.desc} {present_on_adm}")
    if is_inst:
        # examples of institutional codes
        if drg := claim.drg:
            print(f"Billed DRG code: {drg.code}")
        for occurrence in claim.occurrences:
            print(f"Occurrence: {occurrence.code} {occurrence.desc} {occurrence.occurrence_date}")
    for i, line in enumerate(claim.service_lines):
        line_control_number = line.source_line_id or i + 1
        line_charge = line.charge_amount
        procedure = line.procedure or Code(code=None)
        rev_code = getattr(line, 'revenue_code', None) or Code(code=None)
        print(
            f"Line: {line_control_number} Billed: {line_charge} Service dates: {line.service_date_from} - {line.service_date_to}")
        if procedure:
            print(f"Procedure: {procedure.code} Quantity: {line.unit_count}")
        if rev_code:
            print(f"Revenue code: {rev_code.code} {rev_code.desc}")
