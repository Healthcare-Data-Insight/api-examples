package hdi.edi.parser;

import hdi.model.status.*;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

import java.io.File;
import java.util.List;

@SuppressWarnings("NewClassNamingConvention")
@Slf4j
public class ClaimStatus277CAParsingExample implements ParsingExampleHelper {

    @Test
    public void parseClaimStatuses() {
        var edi277File = new File(EDI_FILES_DIR, "/277/277CA-all-fields.edi");
        EdiParsingResults parsingResults;
        try (var parser = new EdiParser(edi277File)) {
            // parse all; use batching if parsing large files
            parsingResults = parser.parse(-1);
        }
        List<ReceiverProviderClaimStatus> allStatuses = parsingResults.statuses();
        // statuses can be reported at a claim, provider or receiver level
        // Receiver status is provided when the entire transaction is rejected
        for (var receiverProviderClaimStatus : allStatuses) {
            // normally, each claim will have a corresponding status
            if (receiverProviderClaimStatus instanceof ClaimStatus claimStatus) {
                // Each claim status contains its patient and billing provider
                // claim identifier
                var pcn = claimStatus.patientControlNumber();
                log.info("** Claim PCN: {}", pcn);
                var billingProvider = claimStatus.provider();
                log.info("Billing provider: {}", billingProvider.identifier());
                var patient = claimStatus.patient();
                log.info("Patient ID: {}", patient.identifier());

                List<StatusInfo> statusInfos = claimStatus.statusInfos();
                // There could be multiple statuses, one per payer's edit
                for (var statusInfo : statusInfos) {
                    // accept or reject
                    StatusActionType actionType = statusInfo.actionType();
                    log.info("Action: {}", actionType);
                    // we can have up to three codes associated with this status
                    for (StatusCodeInfo statusCodeInfo : statusInfo.statusCodeInfos()) {
                        String categoryCode = statusCodeInfo.categoryCode();
                        String statusCode = statusCodeInfo.statusCode();
                        log.info("Status code: {}: {}", categoryCode, statusCode);
                    }
                }
                // If a service lined caused the claim's rejection, there will be a list of line statuses
                for (ServiceLineStatus lineStatus : claimStatus.serviceLineStatuses()) {
                    String controlNumber = lineStatus.controlNumber();
                    log.info("Rejected line's control number: {}", controlNumber);
                    for (var statusInfo : lineStatus.statusInfos()) {
                        for (StatusCodeInfo statusCodeInfo : statusInfo.statusCodeInfos()) {
                            log.info("Line status code: {}: {}", statusCodeInfo.categoryCode(), statusCodeInfo.statusCode());
                        }
                    }
                }
            }
            // some payers can report statuses at the provider level
            else if (receiverProviderClaimStatus instanceof ProviderStatus providerStatus) {
                log.info("** Status for provider: {}", providerStatus.party().identifier());
                for (var statusInfo : providerStatus.statusInfos()) {
                    log.info("Action type: {}", statusInfo.actionType());
                    for (StatusCodeInfo statusCodeInfo : statusInfo.statusCodeInfos()) {
                        log.info("Provider status code: {}: {}", statusCodeInfo.categoryCode(), statusCodeInfo.statusCode());
                    }
                }
            }
            else if (receiverProviderClaimStatus instanceof ReceiverStatus receiverStatus) {
                // see the example below
            }
        }
    }

    /**
     * In some cases the entire transaction can be rejected, so we will not get any claim-level statuses.
     * So we need to check for receiver status
     */
    @Test
    public void parseReceiverStatus() {
        var edi277File = new File(EDI_FILES_DIR, "/277/277CA-receiver-rejected.edi");

        EdiParsingResults parsingResults;
        try (var parser = new EdiParser(edi277File)) {
            // parse all
            parsingResults = parser.parse(-1);
        }
        // Get all statuses from this file
        List<ReceiverProviderClaimStatus> allStatuses = parsingResults.statuses();
        for (var receiverProviderClaimStatus : allStatuses) {
            if (receiverProviderClaimStatus instanceof ClaimStatus claimStatus) {
                // process claim status, see above
                continue;
            }
            else if (receiverProviderClaimStatus instanceof ProviderStatus providerStatus) {
                // process provider status see above
                continue;
            }
            else if (receiverProviderClaimStatus instanceof ReceiverStatus receiverStatus) {
                log.info("** Status for receiver: {}", receiverStatus.party().lastNameOrOrgName());
                String rejectedTransaction = receiverStatus.traceIdentifier();
                log.info("Rejected transaction: {}", rejectedTransaction);
                // iterate over statuses
                for (var statusInfo : receiverStatus.statusInfos()) {
                    log.info("Action type: {}", statusInfo.actionType());
                    for (StatusCodeInfo statusCodeInfo : statusInfo.statusCodeInfos()) {
                        log.info("Receiver status code: {}: {}", statusCodeInfo.categoryCode(), statusCodeInfo.statusCode());
                    }
                }
            }
        }
    }

}