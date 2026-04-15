from __future__ import annotations

from pydantic import Field

from .base import EdiConverterModel, to_camel


class Address(EdiConverterModel):
    line: str | None = None
    line2: str | None = None
    city: str | None = None
    state_code: str | None = None
    zip_code: str | None = None
    country_code: str | None = None
    location_qualifier: str | None = None
    location_identifier: str | None = None
    country_subdivision_code: str | None = None


class Adjudication(EdiConverterModel):
    payer_identifier: str | None = None
    paid_amount: float | None = None
    unit_count: float | None = None
    bundled_or_unbundled_line_number: int | None = None
    procedure: Procedure | None = None
    adjustments: list[Adjustment] = Field(default_factory=list)
    adjudication_or_payment_date: str | None = None
    remaining_patient_liability_amount: float | None = None


class Adjustment(EdiConverterModel):
    group: str | None = None
    reason: Code | None = None
    amount: float | None = None
    quantity: float | None = None


class AmbulanceTransportInfo(EdiConverterModel):
    patient_weight: float | None = None
    reason_code: str | None = None
    reason: str | None = None
    transport_distance: float | None = None
    round_trip_purpose_description: str | None = None
    stretcher_purpose_description: str | None = None


class Amount(EdiConverterModel):
    qualifier_code: str | None = None
    type: str | None = None
    amount: float | None = None


class Attachment(EdiConverterModel):
    report_type_code: str | None = None
    report_transmission_code: str | None = None
    control_number: str | None = None


class AwsInOutKey(EdiConverterModel):
    in_key: str | None = None
    out_key: str | None = None


class AwsRequest(EdiConverterModel):
    in_bucket: str | None = None
    in_key: str | None = None
    out_key: str | None = None
    in_out_keys: list[AwsInOutKey] = Field(default_factory=list)
    out_bucket: str | None = None
    out_format: str | None = None
    csv_schema_name: str | None = None
    warnings_in_output: bool | None = None
    max_warnings: int | None = None
    is_about_only: bool | None = None


class BatchStatus(EdiConverterModel):
    trace_identifier: str | None = None
    status_infos: list[StatusInfo] = Field(default_factory=list)
    accepted_quantity: float | None = None
    accepted_amount: float | None = None
    rejected_quantity: float | None = None
    rejected_amount: float | None = None


class ClaimStatus(EdiConverterModel):
    id: str | None = None
    object_type: str | None = None
    patient: PartyIdName | None = None
    patient_control_number: str | None = None
    status_infos: list[StatusInfo] = Field(default_factory=list)
    payer_claim_control_number: str | None = None
    clearinghouse_trace_number: str | None = None
    bill_type_code: str | None = None
    service_date_from: str | None = None
    service_date_to: str | None = None
    receiver: PartyIdName | None = None
    receiver_batch_status: BatchStatus | None = None
    provider: PartyIdName | None = None
    provider_batch_status: BatchStatus | None = None
    line_statuses: list[ServiceLineStatus] = Field(default_factory=list)
    transaction: Transaction277 | None = None


class Code(EdiConverterModel):
    sub_type: str | None = None
    code: str | None = None
    desc: str | None = None


class CodeAndAmount(EdiConverterModel):
    sub_type: str | None = None
    code: str | None = None
    desc: str | None = None
    amount: float | None = None


class CodeAndDate(EdiConverterModel):
    sub_type: str | None = None
    code: str | None = None
    desc: str | None = None
    occurrence_date: str | None = None


class ConditionsIndicator(EdiConverterModel):
    category_code: str | None = None
    category: str | None = None
    yes_or_no_condition: str | None = None
    condition_codes: list[str] = Field(default_factory=list)


class ContactInfo(EdiConverterModel):
    function_code: str | None = None
    name: str | None = None
    contact_numbers: list[ContactNumber] = Field(default_factory=list)


class ContactNumber(EdiConverterModel):
    type: str | None = None
    number: str | None = None


class ContractInfo(EdiConverterModel):
    contract_type_code: str | None = None
    amount: float | None = None
    percentage: float | None = None
    contract_code: str | None = None
    term_discount_percentage: float | None = None
    version_identifier: str | None = None


class CoordinationOfBenefits(EdiConverterModel):
    payer_responsibility_sequence_code: str | None = None
    group_or_policy_number: str | None = None
    coordination_of_benefits_code: str | None = None
    service_type_codes: list[str] = Field(default_factory=list)
    additional_identifiers: list[Reference] = Field(default_factory=list)
    date_from: str | None = None
    date_to: str | None = None
    insurers: list[Party] = Field(default_factory=list)


class Date(EdiConverterModel):
    qualifier_code: str | None = None
    type: str | None = None
    date: str | None = None
    date_to: str | None = None


class DentClaim(EdiConverterModel):
    id: str | None = None
    object_type: str | None = None
    patient_control_number: str | None = None
    charge_amount: float | None = None
    patient_paid_amount: float | None = None
    facility_code: Code | None = None
    frequency_code: Code | None = None
    service_date_from: str | None = None
    service_date_to: str | None = None
    subscriber: Subscriber | None = None
    patient: Patient | None = None
    other_subscribers: list[OtherSubscriber] = Field(default_factory=list)
    service_lines: list[DentLine] = Field(default_factory=list)
    transaction: Transaction837 | None = None
    provider_signature_indicator: str | None = None
    assignment_participation_code: str | None = None
    assignment_certification_indicator: str | None = None
    release_of_information_code: str | None = None
    related_cause: RelatedCauseInfo | None = None
    special_program_code: str | None = None
    delay_reason_code: str | None = None
    service_authorization_exception_code: str | None = None
    referral_number: str | None = None
    prior_authorization_number: str | None = None
    original_reference_number: str | None = None
    repriced_reference_number: str | None = None
    adjusted_repriced_reference_number: str | None = None
    clearinghouse_trace_number: str | None = None
    medical_record_number: str | None = None
    demonstration_project_identifier: str | None = None
    accident_date: str | None = None
    orthodontic_banding_date: str | None = None
    repricer_received_date: str | None = None
    orthodontic_info: OrthodonticInfo | None = None
    tooth_statuses: list[ToothStatus] = Field(default_factory=list)
    predetermination_of_benefits_identifier: str | None = None
    fixed_format_records: list[str] = Field(default_factory=list)
    claim_note: str | None = None
    billing_provider: Provider | None = None
    pay_to_address: Party | None = None
    pay_to_plan: Party | None = None
    providers: list[Provider] = Field(default_factory=list)
    attachments: list[Attachment] = Field(default_factory=list)
    contract_info: ContractInfo | None = None


