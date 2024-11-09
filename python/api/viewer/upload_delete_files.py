import requests
import env

"""
Upload files to the database, get loaded claims, delete files afterwards
"""


def upload_files(api_url, files):
    # we need to pass an array of tuples (field_name, file-like obj)
    # The field name is always 'files'
    field_and_file_objects = []
    for f in files:
        field_and_file_objects.append(('files', open(f, 'rb')))
    file_upload_response = requests.post(files_api_url, files=field_and_file_objects)
    # Rebuild analytics after the upload
    rebuild_analytics(api_url)
    return file_upload_response.json()


def rebuild_analytics(api_url):
    api_url += '/analytics/rebuild'
    # Don't block
    requests.post(api_url, {'async': 'true'})


files_api_url = env.api_url + '/files'
test_files_dir = '../../../edi_files/837'
# Upload multiple files. Files are processed in parallel, so it is always faster to upload multiple than one by one
files_to_upload = [test_files_dir + '/prof-encounter.dat', test_files_dir + '/anesthesia.dat']
upload_info = upload_files(env.api_url, files_to_upload)
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
        print('Claim {} from {} for the amount {}'.format(pcn, billing_npi, charge))

# We can now delete files
for file_info in file_infos:
    print('Deleting file {}'.format(file_info['name']))
    file_url = file_info['url']
    requests.delete(files_api_url, params={'url': file_url})
