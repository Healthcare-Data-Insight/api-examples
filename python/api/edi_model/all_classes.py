from __future__ import annotations

import datetime as dt

from pydantic import Field

from .base import EdiConverterModel, to_camel
from .enums import AdjustmentGroup, AmbulanceTransportReason, AmountType, ClaimOrEncounterIdentifierType, \
    AdjudicatedClaimStatus, \
    ConditionsIndicatorCategory, DateType, DmeBillingFrequency, EntityRole, EntityType, GenderType, IdentificationType, \
    InsurancePlanType, MeasurementType, PayerRespSequenceType, PaymentMethodType, QuantityType, ReferenceType, \
    RelationshipType, StatusActionType, TransactionHandlingType, UnitType


class Address(EdiConverterModel):
    'OpenAPI schema for Address.'
    line: str | None = Field(default=None, description='Line. EDI: N301.')
    'Line. EDI: N301.'
    line2: str | None = Field(default=None, description='Line2. EDI: N302.')
    'Line2. EDI: N302.'
    city: str | None = Field(default=None, description='City. EDI: N401.')
    'City. EDI: N401.'
    state_code: str | None = Field(default=None, description='State code. EDI: N402.')
    'State code. EDI: N402.'
    zip_code: str | None = Field(default=None, description='Zip code. EDI: N403.')
    'Zip code. EDI: N403.'
    country_code: str | None = Field(default=None, description='Country code. EDI: N404.')
    'Country code. EDI: N404.'
    location_qualifier: str | None = Field(default=None,
                                           description='Location qualifier; only used for 834 transaction. Since: v2.14.8. EDI: N405.')
    'Location qualifier; only used for 834 transaction. Since: v2.14.8. EDI: N405.'
    location_identifier: str | None = Field(default=None,
                                            description='Location identifier; only used for 834 transaction. Since: v2.14.8. EDI: N406.')
    'Location identifier; only used for 834 transaction. Since: v2.14.8. EDI: N406.'
    country_subdivision_code: str | None = Field(default=None,
                                                 description='Country subdivision code; only used for 834 transaction. Since: v2.14.8. EDI: N407.')
    'Country subdivision code; only used for 834 transaction. Since: v2.14.8. EDI: N407.'
class Adjudication(EdiConverterModel):
    'Loop: 2430; Segment: SVD.'
    payer_identifier: str | None = Field(default=None, description='Payer identifier. EDI: SVD01.')
    'Payer identifier. EDI: SVD01.'
    paid_amount: float | None = Field(default=None, description='Paid amount. EDI: SVD02.')
    'Paid amount. EDI: SVD02.'
    unit_count: float | None = Field(default=None, description='Unit count. EDI: SVD05.')
    'Unit count. EDI: SVD05.'
    bundled_or_unbundled_line_number: int | None = Field(default=None,
                                                         description='Bundled or unbundled line number. EDI: SVD06.')
    'Bundled or unbundled line number. EDI: SVD06.'
    procedure: Procedure | None = Field(default=None, description='Procedure. EDI: SVD03.')
    'Procedure. EDI: SVD03.'
    adjustments: list[Adjustment] = Field(default_factory=list, description='Line adjustments. EDI: CAS.')
    'Line adjustments. EDI: CAS.'
    adjudication_or_payment_date: dt.date | None = Field(default=None,
                                                         description='Adjudication or payment date. EDI: DTP03*573.')
    'Adjudication or payment date. EDI: DTP03*573.'
    remaining_patient_liability_amount: float | None = Field(default=None,
                                                             description='Remaining patient liability amount. EDI: AMT02*EAF.')
    'Remaining patient liability amount. EDI: AMT02*EAF.'
class Adjustment(EdiConverterModel):
    'Segment: CAS.'
    group: AdjustmentGroup | None = Field(default=None,
                                          description='Claim adjustment group code as a string constant. EDI: CAS01.')
    'Claim adjustment group code as a string constant. EDI: CAS01.'
    reason: Code | None = Field(default=None, description='Claim adjustment reason code. EDI: CAS02.')
    'Claim adjustment reason code. EDI: CAS02.'
    amount: float | None = Field(default=None, description='Adjustment amount. EDI: CAS03.')
    'Adjustment amount. EDI: CAS03.'
    quantity: float | None = Field(default=None, description='Adjustment quantity. EDI: CAS04.')
    'Adjustment quantity. EDI: CAS04.'
class AmbulanceTransportInfo(EdiConverterModel):
    'Information related to the ambulance service rendered to a patient. Required on all claims involving ambulance transport services. Segment: CR1.'
    patient_weight: float | None = Field(default=None, description='Patient weight. EDI: CR102.')
    'Patient weight. EDI: CR102.'
    reason_code: str | None = Field(default=None, description='Reason code. EDI: CR104.')
    'Reason code. EDI: CR104.'
    reason: AmbulanceTransportReason | None = Field(default=None,
                                                    description='Ambulance transport reason code as a string constant. EDI: CR104.')
    'Ambulance transport reason code as a string constant. EDI: CR104.'
    transport_distance: float | None = Field(default=None, description='Transport distance. EDI: CR106.')
    'Transport distance. EDI: CR106.'
    round_trip_purpose_description: str | None = Field(default=None,
                                                       description='Round trip purpose description. EDI: CR109.')
    'Round trip purpose description. EDI: CR109.'
    stretcher_purpose_description: str | None = Field(default=None,
                                                      description='Stretcher purpose description. EDI: CR110.')
    'Stretcher purpose description. EDI: CR110.'
class Amount(EdiConverterModel):
    'Segment: AMT.'
    qualifier_code: str | None = Field(default=None,
                                       description='Code specifying the type of amount (amount qualifier code). EDI: AMT01.')
    'Code specifying the type of amount (amount qualifier code). EDI: AMT01.'
    type: AmountType | None = Field(default=None,
                                    description='Type of amount; qualifier code translated to a mnemonic string constant (enum). EDI: AMT01.')
    'Type of amount; qualifier code translated to a mnemonic string constant (enum). EDI: AMT01.'
    amount: float | None = Field(default=None, description='Amount. EDI: AMT02.')
    'Amount. EDI: AMT02.'
class Attachment(EdiConverterModel):
    'Segment: PWK.'
    report_type_code: str | None = Field(default=None, description='Report type code. EDI: PWK01.')
    'Report type code. EDI: PWK01.'
    report_transmission_code: str | None = Field(default=None, description='Report transmission code. EDI: PWK02.')
    'Report transmission code. EDI: PWK02.'
    control_number: str | None = Field(default=None, description='Control number. EDI: PWK06.')
    'Control number. EDI: PWK06.'
class AwsInOutKey(EdiConverterModel):
    'OpenAPI schema for AwsInOutKey.'
    in_key: str | None = Field(default=None, description='Name of the EDI file in the input bucket.')
    'Name of the EDI file in the input bucket.'
    out_key: str | None = Field(default=None,
                                description='Name of the converted file in the output bucket. If not provided, the converter will create the key based on the input file name with the appropriate extension.')
    'Name of the converted file in the output bucket. If not provided, the converter will create the key based on the input file name with the appropriate extension.'
class AwsRequest(EdiConverterModel):
    'OpenAPI schema for AwsRequest.'
    in_bucket: str | None = Field(default=None,
                                  description="Name of the bucket containing EDI files. If not defined, the converter will use the value from the 'IN_BUCKET' environment variable.")
    "Name of the bucket containing EDI files. If not defined, the converter will use the value from the 'IN_BUCKET' environment variable."
    in_key: str | None = Field(default=None,
                               description="Name of the EDI file in the input bucket. You must provide one of 'inKey' or 'inOutKeys'.")
    "Name of the EDI file in the input bucket. You must provide one of 'inKey' or 'inOutKeys'."
    out_key: str | None = Field(default=None,
                                description='Name of the converted file in the output bucket. If not provided, the converter will create the key based on the input file name with the appropriate extension.')
    'Name of the converted file in the output bucket. If not provided, the converter will create the key based on the input file name with the appropriate extension.'
    in_out_keys: list[AwsInOutKey] = Field(default_factory=list,
                                           description='List of input/output key pairs to convert multiple files.')
    'List of input/output key pairs to convert multiple files.'
    out_bucket: str | None = Field(default=None,
                                   description="Name of the bucket for converted files. If not defined, the converter will use the value from the 'OUT_BUCKET' environment variable.")
    "Name of the bucket for converted files. If not defined, the converter will use the value from the 'OUT_BUCKET' environment variable."
    out_format: str | None = Field(default=None,
                                   description="The format to convert EDI files to. The function defaults to JSON. You can also define the 'OUT_FORMAT' environment variable to override the default.")
    "The format to convert EDI files to. The function defaults to JSON. You can also define the 'OUT_FORMAT' environment variable to override the default."
    csv_schema_name: str | None = Field(default=None,
                                        description="Name of the <a href='/docs/csv/schemas/#built-in-conversion-schemas'>CSV conversion schema</a>. Defaults to 'lines-with-header-repeat-first-row' (single file schema). You can also define the 'CSV_SCHEMA_NAME' environment variable to override the default.")
    "Name of the <a href='/docs/csv/schemas/#built-in-conversion-schemas'>CSV conversion schema</a>. Defaults to 'lines-with-header-repeat-first-row' (single file schema). You can also define the 'CSV_SCHEMA_NAME' environment variable to override the default."
    warnings_in_output: bool | None = Field(default=None,
                                            description="Include EDI parser warnings in the output files, see <a href='/docs/ediconvert-api/user-guide/#error-handling'>documentation on error handling</a> for more details. You can also define the 'OUTPUT_WARNINGS' environment variable and set its value to 'True'.")
    "Include EDI parser warnings in the output files, see <a href='/docs/ediconvert-api/user-guide/#error-handling'>documentation on error handling</a> for more details. You can also define the 'OUTPUT_WARNINGS' environment variable and set its value to 'True'."
    max_warnings: int | None = Field(default=None,
                                     description="The maximum number of parsing warnings per file before stopping and raising an error. Defaults to 3000. Set to -1 to suppress raising the 'too many warnings' error; the converter will process the entire file.")
    "The maximum number of parsing warnings per file before stopping and raising an error. Defaults to 3000. Set to -1 to suppress raising the 'too many warnings' error; the converter will process the entire file."
    is_about_only: bool | None = Field(default=None,
                                       description="Print the converter's version and license information and exit. All other fields are ignored.")
    "Print the converter's version and license information and exit. All other fields are ignored."
class BatchStatus(EdiConverterModel):
    'Status of multiple claims provided at a provider or a receiver level. At the receiver level, this is a status of all claims in the transaction.'
    trace_identifier: str | None = Field(default=None,
                                         description='Transaction control number from 837 for the status at the receiver level. It is a dummy number for the provider-level status; should be ignored. EDI: TRN02.')
    'Transaction control number from 837 for the status at the receiver level. It is a dummy number for the provider-level status; should be ignored. EDI: TRN02.'
    status_infos: list[StatusInfo] = Field(default_factory=list, description='Status infos.')
    'Status infos.'
    accepted_quantity: float | None = Field(default=None, description='Accepted quantity. EDI: QTY02*QA.')
    'Accepted quantity. EDI: QTY02*QA.'
    accepted_amount: float | None = Field(default=None, description='Accepted amount. EDI: AMT02*YU.')
    'Accepted amount. EDI: AMT02*YU.'
    rejected_quantity: float | None = Field(default=None, description='Rejected quantity. EDI: QTY02*QC.')
    'Rejected quantity. EDI: QTY02*QC.'
    rejected_amount: float | None = Field(default=None, description='Rejected amount. EDI: AMT02*YY.')
    'Rejected amount. EDI: AMT02*YY.'
class ClaimStatus(EdiConverterModel):
    'Status of a single claim. Also contains patient, provider and receiver information. Loop: 2200D.'
    id: str | None = Field(default=None, description='Unique payment identifier assigned by the converter.')
    'Unique payment identifier assigned by the converter.'
    object_type: str | None = Field(default=None, description="Type of this object, always set to 'CLAIM_STATUS'.")
    "Type of this object, always set to 'CLAIM_STATUS'."
    patient: PartyIdName | None = Field(default=None,
                                        description='The insured (subscriber) or patient as stated on 837 claim. EDI: Loop: 2100D, NM1*QC.')
    'The insured (subscriber) or patient as stated on 837 claim. EDI: Loop: 2100D, NM1*QC.'
    patient_control_number: str | None = Field(default=None, description='Patient control number. EDI: TRN02.')
    'Patient control number. EDI: TRN02.'
    status_infos: list[StatusInfo] = Field(default_factory=list, description='Status infos.')
    'Status infos.'
    payer_claim_control_number: str | None = Field(default=None,
                                                   description='Payer claim control number. EDI: REF02*1K.')
    'Payer claim control number. EDI: REF02*1K.'
    clearinghouse_trace_number: str | None = Field(default=None,
                                                   description='Clearinghouse trace number. EDI: REF02*D9.')
    'Clearinghouse trace number. EDI: REF02*D9.'
    bill_type_code: str | None = Field(default=None, description='Bill type code. EDI: REF02*BLT.')
    'Bill type code. EDI: REF02*BLT.'
    service_date_from: dt.date | None = Field(default=None,
                                              description='Service date for professional or statement date for institutional. EDI: DTP03*472.')
    'Service date for professional or statement date for institutional. EDI: DTP03*472.'
    service_date_to: dt.date | None = Field(default=None,
                                            description="The end date of the service or statement date period. Set to 'serviceDateFrom' if the period is a single date. EDI: DTP03*472.")
    "The end date of the service or statement date period. Set to 'serviceDateFrom' if the period is a single date. EDI: DTP03*472."
    receiver: PartyIdName | None = Field(default=None,
                                         description='The Receiver is the entity that expects the response from the Source. Can be a provider, a provider group, a claims clearinghouse, etc. EDI: Loop: 2000B, NM1*40.')
    'The Receiver is the entity that expects the response from the Source. Can be a provider, a provider group, a claims clearinghouse, etc. EDI: Loop: 2000B, NM1*40.'
    receiver_batch_status: BatchStatus | None = Field(default=None,
                                                      description='Receiver batch status. EDI: Loop: 2200B.')
    'Receiver batch status. EDI: Loop: 2200B.'
    provider: PartyIdName | None = Field(default=None,
                                         description='Billing provider for 277CA. EDI: Loop: 2100C, NM1*85.')
    'Billing provider for 277CA. EDI: Loop: 2100C, NM1*85.'
    provider_batch_status: BatchStatus | None = Field(default=None,
                                                      description='Provider batch status. EDI: Loop: 2200C.')
    'Provider batch status. EDI: Loop: 2200C.'
    line_statuses: list[ServiceLineStatus] = Field(default_factory=list,
                                                   description='Rejected service lines. EDI: Loop: 2220D.')
    'Rejected service lines. EDI: Loop: 2220D.'
    transaction: Transaction277 | None = Field(default=None,
                                               description='Parent EDI transaction for this object. EDI: ST.')
    'Parent EDI transaction for this object. EDI: ST.'
class Code(EdiConverterModel):
    'Code and description.'
    sub_type: str | None = Field(default=None, description='Healthcare code subtype, such as CPT, HCPCS, ICD_10, NDC.')
    'Healthcare code subtype, such as CPT, HCPCS, ICD_10, NDC.'
    code: str | None = Field(default=None, description='Healthcare code.')
    'Healthcare code.'
    desc: str | None = Field(default=None, description='Code description.')
    'Code description.'
class CodeAndAmount(Code):
    'OpenAPI schema for CodeAndAmount.'
    amount: float | None = Field(default=None, description='Amount. EDI: HI01-5.')
    'Amount. EDI: HI01-5.'
class CodeAndDate(Code):
    'OpenAPI schema for CodeAndDate.'
    occurrence_date: dt.date | None = Field(default=None, description='Occurrence date. EDI: HI01-4.')
    'Occurrence date. EDI: HI01-4.'
class ConditionsIndicator(EdiConverterModel):
    'Segment: CRC.'
    category_code: str | None = Field(default=None, description='Category code. EDI: CRC01.')
    'Category code. EDI: CRC01.'
    category: ConditionsIndicatorCategory | None = Field(default=None,
                                                         description='Category code as constant (enum). EDI: CRC01.')
    'Category code as constant (enum). EDI: CRC01.'
    yes_or_no_condition: str | None = Field(default=None, description='Yes or no condition. EDI: CRC02.')
    'Yes or no condition. EDI: CRC02.'
    condition_codes: list[str] = Field(default_factory=list,
                                       description='Condition codes. EDI: CRC03, CRC04, CRC05, CRC06, CRC07.')
    'Condition codes. EDI: CRC03, CRC04, CRC05, CRC06, CRC07.'
class ContactInfo(EdiConverterModel):
    'Segment: PER.'
    function_code: str | None = Field(default=None, description='Function code. EDI: PER01.')
    'Function code. EDI: PER01.'
    name: str | None = Field(default=None, description='Name. EDI: PER02.')
    'Name. EDI: PER02.'
    contact_numbers: list[ContactNumber] = Field(default_factory=list, description='Contact numbers.')
    'Contact numbers.'
class ContactNumber(EdiConverterModel):
    'Segment: PER.'
    type: str | None = Field(default=None, description='Type of contact number. EDI: PER03, PER05, PER07.')
    'Type of contact number. EDI: PER03, PER05, PER07.'
    number: str | None = Field(default=None, description='Number. EDI: PER04, PER06, PER08.')
    'Number. EDI: PER04, PER06, PER08.'
class ContractInfo(EdiConverterModel):
    'Required when the submitter is contractually obligated to supply this information on post-adjudicated claims. Segment: CN1.'
    contract_type_code: str | None = Field(default=None, description='Contract type code. EDI: CN101.')
    'Contract type code. EDI: CN101.'
    amount: float | None = Field(default=None, description='Amount. EDI: CN102.')
    'Amount. EDI: CN102.'
    percentage: float | None = Field(default=None, description='Percentage. EDI: CN103.')
    'Percentage. EDI: CN103.'
    contract_code: str | None = Field(default=None, description='Contract code. EDI: CN104.')
    'Contract code. EDI: CN104.'
    term_discount_percentage: float | None = Field(default=None, description='Term discount percentage. EDI: CN105.')
    'Term discount percentage. EDI: CN105.'
    version_identifier: str | None = Field(default=None, description='Version identifier. EDI: CN106.')
    'Version identifier. EDI: CN106.'
class CoordinationOfBenefits(EdiConverterModel):
    'Loop: 2320; Segment: COB.'
    payer_responsibility_sequence_code: str | None = Field(default=None,
                                                           description='Payer responsibility sequence code. EDI: COB01.')
    'Payer responsibility sequence code. EDI: COB01.'
    group_or_policy_number: str | None = Field(default=None, description='Group or policy number. EDI: COB02.')
    'Group or policy number. EDI: COB02.'
    coordination_of_benefits_code: str | None = Field(default=None,
                                                      description='Coordination of benefits code. EDI: COB03.')
    'Coordination of benefits code. EDI: COB03.'
    service_type_codes: list[str] = Field(default_factory=list,
                                          description='Service type codes. Since: v2.14.8. EDI: COB04.')
    'Service type codes. Since: v2.14.8. EDI: COB04.'
    additional_identifiers: list[Reference] = Field(default_factory=list,
                                                    description='Additional identifiers. EDI: REF.')
    'Additional identifiers. EDI: REF.'
    date_from: dt.date | None = Field(default=None, description='Date from. EDI: DTP03*344.')
    'Date from. EDI: DTP03*344.'
    date_to: dt.date | None = Field(default=None, description='Date to. EDI: DTP03*345.')
    'Date to. EDI: DTP03*345.'
    insurers: list[Party] = Field(default_factory=list, description='Insurers.')
    'Insurers.'
class Date(EdiConverterModel):
    'Segment: DTP.'
    qualifier_code: str | None = Field(default=None, description='Code specifying type of date or time. EDI: DTP01.')
    'Code specifying type of date or time. EDI: DTP01.'
    type: DateType | None = Field(default=None,
                                  description='Type of date; qualifier code translated to a mnemonic string constant (enum). EDI: DTP01.')
    'Type of date; qualifier code translated to a mnemonic string constant (enum). EDI: DTP01.'
    date: dt.date | None = Field(default=None,
                                 description="The date value or the first date of the date range ('RD8' qualifier). EDI: DTP03.")
    "The date value or the first date of the date range ('RD8' qualifier). EDI: DTP03."
    date_to: dt.date | None = Field(default=None,
                                    description="The second date if the value is the date range ('RD8' qualifier), otherwise null. EDI: DTP03.")
    "The second date if the value is the date range ('RD8' qualifier), otherwise null. EDI: DTP03."
