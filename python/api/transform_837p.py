import edi_converter
from edi_converter import ObjectType
from edi_model.all_classes import ProfClaim, InterchangeControl, FunctionalGroup, EdiGenClaimRequest

"""
Example of an 837 claim transformation.
Parse an existing 837 file, change some fields, and generate a new 837 file.
"""

edi_837_dir = '../../edi_files/837'

# Prepare the interchange control and functional group
interchange_control = InterchangeControl(
    sender_id_qualifier="ZZ",
    sender_id="123",
    receiver_id_qualifier="ZZ",
    receiver_id="456",
)

functional_group = FunctionalGroup(
    transaction_type="PROF",
    sender_code="1",
    receiver_code="2",
)

# Parse an existing EDI file
file_to_convert = edi_837_dir + '/837P-all-fields.dat'
print('** Transforming claim from ' + file_to_convert)
response = edi_converter.convert_file(file_to_convert, False)
claims = response.json()
for claim_json in claims:
    object_type = ObjectType(claim_json['objectType'])
    if object_type in {ObjectType.ERROR, ObjectType.WARNING}:
        edi_converter.handle_warning_error(claim_json)
        continue
    # Get the claim object
    claim = ProfClaim.model_validate(claim_json)
    # Prepare our transaction
    transaction = claim.transaction
    # The API will set date/time automatically
    transaction.creation_date = None
    transaction.creation_time = None
    # Change whatever other fields we need, e.g., originator application transaction ID
    transaction.originator_application_transaction_id = "app-id"

    # increase charge amount for each line
    total_charge_amount = 0
    for line in claim.service_lines:
        line.charge_amount += 100
        total_charge_amount += line.charge_amount
    # update total charge amount
    claim.charge_amount = total_charge_amount
    # Generate new claim
    ed_gen_request = EdiGenClaimRequest(
        interchange_control=interchange_control,
        functional_group=functional_group,
        transaction=transaction,
        claims=[claim],
    )
    response = edi_converter.generate_claim_edi(ed_gen_request)
    edi_text = response.text
    print("Generated EDI:")
    print(edi_text)