class DentLine(EdiConverterModel):
    source_line_id: str | None = None
    oral_cavity_designation_codes: list[str] = Field(default_factory=list)
    prosthesis_crown_or_inlay_code: str | None = None
    predetermination_of_benefits_identifier: str | None = None
    repriced_reference_number: str | None = None
    adjusted_repriced_reference_number: str | None = None
    prior_authorization: str | None = None
    referral_number: str | None = None
    charge_amount: float | None = None
    sales_tax_amount: float | None = None
    service_date_from: str | None = None
    service_date_to: str | None = None
    prior_placement_date: str | None = None
    orthodontic_banding_date: str | None = None
    replacement_date: str | None = None
    treatment_start_date: str | None = None
    treatment_completion_date: str | None = None
    unit_count: float | None = None
    procedure: Procedure | None = None
    attachments: list[Attachment] = Field(default_factory=list)
    contract_info: ContractInfo | None = None
    providers: list[Provider] = Field(default_factory=list)
    adjudications: list[Adjudication] = Field(default_factory=list)
    adjustments: list[Adjustment] = Field(default_factory=list)
    fixed_format_records: list[str] = Field(default_factory=list)
    tooth_infos: list[ToothInfo] = Field(default_factory=list)
    diag_pointers: list[int] = Field(default_factory=list)
    diags: list[Code] = Field(default_factory=list)


class Disability(EdiConverterModel):
    type_code: str | None = None
    diagnosis_code: str | None = None
    date_from: str | None = None
    date_to: str | None = None


class DmeCertification(EdiConverterModel):
    certification_type_code: str | None = None
    duration_unit_type: str | None = None
    duration: float | None = None


class DmeService(EdiConverterModel):
    duration_unit_type: str | None = None
    length_of_medical_necessity: float | None = None
    rental_price: float | None = None
    purchase_price: float | None = None
    billing_frequency_code: str | None = None
    billing_frequency: str | None = None


class EdiGenClaimRequest(EdiConverterModel):
    interchange_control: InterchangeControl | None = None
    functional_group: FunctionalGroup | None = None
    transaction: Transaction837 | None = None
    claims: list[ProfClaim | InstClaim] = Field(default_factory=list)


class ErrorInfo(EdiConverterModel):
    object_type: str | None = None
    message: str | None = None
    file_name: str | None = None


class FileInfo(EdiConverterModel):
    name: str | None = None
    url: str | None = None
    last_modified_date_time: str | None = None


class FormQuestionResponse(EdiConverterModel):
    question_identifier: str | None = None
    yes_or_no_response: str | None = None
    text_response: str | None = None
    date_response: str | None = None
    number_response: float | None = None


class FormResponse(EdiConverterModel):
    form_type_code: str | None = None
    form_identifier: str | None = None
    responses: list[FormQuestionResponse] = Field(default_factory=list)


class FunctionalGroup(EdiConverterModel):
    transaction_type: str | None = None
    functional_identifier_code: str | None = None
    sender_code: str | None = None
    receiver_code: str | None = None
    date: str | None = None
    time: str | None = None
    control_number: int | None = None
    responsible_agency_code: str | None = None
    version: str | None = None


class HealthCoverage(EdiConverterModel):
    maintenance_type_code: str | None = None
    insurance_line_code: str | None = None
    plan_description: str | None = None
    coverage_level_code: str | None = None
    late_enrollment_indicator: str | None = None
    coverage_dates: list[Date] = Field(default_factory=list)
    contract_amounts: list[Amount] = Field(default_factory=list)
    group_or_policy_numbers: list[Reference] = Field(default_factory=list)
    prior_coverage_month_count: str | None = None
    providers: list[Party] = Field(default_factory=list)
    cobs: list[CoordinationOfBenefits] = Field(default_factory=list)


class InpatientAdjudication(EdiConverterModel):
    covered_days_or_visits_count: int | None = None
    pps_operating_outlier_amount: float | None = None
    lifetime_psychiatric_days_count: int | None = None
    drg_amount: float | None = None
    disproportionate_share_amount: float | None = None
    msp_pass_through_amount: float | None = None
    pps_capital_amount: float | None = None
    pps_capital_fsp_drg_amount: float | None = None
    pps_capital_hsp_drg_amount: float | None = None
    pps_capital_dsh_drg_amount: float | None = None
    old_capital_amount: float | None = None
    pps_capital_ime_amount: float | None = None
    pps_operating_hospital_specific_drg_amount: float | None = None
    cost_report_day_count: int | None = None
    pps_operating_federal_specific_drg_amount: float | None = None
    pps_capital_outlier_amount: float | None = None
    indirect_teaching_amount: float | None = None
    non_payable_professional_component_amount: float | None = None
    pps_capital_exception_amount: float | None = None
    remarks: list[Code] = Field(default_factory=list)


class InstClaim(EdiConverterModel):
    id: str | None = None
    object_type: str | None = None
    patient_control_number: str | None = None
    charge_amount: float | None = None
    facility_code: Code | None = None
    frequency_code: Code | None = None
    statement_date_from: str | None = None
    statement_date_to: str | None = None
    service_date_from: str | None = None
    service_date_to: str | None = None
    subscriber: Subscriber | None = None
    patient: Patient | None = None
    other_subscribers: list[OtherSubscriber] = Field(default_factory=list)
    service_lines: list[InstLine] = Field(default_factory=list)
    transaction: Transaction837 | None = None
    assignment_participation_code: str | None = None
    assignment_certification_indicator: str | None = None
    release_of_information_code: str | None = None
    delay_reason_code: str | None = None
    service_authorization_exception_code: str | None = None
    referral_number: str | None = None
    prior_authorization_number: str | None = None
    original_reference_number: str | None = None
    repriced_reference_number: str | None = None
    adjusted_repriced_reference_number: str | None = None
    clearinghouse_trace_number: str | None = None
    accident_state: str | None = None
    medical_record_number: str | None = None
    peer_review_authorization_number: str | None = None
    demonstration_project_identifier: str | None = None
    admission_date_and_hour: str | None = None
    discharge_time: str | None = None
    admission_type_code: str | None = None
    admission_source_code: str | None = None
    patient_status_code: str | None = None
    patient_responsibility_amount: float | None = None
    fixed_format_records: list[str] = Field(default_factory=list)
    claim_note: str | None = None
    billing_note: str | None = None
    billing_provider: Provider | None = None
    pay_to_address: Party | None = None
    pay_to_plan: Party | None = None
    providers: list[Provider] = Field(default_factory=list)
    diags: list[InstDiagnosis] = Field(default_factory=list)
    drg: Code | None = None
    procs: list[CodeAndDate] = Field(default_factory=list)
    occurrence_spans: list[CodeAndDate] = Field(default_factory=list)
    occurrences: list[CodeAndDate] = Field(default_factory=list)
    value_infos: list[CodeAndAmount] = Field(default_factory=list)
    conditions: list[Code] = Field(default_factory=list)
    attachments: list[Attachment] = Field(default_factory=list)
    contract_info: ContractInfo | None = None
    conditions_indicators: list[ConditionsIndicator] = Field(default_factory=list)


