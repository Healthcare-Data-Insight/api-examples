package hdi.edi.parser;

import hdi.model.PlaceOfServiceType;
import hdi.model.claim.Claim;
import hdi.model.enumtype.UnitType;
import hdi.model.orgperson.EntityRole;
import hdi.model.orgperson.EntityType;
import hdi.model.orgperson.GenderType;
import hdi.model.orgperson.OrgOrPerson;
import hdi.model.patientsubscriber.PatientSubscriber;
import org.junit.Test;

import java.io.File;
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@SuppressWarnings("NewClassNamingConvention")
public class ClaimParsingExample implements ParsingExampleHelper {

    @Test
    public void parseClaim() {
        var ediFile837p = new File(EDI_FILES_DIR + "/837/prof-encounter.dat");
        var parser = new EdiParser(ediFile837p);
        // Parse all claims in the file
        List<Claim> claims = parser.parse837(-1);
        assertThat(claims).isNotEmpty();

        Claim claim = claims.get(0);
        // get some key attributes of the claim
        BigDecimal billedAmount = claim.chargeAmount();
        String patientControlNumber = claim.patientControlNumber();
        // Providers
        OrgOrPerson billingProvider = claim.billingProvider();
        String providerNpi = billingProvider.identifier();
        assertNotNull(billedAmount, patientControlNumber, providerNpi);
        // Service lines
        for (var line : claim.lines()) {
            String procedureCode = line.procedure().code();
            LocalDate serviceDate = line.serviceDateFrom();
            BigDecimal unitCount = line.unitCount();
            UnitType unitType = line.unitType();
            BigDecimal lineChargeAmount = line.chargeAmount();

            assertNotNull(procedureCode, serviceDate, unitCount, unitType, lineChargeAmount);
        }

    }

    /**
     * For large files, we can parse in batches of N claims
     */
    @Test
    public void parseInBatches() {
        var ediFile = new File(EDI_FILES_DIR + "/837/multi-tran.dat");
        int claimCount = 0;
        var parser = new EdiParser(ediFile);
        while (true) {
            // parse two claim at a time
            var claims = parser.parse837(2);
            if (claims.isEmpty()) {
                break;
            }
            // your logic goes here
            // ...
            claimCount += claims.size();
        }

        assertThat(claimCount).isEqualTo(3);
    }


    /**
     * The parser translates EDI qualifiers and some of the codes to Java enums
     */
    @Test
    public void parseEnums() {
        var ediFile837p = new File(EDI_FILES_DIR + "/837/prof-encounter.dat");
        var parser = new EdiParser(ediFile837p);
        List<Claim> claims = parser.parse837(-1);
        Claim claim = claims.get(0);
        PlaceOfServiceType pos = claim.placeOfServiceType();
        assertThat(pos).isEqualTo(PlaceOfServiceType.OFFICE);

        PatientSubscriber patient = claim.subscriber();

        EntityRole entityRole = patient.person().entityRole();
        assertThat(entityRole).isEqualTo(EntityRole.SUBSCRIBER);

        EntityType entityType = patient.person().entityType();
        assertThat(entityType).isEqualTo(EntityType.INDIVIDUAL);

        GenderType genderType = patient.person().gender();
        assertThat(genderType).isEqualTo(GenderType.MALE);
    }


}