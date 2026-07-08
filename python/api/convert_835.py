import json

import env
from edi_model.all_classes import Payment, Code, ProviderAdjustment
from edi_model.enums import ObjectType
from ediconvert_sdk import EdiConverterClient, handle_warning_error

"""
Converts 835 files using multipart request.
The response is an array of JSON objects or a line-delimited JSON (ndjson).
This example uses ndjson as it is more convenient for streaming.
API documentation:
https://datainsight.health/docs/ediconvert-api/reference/#tag/EDI-to-JSON
Schemas:
https://datainsight.health/docs/schemas/835/
"""

# ** 835
# Convert multiple 835 files using multi-part request
edi_835_dir = '../../edi_files/835'
file_names_to_convert = ['claim_adj_reason.dat', '835-all-fields.dat', '835-provider-level-adjustment.dat', '835-validation-issues.edi']
files_to_convert = [edi_835_dir + '/' + file_name for file_name in file_names_to_convert]
print('** Converting files:')
print(*files_to_convert)
# We always convert with full validation, so we can get validation issues
client = EdiConverterClient(base_url=env.api_url)
response = client.conversion.to_json_files(files_to_convert, ndjson=True, validate=True)
cur_transaction_id = None
for response_line_str in response.iter_lines():
    # each line is an object
    # Object types: PAYMENT (paid claim), PROVIDER_ADJUSTMENT (provider-level adjustment), VALIDATION (EDI Validation issue)
    obj = json.loads(response_line_str)
    if handle_warning_error(obj):
        continue
    object_type = ObjectType(obj['objectType'])
    if object_type == ObjectType.PAYMENT:
        paid_claim = Payment.model_validate(obj)
        # print validation issues for this claim
        if paid_claim.validation_issues:
            print(f'Validation issues for claim {paid_claim.patient_control_number}:')
            for issue in paid_claim.validation_issues:
                print(issue)
        pcn = paid_claim.patient_control_number
        charge = paid_claim.charge_amount
        paid = paid_claim.payment_amount
        payer_name = paid_claim.payer.last_name_or_org_name
        print(f'Payment from {payer_name} for claim {pcn} for the amount {paid}; Billed: {charge}')
        if drg := paid_claim.drg:
            print(f"DRG: {drg.code} DRG weight: {paid_claim.drg_weight}")
        # Remark codes from outpatient adjudication (inpatient is similar)
        if outpatient_adjudication := paid_claim.outpatient_adjudication:
            for remark in outpatient_adjudication.remarks:
                remark_code = remark.code
                remark_desc = remark.desc
                print(f'Outpatient adjudication remark: {remark_code} {remark_desc}')

        for i, line in enumerate(paid_claim.service_lines):
            line_control_number = line.source_line_id or i + 1
            line_charge = line.charge_amount
            line_paid = line.paid_amount
            procedure = line.procedure or Code(code=None)
            rev_code = line.revenue_code or Code(code=None)
            print(f"Line: {line_control_number} Billed: {line_charge} Paid: {line_paid}")
            print(f"Procedure: {procedure.code} Revenue code: {rev_code.code}")
            # Line-level adjustments
            for adj in line.adjustments:
                adj_group = adj.group
                reason_code = adj.reason.code
                amount = adj.amount
                print(f'Line adjustment Group: {adj_group} Reason code: {reason_code} Amount: {amount}')
            # Line-level remark codes
            for remark in line.remarks:
                remark_code = remark.code
                remark_desc = remark.desc
                print(f'Remark: {remark_code} {remark_desc}')

    elif object_type == ObjectType.PROVIDER_ADJUSTMENT:
        provider_adjustment = ProviderAdjustment.model_validate(obj)
        payer_name = provider_adjustment.payer.last_name_or_org_name
        fiscal_period = provider_adjustment.fiscal_period_date
        print(f'Provider adjustment from {payer_name} for fiscal period: {fiscal_period}')
        for adj in provider_adjustment.adjustments:
            reason_code = adj.reason.code
            amount = adj.amount
            print(f'Provider adjustment Reason code: {reason_code} Amount: {amount}')