class InstClaimCsv(EdiConverterModel):
    id: str | None = None
    transaction_type: str | None = None
    file_name: str | None = None
    transaction_control_number: str | None = None
    transaction_set_purpose_code: str | None = None
    originator_application_transaction_id: str | None = None
    transaction_creation_date_time: str | None = None
    claim_or_encounter_identifier_type: str | None = None
    patient_control_number: str | None = None
    charge_amount: float | None = None
    facility: Code | None = None
    frequency_type_code: str | None = None
    assignment_participation_code: str | None = None
    assignment_certification_indicator: str | None = None
    release_of_information_code: str | None = None
    delay_reason_code: str | None = None
    billing_provider: Provider | None = None
    subscriber: Subscriber | None = None
    patient: Patient | None = None
    statement_date_from: str | None = None
    statement_date_to: str | None = None
    discharge_time: str | None = None
    admission_date_and_hour: str | None = None
    admission_type_code: str | None = None
    admission_source_code: str | None = None
    patient_status_code: str | None = None
    patient_responsibility_amount: float | None = None
    service_authorization_exception_code: str | None = None
    referral_number: str | None = None
    prior_authorization_number: str | None = None
    payer_claim_control_number: str | None = None
    clearinghouse_trace_number: str | None = None
    repriced_reference_number: str | None = None
    adjusted_repriced_reference_number: str | None = None
    accident_state: str | None = None
    medical_record_number: str | None = None
    demonstration_project_identifier: str | None = None
    note: str | None = None
    billing_note: str | None = None
    principal_diag: InstDiagnosis | None = None
    admitting_diag: Code | None = None
    reason_for_visit_diags: list[Code] = Field(default_factory=list)
    external_cause_of_injury_diags: list[Code] = Field(default_factory=list)
    drg: Code | None = None
    other_diags: list[InstDiagnosis] = Field(default_factory=list)
    principal_procedure: CodeAndDate | None = None
    other_procedures: list[CodeAndDate] = Field(default_factory=list)
    occurrences: list[CodeAndDate] = Field(default_factory=list)
    occurrence_spans: list[CodeAndDate] = Field(default_factory=list)
    conditions: list[Code] = Field(default_factory=list)
    value_infos: list[CodeAndAmount] = Field(default_factory=list)
    attachments: list[Attachment] = Field(default_factory=list)
    attending_provider: Party | None = None
    operating_physician: Provider | None = None
    other_operating_physician: Party | None = None
    referring_provider: Party | None = None
    rendering_provider: Provider | None = None
    service_facility: Party | None = None
    other_subscribers: list[OtherSubscriber] = Field(default_factory=list)
    lines: list[InstLineCsv] = Field(default_factory=list)


class InstDiagnosis(EdiConverterModel):
    sub_type: str | None = None
    code: str | None = None
    desc: str | None = None
    present_on_admission_indicator: str | None = None


class InstLine(EdiConverterModel):
    source_line_id: str | None = None
    repriced_reference_number: str | None = None
    adjusted_repriced_reference_number: str | None = None
    charge_amount: float | None = None
    non_covered_amount: float | None = None
    service_tax_amount: float | None = None
    facility_tax_amount: float | None = None
    service_date_from: str | None = None
    service_date_to: str | None = None
    unit_type: str | None = None
    unit_count: float | None = None
    third_party_note: str | None = None
    procedure: Procedure | None = None
    revenue_code: Code | None = None
    attachments: list[Attachment] = Field(default_factory=list)
    contract_info: ContractInfo | None = None
    providers: list[Provider] = Field(default_factory=list)
    adjudications: list[Adjudication] = Field(default_factory=list)
    adjustments: list[Adjustment] = Field(default_factory=list)
    fixed_format_records: list[str] = Field(default_factory=list)


class InstLineCsv(EdiConverterModel):
    control_number: str | None = None
    revenue_code: Code | None = None
    procedure: Procedure | None = None
    charge_amount: float | None = None
    unit_type: str | None = None
    unit_count: float | None = None
    non_covered_amount: float | None = None
    service_date_from: str | None = None
    service_date_to: str | None = None
    repriced_reference_number: str | None = None
    adjusted_repriced_reference_number: str | None = None
    service_tax_amount: float | None = None
    facility_tax_amount: float | None = None
    third_party_note: str | None = None
    drug: Code | None = None
    drug_quantity: float | None = None
    drug_unit_type: str | None = None
    prescription_number: str | None = None
    attachments: list[Attachment] = Field(default_factory=list)
    operating_physician: Provider | None = None
    other_operating_physician: Party | None = None
    rendering_provider: Provider | None = None
    referring_provider: Party | None = None


class InterchangeControl(EdiConverterModel):
    element_separator: str | None = None
    segment_terminator: str | None = None
    authorization_information_qualifier: str | None = None
    authorization_information: str | None = None
    security_information_qualifier: str | None = None
    security_information: str | None = None
    sender_id_qualifier: str | None = None
    sender_id: str | None = None
    receiver_id_qualifier: str | None = None
    receiver_id: str | None = None
    interchange_date: str | None = None
    interchange_time: str | None = None
    repetition_separator: str | None = None
    interchange_control_version_number: str | None = None
    control_number: int | None = None
    acknowledgment_requested: str | None = None
    interchange_usage_indicator: str | None = None
    component_element_separator: str | None = None


class LanguageInfo(EdiConverterModel):
    code_qualifier: str | None = None
    code: str | None = None
    language_description: str | None = None
    language_use_indicator: str | None = None


class Measurement(EdiConverterModel):
    category_code: str | None = None
    qualifier_code: str | None = None
    type: str | None = None
    value: float | None = None


