import json
import edi_converter

"""
Converts 837/835 files using multipart request or by posting the file's content.
The response is an array of JSON objects or a line-delimited JSON (ndjson)
This example use ndjson as it is more convenient for streaming.
If you want to use well-formed JSON, make sure that your logic can handle large arrays if you have large EDI files.
Documentation:
https://datainsight.health/docs/ediconvert-api/reference/#tag/EDI-to-JSON
"""

# ** 837
edi_837_dir = '../../edi_files/837'
# Convert by posting the file's content
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

# Convert multiple files using multipart request
# We can convert multiple files at the same time, 837p and 837i have the same response
file_names_to_convert = ['prof-encounter.dat', 'chiro.dat', '837I-inst-claim.dat']
files_to_convert = [edi_837_dir + '/' + file_name for file_name in file_names_to_convert]
print('** Converting files:')
print(*files_to_convert)
response = edi_converter.convert_files_with_multipart(files_to_convert, True)
for claim_str in response.iter_lines():
    # each line is a claim object or could be an error/warning
    claim = json.loads(claim_str)
    if edi_converter.handle_warning_error(claim):
        continue
    file_name = claim['transaction']['fileInfo']['name']
    pcn = claim['patientControlNumber']
    charge = claim['chargeAmount']
    billing_npi = claim['billingProvider']['identifier']

    print(f'File {file_name}: Claim {pcn} from {billing_npi} for the amount {charge}')

# ** 835
# Convert multiple 835 files using multi-part request
edi_835_dir = '../../edi_files/835'
file_names_to_convert = ['claim_adj_reason.dat', 'negotiated_discount.dat']
files_to_convert = [edi_835_dir + '/' + file_name for file_name in file_names_to_convert]
print('** Converting files:')
print(*files_to_convert)
response = edi_converter.convert_files_with_multipart(files_to_convert, True)
for payment_str in response.iter_lines():
    # each line is a payment object
    payment = json.loads(payment_str)
    if edi_converter.handle_warning_error(payment):
        continue
    file_name = payment['transaction']['fileInfo']['name']
    payer_name = payment['payer']['lastNameOrOrgName']
    pcn = payment['patientControlNumber']
    charge = payment['chargeAmount']
    paid = payment['paymentAmount']

    print(f'File {file_name}: Payment from {payer_name} for claim {pcn} for the amount {paid}; Billed: {charge}')
