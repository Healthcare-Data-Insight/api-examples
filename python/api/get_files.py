import requests
from datetime import datetime, timedelta
import env

# Get all files loaded over the last few days
date_time_from = datetime.now() - timedelta(days=5)
params = {'loadedDateTimeFrom': date_time_from.isoformat()}
file_infos = requests.get(env.api_url + '/files', params).json()
# Get claims ingested from the files
for file_info in file_infos:
    print('Getting claims for file {}'.format(file_info['name']))
    file_url = file_info['url']
    claims = requests.get(env.api_url + '/claims', {'fileUrl': file_url}).json()
    for claim in claims:
        pcn = claim['patientControlNumber']
        charge = claim['chargeAmount']
        billing_npi = claim['billingProvider']['identifier']
        print(f'Claim {pcn} from {billing_npi} for the amount {charge}')