class Member(EdiConverterModel):
    entity_role: str | None = None
    entity_type: str | None = None
    identification_type: str | None = None
    identifier: str | None = None
    tax_id: str | None = None
    last_name_or_org_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    address: Address | None = None
    contacts: list[ContactInfo] = Field(default_factory=list)
    additional_ids: list[Reference] = Field(default_factory=list)
    birth_date: str | None = None
    gender: str | None = None
    marital_status_code: str | None = None
    ethnicity_code: str | None = None
    ethnicity_codes: list[str] = Field(default_factory=list)
    citizenship_code: str | None = None
    employment_class_codes: list[str] = Field(default_factory=list)
    wage_frequency_code: str | None = None
    wage_amount: float | None = None
    work_hours_count: float | None = None
    employer_location_identification_code: str | None = None
    salary_grade_code: str | None = None
    health_related_code: str | None = None
    height: float | None = None
    weight: float | None = None
    language_info: LanguageInfo | None = None
    languages: list[LanguageInfo] = Field(default_factory=list)


class MemberCoverage(EdiConverterModel):
    id: str | None = None
    object_type: str | None = None
    file_name: str | None = None
    file_effective_dates: list[Date] = Field(default_factory=list)
    master_policy_number: str | None = None
    sponsor: PartyIdName | None = None
    insurer: PartyIdName | None = None
    tpas: list[Tpa] = Field(default_factory=list)
    member_indicator: str | None = None
    relationship_code: str | None = None
    maintenance_type_code: str | None = None
    maintenance_reason_code: str | None = None
    benefit_status_code: str | None = None
    medicare_plan_code: str | None = None
    medicare_eligibility_reason_code: str | None = None
    cobra_event_code: str | None = None
    employment_status_code: str | None = None
    student_status_code: str | None = None
    handicap_indicator: str | None = None
    death_date: str | None = None
    confidentiality_code: str | None = None
    birth_sequence_number: int | None = None
    identifier: str | None = None
    group_or_policy_number: str | None = None
    supplemental_identifiers: list[Reference] = Field(default_factory=list)
    status_info_effective_dates: list[Date] = Field(default_factory=list)
    member: Member | None = None
    incorrect_member: Member | None = None
    contract_amounts: list[Amount] = Field(default_factory=list)
    mailing_address: Address | None = None
    employers: list[Party] = Field(default_factory=list)
    schools: list[Party] = Field(default_factory=list)
    custodial_parent: Party | None = None
    responsible_persons: list[Party] = Field(default_factory=list)
    drop_off_location: Party | None = None
    disabilities: list[Disability] = Field(default_factory=list)
    reporting_categories: list[ReportingCategory] = Field(default_factory=list)
    health_coverages: list[HealthCoverage] = Field(default_factory=list)
    transaction: Transaction834 | None = None


class MemberCoverageCsv(EdiConverterModel):
    id: str | None = None
    file_name: str | None = None
    transaction_control_number: str | None = None
    transaction_set_purpose_code: str | None = None
    originator_application_transaction_id: str | None = None
    transaction_creation_date_time: str | None = None
    transaction_action_code: str | None = None
    file_effective_dates: list[Date] = Field(default_factory=list)
    master_policy_number: str | None = None
    sponsor: PartyIdName | None = None
    insurer: PartyIdName | None = None
    tpas: list[Tpa] = Field(default_factory=list)
    member_indicator: str | None = None
    relationship_code: str | None = None
    maintenance_type_code: str | None = None
    maintenance_reason_code: str | None = None
    benefit_status_code: str | None = None
    medicare_plan_code: str | None = None
    medicare_eligibility_reason_code: str | None = None
    cobra_event_code: str | None = None
    employment_status_code: str | None = None
    student_status_code: str | None = None
    handicap_indicator: str | None = None
    death_date: str | None = None
    confidentiality_code: str | None = None
    birth_sequence_number: int | None = None
    identifier: str | None = None
    group_or_policy_number: str | None = None
    supplemental_identifiers: list[Reference] = Field(default_factory=list)
    status_info_effective_dates: list[Date] = Field(default_factory=list)
    member: Member | None = None
    incorrect_member: Member | None = None
    contract_amounts: list[Amount] = Field(default_factory=list)
    mailing_address: Address | None = None
    employers: list[Party] = Field(default_factory=list)
    schools: list[Party] = Field(default_factory=list)
    custodial_parent: Party | None = None
    responsible_persons: list[Party] = Field(default_factory=list)
    drop_off_location: Party | None = None
    disabilities: list[Disability] = Field(default_factory=list)
    reporting_categories: list[ReportingCategory] = Field(default_factory=list)
    health_coverages: list[HealthCoverage] = Field(default_factory=list)
    transaction: Transaction834 | None = None


class OrthodonticInfo(EdiConverterModel):
    treatment_months_count: float | None = None
    treatment_months_remaining_count: float | None = None
    treatment_indicator: str | None = None


class OtherSubscriber(EdiConverterModel):
    payer_responsibility_sequence: str | None = None
    relationship_type: str | None = None
    group_or_policy_number: str | None = None
    group_name: str | None = None
    coordination_of_benefits_code: str | None = None
    claim_filing_indicator_code: str | None = None
    insurance_plan_type: str | None = None
    person: PersonWithDemographic | None = None
    adjustments: list[Adjustment] = Field(default_factory=list)
    payer_paid_amount: float | None = None
    non_covered_amount: float | None = None
    remaining_patient_liability_amount: float | None = None
    outpatient_adjudication: OutpatientAdjudication | None = None
    payer_prior_authorization_number: str | None = None
    payer_referral_number: str | None = None
    payer_claim_control_number: str | None = None
    payer: Party | None = None
    patient: Party | None = None
    providers: list[Party] = Field(default_factory=list)


class OutpatientAdjudication(EdiConverterModel):
    reimbursement_rate: float | None = None
    hcpcs_payable_amount: float | None = None
    esrd_payment_amount: float | None = None
    non_payable_professional_component_amount: float | None = None
    remarks: list[Code] = Field(default_factory=list)


class Party(EdiConverterModel):
    entity_role: str | None = None
    entity_type: str | None = None
    identification_type: str | None = None
    identifier: str | None = None
    tax_id: str | None = None
    last_name_or_org_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    address: Address | None = None
    contacts: list[ContactInfo] = Field(default_factory=list)
    additional_ids: list[Reference] = Field(default_factory=list)


class PartyIdName(EdiConverterModel):
    entity_role: str | None = None
    entity_type: str | None = None
    identification_type: str | None = None
    identifier: str | None = None
    tax_id: str | None = None
    last_name_or_org_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None


