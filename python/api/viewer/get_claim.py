import requests
import env

'''
Getting a single claim by the Patient Control Number/billing provider NPI or by the ID
'''

claims_api_url = env.api_url + '/claims'
claims = requests.get(claims_api_url, {'pcn': '125WILL', 'billingId': '1234567890'}).json()
# The API returns an array, but there should be only one claim
claim = claims[0]
print(claim)
# if we know the internal ID, we can get a single claim by ID
claim = requests.get(claims_api_url + "/" + claim['id']).json()
print(claim)
