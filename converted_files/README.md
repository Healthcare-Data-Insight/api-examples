# Converted EDI Files

This directory contains converted examples for the EDI source files in [`../edi_files`](../edi_files/). Each transaction set section links the original EDI input to the generated JSON output. When tabular conversion examples are available, the `CSV Format` column links the CSV outputs and the matching Excel workbook. Some CSV conversions produce multiple files, such as claim-level and line-level extracts, so those links are grouped in the same table cell.

Rows labeled `All files` point to batch conversion output files with the `-all-files` suffix. Batch JSON output may include both regular JSON and newline-delimited JSON (`.jsonl`) variants. Validation examples are listed in their own subsection, with links to both the full JSON conversion and the validation-only JSON output.

## 271

| EDI File | JSON Format |
| --- | --- |
| [X279-error-response-from-payer-to-clinic-not-eligible-for-inquiries-with-payer.edi](../edi_files/271/X279-error-response-from-payer-to-clinic-not-eligible-for-inquiries-with-payer.edi) | [X279-error-response-from-payer-to-clinic-not-eligible-for-inquiries-with-payer.json](271/X279-error-response-from-payer-to-clinic-not-eligible-for-inquiries-with-payer.json) |
| [X279-generic-request-by-clinic-for-patient-(subscriber)-eligibility.edi](../edi_files/271/X279-generic-request-by-clinic-for-patient-%28subscriber%29-eligibility.edi) | [X279-generic-request-by-clinic-for-patient-(subscriber)-eligibility.json](271/X279-generic-request-by-clinic-for-patient-%28subscriber%29-eligibility.json) |
| [X279-generic-request-by-physician-for-patient-(dependent)-eligibility.edi](../edi_files/271/X279-generic-request-by-physician-for-patient-%28dependent%29-eligibility.edi) | [X279-generic-request-by-physician-for-patient-(dependent)-eligibility.json](271/X279-generic-request-by-physician-for-patient-%28dependent%29-eligibility.json) |
| [X279-response-to-generic-request-by-clinic-for-patient-(subscriber)-eligibility.edi](../edi_files/271/X279-response-to-generic-request-by-clinic-for-patient-%28subscriber%29-eligibility.edi) | [X279-response-to-generic-request-by-clinic-for-patient-(subscriber)-eligibility.json](271/X279-response-to-generic-request-by-clinic-for-patient-%28subscriber%29-eligibility.json) |
| [X279-response-to-generic-request-by-physician-for-patient-(dependent)-eligibility.edi](../edi_files/271/X279-response-to-generic-request-by-physician-for-patient-%28dependent%29-eligibility.edi) | [X279-response-to-generic-request-by-physician-for-patient-(dependent)-eligibility.json](271/X279-response-to-generic-request-by-physician-for-patient-%28dependent%29-eligibility.json) |

## 274

| EDI File | JSON Format |
| --- | --- |
| [274.edi](../edi_files/274/274.edi) | [274.json](274/274.json) |

## 277

| EDI File | JSON Format |
| --- | --- |
| [All files](../edi_files/277/) | [277CA-all-files.jsonl](277/277CA-all-files.jsonl) |
| [277CA-all-fields.edi](../edi_files/277/277CA-all-fields.edi) | [277CA-all-fields.json](277/277CA-all-fields.json) |
| [277CA-receiver-rejected.edi](../edi_files/277/277CA-receiver-rejected.edi) | [277CA-receiver-rejected.json](277/277CA-receiver-rejected.json) |
| [X212-277-claim-ncpdp-response.edi](../edi_files/277/X212-277-claim-ncpdp-response.edi) | [X212-277-claim-ncpdp-response.json](277/X212-277-claim-ncpdp-response.json) |
| [X212-277-claim-response.edi](../edi_files/277/X212-277-claim-response.edi) | [X212-277-claim-response.json](277/X212-277-claim-response.json) |
| [X212-277-info-receiver-response.edi](../edi_files/277/X212-277-info-receiver-response.edi) | [X212-277-info-receiver-response.json](277/X212-277-info-receiver-response.json) |
| [X212-277-provider-response.edi](../edi_files/277/X212-277-provider-response.edi) | [X212-277-provider-response.json](277/X212-277-provider-response.json) |
| [X214-payer-response.edi](../edi_files/277/X214-payer-response.edi) | [X214-payer-response.json](277/X214-payer-response.json) |
| [X214-payer-response-multiple-responders.edi](../edi_files/277/X214-payer-response-multiple-responders.edi) | [X214-payer-response-multiple-responders.json](277/X214-payer-response-multiple-responders.json) |