class Patient(EdiConverterModel):
    relationship_type: str | None = None
    person: PersonWithDemographic | None = None
    death_date: str | None = None
    weight: float | None = None
    pregnancy_indicator: str | None = None


class PatientSubscriber835(EdiConverterModel):
    person: Party | None = None


class Payment(EdiConverterModel):
    id: str | None = None
    object_type: str | None = None
    patient_control_number: str | None = None
    charge_amount: float | None = None
    payment_amount: float | None = None
    facility_code: Code | None = None
    frequency_code: Code | None = None
    statement_date_from: str | None = None
    statement_date_to: str | None = None
    service_date_from: str | None = None
    service_date_to: str | None = None
    subscriber: PatientSubscriber835 | None = None
    patient: PatientSubscriber835 | None = None
    other_subscribers: list[PatientSubscriber835] = Field(default_factory=list)
    service_lines: list[PaymentLine] = Field(default_factory=list)
    transaction: Transaction835 | None = None
    claim_status_code: str | None = None
    claim_status: str | None = None
    patient_responsibility_amount: float | None = None
    claim_filing_indicator_code: str | None = None
    insurance_plan_type: str | None = None
    payer_control_number: str | None = None
    drg: Code | None = None
    drg_weight: float | None = None
    discharge_fraction: float | None = None
    other_claim_related_ids: list[Reference] = Field(default_factory=list)
    supplemental_amounts: list[Amount] = Field(default_factory=list)
    supplemental_quantities: list[Quantity] = Field(default_factory=list)
    payer: Party | None = None
    payee: Party | None = None
    outpatient_adjudication: OutpatientAdjudication | None = None
    inpatient_adjudication: InpatientAdjudication | None = None
    adjustments: list[Adjustment] = Field(default_factory=list)
    coverage_expiration_date: str | None = None
    claim_received_date: str | None = None
    service_provider: PartyIdName | None = None
    crossover_carrier: PartyIdName | None = None
    corrected_payer: PartyIdName | None = None
    corrected_insured: PartyIdName | None = None
    claim_contacts: list[ContactInfo] = Field(default_factory=list)


class PaymentCsv(EdiConverterModel):
    id: str | None = None
    transaction_type: str | None = None
    file_name: str | None = None
    transaction_control_number: str | None = None
    patient_control_number: str | None = None
    claim_status: str | None = None
    charge_amount: float | None = None
    payment_amount: float | None = None
    patient_responsibility_amount: float | None = None
    claim_filing_indicator_code: str | None = None
    payer_control_number: str | None = None
    facility: Code | None = None
    frequency_type_code: str | None = None
    drg_code: str | None = None
    drg_weight: float | None = None
    discharge_fraction: float | None = None
    total_payment_amount: float | None = None
    credit_or_debit_flag_code: str | None = None
    payment_method_type: str | None = None
    receiver_account_number: str | None = None
    payment_date: str | None = None
    check_or_eft_trace_number: str | None = None
    payer_ein: str | None = None
    production_date: str | None = None
    total_adj_amount: float | None = None
    adjs: list[Adjustment] = Field(default_factory=list)
    payer: Party | None = None
    payee: Party | None = None
    patient: PartyIdName | None = None
    subscriber: PartyIdName | None = None
    corrected_patient: PartyIdName | None = None
    service_provider: PartyIdName | None = None
    crossover_carrier: PartyIdName | None = None
    corrected_payer: PartyIdName | None = None
    other_subscriber: PartyIdName | None = None
    other_claim_related_ids: list[Reference] = Field(default_factory=list)
    service_date_from: str | None = None
    service_date_to: str | None = None
    statement_date_from: str | None = None
    statement_date_to: str | None = None
    coverage_expiration_date: str | None = None
    claim_received_date: str | None = None
    coverage_amount: float | None = None
    supplemental_amts: list[Amount] = Field(default_factory=list)
    supplemental_qties: list[Quantity] = Field(default_factory=list)
    lines: list[PaymentLineCsv] = Field(default_factory=list)


class PaymentLine(EdiConverterModel):
    source_line_id: str | None = None
    repriced_reference_number: str | None = None
    adjusted_repriced_reference_number: str | None = None
    healthcare_policy_id: str | None = None
    charge_amount: float | None = None
    paid_amount: float | None = None
    supplemental_amounts: list[Amount] = Field(default_factory=list)
    supplemental_quantities: list[Quantity] = Field(default_factory=list)
    service_date_from: str | None = None
    service_date_to: str | None = None
    unit_count: float | None = None
    original_unit_count: float | None = None
    drug: Code | None = None
    procedure: Procedure | None = None
    revenue_code: Code | None = None
    original_procedure: Procedure | None = None
    original_revenue_code: Code | None = None
    original_drug: Code | None = None
    providers: list[Provider] = Field(default_factory=list)
    adjustments: list[Adjustment] = Field(default_factory=list)
    remark_codes: list[str] = Field(default_factory=list)
    remarks: list[Code] = Field(default_factory=list)
    service_ids: list[Reference] = Field(default_factory=list)
    rendering_provider_ids: list[Reference] = Field(default_factory=list)


class PaymentLineCsv(EdiConverterModel):
    control_number: str | None = None
    procedure: Procedure | None = None
    revenue_code: str | None = None
    drug_code: str | None = None
    charge_amount: float | None = None
    paid_amount: float | None = None
    unit_count: float | None = None
    original_procedure: Procedure | None = None
    original_revenue_code: str | None = None
    original_drug_code: str | None = None
    original_unit_count: float | None = None
    service_date_from: str | None = None
    service_date_to: str | None = None
    total_adj_amount: float | None = None
    adjs: list[Adjustment] = Field(default_factory=list)
    service_ids: list[Reference] = Field(default_factory=list)
    healthcare_policy_id: str | None = None
    rendering_provider_ids: list[Reference] = Field(default_factory=list)
    allowed_amount: float | None = None
    supplemental_amts: list[Amount] = Field(default_factory=list)
    supplemental_qties: list[Quantity] = Field(default_factory=list)
    remark_codes: list[str] = Field(default_factory=list)


class PersonWithDemographic(EdiConverterModel):
    entity_role: str | None = None
    entity_type: str | None = None
    identification_type: str | None = None
    identifier: str | None = None
    tax_id: str | None = None
    last_name_or_org_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    address: Address | None = None
    contacts: list[ContactInfo] = Field(default_factory=list)
    additional_ids: list[Reference] = Field(default_factory=list)
    birth_date: str | None = None
    gender: str | None = None


class Procedure(EdiConverterModel):
    sub_type: str | None = None
    code: str | None = None
    desc: str | None = None
    modifiers: list[Code] = Field(default_factory=list)