class DentClaim(EdiConverterModel):
    'Loop: 2300; Segment: CLM.'
    id: str | None = Field(default=None, description='Unique payment identifier assigned by the converter.')
    'Unique payment identifier assigned by the converter.'
    object_type: str | None = Field(default=None, description="Type of this object, set to 'CLAIM'.")
    "Type of this object, set to 'CLAIM'."
    patient_control_number: str | None = Field(default=None,
                                               description='Identifier used to track a claim from creation by the health care provider through payment. EDI: CLM01.')
    'Identifier used to track a claim from creation by the health care provider through payment. EDI: CLM01.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: CLM02.')
    'Charge amount. EDI: CLM02.'
    patient_paid_amount: float | None = Field(default=None, description='Patient paid amount. EDI: AMT02*F5.')
    'Patient paid amount. EDI: AMT02*F5.'
    facility_code: Code | None = Field(default=None,
                                       description='Place of service code (professional/dental) or UB facility code (institutional) from the original claim. EDI: CLM05-1.')
    'Place of service code (professional/dental) or UB facility code (institutional) from the original claim. EDI: CLM05-1.'
    frequency_code: Code | None = Field(default=None, description='Frequency code. EDI: CLM05-3.')
    'Frequency code. EDI: CLM05-3.'
    service_date_from: dt.date | None = Field(default=None, description='The earliest service date from service lines.')
    'The earliest service date from service lines.'
    service_date_to: dt.date | None = Field(default=None, description='The latest service date from service lines.')
    'The latest service date from service lines.'
    subscriber: Subscriber | None = Field(default=None, description='The insured (subscriber). EDI: Loop: 2000B.')
    'The insured (subscriber). EDI: Loop: 2000B.'
    patient: Patient | None = Field(default=None,
                                    description='Patient if different from the the insured (subscriber). EDI: Loop: 2110CA.')
    'Patient if different from the the insured (subscriber). EDI: Loop: 2110CA.'
    other_subscribers: list[OtherSubscriber] = Field(default_factory=list,
                                                     description="Other subscribers and their payer's information. EDI: Loop: 2320.")
    "Other subscribers and their payer's information. EDI: Loop: 2320."
    service_lines: list[DentLine] = Field(default_factory=list, description='Service lines. EDI: Loop: 2400.')
    'Service lines. EDI: Loop: 2400.'
    transaction: Transaction837 | None = Field(default=None,
                                               description='Parent EDI transaction for this object. EDI: ST.')
    'Parent EDI transaction for this object. EDI: ST.'
    provider_signature_indicator: str | None = Field(default=None,
                                                     description='Provider signature indicator. EDI: CLM06.')
    'Provider signature indicator. EDI: CLM06.'
    assignment_participation_code: str | None = Field(default=None,
                                                      description='Assignment participation code. EDI: CLM07.')
    'Assignment participation code. EDI: CLM07.'
    assignment_certification_indicator: str | None = Field(default=None,
                                                           description='Assignment certification indicator. EDI: CLM08.')
    'Assignment certification indicator. EDI: CLM08.'
    release_of_information_code: str | None = Field(default=None,
                                                    description='Release of information code. EDI: CLM09.')
    'Release of information code. EDI: CLM09.'
    related_cause: RelatedCauseInfo | None = Field(default=None, description='Related cause. EDI: CLM11.')
    'Related cause. EDI: CLM11.'
    special_program_code: str | None = Field(default=None, description='Special program code. EDI: CLM12.')
    'Special program code. EDI: CLM12.'
    delay_reason_code: str | None = Field(default=None, description='Delay reason code. EDI: CLM20.')
    'Delay reason code. EDI: CLM20.'
    service_authorization_exception_code: str | None = Field(default=None,
                                                             description='Service authorization exception code. EDI: REF02*4N.')
    'Service authorization exception code. EDI: REF02*4N.'
    referral_number: str | None = Field(default=None, description='Referral number. EDI: REF02*9F.')
    'Referral number. EDI: REF02*9F.'
    prior_authorization_number: str | None = Field(default=None,
                                                   description='Prior authorization number. EDI: REF02*G1.')
    'Prior authorization number. EDI: REF02*G1.'
    original_reference_number: str | None = Field(default=None, description='Original reference number. EDI: REF02*F8.')
    'Original reference number. EDI: REF02*F8.'
    repriced_reference_number: str | None = Field(default=None, description='Repriced reference number. EDI: REF02*9A.')
    'Repriced reference number. EDI: REF02*9A.'
    adjusted_repriced_reference_number: str | None = Field(default=None,
                                                           description='Adjusted repriced reference number. EDI: REF02*9C.')
    'Adjusted repriced reference number. EDI: REF02*9C.'
    clearinghouse_trace_number: str | None = Field(default=None,
                                                   description='Clearinghouse trace number. EDI: REF02*D9.')
    'Clearinghouse trace number. EDI: REF02*D9.'
    medical_record_number: str | None = Field(default=None, description='Medical record number. EDI: REF02*EA.')
    'Medical record number. EDI: REF02*EA.'
    demonstration_project_identifier: str | None = Field(default=None,
                                                         description='Demonstration project identifier. EDI: REF02*P4.')
    'Demonstration project identifier. EDI: REF02*P4.'
    accident_date: dt.date | None = Field(default=None, description='Accident date. EDI: DTP03*439.')
    'Accident date. EDI: DTP03*439.'
    orthodontic_banding_date: dt.date | None = Field(default=None,
                                                     description='Orthodontic banding date. EDI: DTP03*452.')
    'Orthodontic banding date. EDI: DTP03*452.'
    repricer_received_date: dt.date | None = Field(default=None, description='Repricer received date. EDI: DTP03*050.')
    'Repricer received date. EDI: DTP03*050.'
    orthodontic_info: OrthodonticInfo | None = Field(default=None, description='Orthodontic info.')
    'Orthodontic info.'
    tooth_statuses: list[ToothStatus] = Field(default_factory=list, description='Tooth statuses.')
    'Tooth statuses.'
    predetermination_of_benefits_identifier: str | None = Field(default=None,
                                                                description='Predetermination of benefits identifier. EDI: REF02*G3.')
    'Predetermination of benefits identifier. EDI: REF02*G3.'
    fixed_format_records: list[str] = Field(default_factory=list, description='Fixed format records. EDI: K301.')
    'Fixed format records. EDI: K301.'
    claim_note: str | None = Field(default=None,
                                   description='Free-form comments or instructions. All note segments are concatenated together into this field. EDI: NTE02.')
    'Free-form comments or instructions. All note segments are concatenated together into this field. EDI: NTE02.'
    billing_provider: Provider | None = Field(default=None, description='Billing provider. EDI: NM1*85.')
    'Billing provider. EDI: NM1*85.'
    pay_to_address: Party | None = Field(default=None, description='Pay to address. EDI: NM1*87.')
    'Pay to address. EDI: NM1*87.'
    pay_to_plan: Party | None = Field(default=None, description='Pay-to plan for subrogation claims. EDI: NM1*PE.')
    'Pay-to plan for subrogation claims. EDI: NM1*PE.'
    providers: list[Provider] = Field(default_factory=list,
                                      description='Providers for this claim, except for the billing provider.')
    'Providers for this claim, except for the billing provider.'
    attachments: list[Attachment] = Field(default_factory=list, description='Attachments. EDI: PWK.')
    'Attachments. EDI: PWK.'
    contract_info: ContractInfo | None = Field(default=None, description='Contract info. EDI: CN1.')
    'Contract info. EDI: CN1.'
class DentLine(EdiConverterModel):
    'Loop: 2400; Segment: SV3.'
    source_line_id: str | None = Field(default=None, description='Line item control number. EDI: REF02*6R.')
    'Line item control number. EDI: REF02*6R.'
    oral_cavity_designation_codes: list[str] = Field(default_factory=list,
                                                     description='Oral cavity designation codes. EDI: SV304.')
    'Oral cavity designation codes. EDI: SV304.'
    prosthesis_crown_or_inlay_code: str | None = Field(default=None,
                                                       description='Prosthesis crown or inlay code. EDI: SV305.')
    'Prosthesis crown or inlay code. EDI: SV305.'
    predetermination_of_benefits_identifier: str | None = Field(default=None,
                                                                description='Predetermination of benefits identifier. EDI: REF02*G3.')
    'Predetermination of benefits identifier. EDI: REF02*G3.'
    repriced_reference_number: str | None = Field(default=None, description='Repriced reference number. EDI: REF02*9B.')
    'Repriced reference number. EDI: REF02*9B.'
    adjusted_repriced_reference_number: str | None = Field(default=None,
                                                           description='Adjusted repriced reference number. EDI: REF02*9D.')
    'Adjusted repriced reference number. EDI: REF02*9D.'
    prior_authorization: str | None = Field(default=None, description='Prior authorization. EDI: REF02*G1.')
    'Prior authorization. EDI: REF02*G1.'
    referral_number: str | None = Field(default=None, description='Referral number. EDI: REF02*9F.')
    'Referral number. EDI: REF02*9F.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: SV302.')
    'Charge amount. EDI: SV302.'
    sales_tax_amount: float | None = Field(default=None, description='Sales tax amount. EDI: AMT02*T.')
    'Sales tax amount. EDI: AMT02*T.'
    service_date_from: dt.date | None = Field(default=None, description='Service date from. EDI: DTP03*472.')
    'Service date from. EDI: DTP03*472.'
    service_date_to: dt.date | None = Field(default=None, description='Service date to. EDI: DTP03*472.')
    'Service date to. EDI: DTP03*472.'
    prior_placement_date: dt.date | None = Field(default=None,
                                                 description='Prior placement date. EDI: DTP03*441, DTP03*139.')
    'Prior placement date. EDI: DTP03*441, DTP03*139.'
    orthodontic_banding_date: dt.date | None = Field(default=None,
                                                     description='Orthodontic banding date. EDI: DTP03*452.')
    'Orthodontic banding date. EDI: DTP03*452.'
    replacement_date: dt.date | None = Field(default=None, description='Replacement date. EDI: DTP03*446.')
    'Replacement date. EDI: DTP03*446.'
    treatment_start_date: dt.date | None = Field(default=None, description='Treatment start date. EDI: DTP03*196.')
    'Treatment start date. EDI: DTP03*196.'
    treatment_completion_date: dt.date | None = Field(default=None,
                                                      description='Treatment completion date. EDI: DTP03*198.')
    'Treatment completion date. EDI: DTP03*198.'
    unit_count: float | None = Field(default=None, description='Unit count. EDI: SV306.')
    'Unit count. EDI: SV306.'
    procedure: Procedure | None = Field(default=None,
                                        description='Procedure. EDI: SV302*HC, SV302*AD, SV302*WK, SV302*IV.')
    'Procedure. EDI: SV302*HC, SV302*AD, SV302*WK, SV302*IV.'
    attachments: list[Attachment] = Field(default_factory=list, description='Attachments. EDI: PWK.')
    'Attachments. EDI: PWK.'
    contract_info: ContractInfo | None = Field(default=None, description='Contract info. EDI: CN1.')
    'Contract info. EDI: CN1.'
    providers: list[Provider] = Field(default_factory=list, description='Providers for this service line.')
    'Providers for this service line.'
    adjudications: list[Adjudication] = Field(default_factory=list, description='Adjudications. EDI: Loop: 2430, SVD.')
    'Adjudications. EDI: Loop: 2430, SVD.'
    adjustments: list[Adjustment] = Field(default_factory=list,
                                          description='Copy of line adjustments from the adjudication list for backward compatibility. EDI: CAS.')
    'Copy of line adjustments from the adjudication list for backward compatibility. EDI: CAS.'
    fixed_format_records: list[str] = Field(default_factory=list, description='Fixed format records. EDI: K301.')
    'Fixed format records. EDI: K301.'
    tooth_infos: list[ToothInfo] = Field(default_factory=list, description='Tooth infos.')
    'Tooth infos.'
    diag_pointers: list[int] = Field(default_factory=list,
                                     description="Diagnosis pointers. Each pointer is an index of the diagnosis in the 'diags' array at the claim level. EDI: SV302.")
    "Diagnosis pointers. Each pointer is an index of the diagnosis in the 'diags' array at the claim level. EDI: SV302."
    diags: list[Code] = Field(default_factory=list,
                              description='Copy of diagnosis codes from the claim based on diagnosis pointers. EDI: SV302.')
    'Copy of diagnosis codes from the claim based on diagnosis pointers. EDI: SV302.'
class Disability(EdiConverterModel):
    'Loop: 2200.'
    type_code: str | None = Field(default=None, description='Type code. EDI: DSB01.')
    'Type code. EDI: DSB01.'
    diagnosis_code: str | None = Field(default=None, description='Diagnosis code. EDI: DSB08.')
    'Diagnosis code. EDI: DSB08.'
    date_from: dt.date | None = Field(default=None, description='Date from. EDI: DTP03*360.')
    'Date from. EDI: DTP03*360.'
    date_to: dt.date | None = Field(default=None, description='Date to. EDI: DTP03*361.')
    'Date to. EDI: DTP03*361.'
class DmeCertification(EdiConverterModel):
    'DME Certification. Required when a Durable Medical Equipment Regional Carrier Certificate of Medical Necessity (DMERC CMN) or a DMERC Information Form (DIF) or Oxygen Therapy Certification is included on this service line. Segment: CR3.'
    certification_type_code: str | None = Field(default=None, description='Certification type code. EDI: CR301.')
    'Certification type code. EDI: CR301.'
    duration_unit_type: UnitType | None = Field(default=None,
                                                description='Unit of measurement for the length of time for DME equipment. EDI: CR302.')
    'Unit of measurement for the length of time for DME equipment. EDI: CR302.'
    duration: float | None = Field(default=None, description='Length of time DME equipment is needed. EDI: CR303.')
    'Length of time DME equipment is needed. EDI: CR303.'
class DmeService(EdiConverterModel):
    'Durable medical equipment rental and purchase price information. Segment: SV5.'
    duration_unit_type: UnitType | None = Field(default=None,
                                                description='Unit of measurement for the length of medical treatment. EDI: SV502.')
    'Unit of measurement for the length of medical treatment. EDI: SV502.'
    length_of_medical_necessity: float | None = Field(default=None,
                                                      description='Length of medical treatment required. EDI: SV503.')
    'Length of medical treatment required. EDI: SV503.'
    rental_price: float | None = Field(default=None, description='Rental price. EDI: SV504.')
    'Rental price. EDI: SV504.'
    purchase_price: float | None = Field(default=None, description='Purchase price. EDI: SV505.')
    'Purchase price. EDI: SV505.'
    billing_frequency_code: str | None = Field(default=None,
                                               description='Frequency at which the rental equipment is billed. EDI: SV506.')
    'Frequency at which the rental equipment is billed. EDI: SV506.'
    billing_frequency: DmeBillingFrequency | None = Field(default=None,
                                                          description='Frequency at which the rental equipment is billed, expressed as enum (string constant). EDI: SV506.')
    'Frequency at which the rental equipment is billed, expressed as enum (string constant). EDI: SV506.'
class EdiGenClaimRequest(EdiConverterModel):
    'Request for EDI writer with interchange and functional group control segments and claims.'
    interchange_control: InterchangeControl | None = Field(default=None, description='Interchange control.')
    'Interchange control.'
    functional_group: FunctionalGroup | None = Field(default=None, description='Functional group.')
    'Functional group.'
    transaction: Transaction837 | None = Field(default=None, description='Transaction.')
    'Transaction.'
    claims: list[InstClaim | ProfClaim] = Field(default_factory=list, description='Claims.')
    'Claims.'
class ErrorInfo(EdiConverterModel):
    'OpenAPI schema for ErrorInfo.'
    object_type: str | None = Field(default=None, description='Type of error, could be ERROR or WARNING.')
    'Type of error, could be ERROR or WARNING.'
    message: str | None = Field(default=None, description='Detailed error message.')
    'Detailed error message.'
    file_name: str | None = Field(default=None, description='File name where the error or warning occurred.')
    'File name where the error or warning occurred.'
class FileInfo(EdiConverterModel):
    'OpenAPI schema for FileInfo.'
    name: str | None = Field(default=None, description='File name.')
    'File name.'
    url: str | None = Field(default=None, description='URL of the file, including the full path.')
    'URL of the file, including the full path.'
    last_modified_date_time: str | None = Field(default=None, description='Last modified date and time of the file.')
    'Last modified date and time of the file.'
class FormQuestionResponse(EdiConverterModel):
    'Response to a question on a form. Segment: FRM.'
    question_identifier: str | None = Field(default=None, description='Question identifier. EDI: FRM01.')
    'Question identifier. EDI: FRM01.'
    yes_or_no_response: str | None = Field(default=None, description='Yes or no response. EDI: FRM02.')
    'Yes or no response. EDI: FRM02.'
    text_response: str | None = Field(default=None, description='Text response. EDI: FRM03.')
    'Text response. EDI: FRM03.'
    date_response: dt.date | None = Field(default=None, description='Date response. EDI: FRM04.')
    'Date response. EDI: FRM04.'
    number_response: float | None = Field(default=None, description='Number response. EDI: FRM05.')
    'Number response. EDI: FRM05.'
class FormResponse(EdiConverterModel):
    'Response to a standardized paper form, such as DMERC CMN. Segment: LQ.'
    form_type_code: str | None = Field(default=None, description='Form type. EDI: LQ01.')
    'Form type. EDI: LQ01.'
    form_identifier: str | None = Field(default=None, description='Specific form number. EDI: LQ02.')
    'Specific form number. EDI: LQ02.'
    responses: list[FormQuestionResponse] = Field(default_factory=list, description='Responses. EDI: FRM.')
    'Responses. EDI: FRM.'
class FunctionalGroup(EdiConverterModel):
    'Segment: GS.'
    transaction_type: str | None = Field(default=None,
                                         description='Transaction type as enum for EDI generator; if not provided, GS01, GS08 must be populated.')
    'Transaction type as enum for EDI generator; if not provided, GS01, GS08 must be populated.'
    functional_identifier_code: str | None = Field(default=None, description='Functional identifier code. EDI: GS01.')
    'Functional identifier code. EDI: GS01.'
    sender_code: str | None = Field(default=None, description='Sender code. EDI: GS02.')
    'Sender code. EDI: GS02.'
    receiver_code: str | None = Field(default=None, description='Receiver code. EDI: GS03.')
    'Receiver code. EDI: GS03.'
    date: dt.date | None = Field(default=None, description='Date. EDI: GS04.')
    'Date. EDI: GS04.'
    time: str | None = Field(default=None, description='Time. EDI: GS05.')
    'Time. EDI: GS05.'
    control_number: int | None = Field(default=None, description='Control number. EDI: GS06.')
    'Control number. EDI: GS06.'
    responsible_agency_code: str | None = Field(default=None, description='Responsible agency code. EDI: GS07.')
    'Responsible agency code. EDI: GS07.'
    version: str | None = Field(default=None, description='Version. EDI: GS08.')
    'Version. EDI: GS08.'
class HealthCoverage(EdiConverterModel):
    'Loop: 2300; Segment: HD.'
    maintenance_type_code: str | None = Field(default=None, description='Maintenance type code. EDI: HD01.')
    'Maintenance type code. EDI: HD01.'
    insurance_line_code: str | None = Field(default=None, description='Insurance line code. EDI: HD03.')
    'Insurance line code. EDI: HD03.'
    plan_description: str | None = Field(default=None, description='Plan description. EDI: HD04.')
    'Plan description. EDI: HD04.'
    coverage_level_code: str | None = Field(default=None, description='Coverage level code. EDI: HD05.')
    'Coverage level code. EDI: HD05.'
    late_enrollment_indicator: str | None = Field(default=None, description='Late enrollment indicator. EDI: HD09.')
    'Late enrollment indicator. EDI: HD09.'
    coverage_dates: list[Date] = Field(default_factory=list, description='Coverage dates. EDI: DTP.')
    'Coverage dates. EDI: DTP.'
    contract_amounts: list[Amount] = Field(default_factory=list, description='Contract amounts. EDI: AMT.')
    'Contract amounts. EDI: AMT.'
    group_or_policy_numbers: list[Reference] = Field(default_factory=list,
                                                     description='Group or policy numbers. EDI: REF.')
    'Group or policy numbers. EDI: REF.'
    prior_coverage_month_count: str | None = Field(default=None,
                                                   description='Prior coverage month count. EDI: REF02*QQ.')
    'Prior coverage month count. EDI: REF02*QQ.'
    providers: list[Party] = Field(default_factory=list, description='Providers.')
    'Providers.'
    cobs: list[CoordinationOfBenefits] = Field(default_factory=list, description='Coordination of Benefits.')
    'Coordination of Benefits.'
class InpatientAdjudication(EdiConverterModel):
    'Contains Remittance Advice Remark Codes at the claim level and/or Medicare or Medicaid-specific amounts for inpatient institutional claims. Segment: MIA.'
    covered_days_or_visits_count: int | None = Field(default=None,
                                                     description='Covered days or visits count. EDI: MIA01.')
    'Covered days or visits count. EDI: MIA01.'
    pps_operating_outlier_amount: float | None = Field(default=None,
                                                       description='Pps operating outlier amount. EDI: MIA02.')
    'Pps operating outlier amount. EDI: MIA02.'
    lifetime_psychiatric_days_count: int | None = Field(default=None,
                                                        description='Lifetime psychiatric days count. EDI: MIA03.')
    'Lifetime psychiatric days count. EDI: MIA03.'
    drg_amount: float | None = Field(default=None, description='Drg amount. EDI: MIA04.')
    'Drg amount. EDI: MIA04.'
    disproportionate_share_amount: float | None = Field(default=None,
                                                        description='Disproportionate share amount. EDI: MIA06.')
    'Disproportionate share amount. EDI: MIA06.'
    msp_pass_through_amount: float | None = Field(default=None, description='Msp pass through amount. EDI: MIA07.')
    'Msp pass through amount. EDI: MIA07.'
    pps_capital_amount: float | None = Field(default=None, description='Pps capital amount. EDI: MIA08.')
    'Pps capital amount. EDI: MIA08.'
    pps_capital_fsp_drg_amount: float | None = Field(default=None,
                                                     description='Pps capital fsp drg amount. EDI: MIA09.')
    'Pps capital fsp drg amount. EDI: MIA09.'
    pps_capital_hsp_drg_amount: float | None = Field(default=None,
                                                     description='Pps capital hsp drg amount. EDI: MIA10.')
    'Pps capital hsp drg amount. EDI: MIA10.'
    pps_capital_dsh_drg_amount: float | None = Field(default=None,
                                                     description='Pps capital dsh drg amount. EDI: MIA11.')
    'Pps capital dsh drg amount. EDI: MIA11.'
    old_capital_amount: float | None = Field(default=None, description='Old capital amount. EDI: MIA12.')
    'Old capital amount. EDI: MIA12.'
    pps_capital_ime_amount: float | None = Field(default=None, description='Pps capital ime amount. EDI: MIA13.')
    'Pps capital ime amount. EDI: MIA13.'
    pps_operating_hospital_specific_drg_amount: float | None = Field(default=None,
                                                                     description='Pps operating hospital specific drg amount. EDI: MIA14.')
    'Pps operating hospital specific drg amount. EDI: MIA14.'
    cost_report_day_count: int | None = Field(default=None, description='Cost report day count. EDI: MIA15.')
    'Cost report day count. EDI: MIA15.'
    pps_operating_federal_specific_drg_amount: float | None = Field(default=None,
                                                                    description='Pps operating federal specific drg amount. EDI: MIA16.')
    'Pps operating federal specific drg amount. EDI: MIA16.'
    pps_capital_outlier_amount: float | None = Field(default=None,
                                                     description='Pps capital outlier amount. EDI: MIA17.')
    'Pps capital outlier amount. EDI: MIA17.'
    indirect_teaching_amount: float | None = Field(default=None, description='Indirect teaching amount. EDI: MIA18.')
    'Indirect teaching amount. EDI: MIA18.'
    non_payable_professional_component_amount: float | None = Field(default=None,
                                                                    description='Non payable professional component amount. EDI: MIA19.')
    'Non payable professional component amount. EDI: MIA19.'
    pps_capital_exception_amount: float | None = Field(default=None,
                                                       description='Pps capital exception amount. EDI: MIA24.')
    'Pps capital exception amount. EDI: MIA24.'
    remarks: list[Code] = Field(default_factory=list,
                                description='Remark codes. EDI: MIA05, MIA20, MIA21, MIA22, MIA23.')
    'Remark codes. EDI: MIA05, MIA20, MIA21, MIA22, MIA23.'
