import requests
import json

import env

"""
Converts 837/835 files using multipart request or by posting the file's content.
The response is an array of JSON objects or a line-delimited JSON (ndjson)
This example use ndjson as it is more convenient for streaming.
If you want to use well-formed JSON, make sure that your logic can handle large arrays if you have large EDI files.
Documentation:
https://datainsight.health/docs/ediconvert-api/reference/#tag/EDI-to-JSON
"""


def convert_files_using_multipart_upload(files, is_ndjson):
    """Creates a multipart request with the list of files and posts it"""
    api_url = env.api_url + '/edi/json'
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
    # ediFileName parameter will propagate the original file name to transaction.fileInfo.name field; if not provided,
    # the converter will generate a name
    # warningsInResponse tells the converter to return parsing warnings to the client as objects (objectType: WARNING)
    params = {'splitTran': True, 'ndjson': is_ndjson, 'warningsInResponse': True, 'ediFileName': file}

    with open(file) as f:
        # Use stream=True to stream the response instead of loading it in memory
        # Note that we're posting the file-like object instead of reading the file into memory
        # This allows for streaming content to the server
        api_response = requests.post(api_url, data=f, params=params, stream=True)
        if api_response.status_code != 200:
            raise Exception(f'Error parsing EDI; Error: {api_response.text}')
    return api_response


# ** 837
edi_837_dir = '../../edi_files/837'
# Convert by posting the file's content
file_to_convert = edi_837_dir + '/prof-encounter.dat'
print('** Converting ' + file_to_convert)
response = convert_file_using_post_text(file_to_convert, True)
for claim_str in response.iter_lines():
    # each line is a claim object; objectType=='CLAIM'.
    # In case of errors or warnings, objectType is set to ERROR or WARNING
    claim = json.loads(claim_str)
    # Most parsing issues are warnings;
    if claim['objectType'] == 'ERROR':
        raise Exception(f'Error parsing EDI; Error: {claim}')
    # since we set warningsInResponse=True, we need to check for warnings too
    if claim['objectType'] == 'WARNING':
        fileName = claim['fileName']
        message = claim['message']
        print(f'Encountered parsing issue with file {fileName}. Warning: {message}')
    else:
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
response = convert_files_using_multipart_upload(files_to_convert, True)
for claim_str in response.iter_lines():
    # each line is a claim object or could be an error
    claim = json.loads(claim_str)
    # Check for errors; because of streaming, we can get an error even if the response status was 200
    if claim['objectType'] == 'ERROR':
        raise Exception(f'Error parsing EDI; Error: {claim}')
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
response = convert_files_using_multipart_upload(files_to_convert, True)
for payment_str in response.iter_lines():
    # each line is a payment object
    payment = json.loads(payment_str)
    if payment['objectType'] == 'ERROR':
        raise Exception(f'Error parsing EDI; Error: {payment}')

    file_name = payment['transaction']['fileInfo']['name']
    payer_name = payment['payer']['lastNameOrOrgName']
    pcn = payment['patientControlNumber']
    charge = payment['chargeAmount']
    paid = payment['paymentAmount']

    print(f'File {file_name}: Payment from {payer_name} for claim {pcn} for the amount {paid}; Billed: {charge}')
