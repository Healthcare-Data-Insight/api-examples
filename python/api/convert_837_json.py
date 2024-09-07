import requests
import json

import env

"""
Upload 837/835 files using multipart request and get a line-delimited list of claims/payments back
"""


def convert_files(files, is_ndjson):
    """Creates a multipart request with the list of files and posts it"""
    api_url = env.api_url + '/edi/json/upload'
    # we need to pass an array of tuples (field_name, file-like obj)
    # The field name is always 'files'
    field_and_file_objects = []
    for f in files:
        field_and_file_objects.append(('files', open(f, 'rb')))
    # Always use splitTran: True for 837/835 transactions
    # If ndjson: True, the server will return a new-line separated list of objects (claims) instead of an array
    params = {'splitTran': True, 'ndjson': is_ndjson}
    # Use stream=True to stream the response instead of loading it in memory
    file_upload_response = requests.post(api_url, files=field_and_file_objects, params=params, stream=True)
    return file_upload_response


# Convert 837
edi_837_dir = '../../edi_files/837'
# We can convert multiple files at the same time, 837p and 837i have the same response
file_names_to_convert = ['prof-encounter.dat', 'chiro.dat', '837I-inst-claim.dat']
files_to_convert = [edi_837_dir + '/' + file_name for file_name in file_names_to_convert]
response = convert_files(files_to_convert, True)
if response.status_code == 200:
    for payment_str in response.iter_lines():
        # each line is a claim object
        payment = json.loads(payment_str)
        file_name = payment['transaction']['fileInfo']['name']
        pcn = payment['patientControlNumber']
        charge = payment['chargeAmount']
        billing_npi = payment['billingProvider']['identifier']

        print(f'File {file_name}: Claim {pcn} from {billing_npi} for the amount {charge}')
else:
    raise Exception(f'Error converting EDI files; Response from the server: {response.text}')

# Convert 835
edi_835_dir = '../../edi_files/835'
file_names_to_convert = ['claim_adj_reason.dat', 'negotiated_discount.dat']
files_to_convert = [edi_835_dir + '/' + file_name for file_name in file_names_to_convert]
response = convert_files(files_to_convert, True)
if response.status_code == 200:
    for payment_str in response.iter_lines():
        # each line is a payment object
        payment = json.loads(payment_str)
        file_name = payment['transaction']['fileInfo']['name']
        payer_name = payment['payer']['lastNameOrOrgName']
        pcn = payment['patientControlNumber']
        charge = payment['chargeAmount']
        paid = payment['paymentAmount']

        print(f'File {file_name}: Payment from {payer_name} for claim {pcn} for the amount {paid}; Billed: {charge}')
else:
    raise Exception(f'Error converting EDI files; Response from the server: {response.text}')




'''
response = convert_files([file_to_convert])
if response.status_code == 200:
    for claim in response.json():
        pcn = claim['patientControlNumber']
        charge = claim['chargeAmount']
        billing_npi = claim['billingProvider']['identifier']
        print('Claim {} from {} for the amount {}'.format(pcn, billing_npi, charge))

else:
    raise Exception('Error converting file ' + file_to_convert)
'''