class InstClaim(EdiConverterModel):
    'Loop: 2300; Segment: CLM.'
    id: str | None = Field(default=None, description='Unique payment identifier assigned by the converter.')
    'Unique payment identifier assigned by the converter.'
    object_type: str | None = Field(default=None, description="Type of this object, set to 'CLAIM'.")
    "Type of this object, set to 'CLAIM'."
    patient_control_number: str | None = Field(default=None,
                                               description='Identifier used to track a claim from creation by the health care provider through payment. EDI: CLM01.')
    'Identifier used to track a claim from creation by the health care provider through payment. EDI: CLM01.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: CLM02.')
    'Charge amount. EDI: CLM02.'
    facility_code: Code | None = Field(default=None,
                                       description='Place of service code (professional/dental) or UB facility code (institutional) from the original claim. EDI: CLM05-1.')
    'Place of service code (professional/dental) or UB facility code (institutional) from the original claim. EDI: CLM05-1.'
    frequency_code: Code | None = Field(default=None, description='Frequency code. EDI: CLM05-3.')
    'Frequency code. EDI: CLM05-3.'
    statement_date_from: dt.date | None = Field(default=None, description='Statement date from. EDI: DTP03*434.')
    'Statement date from. EDI: DTP03*434.'
    statement_date_to: dt.date | None = Field(default=None, description='Statement date to. EDI: DTP03*434.')
    'Statement date to. EDI: DTP03*434.'
    service_date_from: dt.date | None = Field(default=None, description='The earliest service date from service lines.')
    'The earliest service date from service lines.'
    service_date_to: dt.date | None = Field(default=None, description='The latest service date from service lines.')
    'The latest service date from service lines.'
    subscriber: Subscriber | None = Field(default=None, description='The insured (subscriber). EDI: Loop: 2000B.')
    'The insured (subscriber). EDI: Loop: 2000B.'
    patient: Patient | None = Field(default=None,
                                    description='Patient if different from the the insured (subscriber). EDI: Loop: 2110CA.')
    'Patient if different from the the insured (subscriber). EDI: Loop: 2110CA.'
    other_subscribers: list[OtherSubscriber] = Field(default_factory=list,
                                                     description="Other subscribers and their payer's information. EDI: Loop: 2320.")
    "Other subscribers and their payer's information. EDI: Loop: 2320."
    service_lines: list[InstLine] = Field(default_factory=list, description='Service lines. EDI: Loop: 2400.')
    'Service lines. EDI: Loop: 2400.'
    transaction: Transaction837 | None = Field(default=None,
                                               description='Parent EDI transaction for this object. EDI: ST.')
    'Parent EDI transaction for this object. EDI: ST.'
    assignment_participation_code: str | None = Field(default=None,
                                                      description='Assignment participation code. EDI: CLM07.')
    'Assignment participation code. EDI: CLM07.'
    assignment_certification_indicator: str | None = Field(default=None,
                                                           description='Assignment certification indicator. EDI: CLM08.')
    'Assignment certification indicator. EDI: CLM08.'
    release_of_information_code: str | None = Field(default=None,
                                                    description='Release of information code. EDI: CLM09.')
    'Release of information code. EDI: CLM09.'
    delay_reason_code: str | None = Field(default=None, description='Delay reason code. EDI: CLM20.')
    'Delay reason code. EDI: CLM20.'
    service_authorization_exception_code: str | None = Field(default=None,
                                                             description='Service authorization exception code. EDI: REF02*4N.')
    'Service authorization exception code. EDI: REF02*4N.'
    referral_number: str | None = Field(default=None, description='Referral number. EDI: REF02*9F.')
    'Referral number. EDI: REF02*9F.'
    prior_authorization_number: str | None = Field(default=None,
                                                   description='Prior authorization number. EDI: REF02*G1.')
    'Prior authorization number. EDI: REF02*G1.'
    original_reference_number: str | None = Field(default=None, description='Original reference number. EDI: REF02*F8.')
    'Original reference number. EDI: REF02*F8.'
    repriced_reference_number: str | None = Field(default=None, description='Repriced reference number. EDI: REF02*9A.')
    'Repriced reference number. EDI: REF02*9A.'
    adjusted_repriced_reference_number: str | None = Field(default=None,
                                                           description='Adjusted repriced reference number. EDI: REF02*9C.')
    'Adjusted repriced reference number. EDI: REF02*9C.'
    clearinghouse_trace_number: str | None = Field(default=None,
                                                   description='Clearinghouse trace number. EDI: REF02*D9.')
    'Clearinghouse trace number. EDI: REF02*D9.'
    accident_state: str | None = Field(default=None, description='Accident state. EDI: REF02*LU.')
    'Accident state. EDI: REF02*LU.'
    medical_record_number: str | None = Field(default=None, description='Medical record number. EDI: REF02*EA.')
    'Medical record number. EDI: REF02*EA.'
    peer_review_authorization_number: str | None = Field(default=None,
                                                         description='Peer review authorization number. EDI: REF02*G4.')
    'Peer review authorization number. EDI: REF02*G4.'
    demonstration_project_identifier: str | None = Field(default=None,
                                                         description='Demonstration project identifier. EDI: REF02*P4.')
    'Demonstration project identifier. EDI: REF02*P4.'
    admission_date_and_hour: str | None = Field(default=None, description='Admission date and hour. EDI: DTP03*435.')
    'Admission date and hour. EDI: DTP03*435.'
    discharge_time: str | None = Field(default=None, description='Discharge time. EDI: DTP03*096.')
    'Discharge time. EDI: DTP03*096.'
    admission_type_code: str | None = Field(default=None, description='Admission type code. EDI: CL101.')
    'Admission type code. EDI: CL101.'
    admission_source_code: str | None = Field(default=None, description='Admission source code. EDI: CL102.')
    'Admission source code. EDI: CL102.'
    patient_status_code: str | None = Field(default=None, description='Patient status code. EDI: CL103.')
    'Patient status code. EDI: CL103.'
    patient_responsibility_amount: float | None = Field(default=None,
                                                        description='Patient responsibility amount. EDI: AMT02*F3.')
    'Patient responsibility amount. EDI: AMT02*F3.'
    fixed_format_records: list[str] = Field(default_factory=list, description='Fixed format records. EDI: K301.')
    'Fixed format records. EDI: K301.'
    claim_note: str | None = Field(default=None,
                                   description='Free-form comments or instructions. All note segments are concatenated together into this field. EDI: NTE02.')
    'Free-form comments or instructions. All note segments are concatenated together into this field. EDI: NTE02.'
    billing_note: str | None = Field(default=None, description='Billing note. EDI: NTE02*ADD.')
    'Billing note. EDI: NTE02*ADD.'
    billing_provider: Provider | None = Field(default=None, description='Billing provider. EDI: NM1*85.')
    'Billing provider. EDI: NM1*85.'
    pay_to_address: Party | None = Field(default=None, description='Pay to address. EDI: NM1*87.')
    'Pay to address. EDI: NM1*87.'
    pay_to_plan: Party | None = Field(default=None, description='Pay-to plan for subrogation claims. EDI: NM1*PE.')
    'Pay-to plan for subrogation claims. EDI: NM1*PE.'
    providers: list[Provider] = Field(default_factory=list,
                                      description='Providers for this claim, except for the billing provider.')
    'Providers for this claim, except for the billing provider.'
    diags: list[InstDiagnosis] = Field(default_factory=list, description='Diagnosis codes. EDI: HI.')
    'Diagnosis codes. EDI: HI.'
    drg: Code | None = Field(default=None, description='Drg. EDI: HI*DR.')
    'Drg. EDI: HI*DR.'
    procs: list[CodeAndDate] = Field(default_factory=list, description='Claim-level procedures. EDI: HI.')
    'Claim-level procedures. EDI: HI.'
    occurrence_spans: list[CodeAndDate] = Field(default_factory=list, description='Occurrence spans. EDI: HI*BI.')
    'Occurrence spans. EDI: HI*BI.'
    occurrences: list[CodeAndDate] = Field(default_factory=list, description='Occurrences. EDI: HI*BH.')
    'Occurrences. EDI: HI*BH.'
    value_infos: list[CodeAndAmount] = Field(default_factory=list, description='Value infos. EDI: HI*BE.')
    'Value infos. EDI: HI*BE.'
    conditions: list[Code] = Field(default_factory=list, description='Conditions. EDI: HI*BG.')
    'Conditions. EDI: HI*BG.'
    attachments: list[Attachment] = Field(default_factory=list, description='Attachments. EDI: PWK.')
    'Attachments. EDI: PWK.'
    contract_info: ContractInfo | None = Field(default=None, description='Contract info. EDI: CN1.')
    'Contract info. EDI: CN1.'
    conditions_indicators: list[ConditionsIndicator] = Field(default_factory=list,
                                                             description='Conditions indicators. EDI: CRC.')
    'Conditions indicators. EDI: CRC.'
class InstClaimCsv(EdiConverterModel):
    'Loop: 2300; Segment: CLM.'
    id: str | None = Field(default=None, description='Unique payment identifier assigned by the converter.')
    'Unique payment identifier assigned by the converter.'
    transaction_type: str | None = Field(default=None, description='Transaction set identifier code. EDI: ST01.')
    'Transaction set identifier code. EDI: ST01.'
    file_name: str | None = Field(default=None, description='Converted X12 EDI file name.')
    'Converted X12 EDI file name.'
    transaction_control_number: str | None = Field(default=None,
                                                   description='Transaction set control number. EDI: ST02.')
    'Transaction set control number. EDI: ST02.'
    transaction_set_purpose_code: str | None = Field(default=None,
                                                     description='Transaction set purpose code. EDI: BHT02.')
    'Transaction set purpose code. EDI: BHT02.'
    originator_application_transaction_id: str | None = Field(default=None,
                                                              description='Originator application transaction id. EDI: BHT03.')
    'Originator application transaction id. EDI: BHT03.'
    transaction_creation_date_time: str | None = Field(default=None,
                                                       description='Transaction creation date time. EDI: BHT04, BHT05.')
    'Transaction creation date time. EDI: BHT04, BHT05.'
    claim_or_encounter_identifier_type: ClaimOrEncounterIdentifierType | None = Field(default=None,
                                                                                      description='Claim or encounter identifier type. EDI: BHT06.')
    'Claim or encounter identifier type. EDI: BHT06.'
    patient_control_number: str | None = Field(default=None, description='Patient control number. EDI: CLM01.')
    'Patient control number. EDI: CLM01.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: CLM02.')
    'Charge amount. EDI: CLM02.'
    facility: Code | None = Field(default=None,
                                  description='Place of service code for professional/dental claims or UB facility code for institutional claims. EDI: CLM05-1.')
    'Place of service code for professional/dental claims or UB facility code for institutional claims. EDI: CLM05-1.'
    frequency_type_code: str | None = Field(default=None, description='Frequency type code. EDI: CLM05-3.')
    'Frequency type code. EDI: CLM05-3.'
    assignment_participation_code: str | None = Field(default=None,
                                                      description='Assignment participation code. EDI: CLM07.')
    'Assignment participation code. EDI: CLM07.'
    assignment_certification_indicator: str | None = Field(default=None,
                                                           description='Assignment certification indicator. EDI: CLM08.')
    'Assignment certification indicator. EDI: CLM08.'
    release_of_information_code: str | None = Field(default=None,
                                                    description='Release of information code. EDI: CLM09.')
    'Release of information code. EDI: CLM09.'
    delay_reason_code: str | None = Field(default=None, description='Delay reason code. EDI: CLM20.')
    'Delay reason code. EDI: CLM20.'
    billing_provider: Provider | None = Field(default=None, description='Billing provider. EDI: NM1*85.')
    'Billing provider. EDI: NM1*85.'
    subscriber: Subscriber | None = Field(default=None, description='The insured (subscriber). EDI: NM1*44.')
    'The insured (subscriber). EDI: NM1*44.'
    patient: Patient | None = Field(default=None,
                                    description='Patient if different from the the insured (subscriber). EDI: NM1*QC.')
    'Patient if different from the the insured (subscriber). EDI: NM1*QC.'
    statement_date_from: dt.date | None = Field(default=None, description='Statement date from. EDI: DTP03*434.')
    'Statement date from. EDI: DTP03*434.'
    statement_date_to: dt.date | None = Field(default=None, description='Statement date to. EDI: DTP03*434.')
    'Statement date to. EDI: DTP03*434.'
    discharge_time: str | None = Field(default=None, description='Discharge time. EDI: DTP03*096.')
    'Discharge time. EDI: DTP03*096.'
    admission_date_and_hour: str | None = Field(default=None, description='Admission date and hour. EDI: DTP03*435.')
    'Admission date and hour. EDI: DTP03*435.'
    admission_type_code: str | None = Field(default=None, description='Admission type code. EDI: CL101.')
    'Admission type code. EDI: CL101.'
    admission_source_code: str | None = Field(default=None, description='Admission source code. EDI: CL102.')
    'Admission source code. EDI: CL102.'
    patient_status_code: str | None = Field(default=None, description='Patient status code. EDI: CL103.')
    'Patient status code. EDI: CL103.'
    patient_responsibility_amount: float | None = Field(default=None,
                                                        description='Patient responsibility amount. EDI: AMT02*F3.')
    'Patient responsibility amount. EDI: AMT02*F3.'
    service_authorization_exception_code: str | None = Field(default=None,
                                                             description='Service authorization exception code. EDI: REF02*4N.')
    'Service authorization exception code. EDI: REF02*4N.'
    referral_number: str | None = Field(default=None, description='Referral number. EDI: REF02*9F.')
    'Referral number. EDI: REF02*9F.'
    prior_authorization_number: str | None = Field(default=None,
                                                   description='Prior authorization number. EDI: REF02*G1.')
    'Prior authorization number. EDI: REF02*G1.'
    payer_claim_control_number: str | None = Field(default=None,
                                                   description='Payer claim control number. EDI: REF02*F8.')
    'Payer claim control number. EDI: REF02*F8.'
    clearinghouse_trace_number: str | None = Field(default=None,
                                                   description='Clearinghouse trace number. EDI: REF02*D9.')
    'Clearinghouse trace number. EDI: REF02*D9.'
    repriced_reference_number: str | None = Field(default=None, description='Repriced reference number. EDI: REF02*9A.')
    'Repriced reference number. EDI: REF02*9A.'
    adjusted_repriced_reference_number: str | None = Field(default=None,
                                                           description='Adjusted repriced reference number. EDI: REF02*9C.')
    'Adjusted repriced reference number. EDI: REF02*9C.'
    accident_state: str | None = Field(default=None, description='Accident state. EDI: REF02*LU.')
    'Accident state. EDI: REF02*LU.'
    medical_record_number: str | None = Field(default=None, description='Medical record number. EDI: REF02*EA.')
    'Medical record number. EDI: REF02*EA.'
    demonstration_project_identifier: str | None = Field(default=None,
                                                         description='Demonstration project identifier. EDI: REF02*P4.')
    'Demonstration project identifier. EDI: REF02*P4.'
    note: str | None = Field(default=None,
                             description='Free-form comments or instructions. All note segments are concatenated together into this field. EDI: NTE02.')
    'Free-form comments or instructions. All note segments are concatenated together into this field. EDI: NTE02.'
    billing_note: str | None = Field(default=None, description='Billing note. EDI: NTE02*ADD.')
    'Billing note. EDI: NTE02*ADD.'
    principal_diag: InstDiagnosis | None = Field(default=None, description='Principal diagnosis. EDI: HI*ABK.')
    'Principal diagnosis. EDI: HI*ABK.'
    admitting_diag: Code | None = Field(default=None, description='Admitting diagnosis. EDI: HI*ABJ.')
    'Admitting diagnosis. EDI: HI*ABJ.'
    reason_for_visit_diags: list[Code] = Field(default_factory=list, description='Reason for visit diags. EDI: HI*APR.')
    'Reason for visit diags. EDI: HI*APR.'
    external_cause_of_injury_diags: list[Code] = Field(default_factory=list,
                                                       description='External cause of injury diags. EDI: HI*ABN.')
    'External cause of injury diags. EDI: HI*ABN.'
    drg: Code | None = Field(default=None, description='Drg.')
    'Drg.'
    other_diags: list[InstDiagnosis] = Field(default_factory=list, description='Other diags. EDI: HI*ABF.')
    'Other diags. EDI: HI*ABF.'
    principal_procedure: CodeAndDate | None = Field(default=None,
                                                    description='Principal procedure. EDI: HI*BBR, HI*CAH.')
    'Principal procedure. EDI: HI*BBR, HI*CAH.'
    other_procedures: list[CodeAndDate] = Field(default_factory=list, description='Other procedures. EDI: HI*BBQ.')
    'Other procedures. EDI: HI*BBQ.'
    occurrences: list[CodeAndDate] = Field(default_factory=list, description='Occurrences. EDI: HI*BH.')
    'Occurrences. EDI: HI*BH.'
    occurrence_spans: list[CodeAndDate] = Field(default_factory=list, description='Occurrence spans. EDI: HI*BI.')
    'Occurrence spans. EDI: HI*BI.'
    conditions: list[Code] = Field(default_factory=list, description='Conditions. EDI: HI*BG.')
    'Conditions. EDI: HI*BG.'
    value_infos: list[CodeAndAmount] = Field(default_factory=list, description='Value infos. EDI: HI*BE.')
    'Value infos. EDI: HI*BE.'
    attachments: list[Attachment] = Field(default_factory=list, description='Attachments. EDI: PWK.')
    'Attachments. EDI: PWK.'
    attending_provider: Party | None = Field(default=None, description='Attending provider. EDI: NM1*71.')
    'Attending provider. EDI: NM1*71.'
    operating_physician: Provider | None = Field(default=None, description='Operating physician. EDI: NM1*72.')
    'Operating physician. EDI: NM1*72.'
    other_operating_physician: Party | None = Field(default=None, description='Other operating physician. EDI: NM1*ZZ.')
    'Other operating physician. EDI: NM1*ZZ.'
    referring_provider: Party | None = Field(default=None, description='Referring provider. EDI: NM1*DN.')
    'Referring provider. EDI: NM1*DN.'
    rendering_provider: Provider | None = Field(default=None, description='Rendering provider. EDI: NM1*82.')
    'Rendering provider. EDI: NM1*82.'
    service_facility: Party | None = Field(default=None, description='Service facility. EDI: NM1*77.')
    'Service facility. EDI: NM1*77.'
    other_subscribers: list[OtherSubscriber] = Field(default_factory=list,
                                                     description="Other subscribers and their payer's information. EDI: Loop: 2320.")
    "Other subscribers and their payer's information. EDI: Loop: 2320."
    lines: list[InstLineCsv] = Field(default_factory=list, description='Service lines. EDI: Loop: 2400.')
    'Service lines. EDI: Loop: 2400.'
class InstDiagnosis(Code):
    'OpenAPI schema for InstDiagnosis.'
    present_on_admission_indicator: str | None = Field(default=None,
                                                       description='Present on admission indicator. EDI: HI01-9.')
    'Present on admission indicator. EDI: HI01-9.'
class InstLine(EdiConverterModel):
    'Loop: 2400; Segment: SV2.'
    source_line_id: str | None = Field(default=None, description='Line item control number. EDI: REF02*6R.')
    'Line item control number. EDI: REF02*6R.'
    repriced_reference_number: str | None = Field(default=None, description='Repriced reference number. EDI: REF02*9B.')
    'Repriced reference number. EDI: REF02*9B.'
    adjusted_repriced_reference_number: str | None = Field(default=None,
                                                           description='Adjusted repriced reference number. EDI: REF02*9D.')
    'Adjusted repriced reference number. EDI: REF02*9D.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: SV203.')
    'Charge amount. EDI: SV203.'
    non_covered_amount: float | None = Field(default=None, description='Non covered amount. EDI: SV207.')
    'Non covered amount. EDI: SV207.'
    service_tax_amount: float | None = Field(default=None, description='Service tax amount. EDI: AMT02*GT.')
    'Service tax amount. EDI: AMT02*GT.'
    facility_tax_amount: float | None = Field(default=None, description='Facility tax amount. EDI: AMT02*N8.')
    'Facility tax amount. EDI: AMT02*N8.'
    service_date_from: dt.date | None = Field(default=None, description='Service date from. EDI: DTP03*472.')
    'Service date from. EDI: DTP03*472.'
    service_date_to: dt.date | None = Field(default=None, description='Service date to. EDI: DTP03*472.')
    'Service date to. EDI: DTP03*472.'
    unit_type: UnitType | None = Field(default=None, description='Unit type. EDI: SV204.')
    'Unit type. EDI: SV204.'
    unit_count: float | None = Field(default=None, description='Unit count. EDI: SV205.')
    'Unit count. EDI: SV205.'
    third_party_note: str | None = Field(default=None, description='Third party note. EDI: NTE02*TPO.')
    'Third party note. EDI: NTE02*TPO.'
    procedure: Procedure | None = Field(default=None,
                                        description='Procedure. EDI: SV202*HC, SV202*AD, SV202*WK, SV202*IV.')
    'Procedure. EDI: SV202*HC, SV202*AD, SV202*WK, SV202*IV.'
    revenue_code: Code | None = Field(default=None, description='Revenue code. EDI: SV201*RC,NU.')
    'Revenue code. EDI: SV201*RC,NU.'
    attachments: list[Attachment] = Field(default_factory=list, description='Attachments. EDI: PWK.')
    'Attachments. EDI: PWK.'
    contract_info: ContractInfo | None = Field(default=None, description='Contract info. EDI: CN1.')
    'Contract info. EDI: CN1.'
    providers: list[Provider] = Field(default_factory=list, description='Providers for this service line.')
    'Providers for this service line.'
    adjudications: list[Adjudication] = Field(default_factory=list, description='Adjudications. EDI: Loop: 2430, SVD.')
    'Adjudications. EDI: Loop: 2430, SVD.'
    adjustments: list[Adjustment] = Field(default_factory=list,
                                          description='Copy of line adjustments from the adjudication list for backward compatibility. EDI: CAS.')
    'Copy of line adjustments from the adjudication list for backward compatibility. EDI: CAS.'
    fixed_format_records: list[str] = Field(default_factory=list, description='Fixed format records. EDI: K301.')
    'Fixed format records. EDI: K301.'
class InstLineCsv(EdiConverterModel):
    'Loop: 2400.'
    control_number: str | None = Field(default=None, description='Control number. EDI: REF02*6R.')
    'Control number. EDI: REF02*6R.'
    revenue_code: Code | None = Field(default=None, description='Revenue code. EDI: SV201.')
    'Revenue code. EDI: SV201.'
    procedure: Procedure | None = Field(default=None,
                                        description='Procedure. EDI: SV202*HC, SV202*AD, SV202*WK, SV202*IV.')
    'Procedure. EDI: SV202*HC, SV202*AD, SV202*WK, SV202*IV.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: SV203.')
    'Charge amount. EDI: SV203.'
    unit_type: UnitType | None = Field(default=None, description='Unit type. EDI: SV204.')
    'Unit type. EDI: SV204.'
    unit_count: float | None = Field(default=None, description='Unit count. EDI: SV205.')
    'Unit count. EDI: SV205.'
    non_covered_amount: float | None = Field(default=None, description='Non covered amount. EDI: SV207.')
    'Non covered amount. EDI: SV207.'
    service_date_from: dt.date | None = Field(default=None,
                                              description='Service period start date. EDI: DTP03*472, DTP03*150.')
    'Service period start date. EDI: DTP03*472, DTP03*150.'
    service_date_to: dt.date | None = Field(default=None,
                                            description="Service period end date. If not provided in EDI (single day), it is set to 'serviceDateFrom'. EDI: DTP03*151.")
    "Service period end date. If not provided in EDI (single day), it is set to 'serviceDateFrom'. EDI: DTP03*151."
    repriced_reference_number: str | None = Field(default=None, description='Repriced reference number. EDI: REF02*9B.')
    'Repriced reference number. EDI: REF02*9B.'
    adjusted_repriced_reference_number: str | None = Field(default=None,
                                                           description='Adjusted repriced reference number. EDI: REF02*9D.')
    'Adjusted repriced reference number. EDI: REF02*9D.'
    service_tax_amount: float | None = Field(default=None, description='Service tax amount. EDI: AMT02*GT.')
    'Service tax amount. EDI: AMT02*GT.'
    facility_tax_amount: float | None = Field(default=None, description='Facility tax amount. EDI: AMT02*N8.')
    'Facility tax amount. EDI: AMT02*N8.'
    third_party_note: str | None = Field(default=None, description='Third party note. EDI: NTE02.')
    'Third party note. EDI: NTE02.'
    drug: Code | None = Field(default=None, description='Drug. EDI: LIN03.')
    'Drug. EDI: LIN03.'
    drug_quantity: float | None = Field(default=None, description='Drug quantity. EDI: CTP04.')
    'Drug quantity. EDI: CTP04.'
    drug_unit_type: UnitType | None = Field(default=None, description='Drug unit type. EDI: CTP05-1.')
    'Drug unit type. EDI: CTP05-1.'
    prescription_number: str | None = Field(default=None, description='Prescription number. EDI: REF02*XZ.')
    'Prescription number. EDI: REF02*XZ.'
    attachments: list[Attachment] = Field(default_factory=list, description='Attachments. EDI: PWK.')
    'Attachments. EDI: PWK.'
    operating_physician: Provider | None = Field(default=None, description='Operating physician. EDI: NM1*72.')
    'Operating physician. EDI: NM1*72.'
    other_operating_physician: Party | None = Field(default=None, description='Other operating physician. EDI: NM1*ZZ.')
    'Other operating physician. EDI: NM1*ZZ.'
    rendering_provider: Provider | None = Field(default=None, description='Rendering provider. EDI: NM1*82.')
    'Rendering provider. EDI: NM1*82.'
    referring_provider: Party | None = Field(default=None, description='Referring provider. EDI: NM1*DN.')
    'Referring provider. EDI: NM1*DN.'
class InterchangeControl(EdiConverterModel):
    'Segment: ISA.'
    element_separator: str | None = Field(default=None, description='Element separator character.')
    'Element separator character.'
    segment_terminator: str | None = Field(default=None, description='Segment terminator character.')
    'Segment terminator character.'
    authorization_information_qualifier: str | None = Field(default=None,
                                                            description='Authorization information qualifier. EDI: ISA01.')
    'Authorization information qualifier. EDI: ISA01.'
    authorization_information: str | None = Field(default=None, description='Authorization information. EDI: ISA02.')
    'Authorization information. EDI: ISA02.'
    security_information_qualifier: str | None = Field(default=None,
                                                       description='Security information qualifier. EDI: ISA03.')
    'Security information qualifier. EDI: ISA03.'
    security_information: str | None = Field(default=None, description='Security information. EDI: ISA04.')
    'Security information. EDI: ISA04.'
    sender_id_qualifier: str | None = Field(default=None, description='Sender id qualifier. EDI: ISA05.')
    'Sender id qualifier. EDI: ISA05.'
    sender_id: str | None = Field(default=None, description='Sender id. EDI: ISA06.')
    'Sender id. EDI: ISA06.'
    receiver_id_qualifier: str | None = Field(default=None, description='Receiver id qualifier. EDI: ISA07.')
    'Receiver id qualifier. EDI: ISA07.'
    receiver_id: str | None = Field(default=None, description='Receiver id. EDI: ISA08.')
    'Receiver id. EDI: ISA08.'
    interchange_date: dt.date | None = Field(default=None, description='Interchange date. EDI: ISA09.')
    'Interchange date. EDI: ISA09.'
    interchange_time: str | None = Field(default=None, description='Interchange time. EDI: ISA10.')
    'Interchange time. EDI: ISA10.'
    repetition_separator: str | None = Field(default=None, description='Repetition separator. EDI: ISA11.')
    'Repetition separator. EDI: ISA11.'
    interchange_control_version_number: str | None = Field(default=None,
                                                           description='Interchange control version number. EDI: ISA12.')
    'Interchange control version number. EDI: ISA12.'
    control_number: int | None = Field(default=None, description='Control number. EDI: ISA13.')
    'Control number. EDI: ISA13.'
    acknowledgment_requested: str | None = Field(default=None, description='Acknowledgment requested. EDI: ISA14.')
    'Acknowledgment requested. EDI: ISA14.'
    interchange_usage_indicator: str | None = Field(default=None,
                                                    description='Interchange usage indicator. EDI: ISA15.')
    'Interchange usage indicator. EDI: ISA15.'
    component_element_separator: str | None = Field(default=None,
                                                    description='Component element separator. EDI: ISA16.')
    'Component element separator. EDI: ISA16.'
