import requests
def _get_claim_by_pcn(base_url, pcn):
    url = base_url+"/claims/default"
    url = url+"?pcn="+pcn
    response = requests.get(url)
    return response.json()

api_url="http://localhost:4080/clinsight/api"
print('Started')
claim_json=_get_claim_by_pcn(api_url, "125WILL")
print(claim_json)