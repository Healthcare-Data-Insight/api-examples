package hdi.edi.parser;

import hdi.model.coverage.HealthCoverage;
import hdi.model.coverage.MemberCoverage;
import org.junit.Test;

import java.io.File;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@SuppressWarnings("NewClassNamingConvention")
public class Member834ParsingExample implements ParsingExampleHelper {

    @Test
    public void parse834() {
        var ediFile834 = new File(EDI_FILES_DIR + "/834/834-all-fields.edi");
        List<MemberCoverage> memberCoverages;
        try (var parser = new EdiParser(ediFile834).isSplitMode(true)) {
            memberCoverages = parser.parse(-1).memberCoverages();
        }
        assertThat(memberCoverages).isNotEmpty();
        MemberCoverage memberCoverage = memberCoverages.get(0);

        String sponsorId = memberCoverage.sponsor().identifier();
        String insurerId = memberCoverage.insurer().identifier();
        String memberIdentifier = memberCoverage.identifier();
        String memberGroup = memberCoverage.groupOrPolicyNumber();

        assertNotNull(sponsorId, insurerId, memberIdentifier, memberGroup);
        List<HealthCoverage> healthCoverages = memberCoverage.healthCoverages();
        assertThat(healthCoverages).isNotEmpty();
        // HealthCoverage: HD segment and related segments and loops (2300)
        HealthCoverage healthCoverage = healthCoverages.get(0);
        System.out.println(healthCoverage);
    }
}