class LanguageInfo(EdiConverterModel):
    'Segment: LUI.'
    code_qualifier: str | None = Field(default=None, description='Code qualifier. EDI: LUI01.')
    'Code qualifier. EDI: LUI01.'
    code: str | None = Field(default=None, description='Code. EDI: LUI02.')
    'Code. EDI: LUI02.'
    language_description: str | None = Field(default=None, description='Language description. EDI: LUI03.')
    'Language description. EDI: LUI03.'
    language_use_indicator: str | None = Field(default=None, description='Language use indicator. EDI: LUI04.')
    'Language use indicator. EDI: LUI04.'
class Measurement(EdiConverterModel):
    "Measurement, such as a test result for dialysis service lines or a patient's height for DMERC. Segment: MEA."
    category_code: str | None = Field(default=None,
                                      description='Code identifying the broad category to which a measurement applies. EDI: MEA01.')
    'Code identifying the broad category to which a measurement applies. EDI: MEA01.'
    qualifier_code: str | None = Field(default=None,
                                       description='Code identifying a specific product or process characteristic to which a measurement applies. EDI: MEA02.')
    'Code identifying a specific product or process characteristic to which a measurement applies. EDI: MEA02.'
    type: MeasurementType | None = Field(default=None,
                                         description='Code identifying a specific product or process characteristic to which a measurement applies, expressed as enum (string constant). EDI: MEA02.')
    'Code identifying a specific product or process characteristic to which a measurement applies, expressed as enum (string constant). EDI: MEA02.'
    value: float | None = Field(default=None, description='The value of the measurement. EDI: MEA03.')
    'The value of the measurement. EDI: MEA03.'
class MemberCoverage(EdiConverterModel):
    'Main object for 834, contains the member and their health coverage information. Loop: 2000; Segment: INS.'
    id: str | None = Field(default=None, description='Unique identifier assigned by the converter.')
    'Unique identifier assigned by the converter.'
    object_type: str | None = Field(default=None, description="Type of this object, always set to 'MEMBER_COVERAGE'.")
    "Type of this object, always set to 'MEMBER_COVERAGE'."
    file_name: str | None = Field(default=None, description='Converted X12 EDI file name.')
    'Converted X12 EDI file name.'
    file_effective_dates: list[Date] = Field(default_factory=list, description='File effective dates. EDI: DTP.')
    'File effective dates. EDI: DTP.'
    master_policy_number: str | None = Field(default=None, description='Master policy number. EDI: REF02*34.')
    'Master policy number. EDI: REF02*34.'
    sponsor: PartyIdName | None = Field(default=None, description='Sponsor. EDI: Loop: 1000A.')
    'Sponsor. EDI: Loop: 1000A.'
    insurer: PartyIdName | None = Field(default=None, description='Insurer. EDI: Loop: 1000B.')
    'Insurer. EDI: Loop: 1000B.'
    tpas: list[Tpa] = Field(default_factory=list, description='Tpas. EDI: Loop: 1000C.')
    'Tpas. EDI: Loop: 1000C.'
    member_indicator: str | None = Field(default=None, description='Member indicator. EDI: INS01.')
    'Member indicator. EDI: INS01.'
    relationship_code: str | None = Field(default=None, description='Relationship code. EDI: INS02.')
    'Relationship code. EDI: INS02.'
    maintenance_type_code: str | None = Field(default=None, description='Maintenance type code. EDI: INS03.')
    'Maintenance type code. EDI: INS03.'
    maintenance_reason_code: str | None = Field(default=None, description='Maintenance reason code. EDI: INS04.')
    'Maintenance reason code. EDI: INS04.'
    benefit_status_code: str | None = Field(default=None, description='Benefit status code. EDI: INS05.')
    'Benefit status code. EDI: INS05.'
    medicare_plan_code: str | None = Field(default=None,
                                           description='Medicare plan code. Since: v2.14.8. EDI: INS06-1.')
    'Medicare plan code. Since: v2.14.8. EDI: INS06-1.'
    medicare_eligibility_reason_code: str | None = Field(default=None,
                                                         description='Medicare eligibility reason code. Since: v2.14.8. EDI: INS06-2.')
    'Medicare eligibility reason code. Since: v2.14.8. EDI: INS06-2.'
    cobra_event_code: str | None = Field(default=None, description='Cobra event code. EDI: INS07.')
    'Cobra event code. EDI: INS07.'
    employment_status_code: str | None = Field(default=None, description='Employment status code. EDI: INS08.')
    'Employment status code. EDI: INS08.'
    student_status_code: str | None = Field(default=None, description='Student status code. EDI: INS09.')
    'Student status code. EDI: INS09.'
    handicap_indicator: str | None = Field(default=None, description='Handicap indicator. EDI: INS10.')
    'Handicap indicator. EDI: INS10.'
    death_date: dt.date | None = Field(default=None, description='Death date. Since: v2.14.8. EDI: INS12.')
    'Death date. Since: v2.14.8. EDI: INS12.'
    confidentiality_code: str | None = Field(default=None, description='Confidentiality code. EDI: INS13.')
    'Confidentiality code. EDI: INS13.'
    birth_sequence_number: int | None = Field(default=None, description='Birth sequence number. EDI: INS17.')
    'Birth sequence number. EDI: INS17.'
    identifier: str | None = Field(default=None, description='Member identifier. EDI: REF02*0F.')
    'Member identifier. EDI: REF02*0F.'
    group_or_policy_number: str | None = Field(default=None, description='Group or policy number. EDI: REF02*1L.')
    'Group or policy number. EDI: REF02*1L.'
    supplemental_identifiers: list[Reference] = Field(default_factory=list,
                                                      description='Supplemental identifiers. EDI: REF.')
    'Supplemental identifiers. EDI: REF.'
    status_info_effective_dates: list[Date] = Field(default_factory=list,
                                                    description='Status info effective dates. EDI: DTP.')
    'Status info effective dates. EDI: DTP.'
    member: Member | None = Field(default=None, description='Member. EDI: Loop: 2100A, NM1*IL.')
    'Member. EDI: Loop: 2100A, NM1*IL.'
    incorrect_member: Member | None = Field(default=None, description='Incorrect member. EDI: Loop: 2100B, NM1*70.')
    'Incorrect member. EDI: Loop: 2100B, NM1*70.'
    contract_amounts: list[Amount] = Field(default_factory=list,
                                           description='Member policy amounts from the member loop 2100A. EDI: AMT.')
    'Member policy amounts from the member loop 2100A. EDI: AMT.'
    mailing_address: Address | None = Field(default=None, description='Member mailing address.')
    'Member mailing address.'
    employers: list[Party] = Field(default_factory=list, description='Employers. EDI: Loop: 2100D.')
    'Employers. EDI: Loop: 2100D.'
    schools: list[Party] = Field(default_factory=list, description='Schools. EDI: Loop: 2100E.')
    'Schools. EDI: Loop: 2100E.'
    custodial_parent: Party | None = Field(default=None, description='Custodial parent. EDI: Loop: 2100F.')
    'Custodial parent. EDI: Loop: 2100F.'
    responsible_persons: list[Party] = Field(default_factory=list, description='Responsible persons. EDI: Loop: 2100G.')
    'Responsible persons. EDI: Loop: 2100G.'
    drop_off_location: Party | None = Field(default=None, description='Drop off location. EDI: Loop: 2100H.')
    'Drop off location. EDI: Loop: 2100H.'
    disabilities: list[Disability] = Field(default_factory=list, description='Disabilities. EDI: Loop: 2200.')
    'Disabilities. EDI: Loop: 2200.'
    reporting_categories: list[ReportingCategory] = Field(default_factory=list,
                                                          description='Reporting categories. EDI: Loop: 2750.')
    'Reporting categories. EDI: Loop: 2750.'
    health_coverages: list[HealthCoverage] = Field(default_factory=list,
                                                   description='Health coverages. EDI: Loop: 2300.')
    'Health coverages. EDI: Loop: 2300.'
    transaction: Transaction834 | None = Field(default=None,
                                               description='Parent EDI transaction for this object. EDI: ST.')
    'Parent EDI transaction for this object. EDI: ST.'
class MemberCoverageCsv(EdiConverterModel):
    'Main object for 834, contains the member and their health coverage information. Loop: 2000; Segment: INS.'
    id: str | None = Field(default=None, description='Unique identifier assigned by the converter.')
    'Unique identifier assigned by the converter.'
    file_name: str | None = Field(default=None, description='Converted X12 EDI file name.')
    'Converted X12 EDI file name.'
    transaction_control_number: str | None = Field(default=None, description='Transaction control number. EDI: ST02.')
    'Transaction control number. EDI: ST02.'
    transaction_set_purpose_code: str | None = Field(default=None,
                                                     description='Transaction set purpose code. EDI: BGN01.')
    'Transaction set purpose code. EDI: BGN01.'
    originator_application_transaction_id: str | None = Field(default=None,
                                                              description='Originator application transaction id. EDI: BGN02.')
    'Originator application transaction id. EDI: BGN02.'
    transaction_creation_date_time: str | None = Field(default=None,
                                                       description='Transaction creation date time. EDI: BGN03, BGN04.')
    'Transaction creation date time. EDI: BGN03, BGN04.'
    transaction_action_code: str | None = Field(default=None, description='Transaction action code. EDI: BGN08.')
    'Transaction action code. EDI: BGN08.'
    file_effective_dates: list[Date] = Field(default_factory=list, description='File effective dates. EDI: DTP.')
    'File effective dates. EDI: DTP.'
    master_policy_number: str | None = Field(default=None, description='Master policy number. EDI: REF02*34.')
    'Master policy number. EDI: REF02*34.'
    sponsor: PartyIdName | None = Field(default=None, description='Sponsor. EDI: Loop: 1000A.')
    'Sponsor. EDI: Loop: 1000A.'
    insurer: PartyIdName | None = Field(default=None, description='Insurer. EDI: Loop: 1000B.')
    'Insurer. EDI: Loop: 1000B.'
    tpas: list[Tpa] = Field(default_factory=list, description='Tpas. EDI: Loop: 1000C.')
    'Tpas. EDI: Loop: 1000C.'
    member_indicator: str | None = Field(default=None, description='Member indicator. EDI: INS01.')
    'Member indicator. EDI: INS01.'
    relationship_code: str | None = Field(default=None, description='Relationship code. EDI: INS02.')
    'Relationship code. EDI: INS02.'
    maintenance_type_code: str | None = Field(default=None, description='Maintenance type code. EDI: INS03.')
    'Maintenance type code. EDI: INS03.'
    maintenance_reason_code: str | None = Field(default=None, description='Maintenance reason code. EDI: INS04.')
    'Maintenance reason code. EDI: INS04.'
    benefit_status_code: str | None = Field(default=None, description='Benefit status code. EDI: INS05.')
    'Benefit status code. EDI: INS05.'
    medicare_plan_code: str | None = Field(default=None,
                                           description='Medicare plan code. Since: v2.14.8. EDI: INS06-1.')
    'Medicare plan code. Since: v2.14.8. EDI: INS06-1.'
    medicare_eligibility_reason_code: str | None = Field(default=None,
                                                         description='Medicare eligibility reason code. Since: v2.14.8. EDI: INS06-2.')
    'Medicare eligibility reason code. Since: v2.14.8. EDI: INS06-2.'
    cobra_event_code: str | None = Field(default=None, description='Cobra event code. EDI: INS07.')
    'Cobra event code. EDI: INS07.'
    employment_status_code: str | None = Field(default=None, description='Employment status code. EDI: INS08.')
    'Employment status code. EDI: INS08.'
    student_status_code: str | None = Field(default=None, description='Student status code. EDI: INS09.')
    'Student status code. EDI: INS09.'
    handicap_indicator: str | None = Field(default=None, description='Handicap indicator. EDI: INS10.')
    'Handicap indicator. EDI: INS10.'
    death_date: dt.date | None = Field(default=None, description='Death date. Since: v2.14.8. EDI: INS12.')
    'Death date. Since: v2.14.8. EDI: INS12.'
    confidentiality_code: str | None = Field(default=None, description='Confidentiality code. EDI: INS13.')
    'Confidentiality code. EDI: INS13.'
    birth_sequence_number: int | None = Field(default=None, description='Birth sequence number. EDI: INS17.')
    'Birth sequence number. EDI: INS17.'
    identifier: str | None = Field(default=None, description='Member identifier. EDI: REF02*0F.')
    'Member identifier. EDI: REF02*0F.'
    group_or_policy_number: str | None = Field(default=None, description='Group or policy number. EDI: REF02*1L.')
    'Group or policy number. EDI: REF02*1L.'
    supplemental_identifiers: list[Reference] = Field(default_factory=list,
                                                      description='Supplemental identifiers. EDI: REF.')
    'Supplemental identifiers. EDI: REF.'
    status_info_effective_dates: list[Date] = Field(default_factory=list,
                                                    description='Status info effective dates. EDI: DTP.')
    'Status info effective dates. EDI: DTP.'
    member: Member | None = Field(default=None, description='Member. EDI: Loop: 2100A, NM1*IL.')
    'Member. EDI: Loop: 2100A, NM1*IL.'
    incorrect_member: Member | None = Field(default=None, description='Incorrect member. EDI: Loop: 2100B, NM1*70.')
    'Incorrect member. EDI: Loop: 2100B, NM1*70.'
    contract_amounts: list[Amount] = Field(default_factory=list,
                                           description='Member policy amounts from the member loop 2100A. EDI: AMT.')
    'Member policy amounts from the member loop 2100A. EDI: AMT.'
    mailing_address: Address | None = Field(default=None, description='Member mailing address.')
    'Member mailing address.'
    employers: list[Party] = Field(default_factory=list, description='Employers. EDI: Loop: 2100D.')
    'Employers. EDI: Loop: 2100D.'
    schools: list[Party] = Field(default_factory=list, description='Schools. EDI: Loop: 2100E.')
    'Schools. EDI: Loop: 2100E.'
    custodial_parent: Party | None = Field(default=None, description='Custodial parent. EDI: Loop: 2100F.')
    'Custodial parent. EDI: Loop: 2100F.'
    responsible_persons: list[Party] = Field(default_factory=list, description='Responsible persons. EDI: Loop: 2100G.')
    'Responsible persons. EDI: Loop: 2100G.'
    drop_off_location: Party | None = Field(default=None, description='Drop off location. EDI: Loop: 2100H.')
    'Drop off location. EDI: Loop: 2100H.'
    disabilities: list[Disability] = Field(default_factory=list, description='Disabilities. EDI: Loop: 2200.')
    'Disabilities. EDI: Loop: 2200.'
    reporting_categories: list[ReportingCategory] = Field(default_factory=list,
                                                          description='Reporting categories. EDI: Loop: 2750.')
    'Reporting categories. EDI: Loop: 2750.'
    health_coverages: list[HealthCoverage] = Field(default_factory=list,
                                                   description='Health coverages. EDI: Loop: 2300.')
    'Health coverages. EDI: Loop: 2300.'
    transaction: Transaction834 | None = Field(default=None,
                                               description='Parent EDI transaction for this object. EDI: ST.')
    'Parent EDI transaction for this object. EDI: ST.'
class OrthodonticInfo(EdiConverterModel):
    'Segment: DN1.'
    treatment_months_count: float | None = Field(default=None, description='Treatment months count. EDI: DN101.')
    'Treatment months count. EDI: DN101.'
    treatment_months_remaining_count: float | None = Field(default=None,
                                                           description='Treatment months remaining count. EDI: DN102.')
    'Treatment months remaining count. EDI: DN102.'
    treatment_indicator: str | None = Field(default=None, description='Treatment indicator. EDI: DN104.')
    'Treatment indicator. EDI: DN104.'
class OtherSubscriber(EdiConverterModel):
    'OpenAPI schema for OtherSubscriber.'
    payer_responsibility_sequence: PayerRespSequenceType | None = Field(default=None,
                                                                        description='Payer responsibility sequence. EDI: SBR01.')
    'Payer responsibility sequence. EDI: SBR01.'
    relationship_type: RelationshipType | None = Field(default=None,
                                                       description='Relationship type. EDI: SBR02, PAT01.')
    'Relationship type. EDI: SBR02, PAT01.'
    group_or_policy_number: str | None = Field(default=None, description='Group or policy number. EDI: SBR03.')
    'Group or policy number. EDI: SBR03.'
    group_name: str | None = Field(default=None, description='Group name. EDI: SBR04.')
    'Group name. EDI: SBR04.'
    coordination_of_benefits_code: str | None = Field(default=None,
                                                      description='Coordination of benefits code, post-adjudicated claims only. EDI: SBR06.')
    'Coordination of benefits code, post-adjudicated claims only. EDI: SBR06.'
    claim_filing_indicator_code: str | None = Field(default=None,
                                                    description='Claim filing indicator code. EDI: SBR09.')
    'Claim filing indicator code. EDI: SBR09.'
    insurance_plan_type: InsurancePlanType | None = Field(default=None, description='Insurance plan type. EDI: SBR09.')
    'Insurance plan type. EDI: SBR09.'
    person: PersonWithDemographic | None = Field(default=None, description='Person. EDI: NM1.')
    'Person. EDI: NM1.'
    adjustments: list[Adjustment] = Field(default_factory=list,
                                          description='Claim-level adjustments from this payer. EDI: CAS.')
    'Claim-level adjustments from this payer. EDI: CAS.'
    payer_paid_amount: float | None = Field(default=None, description='Payer paid amount. EDI: AMT02*D.')
    'Payer paid amount. EDI: AMT02*D.'
    non_covered_amount: float | None = Field(default=None, description='Non covered amount. EDI: AMT02*A8.')
    'Non covered amount. EDI: AMT02*A8.'
    remaining_patient_liability_amount: float | None = Field(default=None,
                                                             description='Remaining patient liability amount. EDI: AMT02*EAF.')
    'Remaining patient liability amount. EDI: AMT02*EAF.'
    outpatient_adjudication: OutpatientAdjudication | None = Field(default=None,
                                                                   description='Outpatient adjudication. EDI: MOA.')
    'Outpatient adjudication. EDI: MOA.'
    payer_prior_authorization_number: str | None = Field(default=None,
                                                         description='Payer prior authorization number. EDI: REF02*G1.')
    'Payer prior authorization number. EDI: REF02*G1.'
    payer_referral_number: str | None = Field(default=None, description='Payer referral number. EDI: REF02*9F.')
    'Payer referral number. EDI: REF02*9F.'
    payer_claim_control_number: str | None = Field(default=None,
                                                   description='Payer claim control number. EDI: REF02*F8.')
    'Payer claim control number. EDI: REF02*F8.'
    payer: Party | None = Field(default=None, description='Payer. EDI: Loop: 2330B, NM1*PR.')
    'Payer. EDI: Loop: 2330B, NM1*PR.'
    patient: Party | None = Field(default=None,
                                  description="Patient's information; post-adjudicated claims only. EDI: Loop: 2330C, NM1*QC.")
    "Patient's information; post-adjudicated claims only. EDI: Loop: 2330C, NM1*QC."
    providers: list[Party] = Field(default_factory=list, description="Other payer's providers. EDI: NM1.")
    "Other payer's providers. EDI: NM1."
class OutpatientAdjudication(EdiConverterModel):
    'Contains Remittance Advice Remark Codes at the claim level and/or Medicare or Medicaid-specific amounts for outpatient claims. Segment: MOA.'
    reimbursement_rate: float | None = Field(default=None, description='Reimbursement rate. EDI: MOA01.')
    'Reimbursement rate. EDI: MOA01.'
    hcpcs_payable_amount: float | None = Field(default=None, description='Claim HCPCS Payable Amount. EDI: MOA02.')
    'Claim HCPCS Payable Amount. EDI: MOA02.'
    esrd_payment_amount: float | None = Field(default=None, description='Esrd payment amount. EDI: MOA08.')
    'Esrd payment amount. EDI: MOA08.'
    non_payable_professional_component_amount: float | None = Field(default=None,
                                                                    description='Nonpayable Professional Component Amount. EDI: MOA09.')
    'Nonpayable Professional Component Amount. EDI: MOA09.'
    remarks: list[Code] = Field(default_factory=list, description='Remark codes.')
    'Remark codes.'
class PartyIdName(EdiConverterModel):
    'OpenAPI schema for PartyIdName.'
    entity_role: EntityRole | None = Field(default=None, description='Entity role. EDI: NM101, N101.')
    'Entity role. EDI: NM101, N101.'
    entity_type: EntityType | None = Field(default=None, description='Entity type. EDI: NM102.')
    'Entity type. EDI: NM102.'
    identification_type: IdentificationType | None = Field(default=None,
                                                           description='Identification type, e.g., NPI or EIN. This is a qualifier code translated to a string constant (enum). EDI: NM108, N103.')
    'Identification type, e.g., NPI or EIN. This is a qualifier code translated to a string constant (enum). EDI: NM108, N103.'
    identifier: str | None = Field(default=None, description='Identifier. EDI: NM109, N104.')
    'Identifier. EDI: NM109, N104.'
    tax_id: str | None = Field(default=None, description='Tax id. EDI: REF02*TJ, REF02*SY, REF02*EI.')
    'Tax id. EDI: REF02*TJ, REF02*SY, REF02*EI.'
    last_name_or_org_name: str | None = Field(default=None,
                                              description='Organization name or person last name. EDI: NM103, N102.')
    'Organization name or person last name. EDI: NM103, N102.'
    first_name: str | None = Field(default=None, description='First name. EDI: NM104.')
    'First name. EDI: NM104.'
    middle_name: str | None = Field(default=None, description='Middle name. EDI: NM105.')
    'Middle name. EDI: NM105.'
class Patient(EdiConverterModel):
    'OpenAPI schema for Patient.'
    relationship_type: RelationshipType | None = Field(default=None,
                                                       description='Relationship type. EDI: SBR02, PAT01.')
    'Relationship type. EDI: SBR02, PAT01.'
    person: PersonWithDemographic | None = Field(default=None, description='Person. EDI: NM1.')
    'Person. EDI: NM1.'
    death_date: dt.date | None = Field(default=None, description='Death date. EDI: PAT06.')
    'Death date. EDI: PAT06.'
    weight: float | None = Field(default=None, description='Patient weight in pounds. EDI: PAT08.')
    'Patient weight in pounds. EDI: PAT08.'
    pregnancy_indicator: str | None = Field(default=None, description='Pregnancy indicator. EDI: PAT09.')
    'Pregnancy indicator. EDI: PAT09.'
class PatientSubscriber835(EdiConverterModel):
    'Insured subscriber of patient for 835.'
    person: Party | None = Field(default=None, description='Person. EDI: NM1.')
    'Person. EDI: NM1.'
