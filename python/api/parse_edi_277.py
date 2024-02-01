import requests
import env

'''
Parse an arbitrary EDI file. The response contains EDI segment hierarchy matching the X12 spec.
Each segment has a unique name, which is a key in the json dict
'''

parse_api_url = env.api_url + '/edi/parse'
edi_files_dir = '../../edi_files/277'
file_to_parse = edi_files_dir + '/provider_level_response.dat'
with open(file_to_parse) as f:
    data = f.read()

response = requests.post(parse_api_url, data)
if response.status_code == 200 and 'segments' in response.json():
    segments = response.json()['segments']
    # get first transaction
    tran = segments[0]
    # Traverse the path to get the payer, provider and the status objects
    info_source = tran['information_source_level']
    payer = info_source['payer_name']
    receiver_info=info_source['information_receiver_level']
    provider_info=receiver_info['service_provider_level']

    provider=provider_info['provider_name']
    status=provider_info['provider_of_service_trace_identifier']['provider_status_information']
    print(payer)
    print(provider)
    print(status)

else:
    raise Exception('Error parsing file ' + file_to_parse)
