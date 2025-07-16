package hdi.edi.parser;

import hdi.model.orgperson.OrgOrPerson;
import hdi.model.payment.ClaimStatus;
import hdi.model.payment.Payment;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

import java.io.File;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@SuppressWarnings("NewClassNamingConvention")
@Slf4j
public class PaymentParsingExample implements ParsingExampleHelper {

    @Test
    public void parsePayment() {
        var ediFile835 = new File(EDI_FILES_DIR, "/835/835-all-fields.dat");
        List<Payment> payments;
        try (var parser = new EdiParser(ediFile835)) {
            // parse all payments
            payments = parser.parse835(-1);
        }
        assertThat(payments).isNotEmpty();
        Payment payment = payments.get(0);
        // Get key payment fields
        String payerControlNumber = payment.payerControlNumber();
        String patientControlNumber = payment.patientControlNumber();
        BigDecimal chargeAmount = payment.chargeAmount();
        BigDecimal paidAmount = payment.paymentAmount();
        ClaimStatus status = payment.claimStatus();
        OrgOrPerson payee = payment.payee();
        String payeeNpi = payee.identifier();

        assertNotNull(payerControlNumber, status, patientControlNumber, chargeAmount, paidAmount, patientControlNumber, payeeNpi);

        // adjustments at the claim level
        for (var claimAdj : payment.adjustments()) {
            BigDecimal adjAmount = claimAdj.amount();
            String adjReasonCode = claimAdj.reasonCode();
            assertNotNull(adjAmount, adjReasonCode);
        }
        // iterate over lines and get key fields
        for (var line : payment.lines()) {
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
            LocalDate serviceDate = line.serviceDateFrom();
            BigDecimal lineChargeAmount = line.chargeAmount();
            BigDecimal linePaidAmount = line.paidAmount();

            assertNotNull(serviceCode, serviceDate, lineChargeAmount, linePaidAmount);
            for (var lineAdj : line.adjustments()) {
                BigDecimal adjAmount = lineAdj.amount();
                String adjReasonCode = lineAdj.reasonCode();
                assertNotNull(adjAmount, adjReasonCode);
            }
            // remark codes (RARC)
            for (var remark : line.remarks()) {
                assertNotNull(remark.code());
            }
        }
    }

    /**
     * For large files, we can parse in batches of N payments
     */
    @Test
    public void parseInBatches() {
        var ediFile = new File(EDI_FILES_DIR, "/835/dollars_data_separate.dat");
        int count = 0;
        try (var parser = new EdiParser(ediFile).isSplitMode(true)) {
            while (true) {
                // parse one payment at a time. In real life, use 200-500 as the optimal batch size
                var payments = parser.parse835(1);
                if (payments.isEmpty()) {
                    break;
                }
                // Do something with each payment
                for (var payment : payments) {
                    // your logic goes here
                    System.err.println(payment.patientControlNumber());
                }
                // your logic goes here
                // ...
                count += payments.size();
            }
            assertThat(count).isEqualTo(2);
        }
    }
}