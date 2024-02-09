import requests
import env

'''
Parse a 277 EDI file. The response contains EDI segment hierarchy matching the X12 spec.
Each segment has a unique name, which is a key in the json dict
'''

parse_api_url = env.api_url + '/edi/parse'
edi_files_dir = '../../edi_files/277'
file_to_parse = edi_files_dir + '/claim_level_response.dat'
with open(file_to_parse) as f:
    data = f.read()

response = requests.post(parse_api_url, data)
if response.status_code == 200 and 'segments' in response.json():
    segments = response.json()['segments']
    # get first transaction
    tran = segments[0]
    # Traverse the path to get the payer, provider and the status objects
    info_source_list = tran['information_source_level']
    for info_source in info_source_list:
        payer = info_source['payer_name']
        print(payer)
        receiver_list = info_source['information_receiver_level']
        for receiver in receiver_list:
            provider_list = receiver['service_provider_level']
            for provider in provider_list:
                # normally there is only one provider
                provider_name = provider['provider_name'][0]
                print(provider_name)
                subscriber_list = provider['subscriber_level']
                for subscriber in subscriber_list:
                    subscriber_name = subscriber['subscriber_name']
                    print(subscriber_name)
                    claim_statuses = subscriber['claim_status_tracking_number']
                    for status in claim_statuses:
                        print(status)

        # provider_infos=receiver_info['service_provider_level']
        # for provider_info in provider_infos:
        #     provider=provider_info['provider_name']
        #     status=provider_info['provider_of_service_trace_identifier']['provider_status_information']
        # print(status)

else:
    raise Exception('Error parsing file ' + file_to_parse)