class Payment(EdiConverterModel):
    'Loop: 2100; Segment: CLP.'
    id: str | None = Field(default=None, description='Unique payment identifier assigned by the converter.')
    'Unique payment identifier assigned by the converter.'
    object_type: str | None = Field(default=None, description="Type of this object, set to 'PAYMENT'.")
    "Type of this object, set to 'PAYMENT'."
    patient_control_number: str | None = Field(default=None,
                                               description='Identifier used to track a claim from creation by the health care provider through payment. EDI: CLP01.')
    'Identifier used to track a claim from creation by the health care provider through payment. EDI: CLP01.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: CLP02.')
    'Charge amount. EDI: CLP02.'
    payment_amount: float | None = Field(default=None, description='Payment amount. EDI: CLP04.')
    'Payment amount. EDI: CLP04.'
    facility_code: Code | None = Field(default=None,
                                       description='Place of service code (professional/dental) or UB facility code (institutional) from the original claim. EDI: CLP08.')
    'Place of service code (professional/dental) or UB facility code (institutional) from the original claim. EDI: CLP08.'
    frequency_code: Code | None = Field(default=None, description='Frequency code. EDI: CLP09.')
    'Frequency code. EDI: CLP09.'
    statement_date_from: dt.date | None = Field(default=None, description='Statement date from. EDI: DTP03*232.')
    'Statement date from. EDI: DTP03*232.'
    statement_date_to: dt.date | None = Field(default=None, description='Statement date to. EDI: DTP03*233.')
    'Statement date to. EDI: DTP03*233.'
    service_date_from: dt.date | None = Field(default=None, description='The earliest service date from service lines.')
    'The earliest service date from service lines.'
    service_date_to: dt.date | None = Field(default=None, description='The latest service date from service lines.')
    'The latest service date from service lines.'
    subscriber: PatientSubscriber835 | None = Field(default=None,
                                                    description='The insured (subscriber) from the original claim if the insured is different from the patient. EDI: Loop: 2100.')
    'The insured (subscriber) from the original claim if the insured is different from the patient. EDI: Loop: 2100.'
    patient: PatientSubscriber835 | None = Field(default=None,
                                                 description='The insured (subscriber) or patient from the original claim. EDI: Loop: 2100.')
    'The insured (subscriber) or patient from the original claim. EDI: Loop: 2100.'
    other_subscribers: list[PatientSubscriber835] = Field(default_factory=list,
                                                          description='Other subscriber; only one other subscriber is allowed on 835. EDI: Loop: 2100.')
    'Other subscriber; only one other subscriber is allowed on 835. EDI: Loop: 2100.'
    service_lines: list[PaymentLine] = Field(default_factory=list, description='Service lines. EDI: Loop: 2110.')
    'Service lines. EDI: Loop: 2110.'
    transaction: Transaction835 | None = Field(default=None,
                                               description='Parent EDI transaction for this object. EDI: ST.')
    'Parent EDI transaction for this object. EDI: ST.'
    claim_status_code: str | None = Field(default=None, description='Claim status code. EDI: CLP02.')
    'Claim status code. EDI: CLP02.'
    claim_status: AdjudicatedClaimStatus | None = Field(default=None,
                                                        description='Claim status code translated to a string constant (enum). EDI: CLP02.')
    'Claim status code translated to a string constant (enum). EDI: CLP02.'
    patient_responsibility_amount: float | None = Field(default=None,
                                                        description='Patient responsibility amount. EDI: CLP05.')
    'Patient responsibility amount. EDI: CLP05.'
    claim_filing_indicator_code: str | None = Field(default=None,
                                                    description='Claim filing indicator code. EDI: CLP06.')
    'Claim filing indicator code. EDI: CLP06.'
    insurance_plan_type: InsurancePlanType | None = Field(default=None,
                                                          description='Claim filing indicator code translated to a string constant (enum). EDI: CLP06.')
    'Claim filing indicator code translated to a string constant (enum). EDI: CLP06.'
    payer_control_number: str | None = Field(default=None, description='Payer control number. EDI: CLP07.')
    'Payer control number. EDI: CLP07.'
    drg: Code | None = Field(default=None,
                             description='Diagnosis-related group code. Institutional claims only. EDI: CLP11.')
    'Diagnosis-related group code. Institutional claims only. EDI: CLP11.'
    drg_weight: float | None = Field(default=None,
                                     description='Adjudicated DRG weight. Institutional claims only. EDI: CLP12.')
    'Adjudicated DRG weight. Institutional claims only. EDI: CLP12.'
    discharge_fraction: float | None = Field(default=None,
                                             description='Adjudicated discharge fraction. Institutional claims only. This is a percentage expressed as decimal. EDI: CLP13.')
    'Adjudicated discharge fraction. Institutional claims only. This is a percentage expressed as decimal. EDI: CLP13.'
    other_claim_related_ids: list[Reference] = Field(default_factory=list,
                                                     description='Other claim-related identifications. EDI: REF.')
    'Other claim-related identifications. EDI: REF.'
    supplemental_amounts: list[Amount] = Field(default_factory=list,
                                               description='Supplemental claim/payment amounts, such as coverage amount, discount amount, etc. EDI: AMT.')
    'Supplemental claim/payment amounts, such as coverage amount, discount amount, etc. EDI: AMT.'
    supplemental_quantities: list[Quantity] = Field(default_factory=list,
                                                    description='Supplemental claim/payment quantities. EDI: QTY.')
    'Supplemental claim/payment quantities. EDI: QTY.'
    payer: Party | None = Field(default=None, description='Payer. EDI: N1*PR.')
    'Payer. EDI: N1*PR.'
    payee: Party | None = Field(default=None, description='Payee. EDI: N1*PE.')
    'Payee. EDI: N1*PE.'
    outpatient_adjudication: OutpatientAdjudication | None = Field(default=None,
                                                                   description='Outpatient adjudication. EDI: MOA.')
    'Outpatient adjudication. EDI: MOA.'
    inpatient_adjudication: InpatientAdjudication | None = Field(default=None,
                                                                 description='Inpatient adjudication. EDI: MIA.')
    'Inpatient adjudication. EDI: MIA.'
    adjustments: list[Adjustment] = Field(default_factory=list, description='Claim adjustments. EDI: CAS.')
    'Claim adjustments. EDI: CAS.'
    coverage_expiration_date: dt.date | None = Field(default=None,
                                                     description='Coverage expiration date. EDI: DTP03*036.')
    'Coverage expiration date. EDI: DTP03*036.'
    claim_received_date: dt.date | None = Field(default=None, description='Claim received date. EDI: DTP03*050.')
    'Claim received date. EDI: DTP03*050.'
    service_provider: PartyIdName | None = Field(default=None, description='Service provider. EDI: NM1*SJ.')
    'Service provider. EDI: NM1*SJ.'
    crossover_carrier: PartyIdName | None = Field(default=None, description='Crossover carrier. EDI: NM1*TT.')
    'Crossover carrier. EDI: NM1*TT.'
    corrected_payer: PartyIdName | None = Field(default=None,
                                                description='Corrected priority payer, meaning that current payer believes that another payer has priority for making a payment. EDI: NM1*PR.')
    'Corrected priority payer, meaning that current payer believes that another payer has priority for making a payment. EDI: NM1*PR.'
    corrected_insured: PartyIdName | None = Field(default=None, description='Corrected insured. EDI: NM1*74.')
    'Corrected insured. EDI: NM1*74.'
    claim_contacts: list[ContactInfo] = Field(default_factory=list, description='Claim contacts. EDI: PER.')
    'Claim contacts. EDI: PER.'
class PaymentCsv(EdiConverterModel):
    'Loop: 2100; Segment: CLP.'
    id: str | None = Field(default=None, description='Unique payment identifier assigned by the converter.')
    'Unique payment identifier assigned by the converter.'
    transaction_type: str | None = Field(default=None, description='Transaction set identifier code. EDI: ST01.')
    'Transaction set identifier code. EDI: ST01.'
    file_name: str | None = Field(default=None, description='Converted X12 EDI file name.')
    'Converted X12 EDI file name.'
    transaction_control_number: str | None = Field(default=None,
                                                   description='Transaction set control number. EDI: ST02.')
    'Transaction set control number. EDI: ST02.'
    patient_control_number: str | None = Field(default=None,
                                               description='Identifier used to track a claim from creation by the health care provider through payment. EDI: CLP01.')
    'Identifier used to track a claim from creation by the health care provider through payment. EDI: CLP01.'
    claim_status: AdjudicatedClaimStatus | None = Field(default=None, description='Claim status.')
    'Claim status.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: CLP03.')
    'Charge amount. EDI: CLP03.'
    payment_amount: float | None = Field(default=None, description='Payment amount. EDI: CLP04.')
    'Payment amount. EDI: CLP04.'
    patient_responsibility_amount: float | None = Field(default=None,
                                                        description='Patient responsibility amount. EDI: CLP05.')
    'Patient responsibility amount. EDI: CLP05.'
    claim_filing_indicator_code: str | None = Field(default=None,
                                                    description='Claim filing indicator code. EDI: CLP06.')
    'Claim filing indicator code. EDI: CLP06.'
    payer_control_number: str | None = Field(default=None, description='Payer control number. EDI: CLP07.')
    'Payer control number. EDI: CLP07.'
    facility: Code | None = Field(default=None,
                                  description='Place of service code (professional/dental) or UB facility code (institutional) from the original claim. EDI: CLP08.')
    'Place of service code (professional/dental) or UB facility code (institutional) from the original claim. EDI: CLP08.'
    frequency_type_code: str | None = Field(default=None, description='Frequency type code. EDI: CLP09.')
    'Frequency type code. EDI: CLP09.'
    drg_code: str | None = Field(default=None,
                                 description='Diagnosis-related group code. Institutional claims only. EDI: CLP11.')
    'Diagnosis-related group code. Institutional claims only. EDI: CLP11.'
    drg_weight: float | None = Field(default=None,
                                     description='Adjudicated DRG weight. Institutional claims only. EDI: CLP12.')
    'Adjudicated DRG weight. Institutional claims only. EDI: CLP12.'
    discharge_fraction: float | None = Field(default=None,
                                             description='Adjudicated discharge fraction. Institutional claims only. This is a percentage expressed as decimal. EDI: CLP13.')
    'Adjudicated discharge fraction. Institutional claims only. This is a percentage expressed as decimal. EDI: CLP13.'
    total_payment_amount: float | None = Field(default=None, description='Total payment amount. EDI: BPR02.')
    'Total payment amount. EDI: BPR02.'
    credit_or_debit_flag_code: str | None = Field(default=None, description='Credit or debit flag code. EDI: BPR03.')
    'Credit or debit flag code. EDI: BPR03.'
    payment_method_type: PaymentMethodType | None = Field(default=None, description='Payment method type. EDI: BPR04.')
    'Payment method type. EDI: BPR04.'
    receiver_account_number: str | None = Field(default=None, description='Receiver account number. EDI: BPR15.')
    'Receiver account number. EDI: BPR15.'
    payment_date: dt.date | None = Field(default=None, description='Payment date. EDI: BPR16.')
    'Payment date. EDI: BPR16.'
    check_or_eft_trace_number: str | None = Field(default=None, description='Check or eft trace number. EDI: TRN02.')
    'Check or eft trace number. EDI: TRN02.'
    payer_ein: str | None = Field(default=None,
                                  description="Payer identifier. This must be a '1' followed by the payer EIN. This field is also copied to the payerIdentifier field if it wasn't provided in N104. EDI: TRN03.")
    "Payer identifier. This must be a '1' followed by the payer EIN. This field is also copied to the payerIdentifier field if it wasn't provided in N104. EDI: TRN03."
    production_date: dt.date | None = Field(default=None, description='Production date. EDI: DTP03*405.')
    'Production date. EDI: DTP03*405.'
    total_adj_amount: float | None = Field(default=None,
                                           description='Sum total of all adjustments from all service lines.')
    'Sum total of all adjustments from all service lines.'
    adjs: list[Adjustment] = Field(default_factory=list, description='Claim adjustments. EDI: CAS.')
    'Claim adjustments. EDI: CAS.'
    payer: Party | None = Field(default=None, description='Payer. EDI: N1*PR.')
    'Payer. EDI: N1*PR.'
    payee: Party | None = Field(default=None, description='Payee. EDI: N1*PE.')
    'Payee. EDI: N1*PE.'
    patient: PartyIdName | None = Field(default=None,
                                        description='The insured (subscriber) or patient from the original claim. EDI: NM1*QC.')
    'The insured (subscriber) or patient from the original claim. EDI: NM1*QC.'
    subscriber: PartyIdName | None = Field(default=None,
                                           description='The insured (subscriber) from the original claim if the insured is different from the patient. EDI: NM1*44.')
    'The insured (subscriber) from the original claim if the insured is different from the patient. EDI: NM1*44.'
    corrected_patient: PartyIdName | None = Field(default=None, description='Corrected patient. EDI: NM1*74.')
    'Corrected patient. EDI: NM1*74.'
    service_provider: PartyIdName | None = Field(default=None, description='Service provider. EDI: NM1*SJ.')
    'Service provider. EDI: NM1*SJ.'
    crossover_carrier: PartyIdName | None = Field(default=None, description='Crossover carrier. EDI: NM1*TT.')
    'Crossover carrier. EDI: NM1*TT.'
    corrected_payer: PartyIdName | None = Field(default=None,
                                                description='Corrected priority payer, meaning that current payer believes that another payer has priority for making a payment. EDI: NM1*PR.')
    'Corrected priority payer, meaning that current payer believes that another payer has priority for making a payment. EDI: NM1*PR.'
    other_subscriber: PartyIdName | None = Field(default=None, description='Other subscriber. EDI: NM1*GB.')
    'Other subscriber. EDI: NM1*GB.'
    other_claim_related_ids: list[Reference] = Field(default_factory=list,
                                                     description='Other claim-related identifications. EDI: REF.')
    'Other claim-related identifications. EDI: REF.'
    service_date_from: dt.date | None = Field(default=None, description='The earliest service date from service lines.')
    'The earliest service date from service lines.'
    service_date_to: dt.date | None = Field(default=None, description='The latest service date from service lines.')
    'The latest service date from service lines.'
    statement_date_from: dt.date | None = Field(default=None, description='Statement date from. EDI: DTP03*232.')
    'Statement date from. EDI: DTP03*232.'
    statement_date_to: dt.date | None = Field(default=None, description='Statement date to. EDI: DTP03*233.')
    'Statement date to. EDI: DTP03*233.'
    coverage_expiration_date: dt.date | None = Field(default=None,
                                                     description='Coverage expiration date. EDI: DTP03*036.')
    'Coverage expiration date. EDI: DTP03*036.'
    claim_received_date: dt.date | None = Field(default=None, description='Claim received date. EDI: DTP03*050.')
    'Claim received date. EDI: DTP03*050.'
    coverage_amount: float | None = Field(default=None,
                                          description='Coverage amount from the list of supplemental amounts. EDI: AMT02*AU.')
    'Coverage amount from the list of supplemental amounts. EDI: AMT02*AU.'
    supplemental_amts: list[Amount] = Field(default_factory=list,
                                            description='Supplemental claim/payment amounts, such as coverage amount, discount amount, etc. EDI: AMT.')
    'Supplemental claim/payment amounts, such as coverage amount, discount amount, etc. EDI: AMT.'
    supplemental_qties: list[Quantity] = Field(default_factory=list,
                                               description='Supplemental claim/payment quantities. EDI: QTY.')
    'Supplemental claim/payment quantities. EDI: QTY.'
    lines: list[PaymentLineCsv] = Field(default_factory=list,
                                        description='Service payment information. EDI: Loop: 2110.')
    'Service payment information. EDI: Loop: 2110.'
class PaymentLine(EdiConverterModel):
    'Loop: 2110; Segment: SVC.'
    source_line_id: str | None = Field(default=None, description='Line item control number. EDI: REF02*6R.')
    'Line item control number. EDI: REF02*6R.'
    repriced_reference_number: str | None = Field(default=None, description='Repriced reference number. EDI: REF02*9B.')
    'Repriced reference number. EDI: REF02*9B.'
    adjusted_repriced_reference_number: str | None = Field(default=None,
                                                           description='Adjusted repriced reference number. EDI: REF02*9D.')
    'Adjusted repriced reference number. EDI: REF02*9D.'
    healthcare_policy_id: str | None = Field(default=None, description='Healthcare policy id. EDI: REF02*0K.')
    'Healthcare policy id. EDI: REF02*0K.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: SVC02.')
    'Charge amount. EDI: SVC02.'
    paid_amount: float | None = Field(default=None, description='Paid amount. EDI: SVC03.')
    'Paid amount. EDI: SVC03.'
    supplemental_amounts: list[Amount] = Field(default_factory=list,
                                               description='Supplemental amounts, such as allowed amount, deduction amount, etc. EDI: AMT.')
    'Supplemental amounts, such as allowed amount, deduction amount, etc. EDI: AMT.'
    supplemental_quantities: list[Quantity] = Field(default_factory=list,
                                                    description='Supplemental quantities. EDI: QTY.')
    'Supplemental quantities. EDI: QTY.'
    service_date_from: dt.date | None = Field(default=None, description='Service date from. EDI: DTP03*472.')
    'Service date from. EDI: DTP03*472.'
    service_date_to: dt.date | None = Field(default=None, description='Service date to. EDI: DTP03*472.')
    'Service date to. EDI: DTP03*472.'
    unit_count: float | None = Field(default=None, description='Unit count. EDI: SVC05.')
    'Unit count. EDI: SVC05.'
    original_unit_count: float | None = Field(default=None, description='Original unit count. EDI: SVC07.')
    'Original unit count. EDI: SVC07.'
    drug: Code | None = Field(default=None, description='Drug code (NDC). EDI: SVC01.')
    'Drug code (NDC). EDI: SVC01.'
    procedure: Procedure | None = Field(default=None,
                                        description='Procedure. EDI: SVC01*HC, SVC01*AD, SVC01*WK, SVC01*IV.')
    'Procedure. EDI: SVC01*HC, SVC01*AD, SVC01*WK, SVC01*IV.'
    revenue_code: Code | None = Field(default=None, description='Revenue code. EDI: SVC01*RC,NU, SVC04*RC,NU.')
    'Revenue code. EDI: SVC01*RC,NU, SVC04*RC,NU.'
    original_procedure: Procedure | None = Field(default=None,
                                                 description='Submitted procedure code from the claim if it is different from the adjudicated procedure. EDI: SVC06*HC, SVC06*AD, SVC06*WK, SVC06*IV.')
    'Submitted procedure code from the claim if it is different from the adjudicated procedure. EDI: SVC06*HC, SVC06*AD, SVC06*WK, SVC06*IV.'
    original_revenue_code: Code | None = Field(default=None,
                                               description='Submitted revenue code from the claim if it is different from the adjudicated revenue code. EDI: SVC06*RC,NU.')
    'Submitted revenue code from the claim if it is different from the adjudicated revenue code. EDI: SVC06*RC,NU.'
    original_drug: Code | None = Field(default=None,
                                       description='Submitted drug (NDC) code from the claim if it is different from the adjudicated drug code. EDI: SVC06.')
    'Submitted drug (NDC) code from the claim if it is different from the adjudicated drug code. EDI: SVC06.'
    providers: list[Provider] = Field(default_factory=list, description='Providers for this service line.')
    'Providers for this service line.'
    adjustments: list[Adjustment] = Field(default_factory=list, description='Line adjustments. EDI: CAS.')
    'Line adjustments. EDI: CAS.'
    remark_codes: list[str] = Field(default_factory=list, description='Remark codes. EDI: LQ.')
    'Remark codes. EDI: LQ.'
    remarks: list[Code] = Field(default_factory=list, description='Remark codes. EDI: LQ.')
    'Remark codes. EDI: LQ.'
    service_ids: list[Reference] = Field(default_factory=list,
                                         description='Related service-specific identifiers that were used in the process of adjudicating this service. EDI: REF.')
    'Related service-specific identifiers that were used in the process of adjudicating this service. EDI: REF.'
    rendering_provider_ids: list[Reference] = Field(default_factory=list,
                                                    description='Rendering provider identifiers. EDI: REF.')
    'Rendering provider identifiers. EDI: REF.'
class PaymentLineCsv(EdiConverterModel):
    'Loop: 2110; Segment: SVC.'
    control_number: str | None = Field(default=None, description='Line item control number from 837. EDI: REF02*6R.')
    'Line item control number from 837. EDI: REF02*6R.'
    procedure: Procedure | None = Field(default=None,
                                        description='Adjudicated procedure code. EDI: SVC01*HC, SVC01*AD, SVC01*WK, SVC01*IV.')
    'Adjudicated procedure code. EDI: SVC01*HC, SVC01*AD, SVC01*WK, SVC01*IV.'
    revenue_code: str | None = Field(default=None,
                                     description='Adjudicated revenue code. EDI: SVC01*RC,NU, SVC04*RC,NU.')
    'Adjudicated revenue code. EDI: SVC01*RC,NU, SVC04*RC,NU.'
    drug_code: str | None = Field(default=None, description='Adjudicated drug code (NDC). EDI: SVC01.')
    'Adjudicated drug code (NDC). EDI: SVC01.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: SVC02.')
    'Charge amount. EDI: SVC02.'
    paid_amount: float | None = Field(default=None, description='Paid amount. EDI: SVC03.')
    'Paid amount. EDI: SVC03.'
    unit_count: float | None = Field(default=None, description='Unit count. EDI: SVC05.')
    'Unit count. EDI: SVC05.'
    original_procedure: Procedure | None = Field(default=None,
                                                 description='Submitted procedure code from the claim if it is different from the adjudicated procedure. EDI: SVC06*HC, SVC06*AD, SVC06*WK, SVC06*IV.')
    'Submitted procedure code from the claim if it is different from the adjudicated procedure. EDI: SVC06*HC, SVC06*AD, SVC06*WK, SVC06*IV.'
    original_revenue_code: str | None = Field(default=None,
                                              description='Submitted revenue code from the claim if it is different from the adjudicated revenue code. EDI: SVC06*RC,NU.')
    'Submitted revenue code from the claim if it is different from the adjudicated revenue code. EDI: SVC06*RC,NU.'
    original_drug_code: str | None = Field(default=None,
                                           description='Submitted drug (NDC) code from the claim if it is different from the adjudicated drug code. EDI: SVC06.')
    'Submitted drug (NDC) code from the claim if it is different from the adjudicated drug code. EDI: SVC06.'
    original_unit_count: float | None = Field(default=None, description='Original unit count. EDI: SVC07.')
    'Original unit count. EDI: SVC07.'
    service_date_from: dt.date | None = Field(default=None,
                                              description='Service period start date. EDI: DTP03*472, DTP03*150.')
    'Service period start date. EDI: DTP03*472, DTP03*150.'
    service_date_to: dt.date | None = Field(default=None,
                                            description="Service period end date. If not provided in EDI (single day), it is set to 'serviceDateFrom'. EDI: DTP03*151.")
    "Service period end date. If not provided in EDI (single day), it is set to 'serviceDateFrom'. EDI: DTP03*151."
    total_adj_amount: float | None = Field(default=None,
                                           description='Sum total of all adjustments for this service line.')
    'Sum total of all adjustments for this service line.'
    adjs: list[Adjustment] = Field(default_factory=list, description='Line adjustments. EDI: CAS.')
    'Line adjustments. EDI: CAS.'
    service_ids: list[Reference] = Field(default_factory=list,
                                         description='Related service-specific identifiers that were used in the process of adjudicating this service. EDI: REF.')
    'Related service-specific identifiers that were used in the process of adjudicating this service. EDI: REF.'
    healthcare_policy_id: str | None = Field(default=None, description='Healthcare policy id. EDI: REF02*0K.')
    'Healthcare policy id. EDI: REF02*0K.'
    rendering_provider_ids: list[Reference] = Field(default_factory=list,
                                                    description='Rendering provider identifiers. EDI: REF.')
    'Rendering provider identifiers. EDI: REF.'
    allowed_amount: float | None = Field(default=None,
                                         description='Allowed amount -- this is one of the amounts from the list of supplemental amounts.')
    'Allowed amount -- this is one of the amounts from the list of supplemental amounts.'
    supplemental_amts: list[Amount] = Field(default_factory=list,
                                            description='Supplemental amounts, such as allowed amount, deduction amount, etc. EDI: AMT.')
    'Supplemental amounts, such as allowed amount, deduction amount, etc. EDI: AMT.'
    supplemental_qties: list[Quantity] = Field(default_factory=list, description='Supplemental quantities. EDI: QTY.')
    'Supplemental quantities. EDI: QTY.'
    remark_codes: list[str] = Field(default_factory=list, description='Remark codes. EDI: LQ.')
    'Remark codes. EDI: LQ.'
