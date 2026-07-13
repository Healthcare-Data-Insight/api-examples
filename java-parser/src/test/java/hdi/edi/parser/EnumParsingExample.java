package hdi.edi.parser;

import hdi.model.PlaceOfServiceType;
import hdi.model.claim.Claim;
import hdi.model.orgperson.EntityRole;
import hdi.model.orgperson.EntityType;
import hdi.model.orgperson.GenderType;
import hdi.model.patientsubscriber.PatientSubscriber;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

import java.io.File;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;


@SuppressWarnings("NewClassNamingConvention")
@Slf4j
public class EnumParsingExample implements ParsingExampleHelper {
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