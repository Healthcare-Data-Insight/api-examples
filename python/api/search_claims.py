import requests
import env

'''
Search claims and use pagination to retrieve
'''

claims_api_url = env.api_url + '/claims'
# Search for claims containing codes that start with 99
search_str = "code:99"

page_ind = 0
page_size = 50
while True:
    claims = requests.get(claims_api_url,
                          {'search': search_str, 'limit': page_size, 'offset': page_ind * page_size}).json()
    if not claims:
        break

    for claim in claims:
        pcn = claim['patientControlNumber']
        charge = claim['chargeAmount']
        billing_npi = claim['billingProvider']['identifier']
        print('Claim {} from {} for the amount {}'.format(pcn, billing_npi, charge))

    page_ind += 1

