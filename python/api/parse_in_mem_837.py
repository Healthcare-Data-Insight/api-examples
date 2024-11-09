import requests
import env

"""
Parse EDI by posting the content of the file
Note: the "parse" endpoint can only handle small files. Use Convert APIs to parse large files
"""

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
    raise Exception(f'Error parsing EDI; Error: {response.text}')


