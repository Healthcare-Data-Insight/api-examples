package hdi.edi.csv.sql;

import hdi.edi.csv.ConversionSchema;
import hdi.edi.csv.CsvConverter;
import hdi.edi.csv.SchemaHolder;
import hdi.edi.parser.EdiParser;
import hdi.edi.parser.EdiParsingResults;
import hdi.edi.parser.ParsingExampleHelper;
import hdi.edi.parser.TransactionType;
import hdi.model.claim.Claim;
import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

import java.io.File;
import java.io.IOException;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.List;

/**
 * Example demonstrating loading CSV directly into a SQL database.
 */
@Slf4j
public class SqlConverterTest implements ParsingExampleHelper {

    // This schema can be used to test conversion with a subset of fields
    final SchemaHolder schemaHolder = SchemaHolder.loadSchemas("csv_conversion_sql.yaml");

    @Test
    public void insertClaimsTwoTables() {
        parseAndInsert(new File(EDI_FILES_DIR, "/837/837p-all-fields.dat"));
    }

    @SneakyThrows({SQLException.class, IOException.class})
    public void parseAndInsert(File edi837File) {
        String url = "jdbc:sqlserver://localhost;databaseName=claims;trustServerCertificate=true;";
        String user = "SA";
        String password = "SAStrong@Passw0rd";

        var schema = schemaHolder.findSchema(ConversionSchema.DEFAULT_SCHEMA_NAME, TransactionType.PROF);
        try (var parser = new EdiParser(edi837File);
             var connection = DriverManager.getConnection(url, user, password);
             var outputMgr = new SqlOutputMgr(schema, connection)) {
            connection.setAutoCommit(false);

            boolean isDone = false;
            var converter = new CsvConverter(outputMgr.schema(), outputMgr);
            while (!isDone) {
                EdiParsingResults parsingResults = parser.parse(100);
                List<Claim> claims = parsingResults.claims();
                converter.convert(claims);
                var issues = parsingResults.parsingIssues();
                for (var issue : issues) {
                    log.warn("Parsing issue: {}", issue.message());
                }
                // Commit each chunk
                connection.commit();
                isDone = parsingResults.isDone();
            }
            log.info("Insert counts: {}", outputMgr.counts());
        }

    }

}