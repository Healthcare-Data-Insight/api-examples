package hdi.edi.csv.sql;

import hdi.edi.csv.ConversionSchema;
import hdi.edi.csv.CsvConverter;
import hdi.edi.csv.SchemaHolder;
import hdi.edi.parser.EdiParser;
import hdi.edi.parser.EdiParsingResults;
import hdi.edi.parser.TransactionType;
import lombok.extern.slf4j.Slf4j;

import java.io.File;
import java.sql.DriverManager;
import java.util.List;

/**
 * 837 parsing examples See JSON schemas for X12 EDI mapping documentation:
 * <a href="https://datainsight.health/docs/schemas/837p/">837P Schema</a>
 * <a href="https://datainsight.health/docs/schemas/837i/">837I Schema</a>
 */

@Slf4j
public class Claim837ParserYear2026 /*extends AbstractClaimParser implements IEDIDocumentEvaluator*/ {


    String OUT_EDI_FILES_DIR = "../out_edi_files";

    final SchemaHolder schemaHolder = SchemaHolder.loadSchemas();
//    final SchemaHolder schemaHolder = SchemaHolder.loadSchemas("csv_conversion_sql.yaml");

    public void parse837(File edi837File, Long etlSourceId, Long transactionId) throws Exception {
        log.info("* Parsing EDI 837 file: " + edi837File.getName());

        String url = "jdbc:sqlserver://localhost;databaseName=claims;trustServerCertificate=true;";
        String user = "SA";
        String password = "SAStrong@Passw0rd";

        // String url =
        // "jdbc:sqlserver://localhost;databaseName=claims;trustServerCertificate=true;";
        // String user = "SA";
        // String password = "SAStrong@Passw0rd";
        log.debug("Connecting to database: " + url + " user: " + user);

        var schema = schemaHolder.findSchema(ConversionSchema.DEFAULT_SCHEMA_NAME, TransactionType.PROF);

        try (var parser = new EdiParser(edi837File);
             var connection = DriverManager.getConnection(url, user, password);
             var outputMgr = new SqlOutputMgrCust(schema, connection, etlSourceId, transactionId)) {

            connection.setAutoCommit(true);

            boolean isDone = false;

            var converter = new CsvConverter(outputMgr.getSchema(), outputMgr);
            while (!isDone) {
                log.info("Parsing EDI 837 file: " + edi837File.getName() + " next 100 records");

                EdiParsingResults parsingResults = parser.parse(100);

                List<hdi.model.claim.Claim> claims = parsingResults.claims();
                converter.convert(claims);

                var issues = parsingResults.parsingIssues();
                for (var issue : issues) {
                    log.warn("Parsing issue: " + issue.message());
                }

                log.debug("Parsed " + claims.size() + " claims, " + issues.size() + " issues.");
                // Commit each chunk
                // connection.commit();
                isDone = parsingResults.isDone();
            }

            log.info("Insert counts: " + outputMgr.getCounts());
        }
    }
}