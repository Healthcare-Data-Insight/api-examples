package hdi.edi.parser;

import hdi.edi.converter.EdiFileConverter;
import hdi.edi.converter.NamedWriter;
import hdi.edi.converter.OutputFormat;
import hdi.edi.csv.ConversionSchema;
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

    public static final File OUT_DIR = new File("converted");

    @Test
    public void convertSingleFileToJson() {
        var ediFile = new File(EDI_FILES_DIR, "/837/prof-encounter.dat");
        var converter = new EdiFileConverter(OutputFormat.JSON);
        converter.convertFile(ediFile, OUT_DIR);
    }

    @Test
    public void convertMultipleFilesToJsonLines() {
        var converter = new EdiFileConverter(OutputFormat.JSONL)
                // Write parsing warnings to the output, see https://datainsight.health/docs/ediconvert-api/user-guide/#error-handling for more details
                .isSerializeParsingIssues(true);

        // Convert each file into a corresponding JSON file. If the output file is an existing directory, each file will be converted individually
        converter.convertFiles(new File(EDI_FILES_DIR + "/837"), "*.dat", false, OUT_DIR);

        // Convert all files into a single JSON file. The output file must not be an existing directory
        var outFile = new File(OUT_DIR, "all-837");
        converter.convertFiles(new File(EDI_FILES_DIR + "/837"), "*.dat", false, outFile);
    }

    @Test
    public void convertMultipleFilesToCsv() {
        var converter = new EdiFileConverter(OutputFormat.CSV)
                .csvConversionSchemaName("default");

        // Convert all files into a single CSV file. By default, the converter creates two files, one for claims and one for lines (*-Lines.csv)
        var outFile = new File(OUT_DIR, "all-837.csv");
        converter.convertFiles(new File(EDI_FILES_DIR + "/837/"), "*.dat", false, outFile);

        outFile = new File(OUT_DIR, "all-837-claims-and-lines.csv");
        // Change the conversion schema to produce a single CSV file with claim-level data repeating for each line
        converter.csvConversionSchemaName(ConversionSchema.SINGLE_FILE_REPEAT_ALL_SCHEMA_NAME);
        converter.convertFiles(new File(EDI_FILES_DIR + "/837/"), "*.dat", false, outFile);
    }

    // If you want to convert to a non-file output, you can provide your own writer
    @Test
    public void convertMultipleFilesToWriter() {
        var converter = new EdiFileConverter(OutputFormat.JSON)
                .isSerializeParsingIssues(true);

        StringWriter stringWriter = new StringWriter();
        var writer = new NamedWriter("String", stringWriter);

        // Convert all files into a Writer
        converter.convertFiles(new File(EDI_FILES_DIR + "/837"), "*.dat", false, writer);
        System.out.println(stringWriter);
    }
}