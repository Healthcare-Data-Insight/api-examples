import requests
import env

def get_claim_by_pcn(base_url, pcn):
    url = base_url + "/claims"
    url = url + "?pcn=" + pcn
    response = requests.get(url)
    return response.json()

def get_claim_by_id(base_url, id):
    url = base_url + "/claims"
    url = url + "/" + id
    response = requests.get(url)
    return response.json()

claim_json = get_claim_by_pcn(env.api_url, "125WILL")
first_claim = claim_json[0]
claim=get_claim_by_id(env.api_url, first_claim["id"])

print(claim)