class ProfClaim(EdiConverterModel):
    id: str | None = None
    object_type: str | None = None
    patient_control_number: str | None = None
    ''' Patient Control Number '''
    # Patient charge amount
    charge_amount: float | None = None
    patient_paid_amount: float | None = None
    facility_code: Code | None = None
    frequency_code: Code | None = None
    service_date_from: str | None = None
    service_date_to: str | None = None
    subscriber: Subscriber | None = None
    patient: Patient | None = None
    other_subscribers: list[OtherSubscriber] = Field(default_factory=list)
    service_lines: list[ProfLine] = Field(default_factory=list)
    transaction: Transaction837 | None = None
    provider_signature_indicator: str | None = None
    assignment_participation_code: str | None = None
    assignment_certification_indicator: str | None = None
    release_of_information_code: str | None = None
    patient_signature_source_code: str | None = None
    related_cause: RelatedCauseInfo | None = None
    special_program_code: str | None = None
    delay_reason_code: str | None = None
    service_authorization_exception_code: str | None = None
    referral_number: str | None = None
    prior_authorization_number: str | None = None
    original_reference_number: str | None = None
    repriced_reference_number: str | None = None
    adjusted_repriced_reference_number: str | None = None
    clearinghouse_trace_number: str | None = None
    medical_record_number: str | None = None
    demonstration_project_identifier: str | None = None
    onset_of_current_illness_or_injury_date: str | None = None
    initial_treatment_date: str | None = None
    last_seen_date: str | None = None
    acute_manifestation_date: str | None = None
    accident_date: str | None = None
    last_menstrual_period_date: str | None = None
    last_x_ray_date: str | None = None
    prescription_date: str | None = None
    disability_date_from: str | None = None
    disability_date_to: str | None = None
    last_worked_date: str | None = None
    authorized_return_to_work_date: str | None = None
    admission_date: str | None = None
    discharge_date: str | None = None
    assumed_care_date: str | None = None
    relinquished_care_date: str | None = None
    property_casualty_first_contact_date: str | None = None
    repricer_received_date: str | None = None
    fixed_format_records: list[str] = Field(default_factory=list)
    claim_note: str | None = None
    billing_provider: Provider | None = None
    pay_to_address: Party | None = None
    pay_to_plan: Party | None = None
    providers: list[Provider] = Field(default_factory=list)
    diags: list[Code] = Field(default_factory=list)
    procs: list[Code] = Field(default_factory=list)
    conditions: list[Code] = Field(default_factory=list)
    attachments: list[Attachment] = Field(default_factory=list)
    contract_info: ContractInfo | None = None
    ambulance_transport_info: AmbulanceTransportInfo | None = None
    spinal_manipulation_info: SpinalManipulationInfo | None = None
    conditions_indicators: list[ConditionsIndicator] = Field(default_factory=list)


class ProfClaimCsv(EdiConverterModel):
    id: str | None = None
    transaction_type: str | None = None
    file_name: str | None = None
    transaction_control_number: str | None = None
    transaction_set_purpose_code: str | None = None
    originator_application_transaction_id: str | None = None
    transaction_creation_date_time: str | None = None
    claim_or_encounter_identifier_type: str | None = None
    patient_control_number: str | None = None
    charge_amount: float | None = None
    place_of_service: str | None = None
    facility: Code | None = None
    frequency_type_code: str | None = None
    provider_signature_indicator: str | None = None
    assignment_participation_code: str | None = None
    assignment_certification_indicator: str | None = None
    release_of_information_code: str | None = None
    delay_reason_code: str | None = None
    billing_provider: Provider | None = None
    subscriber: Subscriber | None = None
    patient: Patient | None = None
    service_date_from: str | None = None
    service_date_to: str | None = None
    onset_of_current_illness_or_injury_date: str | None = None
    initial_treatment_date: str | None = None
    last_seen_date: str | None = None
    acute_manifestation_date: str | None = None
    accident_date: str | None = None
    last_menstrual_period_date: str | None = None
    last_x_ray_date: str | None = None
    prescription_date: str | None = None
    assumed_care_date: str | None = None
    relinquished_care_date: str | None = None
    admission_date: str | None = None
    discharge_date: str | None = None
    patient_paid_amount: float | None = None
    service_authorization_exception_code: str | None = None
    referral_number: str | None = None
    prior_authorization_number: str | None = None
    payer_claim_control_number: str | None = None
    clearinghouse_trace_number: str | None = None
    repriced_reference_number: str | None = None
    adjusted_repriced_reference_number: str | None = None
    medical_record_number: str | None = None
    demonstration_project_identifier: str | None = None
    note: str | None = None
    diags: list[Code] = Field(default_factory=list)
    anesthesia_procedure: Code | None = None
    conditions: list[Code] = Field(default_factory=list)
    attachments: list[Attachment] = Field(default_factory=list)
    referring_provider: Party | None = None
    rendering_provider: Provider | None = None
    service_facility: Party | None = None
    supervising_provider: Party | None = None
    ambulance_pick_up: Party | None = None
    ambulance_drop_off: Party | None = None
    other_subscribers: list[OtherSubscriber] = Field(default_factory=list)
    lines: list[ProfLineCsv] = Field(default_factory=list)


class ProfLine(EdiConverterModel):
    source_line_id: str | None = None
    place_of_service_code: str | None = None
    emergency_indicator: str | None = None
    epsdt_indicator: str | None = None
    family_planning_indicator: str | None = None
    copay_status_code: str | None = None
    repriced_reference_number: str | None = None
    adjusted_repriced_reference_number: str | None = None
    prior_authorization: str | None = None
    referral_number: str | None = None
    charge_amount: float | None = None
    sales_tax_amount: float | None = None
    purchased_service_provider_identifier: str | None = None
    purchased_service_charge_amount: float | None = None
    service_date_from: str | None = None
    service_date_to: str | None = None
    prescription_date: str | None = None
    last_certification_date: str | None = None
    certification_revision_date: str | None = None
    begin_therapy_date: str | None = None
    last_seen_date: str | None = None
    test_performed_date: str | None = None
    last_x_ray_date: str | None = None
    initial_treatment_date: str | None = None
    unit_type: str | None = None
    unit_count: float | None = None
    ambulance_patient_count: int | None = None
    drug: Code | None = None
    drug_quantity: float | None = None
    drug_unit_type: str | None = None
    prescription_number: str | None = None
    line_note: str | None = None
    third_party_note: str | None = None
    procedure: Procedure | None = None
    dme_service: DmeService | None = None
    attachments: list[Attachment] = Field(default_factory=list)
    contract_info: ContractInfo | None = None
    ambulance_transport_info: AmbulanceTransportInfo | None = None
    dme_certification: DmeCertification | None = None
    conditions_indicators: list[ConditionsIndicator] = Field(default_factory=list)
    measurements: list[Measurement] = Field(default_factory=list)
    providers: list[Provider] = Field(default_factory=list)
    adjudications: list[Adjudication] = Field(default_factory=list)
    adjustments: list[Adjustment] = Field(default_factory=list)
    fixed_format_records: list[str] = Field(default_factory=list)
    forms: list[FormResponse] = Field(default_factory=list)
    diag_pointers: list[int] = Field(default_factory=list)
    diags: list[Code] = Field(default_factory=list)


