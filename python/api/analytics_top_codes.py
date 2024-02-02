import requests
import env

'''
Get top codes by charge amount
'''

top_codes_api_url= env.api_url + '/analytics/top/codes'
# get top procedure codes for professional claims
top_codes = requests.get(top_codes_api_url+'/procedures', {'claimType': 'prof'}).json()
# The API returns an array of top procedure codes by charge amount
print('Top Procedure Codes')
for top_code in top_codes:
    print('Code: {} Total charge amount: {} Max charge amount: {} Claim count: {}'.format(top_code['id'], top_code['chargeAmt'], top_code['chargeAmtMax'], top_code['claimCnt']))

# Same for DX codes
top_codes = requests.get(top_codes_api_url+'/diags', {'claimType': 'prof'}).json()
print('Top Diagnosis Codes')
for top_code in top_codes:
    print('Code: {} Total charge amount: {} Max charge amount: {} Claim count: {}'.format(top_code['id'], top_code['chargeAmt'], top_code['chargeAmtMax'], top_code['claimCnt']))