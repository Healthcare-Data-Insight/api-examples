package hdi.edi.parser;

import hdi.model.PlaceOfServiceType;
import hdi.model.claim.Claim;
import hdi.model.enumtype.UnitType;
import hdi.model.orgperson.EntityRole;
import hdi.model.orgperson.EntityType;
import hdi.model.orgperson.GenderType;
import hdi.model.orgperson.OrgOrPerson;
import hdi.model.patientsubscriber.PatientSubscriber;
import hdi.model.payment.ClaimStatus;
import hdi.model.payment.Payment;
import org.junit.Test;

import java.io.File;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@SuppressWarnings("NewClassNamingConvention")
public class PaymentParsingExample implements ParsingExampleHelper {

    @Test
    public void parsePayments() {
        var ediFile835 = new File(EDI_FILES_DIR + "/835/dollars_data_separate.dat");
        var parser = new EdiParser(ediFile835);

        EdiParsingResults results = parser.parse();
        List<Payment> payments = results.payments();
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

        // iterate over lines and get key fields
        for (var line : payment.lines()) {
            String procedureCode = line.procedure().code();
            LocalDate serviceDate = line.serviceDateFrom();
            BigDecimal lineChargeAmount = line.chargeAmount();
            BigDecimal linePaidAmount = line.paidAmount();

            assertNotNull(procedureCode, serviceDate, lineChargeAmount, linePaidAmount);
        }

    }
}