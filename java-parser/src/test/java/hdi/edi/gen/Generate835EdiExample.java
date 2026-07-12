package hdi.edi.gen;

import hdi.codeent.CodeEntity;
import hdi.codeent.PrimaryCodeType;
import hdi.edi.EdiTransaction;
import hdi.edi.ediwriter.EdiWriter;
import hdi.edi.parser.ParsingExampleHelper;
import hdi.edi.parser.TransactionType;
import hdi.model.Amount;
import hdi.model.ServiceLine;
import hdi.model.enumtype.CarcRarcType;
import hdi.model.enumtype.IdentificationType;
import hdi.model.enumtype.ProcType;
import hdi.model.enumtype.UbCodeType;
import hdi.model.orgperson.*;
import hdi.model.patientsubscriber.PatientSubscriber;
import hdi.model.payment.*;
import org.apache.commons.io.FileUtils;
import org.junit.Test;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.time.LocalDate;
import java.util.List;

@SuppressWarnings("NewClassNamingConvention")
public class Generate835EdiExample implements ParsingExampleHelper {

    @Test
    public void generate835Edi() throws IOException {
        File ediFile = new File(OUT_EDI_FILES_DIR, "835-simple.edi");
        try (var fileWriter = new FileWriter(ediFile);
             var ediWriter = new EdiWriter(fileWriter)) {

            GenerateEdiExampleHelper.writeIsaAndGs(ediWriter, TransactionType.PAYMENT);
            var tran = create835Transaction();
            ediWriter.writeTransaction(tran);

            var payment = createPayment();
            // The writer will perform full validation of the claim
            var validationIssues = ediWriter.writePayment(payment);
            logValidationIssues(validationIssues);
            // Closing segments will be written automatically when the writer is closed
        }
        var s = FileUtils.readFileToString(ediFile, StandardCharsets.UTF_8);
        System.out.println(s);
    }

    private Payment createPayment() {
        var payment = Payment.createPayment("5554555444",
                "94060555410000",
                AdjudicatedClaimStatus.PRIMARY,
                InsurancePlanType.PPO);
        payment.facilityCode(new CodeEntity(UbCodeType.PLACE_OF_SERVICE, "11"));
        payment.frequencyCode(new CodeEntity(UbCodeType.FREQUENCY_CODE, "1"));
        payment.patient(createPatient());
        payment.patientResponsibilityAmount(new BigDecimal("300.00"));
        payment.addLine(createServiceLine());

        return payment;
    }

    private PatientSubscriber createPatient() {
        return new PatientSubscriber()
                .person(new OrgOrPerson(EntityRole.PATIENT, EntityType.INDIVIDUAL, IdentificationType.MEMBER_ID, "33344555510", "BUDD", "WILLIAM"));
    }

    private ServiceLine createServiceLine() {
        return new ServiceLine()
                .chargeAmount(new BigDecimal("800.00"))
                .paidAmount(new BigDecimal("500.00"))
                .supplementalAmounts(List.of(createSupplementalAmount()))
                .serviceDateFrom(LocalDate.of(2024, 3, 1))
                .procedure(new CodeEntity(PrimaryCodeType.PROCEDURE, ProcType.CPT, "99211"))
                .adjustments(List.of(createAdjustment()));
    }

    private Amount createSupplementalAmount() {
        return new Amount()
                .qualifierCode("B6")
                .amount(new BigDecimal("800.00"));
    }

    private Adjustment createAdjustment() {
        return new Adjustment(
                AdjustmentGroup.PATIENT_RESPONSIBILITY,
                new CodeEntity(PrimaryCodeType.CLAIM_ADJUSTMENT_REASON_CODE, CarcRarcType.CARC, "1"),
                new BigDecimal("300.00"));
    }

    private EdiTransaction create835Transaction() {
        // The writer will assign a unique Originator Application ID if not set
        var tran = new EdiTransaction(TransactionType.PAYMENT);
        tran.transactionHandlingType(TransactionHandlingType.PAYMENT_AND_ADVICE);
        tran.totalPaymentAmount(new BigDecimal("1000.00"));
        tran.creditOrDebitFlagCode("C");
        tran.paymentMethodType(PaymentMethodType.CHECK);
        tran.receiverAccountNumber("456");
        tran.paymentDate(LocalDate.parse("2026-06-01"));
        tran.checkOrEftTraceNumber("12345");
        tran.payerIdentifier("PAYER_ID01");

        var payer = new OrgOrPerson(EntityRole.PAYER, null, null, "ANY PLAN USA");
        var address = new Address("1 WALK THIS WAY", null, "ANYCITY", "OH", "45209");
        payer.address(address);
        // Technical contact is required for the payer
        var payerContact = new ContactInfo("BL", "EDI");
        payerContact.addContactNumber(ContactType.EMAIL, "test@test.com");
        payer.addContact(payerContact);
        tran.sender(payer);

        var payee = new OrgOrPerson(EntityRole.PAYEE, IdentificationType.NPI, "PROVIDER2_NPI", "PROVIDER");
        tran.receiver(payee);

        return tran;
    }


}