## 834

| EDI File | JSON Format | CSV Format |
| --- | --- | --- |
| [All files](../edi_files/834/) | [834-all-files.jsonl](834/834-all-files.jsonl) | [834-all-files.csv](834/834-all-files.csv)<br>[834-all-files.xlsx](834/834-all-files.xlsx) |
| [834-all-fields.edi](../edi_files/834/834-all-fields.edi) | [834-all-fields.json](834/834-all-fields.json) | [834-all-fields.csv](834/834-all-fields.csv)<br>[834-all-fields.xlsx](834/834-all-fields.xlsx) |
| [X220-add-dependent-(full-time-student)-to-existing-enrollment.edi](../edi_files/834/X220-add-dependent-%28full-time-student%29-to-existing-enrollment.edi) | [X220-add-dependent-(full-time-student)-to-existing-enrollment.json](834/X220-add-dependent-%28full-time-student%29-to-existing-enrollment.json) | [X220-add-dependent-(full-time-student)-to-existing-enrollment.csv](834/X220-add-dependent-%28full-time-student%29-to-existing-enrollment.csv)<br>[X220-add-dependent-(full-time-student)-to-existing-enrollment.xlsx](834/X220-add-dependent-%28full-time-student%29-to-existing-enrollment.xlsx) |
| [X220-add-subscriber-coverage.edi](../edi_files/834/X220-add-subscriber-coverage.edi) | [X220-add-subscriber-coverage.json](834/X220-add-subscriber-coverage.json) | [X220-add-subscriber-coverage.csv](834/X220-add-subscriber-coverage.csv)<br>[X220-add-subscriber-coverage.xlsx](834/X220-add-subscriber-coverage.xlsx) |
| [X220-cancel-a-dependent.edi](../edi_files/834/X220-cancel-a-dependent.edi) | [X220-cancel-a-dependent.json](834/X220-cancel-a-dependent.json) | [X220-cancel-a-dependent.csv](834/X220-cancel-a-dependent.csv)<br>[X220-cancel-a-dependent.xlsx](834/X220-cancel-a-dependent.xlsx) |
| [X220-change-subscriber-information.edi](../edi_files/834/X220-change-subscriber-information.edi) | [X220-change-subscriber-information.json](834/X220-change-subscriber-information.json) | [X220-change-subscriber-information.csv](834/X220-change-subscriber-information.csv)<br>[X220-change-subscriber-information.xlsx](834/X220-change-subscriber-information.xlsx) |
| [X220-enroll-employee-in-managed-care-product.edi](../edi_files/834/X220-enroll-employee-in-managed-care-product.edi) | [X220-enroll-employee-in-managed-care-product.json](834/X220-enroll-employee-in-managed-care-product.json) | [X220-enroll-employee-in-managed-care-product.csv](834/X220-enroll-employee-in-managed-care-product.csv)<br>[X220-enroll-employee-in-managed-care-product.xlsx](834/X220-enroll-employee-in-managed-care-product.xlsx) |
| [X220-enroll-employee-in-multiple-health-care-insurance-products.edi](../edi_files/834/X220-enroll-employee-in-multiple-health-care-insurance-products.edi) | [X220-enroll-employee-in-multiple-health-care-insurance-products.json](834/X220-enroll-employee-in-multiple-health-care-insurance-products.json) | [X220-enroll-employee-in-multiple-health-care-insurance-products.csv](834/X220-enroll-employee-in-multiple-health-care-insurance-products.csv)<br>[X220-enroll-employee-in-multiple-health-care-insurance-products.xlsx](834/X220-enroll-employee-in-multiple-health-care-insurance-products.xlsx) |
| [X220-reinstate-an-employee.edi](../edi_files/834/X220-reinstate-an-employee.edi) | [X220-reinstate-an-employee.json](834/X220-reinstate-an-employee.json) | [X220-reinstate-an-employee.csv](834/X220-reinstate-an-employee.csv)<br>[X220-reinstate-an-employee.xlsx](834/X220-reinstate-an-employee.xlsx) |
| [X220-reinstate-employee-at-coverage-(hd)-level.edi](../edi_files/834/X220-reinstate-employee-at-coverage-%28hd%29-level.edi) | [X220-reinstate-employee-at-coverage-(hd)-level.json](834/X220-reinstate-employee-at-coverage-%28hd%29-level.json) | [X220-reinstate-employee-at-coverage-(hd)-level.csv](834/X220-reinstate-employee-at-coverage-%28hd%29-level.csv)<br>[X220-reinstate-employee-at-coverage-(hd)-level.xlsx](834/X220-reinstate-employee-at-coverage-%28hd%29-level.xlsx) |
| [X220-reinstate-member-eligibility-(ins).edi](../edi_files/834/X220-reinstate-member-eligibility-%28ins%29.edi) | [X220-reinstate-member-eligibility-(ins).json](834/X220-reinstate-member-eligibility-%28ins%29.json) | [X220-reinstate-member-eligibility-(ins).csv](834/X220-reinstate-member-eligibility-%28ins%29.csv)<br>[X220-reinstate-member-eligibility-(ins).xlsx](834/X220-reinstate-member-eligibility-%28ins%29.xlsx) |
| [X220-terminate-eligibility-for-subscriber.edi](../edi_files/834/X220-terminate-eligibility-for-subscriber.edi) | [X220-terminate-eligibility-for-subscriber.json](834/X220-terminate-eligibility-for-subscriber.json) | [X220-terminate-eligibility-for-subscriber.csv](834/X220-terminate-eligibility-for-subscriber.csv)<br>[X220-terminate-eligibility-for-subscriber.xlsx](834/X220-terminate-eligibility-for-subscriber.xlsx) |

