import json

import env
from edi_model.all_classes import MemberCoverage
from ediconvert_sdk import EdiConverterClient, handle_warning_error

"""
Converts 834 X220 (benefit enrollment and maintenance) file.
The response is an array of JSON objects or a line-delimited JSON (ndjson).
Each object represents a member with nested sponsor, payer, subscriber and health coverage objects.
This example uses ndjson as it is more convenient for streaming.
We use the MemberCoverage object to deserialize the response.

API documentation:
https://datainsight.health/docs/ediconvert-api/reference/#tag/EDI-to-JSON
Schemas:
https://datainsight.health/docs/schemas/834/
"""

edi_834_dir = '../../edi_files/834'


def enum_name(value):
    return value.name if value else None


# Convert by posting the file's content
file_to_convert = edi_834_dir + '/834-all-fields.edi'

client = EdiConverterClient(base_url=env.api_url)
response = client.conversion.to_json_file(file_to_convert, ndjson=True, validate=True)
for member_coverage_str in response.iter_lines():
    obj = json.loads(member_coverage_str)
    if handle_warning_error(obj):
        continue
    # each line is a member coverage object
    member_coverage = MemberCoverage.model_validate(obj)
    # print validation issues for this claim
    if member_coverage.validation_issues:
        print(f'Validation issues for member {member_coverage.member.identifier}:')
        for issue in member_coverage.validation_issues:
            print(issue)
    member_id = member_coverage.identifier
    subscriber = member_coverage.member
    group = member_coverage.group_or_policy_number
    sponsor = member_coverage.sponsor

    print(f"* Plan sponsor: {sponsor.identifier}, group {group}, "
          f"member {member_id} {subscriber.last_name_or_org_name}")
    print("Health coverage:")
    for health_coverage in member_coverage.health_coverages:
        print(f"Maintenance code: {health_coverage.maintenance_type_code}, "
              f"insurance linecode {health_coverage.insurance_line_code}")
        print("Coverage dates:")
        for date in health_coverage.coverage_dates:
            print(f"Date: {date.date}, qualifier code: {date.qualifier_code}")
        print("Contract amounts:")
        for amount in health_coverage.contract_amounts:
            print(f"Amount: {amount.amount}, qualifier code: {amount.qualifier_code}")
        print("Providers:")
        for provider in health_coverage.providers:
            print(f"Type: {enum_name(provider.entity_role)}, "
                  f"ID: {provider.identifier}, "
                  f"name: {provider.last_name_or_org_name}")
            if provider.change_reason:
                print(f"Change reason code: {provider.change_reason.reason_code}, "
                      f"action code: {provider.change_reason.action_code}, "
                      f"effective date: {provider.change_reason.effective_date}")
