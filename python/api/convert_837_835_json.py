import requests
import json

import env

"""
Converts 837/835 files using multipart request or by posting the file's content.
The response is an array of JSON objects or a line-delimited JSON (ndjson)
This example use ndjson as it is more convenient for streaming.
If you want to use well-formed JSON, make sure that your logic can handle large arrays if you have large EDI files.
Documentation:
https://datainsight.health/clinsight/swagger-ui/index.html#/EDI-to-JSON%20Parsing%20and%20Conversion
"""


def convert_files_using_multipart_upload(files, is_ndjson):
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
    api_response = requests.post(api_url, files=field_and_file_objects, params=params, stream=True)
    if api_response.status_code != 200:
        raise Exception(f'Error parsing EDI; Error: {api_response.text}')
    return api_response


def convert_file_using_post_text(file, is_ndjson):
    """Open file and post the content"""
    api_url = env.api_url + '/edi/json'
    # Always use splitTran: True for 837/835 transactions
    # If ndjson: True, the server will return a new-line separated list of objects (claims) instead of an array
    params = {'splitTran': True, 'ndjson': is_ndjson}

    with open(file) as f:
        # Use stream=True to stream the response instead of loading it in memory
        # Note that we're posing the file-like object instead of reading the file into memory
        # This allows for streaming content to the server
        api_response = requests.post(api_url, data=f, params=params, stream=True)
        if api_response.status_code != 200:
            raise Exception(f'Error parsing EDI; Error: {api_response.text}')
    return api_response


# ** 837
# Multi-part upload
edi_837_dir = '../../edi_files/837'
# We can convert multiple files at the same time, 837p and 837i have the same response
file_names_to_convert = ['prof-encounter.dat', 'chiro.dat', '837I-inst-claim.dat']
files_to_convert = [edi_837_dir + '/' + file_name for file_name in file_names_to_convert]
print('** Converting files:')
print(*files_to_convert)
response = convert_files_using_multipart_upload(files_to_convert, True)
for claim_str in response.iter_lines():
    # each line is a claim object
    claim = json.loads(claim_str)
    file_name = claim['transaction']['fileInfo']['name']
    pcn = claim['patientControlNumber']
    charge = claim['chargeAmount']
    billing_npi = claim['billingProvider']['identifier']

    print(f'File {file_name}: Claim {pcn} from {billing_npi} for the amount {charge}')

# Convert by posting the file's content
file_to_convert = edi_837_dir + '/prof-encounter.dat'
print('** Converting ' + file_to_convert)
response = convert_file_using_post_text(file_to_convert, True)
for claim_str in response.iter_lines():
    # each line is a claim object
    claim = json.loads(claim_str)
    pcn = claim['patientControlNumber']
    charge = claim['chargeAmount']
    billing_npi = claim['billingProvider']['identifier']

    print(f'Claim {pcn} from {billing_npi} for the amount {charge}')

# ** 835
# Convert 835 using multi-part request
edi_835_dir = '../../edi_files/835'
file_names_to_convert = ['claim_adj_reason.dat', 'negotiated_discount.dat']
files_to_convert = [edi_835_dir + '/' + file_name for file_name in file_names_to_convert]
print('** Converting files:')
print(*files_to_convert)
response = convert_files_using_multipart_upload(files_to_convert, True)
for payment_str in response.iter_lines():
    # each line is a payment object
    payment = json.loads(payment_str)
    file_name = payment['transaction']['fileInfo']['name']
    payer_name = payment['payer']['lastNameOrOrgName']
    pcn = payment['patientControlNumber']
    charge = payment['chargeAmount']
    paid = payment['paymentAmount']

    print(f'File {file_name}: Payment from {payer_name} for claim {pcn} for the amount {paid}; Billed: {charge}')
