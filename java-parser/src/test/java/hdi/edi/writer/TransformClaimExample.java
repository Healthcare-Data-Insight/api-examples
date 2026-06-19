package hdi.edi.writer;

import hdi.edi.ediwriter.EdiWriter;
import hdi.edi.parser.EdiParser;
import hdi.edi.parser.EdiParsingResults;
import hdi.edi.parser.ParsingExampleHelper;
import hdi.edi.parser.TransactionType;
import hdi.model.claim.Claim;
import hdi.model.control.FunctionalGroup;
import hdi.model.control.InterchangeControl;
import org.apache.commons.io.FileUtils;
import org.junit.Test;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.math.BigDecimal;
import java.nio.charset.Charset;
import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

@SuppressWarnings("NewClassNamingConvention")
// Parse 837, update fields and generate new 837
public class TransformClaimExample implements ParsingExampleHelper {

    @Test
    public void parseAndGenerate837pEdi() throws IOException {
        File inEdiFile = new File(EDI_FILES_DIR, "/837/837p-all-fields.dat");
        File outEdiFile = new File(OUT_EDI_FILES_DIR, "837p-generated.edi");
        try (var parser = new EdiParser(inEdiFile);
             var fileWriter = new FileWriter(outEdiFile);
             var ediWriter = new EdiWriter(fileWriter)) {
            boolean isDone = false;
            while (!isDone) {
                EdiParsingResults parsingResults = parser.parse(100);
                writeIsaAndGs(ediWriter, TransactionType.PROF);

                List<Claim> claims = parsingResults.claims();
                for (var claim : claims) {
                    var transaction = claim.transaction();
                    // update transaction date and time
                    transaction.creationDate(LocalDate.now());
                    transaction.creationTime(LocalTime.now());
                    // update application transaction ID and sender if needed
                    transaction.originatorApplicationTransactionId("MyApplicationId");
                    ediWriter.writeTransaction(transaction);
                    // update the claim: we will increase the charge amount by 10%
                    BigDecimal totalChargeAmount = BigDecimal.ZERO;
                    for (var line : claim.lines()) {
                        line.chargeAmount(line.chargeAmount().multiply(BigDecimal.valueOf(1.1)));
                        totalChargeAmount = totalChargeAmount.add(line.chargeAmount());
                    }
                    claim.chargeAmount(totalChargeAmount);
                    var validationIssues = ediWriter.writeClaim(claim);
                    printValidationIssues(validationIssues);

                }
                isDone = parsingResults.isDone();
            }
        }
        var s = FileUtils.readFileToString(outEdiFile, Charset.defaultCharset());
        System.out.println(s);
    }


    private void writeIsaAndGs(EdiWriter ediWriter, TransactionType transactionType) {
        // EDI writer will assign a unique interchange control number
        var isa = new InterchangeControl("ZZ", "123", "ZZ", "456");
        // EDI writer will assign a unique group control number
        var gs = new FunctionalGroup(transactionType, "1", "2");
        ediWriter.writeIsa(isa);
        ediWriter.writeFunctionalGroup(gs);
    }

}