import json

import edi_converter
from edi_converter import ObjectType
from edi_model.all_classes import Payment, Code

"""
Converts 835 files using multipart request or by posting the file's content.
The response is an array of JSON objects or a line-delimited JSON (ndjson)
This example uses ndjson as it is more convenient for streaming.
API documentation:
https://datainsight.health/docs/ediconvert-api/reference/#tag/EDI-to-JSON
Schemas:
https://datainsight.health/docs/schemas/835/
"""

# ** 835
# Convert multiple 835 files using multi-part request
edi_835_dir = '../../edi_files/835'
file_names_to_convert = ['claim_adj_reason.dat', '835-all-fields.dat', '835-provider-level-adjustment.dat']
files_to_convert = [edi_835_dir + '/' + file_name for file_name in file_names_to_convert]
print('** Converting files:')
print(*files_to_convert)
response = edi_converter.convert_files_with_multipart(files_to_convert, True)
cur_transaction_id = None
for response_line_str in response.iter_lines():
    # each line is an object
    # Object types: PAYMENT (paid claim), PROVIDER_ADJUSTMENT (provider-level adjustment), WARNING (parser's warning)
    obj = json.loads(response_line_str)
    object_type = ObjectType(obj['objectType'])
    if object_type in {ObjectType.ERROR, ObjectType.WARNING}:
        edi_converter.handle_warning_error(obj)
        continue
    if object_type == ObjectType.PAYMENT:
        claim_payment = Payment.model_validate(obj)
        pcn = claim_payment.patient_control_number
        charge = claim_payment.charge_amount
        paid = claim_payment.payment_amount
        payer_name = claim_payment.payer.last_name_or_org_name
        print(f'Payment from {payer_name} for claim {pcn} for the amount {paid}; Billed: {charge}')
        if drg := claim_payment.drg:
            print(f"DRG: {drg.code} DRG weight: {claim_payment.drg_weight}")
        # Remark codes from outpatient adjudication (inpatient is similar)
        if outpatient_adjudication := claim_payment.outpatient_adjudication:
            for remark in outpatient_adjudication.remarks:
                remark_code = remark.code
                remark_desc = remark.desc
                print(f'Outpatient adjudication remark: {remark_code} {remark_desc}')

        for i, line in enumerate(claim_payment.service_lines):
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