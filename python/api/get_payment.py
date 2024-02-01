import requests
import env

'''
Getting a single payment by the Payer Control Number and/or Patient Control Number and the payee ID
'''

payments_api_url= env.api_url + '/payments'

payments = requests.get(payments_api_url, {'payerControlNumber': '94060555410000', 'payeeId': '5544667733'}).json()
# The API returns an array, but there should be only one payment
print(payments[0])

# You can also use the Patient Control Number (or a combination)
payments = requests.get(payments_api_url, {'pcn': '5554555444', 'payeeId': '5544667733'}).json()
print(payments[0])

