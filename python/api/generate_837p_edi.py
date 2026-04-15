from datetime import date
from pathlib import Path

import edi_converter
from edi_model.all_classes import *

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "out"
OUTPUT_EDI_PATH = OUTPUT_DIR / "837p-minimal-generated.edi"


def build_request() -> EdiGenClaimRequest:
    """
    Builds a minimal 837P EDI claim request

    Returns:
        EdiGenClaimRequest: The generated claim request.
    """
    interchange_control = InterchangeControl(
        sender_id_qualifier="ZZ",
        sender_id="123",
        receiver_id_qualifier="ZZ",
        receiver_id="456",
        interchange_date=date(2026, 3, 22),
        interchange_time="10:06",
        control_number=1,
    )

    functional_group = FunctionalGroup(
        transaction_type="PROF",
        functional_identifier_code="HC",
        sender_code="1",
        receiver_code="2",
        date=date(2026, 3, 22),
        time="10:06",
        control_number=1,
        version="005010X222A2",
    )

    transaction = Transaction837(
        transaction_type="PROF",
        originator_application_transaction_id="1",
        creation_date=date(2026, 3, 22),
        creation_time="10:06",
        sender=Party(
            identifier="TGJ23",
            last_name_or_org_name="PREMIER BILLING SERVICE",
            contacts=[
                ContactInfo(
                    function_code="IC",
                    contact_numbers=[
                        ContactNumber(
                            type="EMAIL",
                            number="test@test.com",
                        )
                    ],
                )
            ],
        ),
        receiver=PartyIdName(
            identifier="66783JJT",
            last_name_or_org_name="KEY INSURANCE COMPANY",
        ),
    )

    subscriber = Subscriber(
        payer_responsibility_sequence=PayerRespSequenceType.PRIMARY,
        relationship_type=RelationshipType.SELF,
        group_or_policy_number="2222",
        claim_filing_indicator_code="CI",
        insurance_plan_type=InsurancePlanType.COMMERCIAL,
        person=PersonWithDemographic(
            identifier="JS00111223333",
            last_name_or_org_name="Smith",
            first_name="Jane",
            address=Address(
                city="MAIMI",
                state_code="FL",
                zip_code="33111",
            ),
        ),
        payer=Party(
            identifier="999996666",
            last_name_or_org_name="KEY INSURANCE COMPANY",
            address=Address(
                city="MAIMI",
                state_code="FL",
                zip_code="33111",
            ),
        ),
    )

    claim = ProfClaim(
        patient_control_number="26463774",
        charge_amount=100.00,
        facility_code=Code(code="11"),
        frequency_code=Code(code="1"),
        subscriber=subscriber,
        provider_signature_indicator="Y",
        assignment_participation_code="A",
        assignment_certification_indicator="Y",
        release_of_information_code="I",
        clearinghouse_trace_number="17312345600006351",
        billing_provider=Provider(
            identifier="9876543210",
            tax_id="587654321",
            last_name_or_org_name="Ben Kildare Service",
            address=Address(
                line="234 SEAWAY ST",
                city="MIAMI",
                state_code="FL",
                zip_code="33111",
            ),
        ),
        diags=[Code(code="J020"), Code(code="Z1159")],
        service_lines=[
            ProfLine(
                charge_amount=40.00,
                service_date_from=date(2006, 10, 3),
                unit_type=UnitType.UNIT,
                unit_count=1,
                procedure=Procedure(code="99213"),
                diag_pointers=[1],
            )
        ],
    )

    return EdiGenClaimRequest(
        interchange_control=interchange_control,
        functional_group=functional_group,
        transaction=transaction,
        claims=[claim],
    )


def main() -> None:
    request = build_request()
    response = edi_converter.generate_claim_edi(request)

    if response.status_code == 417:
        validation_issues = [
            ValidationIssue.model_validate(issue_json) for issue_json in response.json()
        ]
        print("Validation issues:")
        for issue in validation_issues:
            print(issue)
        return

    edi_text = response.text
    if not edi_text.startswith("ISA*00*"):
        raise RuntimeError(
            'Unexpected response body: generated EDI did not start with "ISA*00*".'
        )

    print("Generated EDI:")
    print(edi_text)

if __name__ == "__main__":
    main()