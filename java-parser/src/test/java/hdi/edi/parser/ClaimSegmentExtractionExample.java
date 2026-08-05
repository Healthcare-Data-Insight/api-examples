package hdi.edi.parser;

import hdi.model.claim.Claim;
import hdi.model.enumtype.UnitType;
import hdi.model.orgperson.OrgOrPerson;
import hdi.model.patientsubscriber.RelationshipType;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

import java.io.File;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

/**
 * Advanced example of extracting claim segments from EDI 837 files.
 */
@SuppressWarnings("NewClassNamingConvention")
@Slf4j
public class ClaimSegmentExtractionExample implements ParsingExampleHelper {

    @Test
    public void parse837p() {
        parse837(new File(EDI_FILES_DIR, "/837/837p-all-fields.dat"));
    }

    @Test
    public void parse837i() {
        parse837(new File(EDI_FILES_DIR, "/837/837i-all-fields.dat"));
    }

    public void parse837(File edi837File) {
        log.info("* Parsing EDI 837 file: {}", edi837File.getName());
        try (var parser = new EdiParser(edi837File)
                // enable validation mode
                .isValidationMode(true)) {
            EdiParsingResults parsingResults;
            do {
                parsingResults = parser.parse(DEFAULT_CHUNK_SIZE);
                var claims = parsingResults.claims();
                for (var claim : claims) {
                    processClaim(claim);
                }
                // Extract HI segments from the parsed EDI file
                var claimSegsList = extractSegments(parsingResults, claims, SegmentType.HI);
                for (var claimSegs : claimSegsList) {
                    System.out.println(claimSegs.claim.patientControlNumber());
                    System.out.println(claimSegs.segsToEdiStr());
                }
            } while (!parsingResults.isDone());
        }
    }

    private List<ClaimSegs> extractSegments(EdiParsingResults parsingResults, List<Claim> claims, SegmentType segmentType) {
        List<ClaimSegs> claimSegs = new ArrayList<>();
        int claimI = 0;
        for (var seg : parsingResults.segs()) {
            if (seg.isInType(SegmentType.ST)) {
                var clmSegs = seg.findChildSegs(SegmentType.CLM);
                for (var clmSeg : clmSegs) {
                    var hiSegs = clmSeg.findChildSegs(segmentType);
                    claimSegs.add(new ClaimSegs(claims.get(claimI), hiSegs));
                    ++claimI;
                }
            }
        }
        return claimSegs;
    }

    record ClaimSegs(Claim claim, List<EdiSeg> segs) {
        private String segsToEdiStr() {
            return segs.stream().map(EdiSeg::rawStringWithSegID).collect(Collectors.joining("\n"));
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
}