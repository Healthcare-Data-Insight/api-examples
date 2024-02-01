import requests
import env


def rebuild_analytics(api_url):
    api_url += '/analytics/rebuild'
    # Don't block
    requests.post(api_url, {'async': 'true'})


def upload_files(api_url, file):
    files_api_url = api_url + '/files'
    print('Uploading {} to {}'.format(file, files_api_url))
    file_upload_response = requests.post(files_api_url, files={'files': open(file, 'rb')})
    # Rebuild analytics after the upload
    rebuild_analytics(api_url)
    return file_upload_response.json()


test_files_dir = "../../sample_files"
test_file = test_files_dir + "/837/prof-encounter.dat"

upload_info = upload_files(env.api_url, test_file)
file_infos = upload_info['files']
for file_info in file_infos:
    print('Getting claims for file {}'.format(file_info['name']))
    file_url = file_info['url']
    claims = requests.get(env.api_url + '/claims', {'fileUrl': file_url}).json()

    # Do something useful with our claims
    for claim in claims:
        pcn = claim['patientControlNumber']
        charge = claim['chargeAmount']
        billing_npi = claim['billingProvider']['identifier']
        print("Claim {} from {} for the amount {}".format(pcn, billing_npi, charge))
