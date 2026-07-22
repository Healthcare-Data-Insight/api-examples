package hdi.edi.parser;

import hdi.edi.EdiTransaction;
import hdi.edi.validation.ValidationIssue;
import hdi.model.control.FunctionalGroup;
import hdi.model.control.InterchangeControl;
import hdi.model.status.*;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

import java.io.File;
import java.time.LocalDateTime;
import java.util.List;

@SuppressWarnings("NewClassNamingConvention")
@Slf4j
public class ClaimStatus277CAParsingExample implements ParsingExampleHelper {
    @Test
    public void parse277CAClaimStatus() {
        parse277CA(new File(EDI_FILES_DIR, "/277/277CA-all-fields.edi"));
    }

    /**
     * In some cases the entire transaction can be rejected, so we will not get any claim-level statuses.
     */
    @Test
    public void parse277CAReceiverStatus() {
        parse277CA(new File(EDI_FILES_DIR, "/277/277CA-receiver-rejected.edi"));
    }

    public void parse277CA(File edi277File) {
        log.info("* Parsing 277CA file: {}", edi277File.getName());
        try (var parser = new EdiParser(edi277File)
                // Turn validation mode on
                .isValidationMode(true)) {
            EdiParsingResults parsingResults;
            do {                // parse 20 transactions at a time
                parsingResults = parser.parse(DEFAULT_CHUNK_SIZE);
                for (var rootObj : parsingResults.rootObjs()) {
                    // statuses can be reported at a claim, provider or receiver level
                    // Receiver status is provided when the entire transaction is rejected
                    // normally, each claim will have a corresponding status
                    if (rootObj instanceof ClaimStatus claimStatus) {
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
                    else if (rootObj instanceof ProviderStatus providerStatus) {
                        log.info("** Status for provider: {}", providerStatus.party().identifier());
                        for (var statusInfo : providerStatus.statusInfos()) {
                            log.info("Action type: {}", statusInfo.actionType());
                            for (StatusCodeInfo statusCodeInfo : statusInfo.statusCodeInfos()) {
                                log.info("Provider status code: {}: {}", statusCodeInfo.categoryCode(), statusCodeInfo.statusCode());
                            }
                        }
                    }
                    // If the transaction was rejected, we need to check for receiver status
                    else if (rootObj instanceof ReceiverStatus receiverStatus) {
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
                    else if (rootObj instanceof EdiTransaction transaction && transaction.transactionType() == TransactionType.CLAIM_ACK) {
                        process277CATransaction(transaction);
                    }
                    else if (rootObj instanceof InterchangeControl interchangeControl) {
                        log.info("ISA segment info:\n{}", interchangeControl);
                    }
                    else if (rootObj instanceof FunctionalGroup functionalGroup) {
                        log.info("GS segment info:\n{}", functionalGroup);
                    }
                    // validation issue at the transaction level
                    else if (rootObj instanceof ValidationIssue validationIssue) {
                        // validation issues are logged by the parser; here you can do additional processing
                    }
                    else {
                        throw new IllegalStateException("Unexpected object for 277 transaction: " + rootObj);
                    }
                }
            } while (!parsingResults.isDone());
        }
    }

    private void process277CATransaction(EdiTransaction transaction) {
        String controlNumber = transaction.controlNumber();
        LocalDateTime transactionDateTime = transaction.getCreationDateTime();
        log.info("Transaction: {} {}", controlNumber, transactionDateTime);
    }
}