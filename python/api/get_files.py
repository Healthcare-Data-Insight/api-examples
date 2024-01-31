import requests
from datetime import datetime, timedelta
import env

# Get all files loaded over the last few days
date_time_from = datetime.now() - timedelta(days=5)
params = {'loadedDateTimeFrom': date_time_from.isoformat()}
files = requests.get(env.api_url + '/files', params).json()
# Get claims ingested from the files
for file in files:
    print('Getting claims for file {}'.format(file['name']))
    file_url = file['url']
    claims = requests.get(env.api_url + '/claims', {'fileUrl': file_url}).json()
    for claim in claims:
        pcn = claim['patientControlNumber']
        charge = claim['chargeAmount']
        billing_npi = claim['billingProvider']['identifier']
        print('Claim {} from {} for the amount {}'.format(pcn, billing_npi, charge))
