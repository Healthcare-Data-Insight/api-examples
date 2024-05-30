import requests
import env
import pandas as pd
from requests_toolbelt.downloadutils import stream

'''
Parse EDI as CSV
'''

parse_api_url = env.api_url + '/edi/csv'
csv_file = './out/payments.csv'

edi_files_dir = '../../edi_files/835'
file_to_parse = edi_files_dir + '/negotiated_discount.dat'
with open(file_to_parse) as f:
    data = f.read()

with open(csv_file, 'wb') as fd:
    response = requests.post(parse_api_url, data=data, stream=True)
    if response.status_code != 200:
        raise Exception('Error parsing file ' + file_to_parse)
    stream.stream_response_to_file(response, path=fd)

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
    memberName = row['SubscriberLastNameOrOrgName']
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
