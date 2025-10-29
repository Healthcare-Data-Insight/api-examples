package hdi.edi.parser;

import hdi.model.PlaceOfServiceType;
import hdi.model.claim.Claim;
import hdi.model.enumtype.UnitType;
import hdi.model.orgperson.EntityRole;
import hdi.model.orgperson.EntityType;
import hdi.model.orgperson.GenderType;
import hdi.model.orgperson.OrgOrPerson;
import hdi.model.patientsubscriber.PatientSubscriber;
import hdi.model.patientsubscriber.RelationshipType;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

import java.io.File;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * 837 parsing examples
 * See JSON schemas for X12 EDI mapping documentation:
 * <a href="https://datainsight.health/docs/schemas/837p/">837P Schema</a>
 * <a href="https://datainsight.health/docs/schemas/837i/">837I Schema</a>
 */
@SuppressWarnings("NewClassNamingConvention")
@Slf4j
public class Claim837ParsingExample implements ParsingExampleHelper {

    @Test
    public void parseAllFields837p() {
        parse837(new File(EDI_FILES_DIR, "/837/837p-all-fields.dat"));
    }

    @Test
    public void parseAllFields837i() {
        parse837(new File(EDI_FILES_DIR, "/837/837i-all-fields.dat"));
    }

    public void parse837(File edi837File) {
        log.info("* Parsing EDI 837 file: {}", edi837File.getName());
        try (var parser = new EdiParser(edi837File)) {
            boolean isDone = false;
            while (!isDone) {
                EdiParsingResults parsingResults = parser.parse(100);
                List<Claim> claims = parsingResults.claims();
                for (var claim : claims) {
                    processClaim(claim);
                }
                var issues = parsingResults.parsingIssues();
                for (var issue : issues) {
                    log.warn("Parsing issue: {}", issue.message());
                }
                isDone = parsingResults.isDone();
            }
        }
    }

    private void processClaim(Claim claim) {
        // get some key attributes of the claim
        BigDecimal chargeAmount = claim.chargeAmount();
        String patientControlNumber = claim.patientControlNumber();
        OrgOrPerson billingProvider = claim.billingProvider();
        String providerNpi = billingProvider.identifier();
        assertNotNull(chargeAmount, patientControlNumber, providerNpi);
        log.info("Claim: {} {} ", patientControlNumber, chargeAmount);
        var subscriber = claim.subscriber();
        String subscriberIdentifier = subscriber.person().identifier();
        String payerIdenfifier = subscriber.payer().identifier();
        RelationshipType patientRelationshipType = subscriber.relationshipType();
        String patientName = subscriber.person().lastNameOrOrgName();
        var patient = claim.patient();
        if (patient != null) {
            // the patient is not a subscriber
            patientRelationshipType = patient.relationshipType();
            patientName = patient.person().lastNameOrOrgName();
        }
        log.info("Payer ID: {} Subscriber ID: {} Patient: {} {}", payerIdenfifier, subscriberIdentifier, patientRelationshipType, patientName);
        for (var dx : claim.diags()) {
            String poa = "";
            if (claim.isInstClaimOrPayment()) {
                poa = "POA: " + dx.presentOnAdmissionIndicator();
            }
            log.info("Diagnosis: {} {} {}", dx.subType(), dx.code(), poa);
        }
        // Institutional codes
        for (var px : claim.procs()) {
            log.info("Claim-level procedure code: {} {}", px.subType(), px.code());
        }
        for (var occurrence : claim.occurrences()) {
            log.info("Occurrence code: {} {}", occurrence.code(), occurrence.occurrenceDate());
        }
        for (var valueInfo : claim.valueInfos()) {
            log.info("Value code: {} {}", valueInfo.code(), valueInfo.amount());
        }
        // Occurrence span codes, etc
        // Service lines
        for (var line : claim.lines()) {
            // control number or line index
            String lineId = line.sourceLineId();
            String procedureCode = "";
            if (line.procedure() != null)
                procedureCode = line.procedure().code();
            // inst. claims can have revenue codes, procedure code is optional
            String revenueCode = "";
            if (line.revenueCode() != null)
                revenueCode = line.revenueCode().code();
            LocalDate serviceDateFrom = line.serviceDateFrom();
            BigDecimal unitCount = line.unitCount();
            UnitType unitType = line.unitType();
            BigDecimal lineChargeAmount = line.chargeAmount();
            log.info("Line: {} Code: {} {} Dates: {}-{} Billed: {} Quantity: {}", lineId, revenueCode, procedureCode, serviceDateFrom, line.serviceDateTo(), lineChargeAmount, unitCount);

            assertNotNull(procedureCode, serviceDateFrom, unitCount, unitType, lineChargeAmount);
        }

    }


    /**
     * The parser translates EDI qualifiers and some of the codes to Java enums
     */
    @Test
    public void parseEnums() {
        var ediFile837p = new File(EDI_FILES_DIR + "/837/prof-encounter.dat");
        List<Claim> claims;
        try (var parser = new EdiParser(ediFile837p)) {
            // Parse all claims in the file
            claims = parser.parse().claims();
        }
        Claim claim = claims.get(0);
        PlaceOfServiceType pos = claim.placeOfServiceType();
        assertThat(pos).isEqualTo(PlaceOfServiceType.OFFICE);

        PatientSubscriber patient = claim.subscriber();

        EntityRole entityRole = patient.person().entityRole();
        assertThat(entityRole).isEqualTo(EntityRole.INSURED_SUBSCRIBER);
        // Use ediCode to get the actual EDI qualifier
        String ediQualifierCode = entityRole.ediValue();
        log.info("Entity Role: {} EDI Qualifier Code: {}", entityRole, ediQualifierCode);

        EntityType entityType = patient.person().entityType();
        assertThat(entityType).isEqualTo(EntityType.INDIVIDUAL);

        GenderType genderType = patient.person().gender();
        assertThat(genderType).isEqualTo(GenderType.MALE);
    }
}