class Procedure(Code):
    'Procedure code with description and optional modifiers. Segment: HI, SV3, SVC, SV2, SV1.'
    modifiers: list[Code] = Field(default_factory=list, description='Modifiers.')
    'Modifiers.'
class ProfClaim(EdiConverterModel):
    'Loop: 2300; Segment: CLM.'
    id: str | None = Field(default=None, description='Unique payment identifier assigned by the converter.')
    'Unique payment identifier assigned by the converter.'
    object_type: str | None = Field(default=None, description="Type of this object, set to 'CLAIM'.")
    "Type of this object, set to 'CLAIM'."
    patient_control_number: str | None = Field(default=None,
                                               description='Identifier used to track a claim from creation by the health care provider through payment. EDI: CLM01.')
    'Identifier used to track a claim from creation by the health care provider through payment. EDI: CLM01.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: CLM02.')
    'Charge amount. EDI: CLM02.'
    patient_paid_amount: float | None = Field(default=None, description='Patient paid amount. EDI: AMT02*F5.')
    'Patient paid amount. EDI: AMT02*F5.'
    facility_code: Code | None = Field(default=None,
                                       description='Place of service code (professional/dental) or UB facility code (institutional) from the original claim. EDI: CLM05-1.')
    'Place of service code (professional/dental) or UB facility code (institutional) from the original claim. EDI: CLM05-1.'
    frequency_code: Code | None = Field(default=None, description='Frequency code. EDI: CLM05-3.')
    'Frequency code. EDI: CLM05-3.'
    service_date_from: dt.date | None = Field(default=None, description='The earliest service date from service lines.')
    'The earliest service date from service lines.'
    service_date_to: dt.date | None = Field(default=None, description='The latest service date from service lines.')
    'The latest service date from service lines.'
    subscriber: Subscriber | None = Field(default=None, description='The insured (subscriber). EDI: Loop: 2000B.')
    'The insured (subscriber). EDI: Loop: 2000B.'
    patient: Patient | None = Field(default=None,
                                    description='Patient if different from the the insured (subscriber). EDI: Loop: 2110CA.')
    'Patient if different from the the insured (subscriber). EDI: Loop: 2110CA.'
    other_subscribers: list[OtherSubscriber] = Field(default_factory=list,
                                                     description="Other subscribers and their payer's information. EDI: Loop: 2320.")
    "Other subscribers and their payer's information. EDI: Loop: 2320."
    service_lines: list[ProfLine] = Field(default_factory=list, description='Service lines. EDI: Loop: 2400.')
    'Service lines. EDI: Loop: 2400.'
    transaction: Transaction837 | None = Field(default=None,
                                               description='Parent EDI transaction for this object. EDI: ST.')
    'Parent EDI transaction for this object. EDI: ST.'
    provider_signature_indicator: str | None = Field(default=None,
                                                     description='Provider signature indicator. EDI: CLM06.')
    'Provider signature indicator. EDI: CLM06.'
    assignment_participation_code: str | None = Field(default=None,
                                                      description='Assignment participation code. EDI: CLM07.')
    'Assignment participation code. EDI: CLM07.'
    assignment_certification_indicator: str | None = Field(default=None,
                                                           description='Assignment certification indicator. EDI: CLM08.')
    'Assignment certification indicator. EDI: CLM08.'
    release_of_information_code: str | None = Field(default=None,
                                                    description='Release of information code. EDI: CLM09.')
    'Release of information code. EDI: CLM09.'
    patient_signature_source_code: str | None = Field(default=None,
                                                      description='Patient signature source code. EDI: CLM10.')
    'Patient signature source code. EDI: CLM10.'
    related_cause: RelatedCauseInfo | None = Field(default=None, description='Related cause. EDI: CLM11.')
    'Related cause. EDI: CLM11.'
    special_program_code: str | None = Field(default=None, description='Special program code. EDI: CLM12.')
    'Special program code. EDI: CLM12.'
    delay_reason_code: str | None = Field(default=None, description='Delay reason code. EDI: CLM20.')
    'Delay reason code. EDI: CLM20.'
    service_authorization_exception_code: str | None = Field(default=None,
                                                             description='Service authorization exception code. EDI: REF02*4N.')
    'Service authorization exception code. EDI: REF02*4N.'
    referral_number: str | None = Field(default=None, description='Referral number. EDI: REF02*9F.')
    'Referral number. EDI: REF02*9F.'
    prior_authorization_number: str | None = Field(default=None,
                                                   description='Prior authorization number. EDI: REF02*G1.')
    'Prior authorization number. EDI: REF02*G1.'
    original_reference_number: str | None = Field(default=None, description='Original reference number. EDI: REF02*F8.')
    'Original reference number. EDI: REF02*F8.'
    repriced_reference_number: str | None = Field(default=None, description='Repriced reference number. EDI: REF02*9A.')
    'Repriced reference number. EDI: REF02*9A.'
    adjusted_repriced_reference_number: str | None = Field(default=None,
                                                           description='Adjusted repriced reference number. EDI: REF02*9C.')
    'Adjusted repriced reference number. EDI: REF02*9C.'
    clearinghouse_trace_number: str | None = Field(default=None,
                                                   description='Clearinghouse trace number. EDI: REF02*D9.')
    'Clearinghouse trace number. EDI: REF02*D9.'
    medical_record_number: str | None = Field(default=None, description='Medical record number. EDI: REF02*EA.')
    'Medical record number. EDI: REF02*EA.'
    demonstration_project_identifier: str | None = Field(default=None,
                                                         description='Demonstration project identifier. EDI: REF02*P4.')
    'Demonstration project identifier. EDI: REF02*P4.'
    onset_of_current_illness_or_injury_date: dt.date | None = Field(default=None,
                                                                    description='Onset of current illness or injury date. EDI: DTP03*431.')
    'Onset of current illness or injury date. EDI: DTP03*431.'
    initial_treatment_date: dt.date | None = Field(default=None, description='Initial treatment date. EDI: DTP03*454.')
    'Initial treatment date. EDI: DTP03*454.'
    last_seen_date: dt.date | None = Field(default=None, description='Last seen date. EDI: DTP03*304.')
    'Last seen date. EDI: DTP03*304.'
    acute_manifestation_date: dt.date | None = Field(default=None,
                                                     description='Acute manifestation date. EDI: DTP03*453.')
    'Acute manifestation date. EDI: DTP03*453.'
    accident_date: dt.date | None = Field(default=None, description='Accident date. EDI: DTP03*439.')
    'Accident date. EDI: DTP03*439.'
    last_menstrual_period_date: dt.date | None = Field(default=None,
                                                       description='Last menstrual period date. EDI: DTP03*484.')
    'Last menstrual period date. EDI: DTP03*484.'
    last_x_ray_date: dt.date | None = Field(default=None, description='Last xray date. EDI: DTP03*455.')
    'Last xray date. EDI: DTP03*455.'
    prescription_date: dt.date | None = Field(default=None,
                                              description='Hearing and vision prescription date. EDI: DTP03*471.')
    'Hearing and vision prescription date. EDI: DTP03*471.'
    disability_date_from: dt.date | None = Field(default=None, description='Disability date from. EDI: DTP03*314.')
    'Disability date from. EDI: DTP03*314.'
    disability_date_to: dt.date | None = Field(default=None, description='Disability date to. EDI: DTP03*361.')
    'Disability date to. EDI: DTP03*361.'
    last_worked_date: dt.date | None = Field(default=None, description='Last worked date. EDI: DTP03*297.')
    'Last worked date. EDI: DTP03*297.'
    authorized_return_to_work_date: dt.date | None = Field(default=None,
                                                           description='Authorized return to work date. EDI: DTP03*296.')
    'Authorized return to work date. EDI: DTP03*296.'
    admission_date: dt.date | None = Field(default=None,
                                           description='Admission date for ambulance claims. EDI: DTP03*435.')
    'Admission date for ambulance claims. EDI: DTP03*435.'
    discharge_date: dt.date | None = Field(default=None, description='Discharge date. EDI: DTP03*096.')
    'Discharge date. EDI: DTP03*096.'
    assumed_care_date: dt.date | None = Field(default=None, description='Assumed care date. EDI: DTP03*090.')
    'Assumed care date. EDI: DTP03*090.'
    relinquished_care_date: dt.date | None = Field(default=None, description='Relinquished care date. EDI: DTP03*091.')
    'Relinquished care date. EDI: DTP03*091.'
    property_casualty_first_contact_date: dt.date | None = Field(default=None,
                                                                 description='Property casualty first contact date. EDI: DTP03*444.')
    'Property casualty first contact date. EDI: DTP03*444.'
    repricer_received_date: dt.date | None = Field(default=None, description='Repricer received date. EDI: DTP03*050.')
    'Repricer received date. EDI: DTP03*050.'
    fixed_format_records: list[str] = Field(default_factory=list, description='Fixed format records. EDI: K301.')
    'Fixed format records. EDI: K301.'
    claim_note: str | None = Field(default=None,
                                   description='Free-form comments or instructions. All note segments are concatenated together into this field. EDI: NTE02.')
    'Free-form comments or instructions. All note segments are concatenated together into this field. EDI: NTE02.'
    billing_provider: Provider | None = Field(default=None, description='Billing provider. EDI: NM1*85.')
    'Billing provider. EDI: NM1*85.'
    pay_to_address: Party | None = Field(default=None, description='Pay to address. EDI: NM1*87.')
    'Pay to address. EDI: NM1*87.'
    pay_to_plan: Party | None = Field(default=None, description='Pay-to plan for subrogation claims. EDI: NM1*PE.')
    'Pay-to plan for subrogation claims. EDI: NM1*PE.'
    providers: list[Provider] = Field(default_factory=list,
                                      description='Providers for this claim, except for the billing provider.')
    'Providers for this claim, except for the billing provider.'
    diags: list[Code] = Field(default_factory=list, description='Diagnosis codes. EDI: HI.')
    'Diagnosis codes. EDI: HI.'
    procs: list[Code] = Field(default_factory=list, description='Anesthesia-related procedures. EDI: HI.')
    'Anesthesia-related procedures. EDI: HI.'
    conditions: list[Code] = Field(default_factory=list, description='Conditions. EDI: HI*BG.')
    'Conditions. EDI: HI*BG.'
    attachments: list[Attachment] = Field(default_factory=list, description='Attachments. EDI: PWK.')
    'Attachments. EDI: PWK.'
    contract_info: ContractInfo | None = Field(default=None, description='Contract info. EDI: CN1.')
    'Contract info. EDI: CN1.'
    ambulance_transport_info: AmbulanceTransportInfo | None = Field(default=None,
                                                                    description='Ambulance transport info. EDI: CR1.')
    'Ambulance transport info. EDI: CR1.'
    spinal_manipulation_info: SpinalManipulationInfo | None = Field(default=None,
                                                                    description='Spinal manipulation info. EDI: CR2.')
    'Spinal manipulation info. EDI: CR2.'
    conditions_indicators: list[ConditionsIndicator] = Field(default_factory=list,
                                                             description='Conditions indicators. EDI: CRC.')
    'Conditions indicators. EDI: CRC.'
class ProfClaimCsv(EdiConverterModel):
    'Loop: 2300; Segment: CLM.'
    id: str | None = Field(default=None, description='Unique payment identifier assigned by the converter.')
    'Unique payment identifier assigned by the converter.'
    transaction_type: str | None = Field(default=None, description='Transaction set identifier code. EDI: ST01.')
    'Transaction set identifier code. EDI: ST01.'
    file_name: str | None = Field(default=None, description='Converted X12 EDI file name.')
    'Converted X12 EDI file name.'
    transaction_control_number: str | None = Field(default=None,
                                                   description='Transaction set control number. EDI: ST02.')
    'Transaction set control number. EDI: ST02.'
    transaction_set_purpose_code: str | None = Field(default=None,
                                                     description='Transaction set purpose code. EDI: BHT02.')
    'Transaction set purpose code. EDI: BHT02.'
    originator_application_transaction_id: str | None = Field(default=None,
                                                              description='Originator application transaction id. EDI: BHT03.')
    'Originator application transaction id. EDI: BHT03.'
    transaction_creation_date_time: str | None = Field(default=None,
                                                       description='Transaction creation date time. EDI: BHT04, BHT05.')
    'Transaction creation date time. EDI: BHT04, BHT05.'
    claim_or_encounter_identifier_type: ClaimOrEncounterIdentifierType | None = Field(default=None,
                                                                                      description='Claim or encounter identifier type. EDI: BHT06.')
    'Claim or encounter identifier type. EDI: BHT06.'
    patient_control_number: str | None = Field(default=None, description='Patient control number. EDI: CLM01.')
    'Patient control number. EDI: CLM01.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: CLM02.')
    'Charge amount. EDI: CLM02.'
    place_of_service: str | None = Field(default=None,
                                         description='Place of service as a string constant (enum). EDI: CLM05.')
    'Place of service as a string constant (enum). EDI: CLM05.'
    facility: Code | None = Field(default=None,
                                  description='Place of service code for professional/dental claims or UB facility code for institutional claims. EDI: CLM05-1.')
    'Place of service code for professional/dental claims or UB facility code for institutional claims. EDI: CLM05-1.'
    frequency_type_code: str | None = Field(default=None, description='Frequency type code. EDI: CLM05-3.')
    'Frequency type code. EDI: CLM05-3.'
    provider_signature_indicator: str | None = Field(default=None,
                                                     description='Provider signature indicator. EDI: CLM06.')
    'Provider signature indicator. EDI: CLM06.'
    assignment_participation_code: str | None = Field(default=None,
                                                      description='Assignment participation code. EDI: CLM07.')
    'Assignment participation code. EDI: CLM07.'
    assignment_certification_indicator: str | None = Field(default=None,
                                                           description='Assignment certification indicator. EDI: CLM08.')
    'Assignment certification indicator. EDI: CLM08.'
    release_of_information_code: str | None = Field(default=None,
                                                    description='Release of information code. EDI: CLM09.')
    'Release of information code. EDI: CLM09.'
    delay_reason_code: str | None = Field(default=None, description='Delay reason code. EDI: CLM20.')
    'Delay reason code. EDI: CLM20.'
    billing_provider: Provider | None = Field(default=None, description='Billing provider. EDI: NM1*85.')
    'Billing provider. EDI: NM1*85.'
    subscriber: Subscriber | None = Field(default=None, description='The insured (subscriber). EDI: NM1*44.')
    'The insured (subscriber). EDI: NM1*44.'
    patient: Patient | None = Field(default=None,
                                    description='Patient if different from the the insured (subscriber). EDI: NM1*QC.')
    'Patient if different from the the insured (subscriber). EDI: NM1*QC.'
    service_date_from: dt.date | None = Field(default=None, description='The earliest service date from service lines.')
    'The earliest service date from service lines.'
    service_date_to: dt.date | None = Field(default=None, description='The latest service date from service lines.')
    'The latest service date from service lines.'
    onset_of_current_illness_or_injury_date: dt.date | None = Field(default=None,
                                                                    description='Onset of current illness or injury date. EDI: DTP03*431.')
    'Onset of current illness or injury date. EDI: DTP03*431.'
    initial_treatment_date: dt.date | None = Field(default=None, description='Initial treatment date. EDI: DTP03*454.')
    'Initial treatment date. EDI: DTP03*454.'
    last_seen_date: dt.date | None = Field(default=None, description='Last seen date. EDI: DTP03*304.')
    'Last seen date. EDI: DTP03*304.'
    acute_manifestation_date: dt.date | None = Field(default=None,
                                                     description='Acute manifestation date. EDI: DTP03*453.')
    'Acute manifestation date. EDI: DTP03*453.'
    accident_date: dt.date | None = Field(default=None, description='Accident date. EDI: DTP03*439.')
    'Accident date. EDI: DTP03*439.'
    last_menstrual_period_date: dt.date | None = Field(default=None,
                                                       description='Last menstrual period date. EDI: DTP03*484.')
    'Last menstrual period date. EDI: DTP03*484.'
    last_x_ray_date: dt.date | None = Field(default=None, description='Last xray date. EDI: DTP03*455.')
    'Last xray date. EDI: DTP03*455.'
    prescription_date: dt.date | None = Field(default=None,
                                              description='Hearing and vision prescription date. EDI: DTP03*471.')
    'Hearing and vision prescription date. EDI: DTP03*471.'
    assumed_care_date: dt.date | None = Field(default=None, description='Assumed care date. EDI: DTP03*090.')
    'Assumed care date. EDI: DTP03*090.'
    relinquished_care_date: dt.date | None = Field(default=None, description='Relinquished care date. EDI: DTP03*091.')
    'Relinquished care date. EDI: DTP03*091.'
    admission_date: dt.date | None = Field(default=None,
                                           description='Admission date for ambulance claims. EDI: DTP03*435.')
    'Admission date for ambulance claims. EDI: DTP03*435.'
    discharge_date: dt.date | None = Field(default=None, description='Discharge date. EDI: DTP03*096.')
    'Discharge date. EDI: DTP03*096.'
    patient_paid_amount: float | None = Field(default=None, description='Patient paid amount. EDI: AMT02*F5.')
    'Patient paid amount. EDI: AMT02*F5.'
    service_authorization_exception_code: str | None = Field(default=None,
                                                             description='Service authorization exception code. EDI: REF02*4N.')
    'Service authorization exception code. EDI: REF02*4N.'
    referral_number: str | None = Field(default=None, description='Referral number. EDI: REF02*9F.')
    'Referral number. EDI: REF02*9F.'
    prior_authorization_number: str | None = Field(default=None,
                                                   description='Prior authorization number. EDI: REF02*G1.')
    'Prior authorization number. EDI: REF02*G1.'
    payer_claim_control_number: str | None = Field(default=None,
                                                   description='Payer claim control number. EDI: REF02*F8.')
    'Payer claim control number. EDI: REF02*F8.'
    clearinghouse_trace_number: str | None = Field(default=None,
                                                   description='Clearinghouse trace number. EDI: REF02*D9.')
    'Clearinghouse trace number. EDI: REF02*D9.'
    repriced_reference_number: str | None = Field(default=None, description='Repriced reference number. EDI: REF02*9A.')
    'Repriced reference number. EDI: REF02*9A.'
    adjusted_repriced_reference_number: str | None = Field(default=None,
                                                           description='Adjusted repriced reference number. EDI: REF02*9C.')
    'Adjusted repriced reference number. EDI: REF02*9C.'
    medical_record_number: str | None = Field(default=None, description='Medical record number. EDI: REF02*EA.')
    'Medical record number. EDI: REF02*EA.'
    demonstration_project_identifier: str | None = Field(default=None,
                                                         description='Demonstration project identifier. EDI: REF02*P4.')
    'Demonstration project identifier. EDI: REF02*P4.'
    note: str | None = Field(default=None,
                             description='Free-form comments or instructions. All note segments are concatenated together into this field. EDI: NTE02.')
    'Free-form comments or instructions. All note segments are concatenated together into this field. EDI: NTE02.'
    diags: list[Code] = Field(default_factory=list, description='Diags. EDI: HI*ABK, HI*ABF.')
    'Diags. EDI: HI*ABK, HI*ABF.'
    anesthesia_procedure: Code | None = Field(default=None, description='Anesthesia procedure. EDI: HI*BP.')
    'Anesthesia procedure. EDI: HI*BP.'
    conditions: list[Code] = Field(default_factory=list, description='Conditions. EDI: HI*BG.')
    'Conditions. EDI: HI*BG.'
    attachments: list[Attachment] = Field(default_factory=list, description='Attachments. EDI: PWK.')
    'Attachments. EDI: PWK.'
    referring_provider: Party | None = Field(default=None, description='Referring provider. EDI: NM1*DN.')
    'Referring provider. EDI: NM1*DN.'
    rendering_provider: Provider | None = Field(default=None, description='Rendering provider. EDI: NM1*82.')
    'Rendering provider. EDI: NM1*82.'
    service_facility: Party | None = Field(default=None, description='Service facility. EDI: NM1*77.')
    'Service facility. EDI: NM1*77.'
    supervising_provider: Party | None = Field(default=None, description='Supervising provider. EDI: NM1*DQ.')
    'Supervising provider. EDI: NM1*DQ.'
    ambulance_pick_up: Party | None = Field(default=None, description='Ambulance pick up. EDI: NM1*PW.')
    'Ambulance pick up. EDI: NM1*PW.'
    ambulance_drop_off: Party | None = Field(default=None, description='Ambulance drop off. EDI: NM1*45.')
    'Ambulance drop off. EDI: NM1*45.'
    other_subscribers: list[OtherSubscriber] = Field(default_factory=list,
                                                     description="Other subscribers and their payer's information. EDI: Loop: 2320.")
    "Other subscribers and their payer's information. EDI: Loop: 2320."
    lines: list[ProfLineCsv] = Field(default_factory=list, description='Service lines. EDI: Loop: 2400.')
    'Service lines. EDI: Loop: 2400.'