### 834 Validation Issues

| EDI File | JSON Format |
| --- | --- |
| [834-validation-issues.edi](../edi_files/834/834-validation-issues.edi) | [834-validation-issues-validation-only.json](834/834-validation-issues-validation-only.json)<br>[834-validation-issues.json](834/834-validation-issues.json) |

## 835

| EDI File | JSON Format | CSV Format |
| --- | --- | --- |
| [All files](../edi_files/835/) | [835-all-files.json](835/835-all-files.json)<br>[835-all-files.jsonl](835/835-all-files.jsonl) | [835-all-files.csv](835/835-all-files.csv)<br>[835-all-files-Lines.csv](835/835-all-files-Lines.csv)<br>[835-all-files-Payments.csv](835/835-all-files-Payments.csv)<br>[835-all-files-repeat-claim.csv](835/835-all-files-repeat-claim.csv)<br>[835-all-files.xlsx](835/835-all-files.xlsx) |
| [835-all-fields.dat](../edi_files/835/835-all-fields.dat) | [835-all-fields.json](835/835-all-fields.json) | [835-all-fields.csv](835/835-all-fields.csv)<br>[835-all-fields.xlsx](835/835-all-fields.xlsx) |
| [835-denial.dat](../edi_files/835/835-denial.dat) | [835-denial.json](835/835-denial.json) | [835-denial.csv](835/835-denial.csv)<br>[835-denial.xlsx](835/835-denial.xlsx) |
| [835-provider-level-adjustment.dat](../edi_files/835/835-provider-level-adjustment.dat) | [835-provider-level-adjustment.json](835/835-provider-level-adjustment.json) | [835-provider-level-adjustment.csv](835/835-provider-level-adjustment.csv)<br>[835-provider-level-adjustment.xlsx](835/835-provider-level-adjustment.xlsx) |
| [claim_adj_reason.dat](../edi_files/835/claim_adj_reason.dat) | [claim_adj_reason.json](835/claim_adj_reason.json) | [claim_adj_reason.csv](835/claim_adj_reason.csv)<br>[claim_adj_reason.xlsx](835/claim_adj_reason.xlsx) |
| [dollars_data_separate.dat](../edi_files/835/dollars_data_separate.dat) | [dollars_data_separate.json](835/dollars_data_separate.json) | [dollars_data_separate.csv](835/dollars_data_separate.csv)<br>[dollars_data_separate.xlsx](835/dollars_data_separate.xlsx) |
| [negotiated_discount.dat](../edi_files/835/negotiated_discount.dat) | [negotiated_discount.json](835/negotiated_discount.json) | [negotiated_discount.csv](835/negotiated_discount.csv)<br>[negotiated_discount.xlsx](835/negotiated_discount.xlsx) |
| [not_covered_inpatient.dat](../edi_files/835/not_covered_inpatient.dat) | [not_covered_inpatient.json](835/not_covered_inpatient.json) | [not_covered_inpatient.csv](835/not_covered_inpatient.csv)<br>[not_covered_inpatient.xlsx](835/not_covered_inpatient.xlsx) |

