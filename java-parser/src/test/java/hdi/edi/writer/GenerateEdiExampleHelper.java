package hdi.edi.writer;

import hdi.edi.ediwriter.EdiWriter;
import hdi.edi.parser.TransactionType;
import hdi.model.control.FunctionalGroup;
import hdi.model.control.InterchangeControl;

public class GenerateEdiExampleHelper {
    public static void writeIsaAndGs(EdiWriter ediWriter, TransactionType transactionType) {
        // EDI writer will assign a unique interchange control number
        var isa = new InterchangeControl("ZZ", "123", "ZZ", "456");
        // EDI writer will assign a unique group control number
        var gs = new FunctionalGroup(transactionType, "1", "2");
        ediWriter.writeIsa(isa);
        ediWriter.writeFunctionalGroup(gs);
    }
}