class ProfLineCsv(EdiConverterModel):
    control_number: str | None = None
    procedure: Procedure | None = None
    charge_amount: float | None = None
    unit_type: str | None = None
    unit_count: float | None = None
    place_of_service: str | None = None
    place_of_service_code: str | None = None
    diag_pointers: list[int] = Field(default_factory=list)
    emergency_indicator: str | None = None
    epsdt_indicator: str | None = None
    family_planning_indicator: str | None = None
    copay_status_code: str | None = None
    service_date_from: str | None = None
    service_date_to: str | None = None
    prescription_date: str | None = None
    begin_therapy_date: str | None = None
    last_seen_date: str | None = None
    test_performed_date: str | None = None
    last_x_ray_date: str | None = None
    initial_treatment_date: str | None = None
    prior_authorization: str | None = None
    referral_number: str | None = None
    repriced_reference_number: str | None = None
    adjusted_repriced_reference_number: str | None = None
    note: str | None = None
    third_party_note: str | None = None
    drug: Code | None = None
    drug_quantity: float | None = None
    drug_unit_type: str | None = None
    prescription_number: str | None = None
    attachments: list[Attachment] = Field(default_factory=list)
    rendering_provider: Provider | None = None
    purchased_service_provider: Party | None = None
    service_facility: Party | None = None
    supervising_provider: Party | None = None
    referring_provider: Party | None = None
    ordering_provider: Party | None = None
    ambulance_pick_up: Party | None = None
    ambulance_drop_off: Party | None = None


class Provider(EdiConverterModel):
    entity_role: str | None = None
    entity_type: str | None = None
    identification_type: str | None = None
    identifier: str | None = None
    tax_id: str | None = None
    last_name_or_org_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    address: Address | None = None
    contacts: list[ContactInfo] = Field(default_factory=list)
    additional_ids: list[Reference] = Field(default_factory=list)
    provider_taxonomy: Code | None = None


class ProviderAdjustment(EdiConverterModel):
    id: str | None = None
    object_type: str | None = None
    provider_identifier: str | None = None
    fiscal_period_date: str | None = None
    adjustments: list[ProviderAdjustmentReasonAmount] = Field(default_factory=list)
    payer: Party | None = None
    payee: Party | None = None
    transaction: Transaction835 | None = None


class ProviderAdjustmentReasonAmount(EdiConverterModel):
    reason: Code | None = None
    reference_identification: str | None = None
    amount: float | None = None


class ProviderStatus(EdiConverterModel):
    id: str | None = None
    object_type: str | None = None
    batch_status: BatchStatus | None = None
    transaction: Transaction277 | None = None
    receiver: PartyIdName | None = None
    receiver_batch_status: BatchStatus | None = None


class Quantity(EdiConverterModel):
    qualifier_code: str | None = None
    type: str | None = None
    quantity: float | None = None


class ReceiverStatus(EdiConverterModel):
    id: str | None = None
    object_type: str | None = None
    batch_status: BatchStatus | None = None
    transaction: Transaction277 | None = None
    receiver: PartyIdName | None = None


class Reference(EdiConverterModel):
    qualifier_code: str | None = None
    type: str | None = None
    identification: str | None = None


class RelatedCauseInfo(EdiConverterModel):
    related_cause_code: str | None = None
    related_cause_code2: str | None = None
    state_code: str | None = None
    country_code: str | None = None


class ReportingCategory(EdiConverterModel):
    name: str | None = None
    identifier_qualifier_code: str | None = None
    identifier_type: str | None = None
    identifier: str | None = None
    date: str | None = None
    date_to: str | None = None


class ServiceLineStatus(EdiConverterModel):
    control_number: str | None = None
    charge_amount: float | None = None
    unit_count: float | None = None
    procedure: Procedure | None = None
    revenue_code: Code | None = None
    prescription_number: str | None = None
    service_date_from: str | None = None
    service_date_to: str | None = None
    status_infos: list[StatusInfo] = Field(default_factory=list)


class SourceLocation(EdiConverterModel):
    file_name: str | None = None
    line_number: int | None = None
    segment_number: int | None = None


class SpinalManipulationInfo(EdiConverterModel):
    condition_code: str | None = None
    description: str | None = None
    additional_description: str | None = None


class StatusCodeInfo(EdiConverterModel):
    category_code: str | None = None
    status_code: str | None = None
    entity_code: str | None = None


class StatusInfo(EdiConverterModel):
    effective_date: str | None = None
    action_code: str | None = None
    action_type: str | None = None
    charge_amount: float | None = None
    status_code_infos: list[StatusCodeInfo] = Field(default_factory=list)
    message: str | None = None


class Subscriber(EdiConverterModel):
    payer_responsibility_sequence: str | None = None
    relationship_type: str | None = None
    group_or_policy_number: str | None = None
    group_name: str | None = None
    claim_filing_indicator_code: str | None = None
    insurance_plan_type: str | None = None
    person: PersonWithDemographic | None = None
    death_date: str | None = None
    weight: float | None = None
    pregnancy_indicator: str | None = None
    property_casualty_claim_number: str | None = None
    payer: Party | None = None


class ToothInfo(EdiConverterModel):
    code: str | None = None
    surface_codes: list[str] = Field(default_factory=list)


class ToothStatus(EdiConverterModel):
    tooth_number: str | None = None
    status_code: str | None = None


class Tpa(EdiConverterModel):
    entity_role: str | None = None
    entity_type: str | None = None
    identification_type: str | None = None
    identifier: str | None = None
    tax_id: str | None = None
    last_name_or_org_name: str | None = None
    first_name: str | None = None
    middle_name: str | None = None
    address: Address | None = None
    contacts: list[ContactInfo] = Field(default_factory=list)
    additional_ids: list[Reference] = Field(default_factory=list)
    account_number: str | None = None
    account_number2: str | None = None


