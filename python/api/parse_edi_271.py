import requests
import env

'''
Parse a 271 EDI file. The response contains EDI segment hierarchy matching the X12 spec.
Each segment has a unique name, which is a key in the json dict
Most loops are lists
The hierarchy follows the X12 EDI spec
'''

parse_api_url = env.api_url + '/edi/parse'
edi_files_dir = '../../edi_files/271'
file_to_parse = edi_files_dir + '/X279-response-to-generic-request-by-clinic-for-patient-(subscriber)-eligibility.edi'

with open(file_to_parse) as f:
    data = f.read()

response = requests.post(parse_api_url, data)
if response.status_code == 200 and 'segments' in response.json():

    root_segments = response.json()['segments']
    for root_seg in root_segments:
        if root_seg['segment_id'] == 'ST':
            tran = root_seg
            info_source_list = tran['information_source_level']
            for info_source in info_source_list:
                receiver_list = info_source['information_receiver_level']
                for receiver in receiver_list:
                    subscriber_list = receiver.get('subscriber_level')
                    for subscriber in subscriber_list:
                        subscriber_info = subscriber.get('subscriber_name')
                        elig_list = subscriber_info.get('subscriber_eligibility_or_benefit_information')
                        for elig in elig_list:
                            print(elig)

else:
    raise Exception('Error parsing file ' + file_to_parse)