### 835 Validation Issues

| EDI File | JSON Format |
| --- | --- |
| [835-validation-issues.edi](../edi_files/835/835-validation-issues.edi) | [835-validation-issues-validation-only.json](835/835-validation-issues-validation-only.json)<br>[835-validation-issues.json](835/835-validation-issues.json) |

## 837

| EDI File | JSON Format | CSV Format |
| --- | --- | --- |
| [All files](../edi_files/837/) | [837-all-files.json](837/837-all-files.json)<br>[837-all-files.jsonl](837/837-all-files.jsonl) | [837P-all-files.csv](837/837P-all-files.csv)<br>[837P-all-files-Claims.csv](837/837P-all-files-Claims.csv)<br>[837P-all-files-Lines.csv](837/837P-all-files-Lines.csv)<br>[837P-all-files-repeat-claim.csv](837/837P-all-files-repeat-claim.csv)<br>[837P-all-files.xlsx](837/837P-all-files.xlsx) |
| [837D-all-fields.dat](../edi_files/837/837D-all-fields.dat) | [837D-all-fields.json](837/837D-all-fields.json) |  |
| [837I-X299-all-fields.dat](../edi_files/837/837I-X299-all-fields.dat) | [837I-X299-all-fields.json](837/837I-X299-all-fields.json) |  |
| [837I-all-fields.dat](../edi_files/837/837I-all-fields.dat) | [837I-all-fields.json](837/837I-all-fields.json)<br>[837I-all-fields.jsonl](837/837I-all-fields.jsonl) | [837I-all-fields.csv](837/837I-all-fields.csv)<br>[837I-all-fields-Claims.csv](837/837I-all-fields-Claims.csv)<br>[837I-all-fields-Lines.csv](837/837I-all-fields-Lines.csv)<br>[837I-all-fields.xlsx](837/837I-all-fields.xlsx) |
| [837I-inst-claim.dat](../edi_files/837/837I-inst-claim.dat) | [837I-inst-claim.json](837/837I-inst-claim.json) | [837I-inst-claim.csv](837/837I-inst-claim.csv)<br>[837I-inst-claim.xlsx](837/837I-inst-claim.xlsx) |
| [837I-minimal.dat](../edi_files/837/837I-minimal.dat) | [837I-minimal.json](837/837I-minimal.json) | [837I-minimal.csv](837/837I-minimal.csv)<br>[837I-minimal.xlsx](837/837I-minimal.xlsx) |
| [837P-X298-all-fields.dat](../edi_files/837/837P-X298-all-fields.dat) | [837P-X298-all-fields.json](837/837P-X298-all-fields.json) |  |
| [837P-all-fields.dat](../edi_files/837/837P-all-fields.dat) | [837P-all-fields.json](837/837P-all-fields.json)<br>[837P-all-fields.jsonl](837/837P-all-fields.jsonl) | [837P-all-fields.csv](837/837P-all-fields.csv)<br>[837P-all-fields-Claims.csv](837/837P-all-fields-Claims.csv)<br>[837P-all-fields-Lines.csv](837/837P-all-fields-Lines.csv)<br>[837P-all-fields.xlsx](837/837P-all-fields.xlsx) |
| [837P-minimal.dat](../edi_files/837/837P-minimal.dat) | [837P-minimal.json](837/837P-minimal.json) | [837P-minimal.csv](837/837P-minimal.csv)<br>[837P-minimal.xlsx](837/837P-minimal.xlsx) |
| [ambulance.dat](../edi_files/837/ambulance.dat) | [ambulance.json](837/ambulance.json) | [ambulance.csv](837/ambulance.csv)<br>[ambulance.xlsx](837/ambulance.xlsx) |
| [anesthesia.dat](../edi_files/837/anesthesia.dat) | [anesthesia.json](837/anesthesia.json) | [anesthesia.csv](837/anesthesia.csv)<br>[anesthesia.xlsx](837/anesthesia.xlsx) |
| [chiro.dat](../edi_files/837/chiro.dat) | [chiro.json](837/chiro.json) | [chiro.csv](837/chiro.csv)<br>[chiro.xlsx](837/chiro.xlsx) |
| [cob-payera-payerb.dat](../edi_files/837/cob-payera-payerb.dat) | [cob-payera-payerb.json](837/cob-payera-payerb.json) | [cob-payera-payerb.csv](837/cob-payera-payerb.csv)<br>[cob-payera-payerb.xlsx](837/cob-payera-payerb.xlsx) |
| [cob-prov-payera.dat](../edi_files/837/cob-prov-payera.dat) | [cob-prov-payera.json](837/cob-prov-payera.json) | [cob-prov-payera.csv](837/cob-prov-payera.csv)<br>[cob-prov-payera.xlsx](837/cob-prov-payera.xlsx) |
| [commercial.dat](../edi_files/837/commercial.dat) | [commercial.json](837/commercial.json) | [commercial.csv](837/commercial.csv)<br>[commercial.xlsx](837/commercial.xlsx) |
| [commercial-replacement.dat](../edi_files/837/commercial-replacement.dat) | [commercial-replacement.json](837/commercial-replacement.json) | [commercial-replacement.csv](837/commercial-replacement.csv)<br>[commercial-replacement.xlsx](837/commercial-replacement.xlsx) |
| [home-infusion-ndc.dat](../edi_files/837/home-infusion-ndc.dat) | [home-infusion-ndc.json](837/home-infusion-ndc.json) | [home-infusion-ndc.csv](837/home-infusion-ndc.csv)<br>[home-infusion-ndc.xlsx](837/home-infusion-ndc.xlsx) |
| [multi-tran.dat](../edi_files/837/multi-tran.dat) | [multi-tran.json](837/multi-tran.json) | [multi-tran.csv](837/multi-tran.csv)<br>[multi-tran.xlsx](837/multi-tran.xlsx) |
| [ppo-repriced.dat](../edi_files/837/ppo-repriced.dat) | [ppo-repriced.json](837/ppo-repriced.json) | [ppo-repriced.csv](837/ppo-repriced.csv)<br>[ppo-repriced.xlsx](837/ppo-repriced.xlsx) |
| [prof-encounter.dat](../edi_files/837/prof-encounter.dat) | [prof-encounter.json](837/prof-encounter.json) | [prof-encounter.csv](837/prof-encounter.csv)<br>[prof-encounter.xlsx](837/prof-encounter.xlsx) |
| [wheelchair.dat](../edi_files/837/wheelchair.dat) | [wheelchair.json](837/wheelchair.json) | [wheelchair.csv](837/wheelchair.csv)<br>[wheelchair.xlsx](837/wheelchair.xlsx) |

### 837 Validation Issues

| EDI File | JSON Format |
| --- | --- |
| [837P-validation-issues.edi](../edi_files/837/837P-validation-issues.edi) | [837P-validation-issues-validation-only.json](837/837P-validation-issues-validation-only.json)<br>[837P-validation-issues.json](837/837P-validation-issues.json) |

## NCPDP

| EDI File | JSON Format |
| --- | --- |
| [b1_telco.dat](../edi_files/ncpdp/b1_telco.dat) | [b1_telco.json](ncpdp/b1_telco.json) |
