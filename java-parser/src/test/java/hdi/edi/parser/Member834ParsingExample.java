package hdi.edi.parser;

import hdi.model.coverage.HealthCoverage;
import hdi.model.coverage.Member;
import hdi.model.coverage.MemberCoverage;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

import java.io.File;
import java.util.List;

@SuppressWarnings("NewClassNamingConvention")
@Slf4j
public class Member834ParsingExample implements ParsingExampleHelper {

    @Test
    public void parse834() {
        var ediFile834 = new File(EDI_FILES_DIR + "/834/834-all-fields.edi");
        List<MemberCoverage> memberCoverages;
        try (var parser = new EdiParser(ediFile834)) {
            boolean isDone = false;
            while (!isDone) {
                // parse 100 members at a time
                EdiParsingResults parsingResults = parser.parse(100);
                memberCoverages = parsingResults.memberCoverages();
                for (var memberCoverage : memberCoverages) {
                    processMemberCoverage(memberCoverage);
                }
                // Parsing issues
                var issues = parsingResults.parsingIssues();
                for (var issue : issues) {
                    log.warn("Parsing issue: {}", issue.message());
                }
                isDone = parsingResults.isDone();
            }
        }
    }

    private void processMemberCoverage(MemberCoverage memberCoverage) {
        String sponsorId = memberCoverage.sponsor().identifier();
        String insurerId = memberCoverage.insurer().identifier();
        String memberIdentifier = memberCoverage.identifier();
        String memberGroup = memberCoverage.groupOrPolicyNumber();

        assertNotNull(sponsorId, insurerId, memberIdentifier, memberGroup);
        log.info("* {} {} {} {}", sponsorId, insurerId, memberIdentifier, memberGroup);
        Member member = memberCoverage.member();
        log.info("Member:\n{}", member);
        List<HealthCoverage> healthCoverages = memberCoverage.healthCoverages();
        for (var healthCoverage : healthCoverages) {
            // HealthCoverage: HD segment and related segments and loops (2300)
            log.info("Health coverage:\n{}", healthCoverage);
        }
    }
}