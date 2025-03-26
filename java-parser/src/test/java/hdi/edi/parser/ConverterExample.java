package hdi.edi.parser;

import hdi.edi.cli.EdiFileConverter;
import hdi.edi.cli.NameAndWriter;
import org.junit.Test;

import java.io.File;
import java.io.StringWriter;


/**
 * Example of converting EDI files to JSON/CSV in bulk.
 * EdiFileConverter provides the same functionality as our CLI, the output is the same.
 * Converter's arguments correspond to CLI options, see https://datainsight.health/docs/ediconvert-cli/ for more details
 */
@SuppressWarnings("NewClassNamingConvention")
public class ConverterExample implements ParsingExampleHelper {

    public static final File OUT_DIR = new File("edi-json");
    // How many claims/payments to convert in one go
    public static final int CHUNK_SIZE = 200;

    @Test
    public void convertSingleFileToJson() {
        var ediFile = new File(EDI_FILES_DIR + "/837/prof-encounter.dat");

        var converter = new EdiFileConverter(
                CHUNK_SIZE,
                true, // use NDJSON/JSON lines instead of JSON array
                false, // Format JSON with indentation
                false // true if converting to CSV, otherwise JSON
        );
        // We need to set the split mode for large transactions
        converter.isSplitMode(true)
                // Write parsing warnings to the output, see https://datainsight.health/docs/ediconvert-api/user-guide/#error-handling for more details
                .isSerializeParsingIssues(true);

        var outFile = new File(OUT_DIR, "prof-encounter.json");

        converter.convertFiles(ediFile, // input EDI file or a directory
                null, // Glob patterns if converting multiple files
                false, // Recursively search for files
                outFile, // output file or a directory
                null    // Writer if converting to something other than files
        );
    }

    @Test
    public void convertMultipleFilesToJson() {
        var converter = new EdiFileConverter(CHUNK_SIZE, true, false, false);
        // We need to set the split mode for large transactions
        converter.isSplitMode(true)
                // Write parsing warnings to the output
                .isSerializeParsingIssues(true);

        // Convert each file into a corresponding JSON file. If the output file is an existing directory, each file will be converted individually
        converter.convertFiles(new File(EDI_FILES_DIR + "/837"), "*.dat", false, OUT_DIR, null);

        // Convert all files into a single JSON file. The output file must not be an existing directory
        var outFile = new File(OUT_DIR, "all-837.json");
        converter.convertFiles(new File(EDI_FILES_DIR + "/837"), "*.dat", false, outFile, null);
    }

    // If you want to convert to a non-file output, you can provide your own writer
    @Test
    public void convertMultipleFilesToJsonWriter() {
        var converter = new EdiFileConverter(CHUNK_SIZE, true, false, false);
        // We need to set the split mode for large transactions
        converter.isSplitMode(true)
                // Write parsing warnings to the output
                .isSerializeParsingIssues(true);

        StringWriter stringWriter = new StringWriter();
        var writer = new NameAndWriter("String", stringWriter);

        // Convert all files into a Writer
        converter.convertFiles(new File(EDI_FILES_DIR + "/837"), "*.dat", false, null, writer);

        System.out.println(stringWriter);
    }


}