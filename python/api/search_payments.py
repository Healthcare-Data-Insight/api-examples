import requests
import env

'''
Search payments and use pagination to retrieve results
'''

payments_api_url = env.api_url + '/payments'
# Search for payments from the "Rushmore Life" payer
search_str = "rushmore life"

page_ind = 0
page_size = 50
while True:
    payments = requests.get(payments_api_url,
                            {'search': search_str, 'limit': page_size, 'offset': page_ind * page_size}).json()
    if not payments:
        break

    for pmt in payments:
        print("Payment {} from {} to {} ({})for the amount of {}. Billed amount: {}".format(
            pmt['payerControlNumber'], pmt['payer']['lastNameOrOrgName'],
            pmt['payee']['lastNameOrOrgName'],pmt['payee']['identifier'],
            pmt['paymentAmount'], pmt['chargeAmount'])
        )

    page_ind += 1
