import json
import edi_converter
from edi_converter import ObjectType

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
    # All objects contain transaction info
    # Converter assigns unique id to each transaction
    transaction = obj['transaction']
    if transaction['id'] != cur_transaction_id:
        # ACH, check or None
        paymentMethodType = transaction['paymentMethodType']
        checkOrEftTraceNumber = transaction['checkOrEftTraceNumber']
        payment_date = transaction['paymentDate']
        # Total payment for all claims in this transaction
        total_payment_amount = transaction['totalPaymentAmount']
        file_name = transaction['fileInfo']['name']
        # Control number assigned by the payer
        control_number = transaction['controlNumber']
        print(
            f'* File {file_name}: Transaction: {control_number} Payment date: {payment_date} Amount: {total_payment_amount}')

    # Payer is also common for provider adjustment and payment objects
    payer_name = obj['payer']['lastNameOrOrgName']
    if object_type == ObjectType.PAYMENT:
        claim_payment = obj
        pcn = claim_payment['patientControlNumber']
        charge = claim_payment['chargeAmount']
        paid = claim_payment['paymentAmount']

        print(f'Payment from {payer_name} for claim {pcn} for the amount {paid}; Billed: {charge}')
        if drg := claim_payment.get('drg'):
            print(f"DRG: {drg['code']} DRG weight: {claim_payment.get('drgWeight')}")
        # Remark codes from outpatient adjudication (inpatient is similar)
        if outpatient_adjudication := claim_payment.get('outpatientAdjudication'):
            for remark in outpatient_adjudication.get('remarks', []):
                remark_code = remark['code']
                remark_desc = remark.get('desc')
                print(f'Outpatient adjudication remark: {remark_code} {remark_desc}')

        for i, line in enumerate(claim_payment.get('serviceLines', [])):
            line_control_number = line.get('sourceLineId', i + 1)
            line_charge = line['chargeAmount']
            line_paid = line['paidAmount']
            procedure = line.get('procedure', {'code': None})
            rev_code = line.get('revenueCode', {'code': None})
            print(f"Line: {line_control_number} Billed: {line_charge} Paid: {line_paid}")
            print(f"Procedure: {procedure['code']} Revenue code: {rev_code['code']}")
            # Line-level adjustments
            for adj in line.get('adjustments', []):
                adj_group = adj['group']
                reason_code = adj['reason']['code']
                amount = adj['amount']
                print(f'Line adjustment Group: {adj_group} Reason code: {reason_code} Amount: {amount}')
            # Line-level remark codes
            for remark in line.get('remarks', []):
                remark_code = remark['code']
                remark_desc = remark.get('desc')
                print(f'Remark: {remark_code} {remark_desc}')

    elif object_type == ObjectType.PROVIDER_ADJUSTMENT:
        provider_adjustment = obj
        fiscal_period = provider_adjustment['fiscalPeriodDate']
        print(f'Provider adjustment from {payer_name} for fiscal period: {fiscal_period}')
        for adj in provider_adjustment['adjustments']:
            reason_code = adj['reason']['code']
            amount = adj['amount']
            print(f'Provider adjustment Reason code: {reason_code} Amount: {amount}')
