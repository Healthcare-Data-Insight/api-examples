package hdi.edi.parser;

import hdi.edi.cli.EdiFileConverter;
import org.junit.Test;

import java.io.File;

@SuppressWarnings("NewClassNamingConvention")
public class ConverterExample implements ParsingExampleHelper {

    public static final File OUT_DIR = new File("edi-json");
    // How many claims/payments to convert in one go
    public static final int CHUNK_SIZE = 200;

    @Test
    public void convertSingleFileToJson() {
        var ediFile = new File(EDI_FILES_DIR + "/837/prof-encounter.dat");

        var converter = new EdiFileConverter(CHUNK_SIZE, true, false, false);
        // We need to set the split mode for large transactions
        converter.isSplitMode(true)
                // Write parsing warnings to the output
                .isSerializeParsingIssues(true);

        var outFile = new File(OUT_DIR, "prof-encounter.json");
        converter.convertFiles(ediFile, null, false, outFile, null);
    }

    @Test
    public void convertMultipleFilesToJson() {
        var converter = new EdiFileConverter(CHUNK_SIZE, true, false, false);
        // We need to set the split mode for large transactions
        converter.isSplitMode(true)
                // Write parsing warnings to the output
                .isSerializeParsingIssues(true);

        // Convert each file into a corresponding JSON file
        converter.convertFiles(new File(EDI_FILES_DIR + "/837"), "*.dat", false, OUT_DIR, null);
        // Convert all files into one JSON
        var outFile = new File(OUT_DIR, "all-837.json");
        converter.convertFiles(new File(EDI_FILES_DIR + "/837"), "*.dat", false, outFile, null);
    }
}