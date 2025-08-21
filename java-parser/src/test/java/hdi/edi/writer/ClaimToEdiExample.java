package hdi.edi.writer;

import hdi.codeent.CodeEntity;
import hdi.edi.EdiTransaction;
import hdi.edi.ediwriter.EdiWriter;
import hdi.edi.parser.EdiParser;
import hdi.edi.parser.ParsingExampleHelper;
import hdi.edi.parser.TransactionType;
import hdi.model.PlaceOfServiceType;
import hdi.model.ServiceLine;
import hdi.model.claim.Claim;
import hdi.model.control.FunctionalGroup;
import hdi.model.control.Isa;
import hdi.model.enumtype.IdentificationType;
import hdi.model.enumtype.UbCodeType;
import hdi.model.enumtype.UnitType;
import hdi.model.orgperson.*;
import hdi.model.patientsubscriber.PatientSubscriber;
import lombok.SneakyThrows;
import org.apache.commons.io.FileUtils;
import org.junit.Test;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.math.BigDecimal;
import java.nio.charset.Charset;
import java.time.LocalDate;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@SuppressWarnings("NewClassNamingConvention")
public class ClaimToEdiExample implements ParsingExampleHelper {

    @Test
    public void write837pEdi() throws IOException {
        File ediFile = new File(OUT_EDI_FILES_DIR , "837p-simple.edi");
        try (var fileWriter = new FileWriter(ediFile);var ediWriter = new EdiWriter(fileWriter)) {
            writeIsaAndGs(ediWriter, TransactionType.PROF);
            var tran = createEdiTransaction(TransactionType.PROF);
            ediWriter.writeTransaction(tran);

            var claim = createSimpleProfClaim();
            claim.billingProvider(createBillingProv());
            claim.subscriber(createSubscriber());
            ediWriter.writeClaim(claim);
        }
        var s = FileUtils.readFileToString(ediFile, Charset.defaultCharset());
        System.err.println(s);
    }

    @Test
    public void write837iEdi() throws IOException {
        File ediFile = new File(OUT_EDI_FILES_DIR , "837i-simple.edi");
        try (var fileWriter = new FileWriter(ediFile);var ediWriter = new EdiWriter(fileWriter)) {
            writeIsaAndGs(ediWriter, TransactionType.INST);
            var tran = createEdiTransaction(TransactionType.INST);
            ediWriter.writeTransaction(tran);

            var claim = createSimpleInstClaim();
            claim.billingProvider(createBillingProv());
            claim.subscriber(createSubscriber());
            ediWriter.writeClaim(claim);
        }
        var s = FileUtils.readFileToString(ediFile, Charset.defaultCharset());
        System.err.println(s);
    }

    private void writeIsaAndGs(EdiWriter ediWriter, TransactionType transactionType) {
        var isa = new Isa("ZZ", "123", "ZZ", "456");
        var gs = new FunctionalGroup(transactionType, "1", "2");
        ediWriter.writeIsa(isa);
        ediWriter.writeFunctionalGroup(gs);
    }

    private Claim createSimpleProfClaim() {
        var claim = Claim.createProfClaim("1234567890", new BigDecimal("100.00"), "11");
        claim.addDiagCodes(List.of("J0300", "Z1159"));

        // providers
        var renderingProv = new OrgOrPerson(EntityRole.RENDERING, EntityType.INDIVIDUAL, IdentificationType.NPI, "1234567890", "Rendering", "Provider");
        claim.addProvider(renderingProv);
        var serviceFacility = new OrgOrPerson(EntityRole.SERVICE_FACILITY, IdentificationType.NPI, "1234567890", "Facility");
        serviceFacility.address(new Address("987 Main St", null, "Anytown", "CA", "12345"));
        claim.addProvider(serviceFacility);

        var line1 = ServiceLine.createProfLine("99213", new BigDecimal("100.00"), BigDecimal.ONE, LocalDate.of(2025, 1, 1), List.of(1, 2));
        line1.procedure().addModifier("25");
        claim.addLine(line1);
        return claim;
    }

    private Claim createSimpleInstClaim() {
        var claim = Claim.createInstClaim("1234567890", new BigDecimal("100.00"), "11", "01", LocalDate.of(2025, 1, 1), LocalDate.of(2025, 1, 31));
        claim.addDiagCodes(List.of("M24562", "E8359", "Z1159"));
        // The first diagnosis was present on admission
        claim.diags().get(0).isPresentOnAdmission(true);
        // add other inst. codes
        claim.addCodeEntity(new CodeEntity(UbCodeType.OCCURRENCE, "01").occurrenceDate(LocalDate.of(2025, 1, 1)));
        claim.addCodeEntity(new CodeEntity(UbCodeType.VALUE, "01").amount(new BigDecimal("100")));

        var line1 = ServiceLine.createInstLine("300", new BigDecimal("100.00"), new BigDecimal("5"))
                // The default is UNIT
                .unitType(UnitType.DAYS)
                .serviceDateFrom(LocalDate.of(2025, 1, 1));
        claim.addLine(line1);
        return claim;
    }

    private PatientSubscriber createSubscriber() {
        var payer = new OrgOrPerson(EntityRole.PAYER, EntityType.BUSINESS, IdentificationType.PAYOR_ID, "1234567890", "Payer", null);
        payer.address(new Address("456 Main St", null, "Anytown", "CA", "12345"));

        var subscriber = PatientSubscriber.createSubscriber("123", "Doe", "John", "1234567890", LocalDate.of(1990, 1, 1), GenderType.MALE);
        subscriber.person().address(new Address("789 Main St", null, "Anytown", "CA", "12345"));
        subscriber.payer(payer);
        return subscriber;
    }

    private OrgOrPerson createBillingProv() {
        var billing = new OrgOrPerson(EntityRole.BILLING_PROVIDER, EntityType.BUSINESS, IdentificationType.NPI, "1234567890", "Billing Provider", null);
        billing.taxId("1234567890");
        billing.address(new Address("123 Main St", null, "Anytown", "CA", "12345"));
        return billing;
    }

    private EdiTransaction createEdiTransaction(TransactionType tranType) {
        var tran = new EdiTransaction(tranType);

        var submitter = new OrgOrPerson(EntityRole.SUBMITTER, IdentificationType.ETIN, "TGJ23", "PREMIER BILLING SERVICE");
        var submitterContact = new ContactInfo();
        submitterContact.addContactNumber(ContactType.EMAIL, "test@test.com");
        submitter.addContact(submitterContact);
        tran.sender(submitter);

        var receiver = new OrgOrPerson(EntityRole.RECEIVER, IdentificationType.ETIN, "66783JJT", "KEY INSURANCE COMPANY");
        tran.receiver(receiver);
        return tran;
    }
}