class ProfLine(EdiConverterModel):
    'Loop: 2400; Segment: SV1.'
    source_line_id: str | None = Field(default=None, description='Line item control number. EDI: REF02*6R.')
    'Line item control number. EDI: REF02*6R.'
    place_of_service_code: str | None = Field(default=None, description='Place of service code. EDI: SV105.')
    'Place of service code. EDI: SV105.'
    emergency_indicator: str | None = Field(default=None, description='Emergency indicator. EDI: SV109.')
    'Emergency indicator. EDI: SV109.'
    epsdt_indicator: str | None = Field(default=None, description='Epsdt indicator. EDI: SV111.')
    'Epsdt indicator. EDI: SV111.'
    family_planning_indicator: str | None = Field(default=None, description='Family planning indicator. EDI: SV112.')
    'Family planning indicator. EDI: SV112.'
    copay_status_code: str | None = Field(default=None, description='Copay status code. EDI: SV115.')
    'Copay status code. EDI: SV115.'
    repriced_reference_number: str | None = Field(default=None, description='Repriced reference number. EDI: REF02*9B.')
    'Repriced reference number. EDI: REF02*9B.'
    adjusted_repriced_reference_number: str | None = Field(default=None,
                                                           description='Adjusted repriced reference number. EDI: REF02*9D.')
    'Adjusted repriced reference number. EDI: REF02*9D.'
    prior_authorization: str | None = Field(default=None, description='Prior authorization. EDI: REF02*G1.')
    'Prior authorization. EDI: REF02*G1.'
    referral_number: str | None = Field(default=None, description='Referral number. EDI: REF02*9F.')
    'Referral number. EDI: REF02*9F.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: SV102.')
    'Charge amount. EDI: SV102.'
    sales_tax_amount: float | None = Field(default=None, description='Sales tax amount. EDI: AMT02*T.')
    'Sales tax amount. EDI: AMT02*T.'
    purchased_service_provider_identifier: str | None = Field(default=None,
                                                              description='Purchased service provider identifier. Since: v2.14.9. EDI: PS101.')
    'Purchased service provider identifier. Since: v2.14.9. EDI: PS101.'
    purchased_service_charge_amount: float | None = Field(default=None,
                                                          description='Purchased service charge amount. Since: v2.14.9. EDI: PS102.')
    'Purchased service charge amount. Since: v2.14.9. EDI: PS102.'
    service_date_from: dt.date | None = Field(default=None, description='Service date from. EDI: DTP03*472.')
    'Service date from. EDI: DTP03*472.'
    service_date_to: dt.date | None = Field(default=None, description='Service date to. EDI: DTP03*472.')
    'Service date to. EDI: DTP03*472.'
    prescription_date: dt.date | None = Field(default=None, description='Prescription date. EDI: DTP03*471.')
    'Prescription date. EDI: DTP03*471.'
    last_certification_date: dt.date | None = Field(default=None,
                                                    description='Last certification date. EDI: DTP03*461.')
    'Last certification date. EDI: DTP03*461.'
    certification_revision_date: dt.date | None = Field(default=None,
                                                        description='Certification revision date. EDI: DTP03*607.')
    'Certification revision date. EDI: DTP03*607.'
    begin_therapy_date: dt.date | None = Field(default=None, description='Begin therapy date. EDI: DTP03*463.')
    'Begin therapy date. EDI: DTP03*463.'
    last_seen_date: dt.date | None = Field(default=None, description='Last seen date. EDI: DTP03*304.')
    'Last seen date. EDI: DTP03*304.'
    test_performed_date: dt.date | None = Field(default=None,
                                                description='Test performed date. EDI: DTP03*738, DTP03*739.')
    'Test performed date. EDI: DTP03*738, DTP03*739.'
    last_x_ray_date: dt.date | None = Field(default=None, description='Last xray date. EDI: DTP03*455.')
    'Last xray date. EDI: DTP03*455.'
    initial_treatment_date: dt.date | None = Field(default=None, description='Initial treatment date. EDI: DTP03*454.')
    'Initial treatment date. EDI: DTP03*454.'
    unit_type: UnitType | None = Field(default=None, description='Unit type. EDI: SV103.')
    'Unit type. EDI: SV103.'
    unit_count: float | None = Field(default=None, description='Unit count. EDI: SV104.')
    'Unit count. EDI: SV104.'
    ambulance_patient_count: int | None = Field(default=None, description='Ambulance patient count. EDI: QTY02*PT.')
    'Ambulance patient count. EDI: QTY02*PT.'
    drug: Code | None = Field(default=None, description='Drug code (NDC). EDI: LIN03.')
    'Drug code (NDC). EDI: LIN03.'
    drug_quantity: float | None = Field(default=None, description='Drug quantity. EDI: CTP04.')
    'Drug quantity. EDI: CTP04.'
    drug_unit_type: UnitType | None = Field(default=None, description='Drug unit type. EDI: CTP05-1.')
    'Drug unit type. EDI: CTP05-1.'
    prescription_number: str | None = Field(default=None, description='Prescription number. EDI: REF02*XZ.')
    'Prescription number. EDI: REF02*XZ.'
    line_note: str | None = Field(default=None, description='Line note. EDI: NTE02*ADD, NTE02*DCP.')
    'Line note. EDI: NTE02*ADD, NTE02*DCP.'
    third_party_note: str | None = Field(default=None, description='Third party note. EDI: NTE02*TPO.')
    'Third party note. EDI: NTE02*TPO.'
    procedure: Procedure | None = Field(default=None,
                                        description='Procedure. EDI: SV101*HC, SV101*AD, SV101*WK, SV101*IV.')
    'Procedure. EDI: SV101*HC, SV101*AD, SV101*WK, SV101*IV.'
    dme_service: DmeService | None = Field(default=None, description='Dme service. Since: v2.14.9. EDI: SV5.')
    'Dme service. Since: v2.14.9. EDI: SV5.'
    attachments: list[Attachment] = Field(default_factory=list, description='Attachments. EDI: PWK.')
    'Attachments. EDI: PWK.'
    contract_info: ContractInfo | None = Field(default=None, description='Contract info. EDI: CN1.')
    'Contract info. EDI: CN1.'
    ambulance_transport_info: AmbulanceTransportInfo | None = Field(default=None,
                                                                    description='Ambulance transport info. EDI: CR1.')
    'Ambulance transport info. EDI: CR1.'
    dme_certification: DmeCertification | None = Field(default=None, description='Dme certification. EDI: CR3.')
    'Dme certification. EDI: CR3.'
    conditions_indicators: list[ConditionsIndicator] = Field(default_factory=list,
                                                             description='Conditions indicators. EDI: CRC.')
    'Conditions indicators. EDI: CRC.'
    measurements: list[Measurement] = Field(default_factory=list, description='Measurements. Since: v2.14.9. EDI: MEA.')
    'Measurements. Since: v2.14.9. EDI: MEA.'
    providers: list[Provider] = Field(default_factory=list, description='Providers for this service line.')
    'Providers for this service line.'
    adjudications: list[Adjudication] = Field(default_factory=list, description='Adjudications. EDI: Loop: 2430, SVD.')
    'Adjudications. EDI: Loop: 2430, SVD.'
    adjustments: list[Adjustment] = Field(default_factory=list,
                                          description='Copy of line adjustments from the adjudication list for backward compatibility. EDI: CAS.')
    'Copy of line adjustments from the adjudication list for backward compatibility. EDI: CAS.'
    fixed_format_records: list[str] = Field(default_factory=list, description='Fixed format records. EDI: K301.')
    'Fixed format records. EDI: K301.'
    forms: list[FormResponse] = Field(default_factory=list, description='Forms. Since: v2.14.9. EDI: LQ.')
    'Forms. Since: v2.14.9. EDI: LQ.'
    diag_pointers: list[int] = Field(default_factory=list,
                                     description="Diagnosis pointers. Each pointer is an index of the diagnosis in the 'diags' array at the claim level. EDI: SV107.")
    "Diagnosis pointers. Each pointer is an index of the diagnosis in the 'diags' array at the claim level. EDI: SV107."
    diags: list[Code] = Field(default_factory=list,
                              description='Copy of diagnosis codes from the claim based on diagnosis pointers. EDI: SV107.')
    'Copy of diagnosis codes from the claim based on diagnosis pointers. EDI: SV107.'
class ProfLineCsv(EdiConverterModel):
    'Loop: 2400.'
    control_number: str | None = Field(default=None, description='Control number. EDI: REF02*6R.')
    'Control number. EDI: REF02*6R.'
    procedure: Procedure | None = Field(default=None,
                                        description='Procedure. EDI: SV101*HC, SV101*AD, SV101*WK, SV101*IV.')
    'Procedure. EDI: SV101*HC, SV101*AD, SV101*WK, SV101*IV.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: SV102.')
    'Charge amount. EDI: SV102.'
    unit_type: UnitType | None = Field(default=None, description='Unit type. EDI: SV103.')
    'Unit type. EDI: SV103.'
    unit_count: float | None = Field(default=None, description='Unit count. EDI: SV104.')
    'Unit count. EDI: SV104.'
    place_of_service: str | None = Field(default=None, description='Place of service. EDI: SV105.')
    'Place of service. EDI: SV105.'
    place_of_service_code: str | None = Field(default=None, description='Place of service code. EDI: SV105.')
    'Place of service code. EDI: SV105.'
    diag_pointers: list[int] = Field(default_factory=list, description='Diag pointers. EDI: SV107.')
    'Diag pointers. EDI: SV107.'
    emergency_indicator: str | None = Field(default=None, description='Emergency indicator. EDI: SV109.')
    'Emergency indicator. EDI: SV109.'
    epsdt_indicator: str | None = Field(default=None, description='Epsdt indicator. EDI: SV111.')
    'Epsdt indicator. EDI: SV111.'
    family_planning_indicator: str | None = Field(default=None, description='Family planning indicator. EDI: SV112.')
    'Family planning indicator. EDI: SV112.'
    copay_status_code: str | None = Field(default=None, description='Copay status code. EDI: SV115.')
    'Copay status code. EDI: SV115.'
    service_date_from: dt.date | None = Field(default=None,
                                              description='Service period start date. EDI: DTP03*472, DTP03*150.')
    'Service period start date. EDI: DTP03*472, DTP03*150.'
    service_date_to: dt.date | None = Field(default=None,
                                            description="Service period end date. If not provided in EDI (single day), it is set to 'serviceDateFrom'. EDI: DTP03*151.")
    "Service period end date. If not provided in EDI (single day), it is set to 'serviceDateFrom'. EDI: DTP03*151."
    prescription_date: dt.date | None = Field(default=None, description='Prescription date. EDI: DTP03*471.')
    'Prescription date. EDI: DTP03*471.'
    begin_therapy_date: dt.date | None = Field(default=None, description='Begin therapy date. EDI: DTP03*463.')
    'Begin therapy date. EDI: DTP03*463.'
    last_seen_date: dt.date | None = Field(default=None, description='Last seen date. EDI: DTP03*304.')
    'Last seen date. EDI: DTP03*304.'
    test_performed_date: dt.date | None = Field(default=None,
                                                description='Test performed date. EDI: DTP03*738, DTP03*739.')
    'Test performed date. EDI: DTP03*738, DTP03*739.'
    last_x_ray_date: dt.date | None = Field(default=None, description='Last xray date. EDI: DTP03*455.')
    'Last xray date. EDI: DTP03*455.'
    initial_treatment_date: dt.date | None = Field(default=None, description='Initial treatment date. EDI: DTP03*454.')
    'Initial treatment date. EDI: DTP03*454.'
    prior_authorization: str | None = Field(default=None, description='Prior authorization. EDI: REF02*G1.')
    'Prior authorization. EDI: REF02*G1.'
    referral_number: str | None = Field(default=None, description='Referral number. EDI: REF02*9F.')
    'Referral number. EDI: REF02*9F.'
    repriced_reference_number: str | None = Field(default=None, description='Repriced reference number. EDI: REF02*9B.')
    'Repriced reference number. EDI: REF02*9B.'
    adjusted_repriced_reference_number: str | None = Field(default=None,
                                                           description='Adjusted repriced reference number. EDI: REF02*9D.')
    'Adjusted repriced reference number. EDI: REF02*9D.'
    note: str | None = Field(default=None, description='Note. EDI: NTE02*ADD, NTE02*DCP.')
    'Note. EDI: NTE02*ADD, NTE02*DCP.'
    third_party_note: str | None = Field(default=None, description='Third party note. EDI: NTE02.')
    'Third party note. EDI: NTE02.'
    drug: Code | None = Field(default=None, description='Drug. EDI: LIN03.')
    'Drug. EDI: LIN03.'
    drug_quantity: float | None = Field(default=None, description='Drug quantity. EDI: CTP04.')
    'Drug quantity. EDI: CTP04.'
    drug_unit_type: UnitType | None = Field(default=None, description='Drug unit type. EDI: CTP05-1.')
    'Drug unit type. EDI: CTP05-1.'
    prescription_number: str | None = Field(default=None, description='Prescription number. EDI: REF02*XZ.')
    'Prescription number. EDI: REF02*XZ.'
    attachments: list[Attachment] = Field(default_factory=list, description='Attachments. EDI: PWK.')
    'Attachments. EDI: PWK.'
    rendering_provider: Provider | None = Field(default=None, description='Rendering provider. EDI: NM1*82.')
    'Rendering provider. EDI: NM1*82.'
    purchased_service_provider: Party | None = Field(default=None,
                                                     description='Purchased service provider. EDI: NM1*QB.')
    'Purchased service provider. EDI: NM1*QB.'
    service_facility: Party | None = Field(default=None, description='Service facility. EDI: NM1*77.')
    'Service facility. EDI: NM1*77.'
    supervising_provider: Party | None = Field(default=None, description='Supervising provider. EDI: NM1*DQ.')
    'Supervising provider. EDI: NM1*DQ.'
    referring_provider: Party | None = Field(default=None, description='Referring provider. EDI: NM1*DN.')
    'Referring provider. EDI: NM1*DN.'
    ordering_provider: Party | None = Field(default=None, description='Ordering provider. EDI: NM1*DK.')
    'Ordering provider. EDI: NM1*DK.'
    ambulance_pick_up: Party | None = Field(default=None, description='Ambulance pick up. EDI: NM1*PW.')
    'Ambulance pick up. EDI: NM1*PW.'
    ambulance_drop_off: Party | None = Field(default=None, description='Ambulance drop off. EDI: NM1*45.')
    'Ambulance drop off. EDI: NM1*45.'
class ProviderAdjustment(EdiConverterModel):
    'Provider level adjustment information for debit or credit transactions such as, accelerated payments, cost report settlements for a fiscal year and timeliness report penalties unrelated to a specific claim or service. Segment: PLB.'
    id: str | None = Field(default=None, description='Unique payment identifier assigned by the converter.')
    'Unique payment identifier assigned by the converter.'
    object_type: str | None = Field(default=None,
                                    description="Type of this object, always set to 'PROVIDER_ADJUSTMENT'.")
    "Type of this object, always set to 'PROVIDER_ADJUSTMENT'."
    provider_identifier: str | None = Field(default=None, description='Provider identifier. EDI: PLB01.')
    'Provider identifier. EDI: PLB01.'
    fiscal_period_date: dt.date | None = Field(default=None, description='Fiscal period date. EDI: PLB02.')
    'Fiscal period date. EDI: PLB02.'
    adjustments: list[ProviderAdjustmentReasonAmount] = Field(default_factory=list, description='Adjustments.')
    'Adjustments.'
    payer: Party | None = Field(default=None, description='Payer. EDI: N1*PR.')
    'Payer. EDI: N1*PR.'
    payee: Party | None = Field(default=None, description='Payee. EDI: N1*PE.')
    'Payee. EDI: N1*PE.'
    transaction: Transaction835 | None = Field(default=None, description='Parent EDI transaction for this adjustment.')
    'Parent EDI transaction for this adjustment.'
class ProviderAdjustmentReasonAmount(EdiConverterModel):
    'Provider-level payment adjustment containing the reason code and the amount.'
    reason: Code | None = Field(default=None, description='Provider adjustment reason code. EDI: PLB03-1.')
    'Provider adjustment reason code. EDI: PLB03-1.'
    reference_identification: str | None = Field(default=None, description='Reference identification. EDI: PLB03-2.')
    'Reference identification. EDI: PLB03-2.'
    amount: float | None = Field(default=None, description='Amount. EDI: PLB04.')
    'Amount. EDI: PLB04.'
class ProviderStatus(EdiConverterModel):
    'Status of claims at a provider level. This object is returned only if there is an issue with the billing provider and no individual claim statuses have been provided.'
    id: str | None = Field(default=None, description='Unique payment identifier assigned by the converter.')
    'Unique payment identifier assigned by the converter.'
    object_type: str | None = Field(default=None,
                                    description="Type of this object, set to 'PROVIDER_STATUS' or 'RECEIVER_STATUS'.")
    "Type of this object, set to 'PROVIDER_STATUS' or 'RECEIVER_STATUS'."
    batch_status: BatchStatus | None = Field(default=None, description='Batch status.')
    'Batch status.'
    transaction: Transaction277 | None = Field(default=None,
                                               description='Parent EDI transaction for this object. EDI: ST.')
    'Parent EDI transaction for this object. EDI: ST.'
    receiver: PartyIdName | None = Field(default=None,
                                         description='The Receiver is the entity that expects the response from the Source. Can be a provider, a provider group, a claims clearinghouse, etc. EDI: Loop: 2000B, NM1*40.')
    'The Receiver is the entity that expects the response from the Source. Can be a provider, a provider group, a claims clearinghouse, etc. EDI: Loop: 2000B, NM1*40.'
    receiver_batch_status: BatchStatus | None = Field(default=None,
                                                      description='Receiver batch status. EDI: Loop: 2200B.')
    'Receiver batch status. EDI: Loop: 2200B.'
class Quantity(EdiConverterModel):
    'Segment: QTY.'
    qualifier_code: str | None = Field(default=None,
                                       description='Code specifying the type of quantity (quantity qualifier code). EDI: QTY01.')
    'Code specifying the type of quantity (quantity qualifier code). EDI: QTY01.'
    type: QuantityType | None = Field(default=None,
                                      description='Type of quantity; qualifier code translated to a mnemonic string constant (enum). EDI: QTY01.')
    'Type of quantity; qualifier code translated to a mnemonic string constant (enum). EDI: QTY01.'
    quantity: float | None = Field(default=None, description='Quantity. EDI: QTY02.')
    'Quantity. EDI: QTY02.'
class ReceiverStatus(EdiConverterModel):
    'Status of claims at a transaction level. This object is returned only if all claims have been rejected and no individual claim statuses have been provided.'
    id: str | None = Field(default=None, description='Unique payment identifier assigned by the converter.')
    'Unique payment identifier assigned by the converter.'
    object_type: str | None = Field(default=None,
                                    description="Type of this object, set to 'PROVIDER_STATUS' or 'RECEIVER_STATUS'.")
    "Type of this object, set to 'PROVIDER_STATUS' or 'RECEIVER_STATUS'."
    batch_status: BatchStatus | None = Field(default=None, description='Batch status.')
    'Batch status.'
    transaction: Transaction277 | None = Field(default=None,
                                               description='Parent EDI transaction for this object. EDI: ST.')
    'Parent EDI transaction for this object. EDI: ST.'
    receiver: PartyIdName | None = Field(default=None,
                                         description='The Receiver is the entity that expects the response from the Source. Can be a provider, a provider group, a claims clearinghouse, etc. EDI: Loop: 2000B, NM1*40.')
    'The Receiver is the entity that expects the response from the Source. Can be a provider, a provider group, a claims clearinghouse, etc. EDI: Loop: 2000B, NM1*40.'
class Reference(EdiConverterModel):
    'Segment: REF.'
    qualifier_code: str | None = Field(default=None,
                                       description='Code qualifying the reference identification. EDI: REF01.')
    'Code qualifying the reference identification. EDI: REF01.'
    type: ReferenceType | None = Field(default=None,
                                       description='Type of reference; qualifier code as a string constant (enum). EDI: REF01.')
    'Type of reference; qualifier code as a string constant (enum). EDI: REF01.'
    identification: str | None = Field(default=None, description='Reference identification. EDI: REF02.')
    'Reference identification. EDI: REF02.'
class RelatedCauseInfo(EdiConverterModel):
    'OpenAPI schema for RelatedCauseInfo.'
    related_cause_code: str | None = Field(default=None, description='Related cause code. EDI: CLM11-1.')
    'Related cause code. EDI: CLM11-1.'
    related_cause_code2: str | None = Field(default=None, description='Related cause code2. EDI: CLM11-2.')
    'Related cause code2. EDI: CLM11-2.'
    state_code: str | None = Field(default=None, description='State code. EDI: CLM11-4.')
    'State code. EDI: CLM11-4.'
    country_code: str | None = Field(default=None, description='Country code. EDI: CLM11-5.')
    'Country code. EDI: CLM11-5.'
class ReportingCategory(EdiConverterModel):
    'OpenAPI schema for ReportingCategory.'
    name: str | None = Field(default=None, description='Name. EDI: N102.')
    'Name. EDI: N102.'
    identifier_qualifier_code: str | None = Field(default=None, description='Identifier qualifier code. EDI: REF01.')
    'Identifier qualifier code. EDI: REF01.'
    identifier_type: ReferenceType | None = Field(default=None, description='Identifier type. EDI: REF01.')
    'Identifier type. EDI: REF01.'
    identifier: str | None = Field(default=None, description='Identifier. EDI: REF02.')
    'Identifier. EDI: REF02.'
    date: dt.date | None = Field(default=None, description='Effective date. EDI: DTP03*007.')
    'Effective date. EDI: DTP03*007.'
    date_to: dt.date | None = Field(default=None, description='End date. EDI: DTP03.')
    'End date. EDI: DTP03.'
class ServiceLineStatus(EdiConverterModel):
    'Service line information and its status. Loop: 2220D.'
    control_number: str | None = Field(default=None, description='Line item control number from 837. EDI: REF02*6R.')
    'Line item control number from 837. EDI: REF02*6R.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: SVC02.')
    'Charge amount. EDI: SVC02.'
    unit_count: float | None = Field(default=None, description='Unit count. EDI: SVC07.')
    'Unit count. EDI: SVC07.'
    procedure: Procedure | None = Field(default=None, description='Procedure. EDI: SVC01.')
    'Procedure. EDI: SVC01.'
    revenue_code: Code | None = Field(default=None, description='Revenue code. EDI: SVC01, SVC04.')
    'Revenue code. EDI: SVC01, SVC04.'
    prescription_number: str | None = Field(default=None, description='Prescription number. EDI: REF02*XZ.')
    'Prescription number. EDI: REF02*XZ.'
    service_date_from: dt.date | None = Field(default=None,
                                              description='Service period start date. EDI: DTP03*472, DTP03*150.')
    'Service period start date. EDI: DTP03*472, DTP03*150.'
    service_date_to: dt.date | None = Field(default=None,
                                            description="Service period end date. If not provided in EDI (single day), it is set to 'serviceDateFrom'. EDI: DTP03*151.")
    "Service period end date. If not provided in EDI (single day), it is set to 'serviceDateFrom'. EDI: DTP03*151."
    status_infos: list[StatusInfo] = Field(default_factory=list, description='Status infos.')
    'Status infos.'
class SourceLocation(EdiConverterModel):
    'Location of the validation issue.'
    file_name: str | None = Field(default=None, description='File name.')
    'File name.'
    line_number: int | None = Field(default=None, description='Line number in the file.')
    'Line number in the file.'
    segment_number: int | None = Field(default=None, description='Segment number in the file.')
    'Segment number in the file.'
class SpinalManipulationInfo(EdiConverterModel):
    'Spinal manipulation service info. Required on chiropractic claims involving spinal manipulation when the information is known to impact the payer’s adjudication process. Segment: CR2.'
    condition_code: str | None = Field(default=None, description='Condition code. EDI: CR208.')
    'Condition code. EDI: CR208.'
    description: str | None = Field(default=None, description='Description of the patient’s condition. EDI: CR210.')
    'Description of the patient’s condition. EDI: CR210.'
    additional_description: str | None = Field(default=None,
                                               description='Additional description of the patient’s condition. EDI: CR211.')
    'Additional description of the patient’s condition. EDI: CR211.'
class StatusCodeInfo(EdiConverterModel):
    'Contains sub-elements of the composite healthcare claim status element (STC01,STC10,STC11).'
    category_code: str | None = Field(default=None, description='Category code. EDI: STC01-1.')
    'Category code. EDI: STC01-1.'
    status_code: str | None = Field(default=None, description='Status code. EDI: STC01-2.')
    'Status code. EDI: STC01-2.'
    entity_code: str | None = Field(default=None, description='Entity code. EDI: STC01-3.')
    'Entity code. EDI: STC01-3.'
class StatusInfo(EdiConverterModel):
    'Status Information. Segment: STC.'
    effective_date: dt.date | None = Field(default=None, description='Effective date. EDI: STC02.')
    'Effective date. EDI: STC02.'
    action_code: str | None = Field(default=None, description='Action code. EDI: STC03.')
    'Action code. EDI: STC03.'
    action_type: StatusActionType | None = Field(default=None,
                                                 description='Status action type (action code translated to constant/enum), ACCEPT or REJECT. EDI: STC03.')
    'Status action type (action code translated to constant/enum), ACCEPT or REJECT. EDI: STC03.'
    charge_amount: float | None = Field(default=None, description='Charge amount. EDI: STC04.')
    'Charge amount. EDI: STC04.'
    status_code_infos: list[StatusCodeInfo] = Field(default_factory=list,
                                                    description='Status code infos. EDI: STC01, STC10, STC11.')
    'Status code infos. EDI: STC01, STC10, STC11.'
    message: str | None = Field(default=None, description='Message. EDI: STC12.')
    'Message. EDI: STC12.'
class Subscriber(EdiConverterModel):
    'OpenAPI schema for Subscriber.'
    payer_responsibility_sequence: PayerRespSequenceType | None = Field(default=None,
                                                                        description='Payer responsibility sequence. EDI: SBR01.')
    'Payer responsibility sequence. EDI: SBR01.'
    relationship_type: RelationshipType | None = Field(default=None,
                                                       description='Relationship type. EDI: SBR02, PAT01.')
    'Relationship type. EDI: SBR02, PAT01.'
    group_or_policy_number: str | None = Field(default=None, description='Group or policy number. EDI: SBR03.')
    'Group or policy number. EDI: SBR03.'
    group_name: str | None = Field(default=None, description='Group name. EDI: SBR04.')
    'Group name. EDI: SBR04.'
    claim_filing_indicator_code: str | None = Field(default=None,
                                                    description='Claim filing indicator code. EDI: SBR09.')
    'Claim filing indicator code. EDI: SBR09.'
    insurance_plan_type: InsurancePlanType | None = Field(default=None, description='Insurance plan type. EDI: SBR09.')
    'Insurance plan type. EDI: SBR09.'
    person: PersonWithDemographic | None = Field(default=None, description='Person. EDI: NM1.')
    'Person. EDI: NM1.'
    death_date: dt.date | None = Field(default=None, description='Death date. EDI: PAT06.')
    'Death date. EDI: PAT06.'
    weight: float | None = Field(default=None, description='Patient weight in pounds. EDI: PAT08.')
    'Patient weight in pounds. EDI: PAT08.'
    pregnancy_indicator: str | None = Field(default=None, description='Pregnancy indicator. EDI: PAT09.')
    'Pregnancy indicator. EDI: PAT09.'
    property_casualty_claim_number: str | None = Field(default=None,
                                                       description='Property casualty claim number. EDI: REF02*Y4.')
    'Property casualty claim number. EDI: REF02*Y4.'
    payer: Party | None = Field(default=None, description='Payer. EDI: Loop: 2330B, NM1*PR.')
    'Payer. EDI: Loop: 2330B, NM1*PR.'
