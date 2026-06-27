from datetime import date
from pathlib import Path

import edi_converter
from edi_model.all_classes import *

OUTPUT_FILE = Path(__file__).parent / "out" / "835-minimal-generated.edi"


def build_request() -> EdiGenPaymentRequest:
    """
    Builds a minimal 835 EDI payment request.

    Returns:
        EdiGenPaymentRequest: The generated payment request.
    """

    interchange_control = InterchangeControl(
        sender_id_qualifier="ZZ",
        sender_id="123",
        receiver_id_qualifier="ZZ",
        receiver_id="456",
        interchange_date=date(2025, 8, 9),
        interchange_time="10:06:00",
        control_number=1,
    )

    functional_group = FunctionalGroup(
        transaction_type=TransactionType.PAYMENT,
        sender_code="1",
        receiver_code="2",
        date=date(2025, 8, 9),
        time="10:06:00",
        control_number=1,
    )

    transaction = Transaction835(
        transaction_type=TransactionType.PAYMENT,
        production_date=date(2026, 6, 1),
        transaction_handling_type=TransactionHandlingType.INFORMATION_ONLY,
        total_payment_amount=1000.00,
        credit_or_debit_flag_code="C",
        payment_method_type=PaymentMethodType.CHECK,
        receiver_account_number="456",
        payment_date=date(2026, 6, 1),
        check_or_eft_trace_number="CHECK_1",
        payer_identifier="PAYER_ID01",
        receiver_identifier="CLEARINGHOUSE_ID",
        sender=Party(
            last_name_or_org_name="ANY PLAN USA",
            address=Address(
                line="1 WALK THIS WAY",
                city="ANYCITY",
                state_code="OH",
                zip_code="45209",
            ),
            contacts=[
                ContactInfo(
                    function_code="BL",
                    name="EDI",
                    contact_numbers=[
                        ContactNumber(
                            type=ContactType.EMAIL,
                            number="test@test.com",
                        )
                    ],
                )
            ],
        ),
        receiver=Party(
            identifier="PROVIDER2_NPI",
            last_name_or_org_name="PROVIDER",
        ),
    )

    payment = Payment(
        patient_control_number="5554555444",
        charge_amount=800.00,
        payment_amount=500.00,
        facility_code=Code(
            sub_type="PLACE_OF_SERVICE",
            code="11",
        ),
        frequency_code=Code(code="1"),
        patient=PatientSubscriber835(
            person=Party(
                identifier="33344555510",
                last_name_or_org_name="BUDD",
                first_name="WILLIAM",
            )
        ),
        claim_status_code="1",
        patient_responsibility_amount=300.00,
        claim_filing_indicator_code="12",
        insurance_plan_type=InsurancePlanType.PPO,
        payer_control_number="94060555410000",
        service_lines=[
            PaymentLine(
                charge_amount=800.00,
                paid_amount=500.00,
                supplemental_amounts=[
                    Amount(
                        qualifier_code="B6",
                        amount=800.00,
                    )
                ],
                service_date_from=date(2024, 3, 1),
                procedure=Procedure(
                    sub_type="CPT",
                    code="99211",
                ),
                adjustments=[
                    Adjustment(
                        group=AdjustmentGroup.PATIENT_RESPONSIBILITY,
                        reason_code="1",
                        amount=300.00,
                    )
                ],
            )
        ],
    )

    return EdiGenPaymentRequest(
        interchange_control=interchange_control,
        functional_group=functional_group,
        transaction=transaction,
        payments=[payment],
    )


def main() -> None:
    request = build_request()
    response = edi_converter.generate_payment_edi(request)
    if response.status_code == 417:
        validation_issues = [
            ValidationIssue.model_validate(issue_json) for issue_json in response.json()
        ]
        print("Validation issues:")
        for issue in validation_issues:
            print(issue)
        return

    if response.status_code != 200:
        raise RuntimeError(
            f"Unexpected response status {response.status_code}: {response.text}"
        )

    edi_text = response.text
    if not edi_text.startswith("ISA*00*"):
        raise RuntimeError(
            'Unexpected response body: generated EDI did not start with "ISA*00*".'
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(edi_text)

    print("Generated EDI:")
    print(edi_text)
    print(f"Saved generated EDI to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()