class Transaction277(EdiConverterModel):
    control_number: str | None = None
    transaction_type: str | None = None
    hierarchical_structure_code: str | None = None
    purpose_code: str | None = None
    originator_application_transaction_id: str | None = None
    creation_date: str | None = None
    creation_time: str | None = None
    trace_identifier: str | None = None
    transaction_set_identifier_code: str | None = None
    implementation_convention_reference: str | None = None
    receipt_date: str | None = None
    process_date: str | None = None
    file_info: FileInfo | None = None
    sender: PartyIdName | None = None


class Transaction834(EdiConverterModel):
    control_number: str | None = None
    transaction_type: str | None = None
    purpose_code: str | None = None
    originator_application_transaction_id: str | None = None
    creation_date: str | None = None
    creation_time: str | None = None
    original_transaction_set_reference_number: str | None = None
    action_code: str | None = None
    transaction_set_identifier_code: str | None = None
    implementation_convention_reference: str | None = None
    file_effective_dates: list[Date] = Field(default_factory=list)
    control_totals: list[Quantity] = Field(default_factory=list)
    file_info: FileInfo | None = None


class Transaction835(EdiConverterModel):
    control_number: str | None = None
    transaction_type: str | None = None
    production_date: str | None = None
    transaction_handling_type: str | None = None
    total_payment_amount: float | None = None
    credit_or_debit_flag_code: str | None = None
    payment_method_type: str | None = None
    payment_format_code: str | None = None
    sender_bank_routing_number: str | None = None
    sender_account_number: str | None = None
    originating_company_id: str | None = None
    originating_company_supplemental_code: str | None = None
    receiver_bank_routing_number: str | None = None
    receiver_account_number: str | None = None
    payment_date: str | None = None
    check_or_eft_trace_number: str | None = None
    payer_identifier: str | None = None
    receiver_identifier: str | None = None
    transaction_set_identifier_code: str | None = None
    implementation_convention_reference: str | None = None
    file_info: FileInfo | None = None


class Transaction837(EdiConverterModel):
    control_number: str | None = None
    transaction_type: str | None = None
    hierarchical_structure_code: str | None = None
    purpose_code: str | None = None
    originator_application_transaction_id: str | None = None
    creation_date: str | None = None
    creation_time: str | None = None
    claim_or_encounter_identifier_type: str | None = None
    transaction_set_identifier_code: str | None = None
    implementation_convention_reference: str | None = None
    file_info: FileInfo | None = None
    sender: Party | None = None
    receiver: PartyIdName | None = None


class ValidationIssue(EdiConverterModel):
    issue_type: str | None = None
    json_path: str | None = None
    field_name: str | None = None
    source_location: SourceLocation | None = None
    loop: str | None = None
    segment: str | None = None
    element: str | None = None
    edi_code: str | None = None
    max_number_of_items: int | None = None
    actual_number_of_items: int | None = None
    length: int | None = None
    actual_length: int | None = None
    data_type: str | None = None
    actual_data_type: str | None = None
    value: str | None = None
    edi_string: str | None = None
    message: str | None = None
    allowed_values: list[str] = Field(default_factory=list)


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
Member.model_rebuild()
MemberCoverage.model_rebuild()
MemberCoverageCsv.model_rebuild()
OrthodonticInfo.model_rebuild()
OtherSubscriber.model_rebuild()
OutpatientAdjudication.model_rebuild()
Party.model_rebuild()
PartyIdName.model_rebuild()
Patient.model_rebuild()
PatientSubscriber835.model_rebuild()
Payment.model_rebuild()
PaymentCsv.model_rebuild()
PaymentLine.model_rebuild()
PaymentLineCsv.model_rebuild()
PersonWithDemographic.model_rebuild()
Procedure.model_rebuild()
ProfClaim.model_rebuild()
ProfClaimCsv.model_rebuild()
ProfLine.model_rebuild()
ProfLineCsv.model_rebuild()
Provider.model_rebuild()
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
Tpa.model_rebuild()
Transaction277.model_rebuild()
Transaction834.model_rebuild()
Transaction835.model_rebuild()
Transaction837.model_rebuild()
ValidationIssue.model_rebuild()

__all__ = [
    "Address",
    "Adjudication",
    "Adjustment",
    "AmbulanceTransportInfo",
    "Amount",
    "Attachment",
    "AwsInOutKey",
    "AwsRequest",
    "BatchStatus",
    "ClaimStatus",
    "Code",
    "CodeAndAmount",
    "CodeAndDate",
    "ConditionsIndicator",
    "ContactInfo",
    "ContactNumber",
    "ContractInfo",
    "CoordinationOfBenefits",
    "Date",
    "DentClaim",
    "DentLine",
    "Disability",
    "DmeCertification",
    "DmeService",
    "EdiGenClaimRequest",
    "ErrorInfo",
    "FileInfo",
    "FormQuestionResponse",
    "FormResponse",
    "FunctionalGroup",
    "HealthCoverage",
    "InpatientAdjudication",
    "InstClaim",
    "InstClaimCsv",
    "InstDiagnosis",
    "InstLine",
    "InstLineCsv",
    "InterchangeControl",
    "LanguageInfo",
    "Measurement",
    "Member",
    "MemberCoverage",
    "MemberCoverageCsv",
    "OrthodonticInfo",
    "OtherSubscriber",
    "OutpatientAdjudication",
    "Party",
    "PartyIdName",
    "Patient",
    "PatientSubscriber835",
    "Payment",
    "PaymentCsv",
    "PaymentLine",
    "PaymentLineCsv",
    "PersonWithDemographic",
    "Procedure",
    "ProfClaim",
    "ProfClaimCsv",
    "ProfLine",
    "ProfLineCsv",
    "Provider",
    "ProviderAdjustment",
    "ProviderAdjustmentReasonAmount",
    "ProviderStatus",
    "Quantity",
    "ReceiverStatus",
    "Reference",
    "RelatedCauseInfo",
    "ReportingCategory",
    "ServiceLineStatus",
    "SourceLocation",
    "SpinalManipulationInfo",
    "StatusCodeInfo",
    "StatusInfo",
    "Subscriber",
    "ToothInfo",
    "ToothStatus",
    "Tpa",
    "Transaction277",
    "Transaction834",
    "Transaction835",
    "Transaction837",
    "ValidationIssue",
    "EdiConverterModel",
    "to_camel",
]