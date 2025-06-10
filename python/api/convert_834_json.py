import json
import edi_converter

"""
Converts 834 X220 (benefit enrollment and maintenance) file. 
The response is an array of JSON objects or a line-delimited JSON (ndjson).
Each object represents a member with nested sponsor, payer, subscriber and health coverage objects.
This example use ndjson as it is more convenient for streaming.
"""

edi_834_dir = '../../edi_files/834'

# Convert by posting the file's content
file_to_convert = edi_834_dir + '/834-all-fields.edi'

response = edi_converter.convert_file(file_to_convert, True)
for member_coverage_str in response.iter_lines():
    obj = json.loads(member_coverage_str)
    if edi_converter.handle_warning_error(obj):
        continue
    # each line is a member coverage object
    member_coverage = obj
    member_id = member_coverage['identifier']
    subscriber = member_coverage['member']
    group = member_coverage['groupOrPolicyNumber']
    sponsor = member_coverage['sponsor']

    print(f"* Plan sponsor: {sponsor['identifier']}, group {group}, "
          f"member {member_id} {subscriber['lastNameOrOrgName']}")
    print("Health coverage:")
    for health_coverage in member_coverage.get('healthCoverages', []):
        print(f"Maintenance code: {health_coverage['maintenanceTypeCode']}, "
              f"insurance linecode {health_coverage['insuranceLineCode']}")
        print("Coverage dates:")
        for date in health_coverage.get('coverageDates', []):
            print(f"Date: {date['date']}, qualifier code: {date['qualifierCode']}")
        print("Contract amounts:")
        for amount in health_coverage.get('contractAmounts', []):
            print(f"Amount: {amount['amount']}, qualifier code: {amount['qualifierCode']}")
        print("Providers:")
        for provider in health_coverage.get('providers', []):
            print(f"Type: {provider['entityRole']}, "
                  f"ID: {provider['identifier']}, "
                  f"name: {provider['lastNameOrOrgName']}")
            change_reason = provider.get('changeReason')
            if change_reason:
                print(f"Change reason code: {change_reason['reasonCode']}, "
                      f"action code: {change_reason['actionCode']}, "
                      f"effective date: {change_reason['effectiveDate']}")
