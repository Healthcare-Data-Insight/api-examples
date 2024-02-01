import requests
import env

'''
Parse EDI without uploading the file
The claim/payment representation is identical to search API
'''

parse_api_url = env.api_url + '/edi/parse'
edi_files_dir = '../../edi_files/837'
file_to_parse = edi_files_dir + '/prof-encounter.dat'
with open(file_to_parse) as f:
    data = f.read()

response = requests.post(parse_api_url, data)
if response.status_code == 200 and 'claims' in response.json():
    for claim in response.json()['claims']:
        pcn = claim['patientControlNumber']
        charge = claim['chargeAmount']
        billing_npi = claim['billingProvider']['identifier']
        print('Claim {} from {} for the amount {}'.format(pcn, billing_npi, charge))

else:
    raise Exception('Error parsing file ' + file_to_parse)


