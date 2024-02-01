import requests
import env
'''
Claims search examples
'''


claims_api_url=env.api_url + '/claims'
search_str="code:M46 spine Greene"
claims = requests.get(claims_api_url, {'search': search_str}).json()
print(claims)
