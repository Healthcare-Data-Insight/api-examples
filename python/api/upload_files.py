import requests

def upload_files(base_url, file):
    url = base_url + "/files/default"
    print("Uploading {} to {} ".format(file, url))
    files_dict = {"files": open(file, 'rb')}
    file_upload_response=requests.post(url, files=files_dict)
    return file_upload_response.json()

def fetch_claims_for_file_url(api_url, file_url):
    api_url = api_url + "/claims/default"
    api_url = api_url+"?fileUrl="+file_url
    # TODO: use pagination
    return requests.get(api_url).json()

clinsight_api_url = "http://localhost:4080/clinsight/api"
test_files_dir = "../../sample_files"
test_file = test_files_dir + "/837/prof-encounter.dat"

upload_info=upload_files(clinsight_api_url, test_file)
file_infos=upload_info["files"]
for file_info in file_infos:
    claims=fetch_claims_for_file_url(clinsight_api_url, file_info["url"])
    # Do something useful with our claims
    for claim in claims:
        pcn=claim["patientControlNumber"]
        charge=claim["chargeAmount"]
        billing_npi=claim["billingProvider"]["identifier"]
        print("Claim {} from {} for the amount {}".format(pcn, billing_npi, charge))

