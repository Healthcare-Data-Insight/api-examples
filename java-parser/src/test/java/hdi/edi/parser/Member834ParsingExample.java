package hdi.edi.parser;

import hdi.edi.EdiTransaction;
import hdi.edi.validation.ValidationIssue;
import hdi.model.control.FunctionalGroup;
import hdi.model.control.InterchangeControl;
import hdi.model.coverage.HealthCoverage;
import hdi.model.coverage.Member;
import hdi.model.coverage.MemberCoverage;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

import java.io.File;
import java.time.LocalDateTime;
import java.util.Collection;
import java.util.List;

@SuppressWarnings("NewClassNamingConvention")
@Slf4j
public class Member834ParsingExample implements ParsingExampleHelper {

    @Test
    public void parse834() {
        var ediFile834 = new File(EDI_FILES_DIR + "/834/834-all-fields.edi");
        try (var parser = new EdiParser(ediFile834)
                .isValidationMode(true)) {
            EdiParsingResults parsingResults;
            do {
                // parse 20 members at a time
                parsingResults = parser.parse(DEFAULT_CHUNK_SIZE);
                // "rootObjs" contains all objects parsed from EDI in the order they appear in the EDI file
                // process all transactions, members, and control segments
                for (var rootObj : parsingResults.rootObjs()) {
                    // MemberCoverage represents INS segment and all related segments
                    if (rootObj instanceof MemberCoverage memberCoverage) {
                        processMemberCoverage(memberCoverage);
                    }
                    else if (rootObj instanceof EdiTransaction transaction && transaction.transactionType() == TransactionType.MEMBER_COVERAGE) {
                        process834Transaction(transaction);
                    }
                    else if (rootObj instanceof InterchangeControl interchangeControl) {
                        log.info("ISA segment info:\n{}", interchangeControl);
                    }
                    else if (rootObj instanceof FunctionalGroup functionalGroup) {
                        log.info("GS segment info:\n{}", functionalGroup);
                    }
                    // validation issue at the transaction level
                    else if (rootObj instanceof ValidationIssue validationIssue) {
                        // validation issues are logged by the parser; here you can do additional processing
                    }
                    else {
                        throw new IllegalStateException("Unexpected object for 837 transaction: " + rootObj);
                    }
                }
            } while (!parsingResults.isDone());
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
        // Validation issues for this member
        processValidationIssues(memberCoverage, memberCoverage.validationIssues());
    }

    private void process834Transaction(EdiTransaction transaction) {
        String controlNumber = transaction.controlNumber();
        LocalDateTime transactionDateTime = transaction.getCreationDateTime();
        log.info("Transaction: {} {}", controlNumber, transactionDateTime);
    }

    // All validations are logged automatically, here you can do additional processing
    private void processValidationIssues(MemberCoverage memberCoverage, Collection<ValidationIssue> issues) {
        // your logic here
    }
}