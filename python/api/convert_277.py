import requests
import env

"""
Parses a 277 EDI file. The response contains EDI segment hierarchy matching the X12 spec.
Each segment has a unique name, which is a key in the json dict
Most loops are lists.
"""

parse_api_url = env.api_url + '/edi/json'
edi_files_dir = '../../edi_files/277'
file_to_parse = edi_files_dir + '/X212-277-claim-response.edi'

with open(file_to_parse) as f:
    response = requests.post(parse_api_url, data=f, stream=True)
if response.status_code == 200:

    root_segments = response.json()
    for root_seg in root_segments:
        if root_seg['segment_id'] == 'ST':
            tran = root_seg
            # Traverse the path to get the payer, provider and the status objects
            info_source_list = tran['information_source_level']
            for info_source in info_source_list:
                payer = info_source.get('payer_name')
                print(payer)
                receiver_list_or_dict = info_source['information_receiver_level']
                receiver_list = receiver_list_or_dict
                if type(receiver_list_or_dict) is dict:
                    receiver_list = [receiver_list_or_dict]
                for receiver in receiver_list:
                    # 277 can be for billing or for service provider
                    provider_list = receiver.get('service_provider_level')
                    if not provider_list:
                        provider_list = receiver.get('billing_provider_of_service_level')
                    for provider in provider_list:
                        # Provider name could be a list or a dict
                        provider_name = provider.get('provider_name')
                        if not provider_name:
                            provider_name = provider['billing_provider_name']
                        print(provider_name)

                        # the next level could be patient or subscriber
                        subscriber_patient_list = provider.get('subscriber_level')
                        if not subscriber_patient_list:
                            subscriber_patient_list = provider.get('patient_level')

                        for subscriber_patient in subscriber_patient_list:
                            subscriber_patient_name = subscriber_patient.get('subscriber_name')
                            if not subscriber_patient_name:
                                subscriber_patient_name = subscriber_patient.get('patient_name')
                            print(subscriber_patient_name)

                            # Patients can optionally have dependents, in which case the status is under dependent
                            subscriber_patient_dependent_list = [subscriber_patient]
                            dependent_list = subscriber_patient.get('dependent_level')
                            if dependent_list:
                                subscriber_patient_dependent_list = dependent_list

                            for subscriber_patient_dependent in subscriber_patient_dependent_list:
                                print('Dependent:')
                                print(subscriber_patient_dependent)
                                claim_statuses = subscriber_patient_dependent['claim_status_tracking_number']
                                for status in claim_statuses:
                                    print(status)

else:
    raise Exception(f'Error parsing EDI files; Error: {response.text}')
