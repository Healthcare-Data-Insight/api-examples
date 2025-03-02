from typing import TextIO
import os
import requests
import env
import csv
from collections import defaultdict
import pandas as pd
from requests_toolbelt.downloadutils import stream
from io import StringIO

"""
Converts 835 files. 
The response is a CSV text.
Documentation:
https://datainsight.health/docs/ediconvert-api/reference/#tag/EDI-to-CSV
"""

api_url = env.api_url + '/edi/csv'


def convert_file_using_post_text(file, schema_name=None):
    """
    Opens file, post the content and return the response.
    """
    # ediFileName parameter will propagate the original file name to transaction.fileInfo.name field; if not provided,
    # the converter will generate a name
    # warningsInResponse tells the converter to return parsing warnings to the client (line starts with 'WARNING:')
    params = {'warningsInResponse': True, 'ediFileName': file}

    if schema_name:
        params['schemaName'] = schema_name
    fileIO: TextIO
    with open(file) as fileIO:
        # Use stream=True to stream the response instead of loading it in memory
        api_response = requests.post(api_url, data=fileIO, params=params, stream=True)
    if api_response.status_code != 200:
        raise Exception(f'Error converting EDI; Error: {api_response.text}')
    return api_response


def convert_files_using_multipart_upload(files, schema_name=None):
    """Create a multipart request with the list of files, posts it and return the response"""
    # we need to pass an array of tuples (field_name, file-like obj)
    # The field name is always 'files'
    field_and_file_objects = []
    for f in files:
        field_and_file_objects.append(('files', open(f, 'rb')))
    params = {}
    if schema_name:
        params = {'schemaName': schema_name}
    # Use stream=True to stream the response instead of loading it in memory
    api_response = requests.post(api_url, files=field_and_file_objects, params=params, stream=True)
    if api_response.status_code != 200:
        raise Exception(f'Error parsing EDI; Error: {api_response.text}')
    return api_response


current_claim_id = ''


def print_row(row):
    global current_claim_id
    if isinstance(row, dict):
        row = defaultdict(lambda: '', row)
    # ID is a unique string assigned to each claim/payment, same for all lines for the same claim
    claim_id = row['Id']
    # errors and warnings are reported in the first column (id)
    if claim_id.startswith("ERROR:"):
        raise Exception(f'Error parsing EDI file; Error: {claim_id}')
    # since we set warningsInResponse=True, we need to check for warnings too
    if claim_id.startswith("WARNING:"):
        print(f'Parsing warning: {claim_id}')
    else:
        pcn = row['PatientControlNumber']
        payer_control_number = row['PayerControlNumber']
        status = row['ClaimStatus']
        member_id = row['SubscriberIdentifier']
        member_name = row['SubscriberLastName']
        charged = row['ChargeAmount']
        paid = row['PaymentAmount']
        # Print payment info only once
        if current_claim_id != claim_id:
            print(
                f'Payment {payer_control_number} for claim {pcn}; status {status}. Member: {member_id} - {member_name}. '
                f'Charges: {charged}, Paid: {paid}')
        # line-level fields
        service_code = row['LineProcedureCode']
        if not service_code:
            service_code = row['LineRevenueCode']
        if not service_code:
            service_code = row['LineDrugCode']
        line_charged = row['LineChargeAmount']
        line_paid = row['LinePaidAmount']
        print(f'Service line: service code: {service_code}, charges: {line_charged}, paid: {line_paid}')
        current_claim_id = claim_id


edi_files_dir = '../../edi_files/835'
file_to_parse = edi_files_dir + '/835-all-fields.dat'

# Convert a small file using response.text and csv module
print('** Convert from response.text, all fields')
response = convert_file_using_post_text(file_to_parse)
csv_input = StringIO(response.text)
csv_reader = csv.DictReader(csv_input, delimiter=',')
for row_number, csv_row in enumerate(csv_reader, start=1):
    print_row(csv_row)

# By default, we convert all fields. You can customize what fields to convert and how using the conversion schema
# Several named schemas are provided out of the box, see https://datainsight.health/docs/csv/schemas/
print('** Convert from response.text, only key fields')
response = convert_file_using_post_text(file_to_parse, 'key-fields')
csv_input = StringIO(response.text)
csv_reader = csv.DictReader(csv_input, delimiter=',')
current_claim_id = ''
for row_number, csv_row in enumerate(csv_reader, start=1):
    print_row(csv_row)

# For large files we don't want to use response.text
print('** Convert using streaming, all fields')
# Stream the response to a file first, then read the file using csv module
response = convert_file_using_post_text(file_to_parse)
csv_file = './out/payments.csv'
with open(csv_file, 'wb') as f:
    stream.stream_response_to_file(response, path=f)

with open(csv_file, mode='r') as csv_input:
    current_claim_id = ''
    csv_reader = csv.DictReader(csv_input, delimiter=',')
    for row_number, csv_row in enumerate(csv_reader, start=1):
        print_row(csv_row)

# Convert multiple files at once using multipart upload
print('** Convert multiple files using streaming, all fields')
files = os.listdir(edi_files_dir)
files_to_convert = [edi_files_dir + '/' + file_name for file_name in files]
print(files)
response = convert_files_using_multipart_upload(files_to_convert)
with open(csv_file, 'wb') as f:
    stream.stream_response_to_file(response, path=f)

with open(csv_file, mode='r') as csv_input:
    current_claim_id = ''
    csv_reader = csv.DictReader(csv_input, delimiter=',')
    for row_number, csv_row in enumerate(csv_reader, start=1):
        print_row(csv_row)

# Raw response text without parsing CSV
print('** Convert using streaming; print raw text')
response = convert_file_using_post_text(file_to_parse)
for line in response.iter_lines(decode_unicode=True):
    if line.startswith("ERROR:"):
        raise Exception(f'Error parsing EDI; Error: {line}')
    if line.startswith("WARNING:"):
        print(f'Parsing warning: {line}')
    else:
        print(line)

print('** Convert using streaming and pandas; all fields')
response = convert_file_using_post_text(file_to_parse)
with open(csv_file, 'wb') as f:
    stream.stream_response_to_file(response, path=f)
df = pd.read_csv(csv_file, sep=',')
print(df.shape)
df.fillna('', inplace=True)
current_claim_id = ''
for _, csv_row in df.iterrows():
    print_row(csv_row)