class ToothInfo(EdiConverterModel):
    'Segment: TOO.'
    code: str | None = Field(default=None, description='Code. EDI: TOO02.')
    'Code. EDI: TOO02.'
    surface_codes: list[str] = Field(default_factory=list, description='Surface codes. EDI: TOO03.')
    'Surface codes. EDI: TOO03.'
class ToothStatus(EdiConverterModel):
    'Segment: DN2.'
    tooth_number: str | None = Field(default=None, description='Tooth number. EDI: DN201.')
    'Tooth number. EDI: DN201.'
    status_code: str | None = Field(default=None, description='Status code. EDI: DN202.')
    'Status code. EDI: DN202.'
class Transaction277(EdiConverterModel):
    'OpenAPI schema for Transaction277.'
    control_number: str | None = Field(default=None, description='Control number. EDI: ST02.')
    'Control number. EDI: ST02.'
    transaction_type: str | None = Field(default=None,
                                         description='Transaction type translated to string constant, PROF for 837P, INST for 837I, etc. Required in order for EDI generator to populate defaults. EDI: ST01, ST03.')
    'Transaction type translated to string constant, PROF for 837P, INST for 837I, etc. Required in order for EDI generator to populate defaults. EDI: ST01, ST03.'
    hierarchical_structure_code: str | None = Field(default=None,
                                                    description='Hierarchical structure code. EDI: BHT01.')
    'Hierarchical structure code. EDI: BHT01.'
    purpose_code: str | None = Field(default=None, description='Purpose code. EDI: BHT02.')
    'Purpose code. EDI: BHT02.'
    originator_application_transaction_id: str | None = Field(default=None,
                                                              description='Originator application transaction id. EDI: BHT03.')
    'Originator application transaction id. EDI: BHT03.'
    creation_date: dt.date | None = Field(default=None, description='Creation date. EDI: BHT04.')
    'Creation date. EDI: BHT04.'
    creation_time: str | None = Field(default=None, description='Creation time. EDI: BHT05.')
    'Creation time. EDI: BHT05.'
    trace_identifier: str | None = Field(default=None, description='Trace identifier. EDI: TRN02.')
    'Trace identifier. EDI: TRN02.'
    transaction_set_identifier_code: str | None = Field(default=None,
                                                        description='Transaction set identifier code. EDI: ST01.')
    'Transaction set identifier code. EDI: ST01.'
    implementation_convention_reference: str | None = Field(default=None,
                                                            description='Implementation convention reference. EDI: ST03.')
    'Implementation convention reference. EDI: ST03.'
    receipt_date: dt.date | None = Field(default=None, description='Receipt date. EDI: DTP03*050.')
    'Receipt date. EDI: DTP03*050.'
    process_date: dt.date | None = Field(default=None, description='Process date. EDI: DTP03*009.')
    'Process date. EDI: DTP03*009.'
    file_info: FileInfo | None = Field(default=None, description='File info.')
    'File info.'
    sender: Party | None = Field(default=None, description='Information source name.')
    'Information source name.'
class Transaction834(EdiConverterModel):
    'OpenAPI schema for Transaction834.'
    control_number: str | None = Field(default=None, description='Control number. EDI: ST02.')
    'Control number. EDI: ST02.'
    transaction_type: str | None = Field(default=None,
                                         description='Transaction type translated to string constant, PROF for 837P, INST for 837I, etc. Required in order for EDI generator to populate defaults. EDI: ST01, ST03.')
    'Transaction type translated to string constant, PROF for 837P, INST for 837I, etc. Required in order for EDI generator to populate defaults. EDI: ST01, ST03.'
    purpose_code: str | None = Field(default=None, description='Purpose code. EDI: BGN01.')
    'Purpose code. EDI: BGN01.'
    originator_application_transaction_id: str | None = Field(default=None,
                                                              description='Originator application transaction id. EDI: BGN02.')
    'Originator application transaction id. EDI: BGN02.'
    creation_date: dt.date | None = Field(default=None, description='Creation date. EDI: BGN03.')
    'Creation date. EDI: BGN03.'
    creation_time: str | None = Field(default=None, description='Creation time. EDI: BGN04.')
    'Creation time. EDI: BGN04.'
    original_transaction_set_reference_number: str | None = Field(default=None,
                                                                  description='Original transaction set reference number. EDI: BGN06.')
    'Original transaction set reference number. EDI: BGN06.'
    action_code: str | None = Field(default=None, description='Action code. EDI: BGN08.')
    'Action code. EDI: BGN08.'
    transaction_set_identifier_code: str | None = Field(default=None,
                                                        description='Transaction set identifier code. EDI: ST01.')
    'Transaction set identifier code. EDI: ST01.'
    implementation_convention_reference: str | None = Field(default=None,
                                                            description='Implementation convention reference. EDI: ST03.')
    'Implementation convention reference. EDI: ST03.'
    file_effective_dates: list[Date] = Field(default_factory=list, description='File effective dates. EDI: DTP.')
    'File effective dates. EDI: DTP.'
    control_totals: list[Quantity] = Field(default_factory=list, description='Control totals. EDI: QTY.')
    'Control totals. EDI: QTY.'
    file_info: FileInfo | None = Field(default=None, description='File info.')
    'File info.'
class Transaction835(EdiConverterModel):
    'OpenAPI schema for Transaction835.'
    control_number: str | None = Field(default=None, description='Control number. EDI: ST02.')
    'Control number. EDI: ST02.'
    transaction_type: str | None = Field(default=None,
                                         description='Transaction type translated to string constant, PROF for 837P, INST for 837I, etc. Required in order for EDI generator to populate defaults. EDI: ST01, ST03.')
    'Transaction type translated to string constant, PROF for 837P, INST for 837I, etc. Required in order for EDI generator to populate defaults. EDI: ST01, ST03.'
    production_date: dt.date | None = Field(default=None, description='Production date. EDI: DTP03*405.')
    'Production date. EDI: DTP03*405.'
    transaction_handling_type: TransactionHandlingType | None = Field(default=None,
                                                                      description='Transaction handling type. EDI: BPR01.')
    'Transaction handling type. EDI: BPR01.'
    total_payment_amount: float | None = Field(default=None, description='Total payment amount. EDI: BPR02.')
    'Total payment amount. EDI: BPR02.'
    credit_or_debit_flag_code: str | None = Field(default=None, description='Credit or debit flag code. EDI: BPR03.')
    'Credit or debit flag code. EDI: BPR03.'
    payment_method_type: PaymentMethodType | None = Field(default=None,
                                                          description='Payment method type: ACH, CHECK, WIRE_TRANSFER, NON_PAYMENT. EDI: BPR04.')
    'Payment method type: ACH, CHECK, WIRE_TRANSFER, NON_PAYMENT. EDI: BPR04.'
    payment_format_code: str | None = Field(default=None, description='Payment format code. EDI: BPR05.')
    'Payment format code. EDI: BPR05.'
    sender_bank_routing_number: str | None = Field(default=None, description='Sender bank routing number. EDI: BPR07.')
    'Sender bank routing number. EDI: BPR07.'
    sender_account_number: str | None = Field(default=None, description='Sender account number. EDI: BPR09.')
    'Sender account number. EDI: BPR09.'
    originating_company_id: str | None = Field(default=None,
                                               description='If provided, should be identical to payerIdentifier. EDI: BPR10.')
    'If provided, should be identical to payerIdentifier. EDI: BPR10.'
    originating_company_supplemental_code: str | None = Field(default=None,
                                                              description='Originating company supplemental code. EDI: BPR11, TRN04.')
    'Originating company supplemental code. EDI: BPR11, TRN04.'
    receiver_bank_routing_number: str | None = Field(default=None,
                                                     description='Receiver bank routing number. EDI: BPR13.')
    'Receiver bank routing number. EDI: BPR13.'
    receiver_account_number: str | None = Field(default=None, description='Receiver account number. EDI: BPR15.')
    'Receiver account number. EDI: BPR15.'
    payment_date: dt.date | None = Field(default=None, description='Payment date. EDI: BPR16.')
    'Payment date. EDI: BPR16.'
    check_or_eft_trace_number: str | None = Field(default=None, description='Check or eft trace number. EDI: TRN02.')
    'Check or eft trace number. EDI: TRN02.'
    payer_identifier: str | None = Field(default=None,
                                         description="This must be a 1 followed by the payer's EIN or TIN. This ID will be used as the identifier in the payer object if no other identifier was provided. EDI: TRN03.")
    "This must be a 1 followed by the payer's EIN or TIN. This ID will be used as the identifier in the payer object if no other identifier was provided. EDI: TRN03."
    receiver_identifier: str | None = Field(default=None,
                                            description="Receiver's identifier when different from payee (e.g., a clearinghouse). EDI: REF02*EV.")
    "Receiver's identifier when different from payee (e.g., a clearinghouse). EDI: REF02*EV."
    transaction_set_identifier_code: str | None = Field(default=None,
                                                        description='Transaction set identifier code. EDI: ST01.')
    'Transaction set identifier code. EDI: ST01.'
    implementation_convention_reference: str | None = Field(default=None,
                                                            description='Implementation convention reference. EDI: ST03.')
    'Implementation convention reference. EDI: ST03.'
    file_info: FileInfo | None = Field(default=None, description='File info.')
    'File info.'
class Transaction837(EdiConverterModel):
    'OpenAPI schema for Transaction837.'
    control_number: str | None = Field(default=None, description='Control number. EDI: ST02.')
    'Control number. EDI: ST02.'
    transaction_type: str | None = Field(default=None,
                                         description='Transaction type translated to string constant, PROF for 837P, INST for 837I, etc. Required in order for EDI generator to populate defaults. EDI: ST01, ST03.')
    'Transaction type translated to string constant, PROF for 837P, INST for 837I, etc. Required in order for EDI generator to populate defaults. EDI: ST01, ST03.'
    hierarchical_structure_code: str | None = Field(default=None,
                                                    description='Hierarchical structure code. EDI: BHT01.')
    'Hierarchical structure code. EDI: BHT01.'
    purpose_code: str | None = Field(default=None, description='Purpose code. EDI: BHT02.')
    'Purpose code. EDI: BHT02.'
    originator_application_transaction_id: str | None = Field(default=None,
                                                              description='Originator application transaction id. EDI: BHT03.')
    'Originator application transaction id. EDI: BHT03.'
    creation_date: dt.date | None = Field(default=None, description='Creation date. EDI: BHT04.')
    'Creation date. EDI: BHT04.'
    creation_time: str | None = Field(default=None, description='Creation time. EDI: BHT05.')
    'Creation time. EDI: BHT05.'
    claim_or_encounter_identifier_type: ClaimOrEncounterIdentifierType | None = Field(default=None,
                                                                                      description='Claim or encounter identifier type. EDI: BHT06.')
    'Claim or encounter identifier type. EDI: BHT06.'
    transaction_set_identifier_code: str | None = Field(default=None,
                                                        description='Transaction set identifier code. EDI: ST01.')
    'Transaction set identifier code. EDI: ST01.'
    implementation_convention_reference: str | None = Field(default=None,
                                                            description='Implementation convention reference. EDI: ST03.')
    'Implementation convention reference. EDI: ST03.'
    file_info: FileInfo | None = Field(default=None, description='File info.')
    'File info.'
    sender: Party | None = Field(default=None, description='Submitter or sender of this transaction.')
    'Submitter or sender of this transaction.'
    receiver: PartyIdName | None = Field(default=None, description='Receiver of this transaction.')
    'Receiver of this transaction.'
class ValidationIssue(EdiConverterModel):
    'EDI validation issue details.'
    issue_type: str | None = Field(default=None, description='Issue type.')
    'Issue type.'
    json_path: str | None = Field(default=None, description='JSON path for the object where the issue was detected.')
    'JSON path for the object where the issue was detected.'
    field_name: str | None = Field(default=None, description='Field name or element name.')
    'Field name or element name.'
    source_location: SourceLocation | None = Field(default=None, description='Location of the issue in the EDI file.')
    'Location of the issue in the EDI file.'
    loop: str | None = Field(default=None, description='EDI loop where the issue was found.')
    'EDI loop where the issue was found.'
    segment: str | None = Field(default=None, description='EDI segment ID.')
    'EDI segment ID.'
    element: str | None = Field(default=None, description='EDI element designator.')
    'EDI element designator.'
    edi_code: str | None = Field(default=None,
                                 description='EDI qualifier or code for the segment if the segment is uniquely identified by the code.')
    'EDI qualifier or code for the segment if the segment is uniquely identified by the code.'
    max_number_of_items: int | None = Field(default=None,
                                            description='Maximum number of items allowed for the segment or list.')
    'Maximum number of items allowed for the segment or list.'
    actual_number_of_items: int | None = Field(default=None, description='Actual number of items.')
    'Actual number of items.'
    length: int | None = Field(default=None, description="Expected length of the element's value.")
    "Expected length of the element's value."
    actual_length: int | None = Field(default=None, description='Actual length.')
    'Actual length.'
    data_type: str | None = Field(default=None, description='Expected data type.')
    'Expected data type.'
    actual_data_type: str | None = Field(default=None, description='Actual data type.')
    'Actual data type.'
    value: str | None = Field(default=None, description='Value with the issue.')
    'Value with the issue.'
    edi_string: str | None = Field(default=None, description='Value that caused the issue.')
    'Value that caused the issue.'
    message: str | None = Field(default=None, description='Additional message describing the issue.')
    'Additional message describing the issue.'
    allowed_values: list[str] = Field(default_factory=list, description='Allowed values.')
    'Allowed values.'
class Party(PartyIdName):
    'OpenAPI schema for Party.'
    address: Address | None = Field(default=None, description='Address.')
    'Address.'
    contacts: list[ContactInfo] = Field(default_factory=list, description='Contacts.')
    'Contacts.'
    additional_ids: list[Reference] = Field(default_factory=list, description='Other identifications. EDI: REF.')
    'Other identifications. EDI: REF.'
class PersonWithDemographic(Party):
    'OpenAPI schema for PersonWithDemographic.'
    birth_date: dt.date | None = Field(default=None, description='Birth date. EDI: DMG02.')
    'Birth date. EDI: DMG02.'
    gender: GenderType | None = Field(default=None, description='Gender. EDI: DMG03.')
    'Gender. EDI: DMG03.'
class Provider(Party):
    'OpenAPI schema for Provider.'
    provider_taxonomy: Code | None = Field(default=None,
                                           description="Provider's specialty information (taxonomy). Populated only for billing, rendering, operating providers. EDI: PRV.")
    "Provider's specialty information (taxonomy). Populated only for billing, rendering, operating providers. EDI: PRV."
class Tpa(Party):
    'Loop: 1100C, 1000C.'
    account_number: str | None = Field(default=None, description='Account number. EDI: ACT01.')
    'Account number. EDI: ACT01.'
    account_number2: str | None = Field(default=None, description='Account number2. EDI: ACT06.')
    'Account number2. EDI: ACT06.'
class Member(PersonWithDemographic):
    'Loop: 2100A; Segment: NM1.'
    marital_status_code: str | None = Field(default=None, description='Marital status code. EDI: DMG04.')
    'Marital status code. EDI: DMG04.'
    ethnicity_code: str | None = Field(default=None,
                                       description="Ethnicity code. Deprecated: Use 'ethnicityCodes' instead. EDI: DMG05.")
    "Ethnicity code. Deprecated: Use 'ethnicityCodes' instead. EDI: DMG05."
    ethnicity_codes: list[str] = Field(default_factory=list, description='Ethnicity codes. Since: v2.14.8. EDI: DMG05.')
    'Ethnicity codes. Since: v2.14.8. EDI: DMG05.'
    citizenship_code: str | None = Field(default=None, description='Citizenship code. EDI: DMG06.')
    'Citizenship code. EDI: DMG06.'
    employment_class_codes: list[str] = Field(default_factory=list,
                                              description='Employment class codes. EDI: EC01, EC02, EC03.')
    'Employment class codes. EDI: EC01, EC02, EC03.'
    wage_frequency_code: str | None = Field(default=None, description='Wage frequency code. EDI: ICM01.')
    'Wage frequency code. EDI: ICM01.'
    wage_amount: float | None = Field(default=None, description='Wage amount. EDI: ICM02.')
    'Wage amount. EDI: ICM02.'
    work_hours_count: float | None = Field(default=None, description='Work hours count. EDI: ICM03.')
    'Work hours count. EDI: ICM03.'
    employer_location_identification_code: str | None = Field(default=None,
                                                              description='Employer location identification code. EDI: ICM04.')
    'Employer location identification code. EDI: ICM04.'
    salary_grade_code: str | None = Field(default=None, description='Salary grade code. EDI: ICM05.')
    'Salary grade code. EDI: ICM05.'
    health_related_code: str | None = Field(default=None, description='Health related code. EDI: HLH01.')
    'Health related code. EDI: HLH01.'
    height: float | None = Field(default=None, description='Height. EDI: HLH02.')
    'Height. EDI: HLH02.'
    weight: float | None = Field(default=None, description='Weight. EDI: HLH03.')
    'Weight. EDI: HLH03.'
    language_info: LanguageInfo | None = Field(default=None,
                                               description="Language info. Deprecated: Use 'languages' instead. EDI: LUI.")
    "Language info. Deprecated: Use 'languages' instead. EDI: LUI."
    languages: list[LanguageInfo] = Field(default_factory=list, description='Languages. Since: v2.14.8. EDI: LUI.')
    'Languages. Since: v2.14.8. EDI: LUI.'

Address.model_rebuild()
Adjudication.model_rebuild()
Adjustment.model_rebuild()
AmbulanceTransportInfo.model_rebuild()
Amount.model_rebuild()
Attachment.model_rebuild()
AwsInOutKey.model_rebuild()
AwsRequest.model_rebuild()
BatchStatus.model_rebuild()
ClaimStatus.model_rebuild()
Code.model_rebuild()
CodeAndAmount.model_rebuild()
CodeAndDate.model_rebuild()
ConditionsIndicator.model_rebuild()
ContactInfo.model_rebuild()
ContactNumber.model_rebuild()
ContractInfo.model_rebuild()
CoordinationOfBenefits.model_rebuild()
Date.model_rebuild()
DentClaim.model_rebuild()
DentLine.model_rebuild()
Disability.model_rebuild()
DmeCertification.model_rebuild()
DmeService.model_rebuild()
EdiGenClaimRequest.model_rebuild()
ErrorInfo.model_rebuild()
FileInfo.model_rebuild()
FormQuestionResponse.model_rebuild()
FormResponse.model_rebuild()
FunctionalGroup.model_rebuild()
HealthCoverage.model_rebuild()
InpatientAdjudication.model_rebuild()
InstClaim.model_rebuild()
InstClaimCsv.model_rebuild()
InstDiagnosis.model_rebuild()
InstLine.model_rebuild()
InstLineCsv.model_rebuild()
InterchangeControl.model_rebuild()
LanguageInfo.model_rebuild()
Measurement.model_rebuild()
MemberCoverage.model_rebuild()
MemberCoverageCsv.model_rebuild()
OrthodonticInfo.model_rebuild()
OtherSubscriber.model_rebuild()
OutpatientAdjudication.model_rebuild()
PartyIdName.model_rebuild()
Patient.model_rebuild()
PatientSubscriber835.model_rebuild()
Payment.model_rebuild()
PaymentCsv.model_rebuild()
PaymentLine.model_rebuild()
PaymentLineCsv.model_rebuild()
Procedure.model_rebuild()
ProfClaim.model_rebuild()
ProfClaimCsv.model_rebuild()
ProfLine.model_rebuild()
ProfLineCsv.model_rebuild()
ProviderAdjustment.model_rebuild()
ProviderAdjustmentReasonAmount.model_rebuild()
ProviderStatus.model_rebuild()
Quantity.model_rebuild()
ReceiverStatus.model_rebuild()
Reference.model_rebuild()
RelatedCauseInfo.model_rebuild()
ReportingCategory.model_rebuild()
ServiceLineStatus.model_rebuild()
SourceLocation.model_rebuild()
SpinalManipulationInfo.model_rebuild()
StatusCodeInfo.model_rebuild()
StatusInfo.model_rebuild()
Subscriber.model_rebuild()
ToothInfo.model_rebuild()
ToothStatus.model_rebuild()
Transaction277.model_rebuild()
Transaction834.model_rebuild()
Transaction835.model_rebuild()
Transaction837.model_rebuild()
ValidationIssue.model_rebuild()
Party.model_rebuild()
PersonWithDemographic.model_rebuild()
Provider.model_rebuild()
Tpa.model_rebuild()
Member.model_rebuild()

__all__ = [
    'EdiConverterModel',
    'to_camel',
    'AdjustmentGroup',
    'AmbulanceTransportReason',
    'AmountType',
    'ClaimOrEncounterIdentifierType',
    'AdjudicatedClaimStatus',
    'ConditionsIndicatorCategory',
    'DateType',
    'DmeBillingFrequency',
    'EntityRole',
    'EntityType',
    'GenderType',
    'IdentificationType',
    'InsurancePlanType',
    'MeasurementType',
    'PayerRespSequenceType',
    'PaymentMethodType',
    'QuantityType',
    'ReferenceType',
    'RelationshipType',
    'StatusActionType',
    'TransactionHandlingType',
    'UnitType',
    'Address',
    'Adjudication',
    'Adjustment',
    'AmbulanceTransportInfo',
    'Amount',
    'Attachment',
    'AwsInOutKey',
    'AwsRequest',
    'BatchStatus',
    'AdjudicatedClaimStatus',
    'Code',
    'CodeAndAmount',
    'CodeAndDate',
    'ConditionsIndicator',
    'ContactInfo',
    'ContactNumber',
    'ContractInfo',
    'CoordinationOfBenefits',
    'Date',
    'DentClaim',
    'DentLine',
    'Disability',
    'DmeCertification',
    'DmeService',
    'EdiGenClaimRequest',
    'ErrorInfo',
    'FileInfo',
    'FormQuestionResponse',
    'FormResponse',
    'FunctionalGroup',
    'HealthCoverage',
    'InpatientAdjudication',
    'InstClaim',
    'InstClaimCsv',
    'InstDiagnosis',
    'InstLine',
    'InstLineCsv',
    'InterchangeControl',
    'LanguageInfo',
    'Measurement',
    'MemberCoverage',
    'MemberCoverageCsv',
    'OrthodonticInfo',
    'OtherSubscriber',
    'OutpatientAdjudication',
    'PartyIdName',
    'Patient',
    'PatientSubscriber835',
    'Payment',
    'PaymentCsv',
    'PaymentLine',
    'PaymentLineCsv',
    'Procedure',
    'ProfClaim',
    'ProfClaimCsv',
    'ProfLine',
    'ProfLineCsv',
    'ProviderAdjustment',
    'ProviderAdjustmentReasonAmount',
    'ProviderStatus',
    'Quantity',
    'ReceiverStatus',
    'Reference',
    'RelatedCauseInfo',
    'ReportingCategory',
    'ServiceLineStatus',
    'SourceLocation',
    'SpinalManipulationInfo',
    'StatusCodeInfo',
    'StatusInfo',
    'Subscriber',
    'ToothInfo',
    'ToothStatus',
    'Transaction277',
    'Transaction834',
    'Transaction835',
    'Transaction837',
    'ValidationIssue',
    'Party',
    'PersonWithDemographic',
    'Provider',
    'Tpa',
    'Member',
]