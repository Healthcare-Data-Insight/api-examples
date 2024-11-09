import requests
import env
import pandas as pd
from requests_toolbelt.downloadutils import stream

"""
Converts 837/835 files using multipart request or by posting the file's content.
The response is a CSV text.
Documentation:
https://datainsight.health/clinsight/swagger-ui/index.html#/EDI-to-CSV%20Conversion
"""


def convert_file_using_post_text(file):
    api_url = env.api_url + '/edi/csv'

    with open(file) as f:
        api_response = requests.post(api_url, data=f, stream=True)
    if api_response.status_code != 200:
        raise Exception(f'Error converting EDI; Error: {api_response.text}')
    return api_response


edi_files_dir = '../../edi_files/835'
file_to_parse = edi_files_dir + '/835-all-fields.dat'

# Parse the file and print the CSV response
response = convert_file_using_post_text(file_to_parse)
for line in response.iter_lines(decode_unicode=True):
    print(line)

# Parse the file, save the CSV to a file and use pandas to read it
response = convert_file_using_post_text(file_to_parse)

csv_file = './out/payments.csv'
with open(csv_file, 'wb') as f:
    stream.stream_response_to_file(response, path=f)

df = pd.read_csv(csv_file, sep=',')
print(df.shape)
payment_id = ''
for _, row in df.iterrows():
    # ID is a unique string assigned to each claim/payment
    #  data is duplicated for each line
    current_payment_id = row['Id']
    pcn = row['PatientControlNumber']
    payerControlNumber = row['PayerControlNumber']
    status = row['ClaimStatus']
    memberId = row['SubscriberIdentifier']
    memberName = row['SubscriberLastName']
    charged = row['ChargeAmount']
    paid = row['PaymentAmount']
    # Print payment info only once
    if current_payment_id != payment_id:
        print(
            f'Payment {payerControlNumber} for claim {pcn}. Member: {memberId} - {memberName}. Charges: {charged} Paid: {paid}')
    # line-level fields
    procedure = row['LineProcedureCode']
    lineCharged = row['LineChargeAmount']
    linePaid = row['LinePaidAmount']
    print(f'Service line: procedure: {procedure}, charges: {lineCharged}, paid: {linePaid}')

    payment_id = current_payment_id
