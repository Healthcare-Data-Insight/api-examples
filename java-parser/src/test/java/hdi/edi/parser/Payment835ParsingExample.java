package hdi.edi.parser;

import hdi.edi.EdiTransaction;
import hdi.edi.validation.ValidationIssue;
import hdi.model.control.FunctionalGroup;
import hdi.model.control.InterchangeControl;
import hdi.model.orgperson.OrgOrPerson;
import hdi.model.payment.*;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

import java.io.File;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.Collection;

@SuppressWarnings("NewClassNamingConvention")
@Slf4j
public class Payment835ParsingExample implements ParsingExampleHelper {

    @Test
    public void parseRegular835() {
        parse835(new File(EDI_FILES_DIR, "/835/835-all-fields.dat"));
    }

    @Test
    public void parseProviderAdjustments835() {
        parse835(new File(EDI_FILES_DIR, "/835/835-provider-level-adjustment.dat"));
    }

    public void parse835(File edi835File) {
        log.info("* Parsing EDI 835 file: {}", edi835File.getName());
        try (var parser = new EdiParser(edi835File)
                // Turn validation mode on
                .isValidationMode(true)) {
            EdiParsingResults parsingResults;
            do {                // parse 20 payments or adjustments at a time
                parsingResults = parser.parse(DEFAULT_CHUNK_SIZE);
                // "rootObjs" contains all objects parsed from EDI in the order they appear in the EDI file
                // process all transactions, claims, payments, and provider adjustments
                for (var rootObj : parsingResults.rootObjs()) {
                    if (rootObj instanceof EdiTransaction transaction && transaction.transactionType() == TransactionType.PAYMENT) {
                        process835Transaction(transaction);
                    }
                    // Each payment is an adjudicated claim (CLP segment)
                    else if (rootObj instanceof Payment payment) {
                        processPayment(payment);
                    }
                    // Provider-level adjustment (PLB segment) is unrelated to a specific claim, could be a forwarding balance, accelerated payments, cost report settlements for a fiscal year, etc.
                    else if (rootObj instanceof ProviderAdjustment providerAdjustment) {
                        processProviderAdjustment(providerAdjustment);
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
                        throw new IllegalStateException("Unexpected object for 835 transaction: " + rootObj);
                    }
                }
            } while (!parsingResults.isDone());
        }
    }

    private void process835Transaction(EdiTransaction transaction) {
        // ACH or check. Can also be NON_PAYMENT in case of denials
        PaymentMethodType paymentMethodType = transaction.paymentMethodType();
        // Fields related to ACH or check payment
        LocalDate paymentDate = transaction.paymentDate();
        String checkOrEftTraceNumber = transaction.checkOrEftTraceNumber();
        // how much was paid for all claims in this transaction
        BigDecimal totalPaymentAmount = transaction.totalPaymentAmount();
        // transaction.id() is a unique identifier assigned by the parser; you can use it to correlate transaction from each payment
        log.info("Transaction: {} {} {} {} ", transaction.id(), paymentDate, paymentMethodType, totalPaymentAmount);
    }

    private void processPayment(Payment payment) {
        String payerControlNumber = payment.payerControlNumber();
        String patientControlNumber = payment.patientControlNumber();
        BigDecimal chargeAmount = payment.chargeAmount();
        BigDecimal paidAmount = payment.paymentAmount();
        AdjudicatedClaimStatus status = payment.claimStatus();
        OrgOrPerson payer = payment.payer();
        log.info("Payment: {} {} {} {} {} {}",
                payer.identifier(), payerControlNumber, patientControlNumber, chargeAmount, paidAmount, status);
        OrgOrPerson payee = payment.payee();
        String payeeNpi = payee.identifier();
        assertNotNull(payerControlNumber, status, patientControlNumber, chargeAmount, paidAmount, patientControlNumber, payeeNpi, payer.identifier());

        // adjustments at the claim level
        for (var claimAdj : payment.adjustments()) {
            BigDecimal adjAmount = claimAdj.amount();
            String adjReasonCode = claimAdj.reasonCode();
            assertNotNull(adjAmount, adjReasonCode);
            log.info("Claim adjustment: {} {}", adjReasonCode, adjAmount);
        }
        // claim-level remarks for outpatient claims
        if (payment.outpatientAdjudication() != null) {
            for (var remark : payment.outpatientAdjudication().remarks()) {
                log.info("Outpatient adjudication remark: {}", remark.code());
            }
        }
        if (payment.inpatientAdjudication() != null) {
            for (var remark : payment.inpatientAdjudication().remarks()) {
                log.info("Inpatient adjudication remark: {}", remark.code());
            }
        }
        // iterate over lines and get key fields
        for (var line : payment.lines()) {
            // control number or line index
            String lineId = line.sourceLineId();
            String serviceCode = null;
            if (line.procedure() != null) {
                serviceCode = line.procedure().code();
            }
            if (line.revenueCode() != null) {
                serviceCode = line.revenueCode().code();
            }
            if (line.drug() != null) {
                serviceCode = line.drug().code();
            }
            LocalDate serviceDateFrom = line.serviceDateFrom();
            BigDecimal lineChargeAmount = line.chargeAmount();
            BigDecimal linePaidAmount = line.paidAmount();

            assertNotNull(serviceCode, serviceDateFrom, lineChargeAmount, linePaidAmount);
            log.info("Line: {} Code: {} Dates: {}-{} Billed: {} Paid: {}", lineId, serviceCode, serviceDateFrom, line.serviceDateTo(), lineChargeAmount, linePaidAmount);
            for (var lineAdj : line.adjustments()) {
                BigDecimal adjAmount = lineAdj.amount();
                String adjReasonCode = lineAdj.reasonCode();
                AdjustmentGroup adjustmentGroup = lineAdj.group();
                assertNotNull(adjAmount, adjReasonCode);
                log.info("Line adjustment: {} {} {}", adjustmentGroup, adjReasonCode, adjAmount);
            }
            // remark codes (RARC)
            for (var remark : line.remarks()) {
                assertNotNull(remark.code());
                log.info("Line remark: {}", remark.code());
            }
        }
        // Validation issues for this payment
        processValidationIssues(payment, payment.validationIssues());
    }

    private void processProviderAdjustment(ProviderAdjustment providerAdjustment) {
        String providerId = providerAdjustment.providerIdentifier();
        String payerId = providerAdjustment.payer().identifier();
        log.info("Provider-level adjustments for fiscal year {}; Provider {}; payer {}:",
                providerAdjustment.fiscalPeriodDate(), providerId, payerId);
        for (var adjustment : providerAdjustment.adjustments()) {
            log.info("Adjustment: {} {}", adjustment.reason().code(), adjustment.amount());
        }
    }

    // All validations are logged automatically, here you can do additional processing
    private void processValidationIssues(Payment payment, Collection<ValidationIssue> issues) {
        // your logic here
    }
}