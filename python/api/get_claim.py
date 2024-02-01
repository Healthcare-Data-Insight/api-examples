import requests
import env
'''
Getting a single claim by the Patient Control Number or by the ID
'''

claims_api_url=env.api_url + '/claims'
claims = requests.get(claims_api_url, {'pcn': '125WILL', 'billingId': '1234567890'}).json()

first_claim = claims[0]
claim = requests.get(claims_api_url+"/"+first_claim['id']).json()

print(claim)
