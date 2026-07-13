package hdi.edi.csv.sql;

import hdi.edi.csv.ConversionSchema;
import hdi.edi.csv.OutputMgr;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;

import java.io.Closeable;
import java.io.IOException;
import java.sql.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import static hdi.edi.csv.ConversionSchema.HEADER_LIST_NAME;
import static hdi.edi.csv.ConversionSchema.LINE_LIST_NAME;

/**
 * Manages SQL database output for CSV conversion operations.
 * <p>
 * This class handles writing parsed EDI claim data directly into SQL database tables.
 * It generates and executes INSERT statements based on the conversion schema, supporting
 * multiple list types (headers and lines) that map to different database tables.
 * </p>
 * <p>
 * The class maintains prepared statements for each list type and tracks the number of
 * rows inserted. It automatically maps CSV headers to database columns and handles
 * special column name transformations (e.g., "Id" to "converterClaimId").
 * </p>
 *
 * @see OutputMgr
 * @see ConversionSchema
 */
@Slf4j
public class SqlOutputMgrCust implements Closeable, OutputMgr {

    /**
     * The conversion schema that defines the structure and mapping rules for the data.
     */

    final ConversionSchema schema;
    /**
     * The JDBC database connection used for executing SQL statements.
     */
    final Connection connection;
    /**
     * Cache of prepared INSERT statements, keyed by list name (e.g., "header", "line").
     */
    final Map<String, PreparedStatement> insertStmts = new HashMap<>();
    /**
     * Tracks the number of rows inserted for each list type.
     */
    final Map<String, Integer> counts = new HashMap<>();

    Long generatedKey = null;

    /**
     * Revised by M365 Copilot
     * This stores CI_CLAIM_FILE_TRANSACTION.id
     * and will be inserted into TransactionID column for header rows.
     */
    private final Long transactionId;

    /**
     * Revised by M365 Copilot
     * This stores source manager id and will be inserted into EtlSourceID for header rows.
     */
    private final Long etlSourceId;


    /**
     * Constructs a new SQL output manager.
     *
     * @param schema     the conversion schema defining data structure and mappings
     * @param connection the JDBC database connection to use for inserts
     */
    /** Old
     public SqlOutputMgr(ConversionSchema schema, Connection connection) {
     this.schema = schema;
     this.connection = connection;
     }
     **/


    /**
     * Revised by M365 Copilot
     * Updated constructor to accept etlSourceId and transactionId.
     */
    public SqlOutputMgrCust(ConversionSchema schema, Connection connection, Long etlSourceId, Long transactionId) {
        this.schema = schema;
        this.connection = connection;
        this.etlSourceId = etlSourceId;
        this.transactionId = transactionId;
    }

    /**
     * Processes headers for a given list and generates the corresponding SQL INSERT statement.
     * This method is invoked once for each list type before any data rows are written.
     *
     * @param listName the name of the list (e.g., "header", "line")
     * @param row      the header row containing column names (not used in current implementation)
     * @throws SQLException if SQL generation or statement preparation fails
     */

    @Override
    public void writeHeaders(String listName, List<String> row) {
        try {
            generateSql(listName);
        } catch (SQLException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }

    /**
     * Generates and prepares an INSERT SQL statement for the specified list type.
     * Maps list names to table names and creates parameterized statements with placeholders.
     *
     * @param listName the name of the list to generate SQL for
     * @throws SQLException             if statement preparation fails
     * @throws IllegalArgumentException if the list name is not recognized
     */
    private void generateSql(String listName) throws SQLException {

        String tableName = "";
        if (listName.equalsIgnoreCase(HEADER_LIST_NAME)) {
            tableName = "lz_claim";
        }
        else if (listName.equalsIgnoreCase(LINE_LIST_NAME)) {
            tableName = "lz_claim_lines";
        }
        else {
            throw new IllegalArgumentException("Invlid listname passed");
        }

        List<String> columnNames = tableName.equals("lz_claim") ? createColumnNames(listName) : createColumnNamesLines(listName);
        String columns = StringUtils.join(columnNames, ",");
        String placeholders = StringUtils.repeat("?", ",", columnNames.size());
        var sql = "insert into " + tableName + " (" + columns + ") values (" + placeholders + ")";
        log.info("Generated SQL for list " + listName + ", \n " + sql);
        // Prepare statement so we can retrieve autogenerated primary keys after insert
        var stmt = connection.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS);

        insertStmts.put(listName, stmt);
    }

    /**
     * Creates a list of database column names from the schema headers for a given list.
     * Applies special transformations, such as renaming "Id" to "converterClaimId".
     *
     * @param listName the name of the list to get column names for
     * @return a list of column names to use in SQL statements
     */
    private List<String> createColumnNames(String listName) {
        var headers = schema.headers().get(listName);

        List<String> columnNames = new ArrayList<>();

        for (var header : headers) {
            String columnName = (String) header;
            /*
            if (columnName.equalsIgnoreCase("ClaimId")) { //Field name in CSV file (case doesn't matter)
                columnName = "ClaimId"; // database column name (Case sensitive)
            }
            if (columnName.equalsIgnoreCase("TransactionID")) { //Field name in CSV file (case doesn't matter)
                columnName = "TransactionID"; // database column name (Case sensitive)
            }
            */

            if (columnName.equalsIgnoreCase("Id")) {
                columnName = "Id";
            }
            if (columnName.equalsIgnoreCase("TransactionType")) {
                columnName = "TransactionType";
            }
            if (columnName.equalsIgnoreCase("FileName")) {
                columnName = "FileName";
            }
            if (columnName.equalsIgnoreCase("TransactionControlNumber")) {
                columnName = "TransactionControlNumber";
            }
            if (columnName.equalsIgnoreCase("TransactionSetPurposeCode")) {
                columnName = "TransactionSetPurposeCode";
            }
            if (columnName.equalsIgnoreCase("OriginatorApplicationTransactionId")) {
                columnName = "OriginatorApplicationTransactionId";
            }
            if (columnName.equalsIgnoreCase("TransactionCreationDateTime")) {
                columnName = "TransactionCreationDateTime";
            }
            if (columnName.equalsIgnoreCase("ClaimOrEncounterIdentifierType")) {
                columnName = "ClaimOrEncounterIdentifierType";
            }
            if (columnName.equalsIgnoreCase("PatientControlNumber")) {
                columnName = "PatientControlNumber";
            }
            if (columnName.equalsIgnoreCase("ChargeAmount")) {
                columnName = "ChargeAmount";
            }
            if (columnName.equalsIgnoreCase("PlaceOfService")) {
                columnName = "PlaceOfService";
            }
            if (columnName.equalsIgnoreCase("FacilityCode")) {
                columnName = "FacilityCode";
            }
            if (columnName.equalsIgnoreCase("FrequencyTypeCode")) {
                columnName = "FrequencyTypeCode";
            }
            if (columnName.equalsIgnoreCase("ProviderSignatureIndicator")) {
                columnName = "ProviderSignatureIndicator";
            }
            if (columnName.equalsIgnoreCase("AssignmentParticipationCode")) {
                columnName = "AssignmentParticipationCode";
            }
            if (columnName.equalsIgnoreCase("AssignmentCertificationIndicator")) {
                columnName = "AssignmentCertificationIndicator";
            }
            if (columnName.equalsIgnoreCase("ReleaseOfInformationCode")) {
                columnName = "ReleaseOfInformationCode";
            }
            if (columnName.equalsIgnoreCase("DelayReasonCode")) {
                columnName = "DelayReasonCode";
            }
            if (columnName.equalsIgnoreCase("BillingProviderIdentificationType")) {
                columnName = "BillingProviderIdentificationType";
            }
            if (columnName.equalsIgnoreCase("BillingProviderIdentifier")) {
                columnName = "BillingProviderIdentifier";
            }
            if (columnName.equalsIgnoreCase("BillingProviderTaxId")) {
                columnName = "BillingProviderTaxId";
            }
            if (columnName.equalsIgnoreCase("BillingProviderLastNameOrOrgName")) {
                columnName = "BillingProviderLastNameOrOrgName";
            }
            if (columnName.equalsIgnoreCase("BillingProviderFirstName")) {
                columnName = "BillingProviderFirstName";
            }
            if (columnName.equalsIgnoreCase("BillingProviderMiddleName")) {
                columnName = "BillingProviderMiddleName";
            }
            if (columnName.equalsIgnoreCase("BillingProviderAddressLine")) {
                columnName = "BillingProviderAddressLine";
            }
            if (columnName.equalsIgnoreCase("BillingProviderAddressLine2")) {
                columnName = "BillingProviderAddressLine2";
            }
            if (columnName.equalsIgnoreCase("BillingProviderAddressCity")) {
                columnName = "BillingProviderAddressCity";
            }
            if (columnName.equalsIgnoreCase("BillingProviderAddressStateCode")) {
                columnName = "BillingProviderAddressStateCode";
            }
            if (columnName.equalsIgnoreCase("BillingProviderAddressZipCode")) {
                columnName = "BillingProviderAddressZipCode";
            }
            if (columnName.equalsIgnoreCase("BillingProviderProviderTaxonomyCode")) {
                columnName = "BillingProviderProviderTaxonomyCode";
            }
            if (columnName.equalsIgnoreCase("BillingProviderContact1Name")) {
                columnName = "BillingProviderContact1Name";
            }
            if (columnName.equalsIgnoreCase("BillingProviderContact1ContactNumber1Type")) {
                columnName = "BillingProviderContact1ContactNumber1Type";
            }
            if (columnName.equalsIgnoreCase("BillingProviderContact1ContactNumber1Number")) {
                columnName = "BillingProviderContact1ContactNumber1Number";
            }
            if (columnName.equalsIgnoreCase("BillingProviderContact1ContactNumber2Type")) {
                columnName = "BillingProviderContact1ContactNumber2Type";
            }
            if (columnName.equalsIgnoreCase("BillingProviderContact1ContactNumber2Number")) {
                columnName = "BillingProviderContact1ContactNumber2Number";
            }
            if (columnName.equalsIgnoreCase("BillingProviderContact2Name")) {
                columnName = "BillingProviderContact2Name";
            }
            if (columnName.equalsIgnoreCase("BillingProviderContact2ContactNumber1Type")) {
                columnName = "BillingProviderContact2ContactNumber1Type";
            }
            if (columnName.equalsIgnoreCase("BillingProviderContact2ContactNumber1Number")) {
                columnName = "BillingProviderContact2ContactNumber1Number";
            }
            if (columnName.equalsIgnoreCase("BillingProviderContact2ContactNumber2Type")) {
                columnName = "BillingProviderContact2ContactNumber2Type";
            }
            if (columnName.equalsIgnoreCase("BillingProviderContact2ContactNumber2Number")) {
                columnName = "BillingProviderContact2ContactNumber2Number";
            }
            if (columnName.equalsIgnoreCase("BillingProviderAdditionalId1Type")) {
                columnName = "BillingProviderAdditionalId1Type";
            }
            if (columnName.equalsIgnoreCase("BillingProviderAdditionalId1Identification")) {
                columnName = "BillingProviderAdditionalId1Identification";
            }
            if (columnName.equalsIgnoreCase("BillingProviderAdditionalId2Type")) {
                columnName = "BillingProviderAdditionalId2Type";
            }
            if (columnName.equalsIgnoreCase("BillingProviderAdditionalId2Identification")) {
                columnName = "BillingProviderAdditionalId2Identification";
            }
            if (columnName.equalsIgnoreCase("SubscriberPayerResponsibilitySequence")) {
                columnName = "SubscriberPayerResponsibilitySequence";
            }
            if (columnName.equalsIgnoreCase("SubscriberRelationshipType")) {
                columnName = "SubscriberRelationshipType";
            }
            if (columnName.equalsIgnoreCase("SubscriberGroupOrPolicyNumber")) {
                columnName = "SubscriberGroupOrPolicyNumber";
            }
            if (columnName.equalsIgnoreCase("SubscriberGroupName")) {
                columnName = "SubscriberGroupName";
            }
            if (columnName.equalsIgnoreCase("SubscriberClaimFilingIndicatorCode")) {
                columnName = "SubscriberClaimFilingIndicatorCode";
            }
            if (columnName.equalsIgnoreCase("SubscriberIdentificationType")) {
                columnName = "SubscriberIdentificationType";
            }
            if (columnName.equalsIgnoreCase("SubscriberIdentifier")) {
                columnName = "SubscriberIdentifier";
            }
            if (columnName.equalsIgnoreCase("SubscriberTaxId")) {
                columnName = "SubscriberTaxId";
            }
            if (columnName.equalsIgnoreCase("SubscriberLastName")) {
                columnName = "SubscriberLastName";
            }
            if (columnName.equalsIgnoreCase("SubscriberFirstName")) {
                columnName = "SubscriberFirstName";
            }
            if (columnName.equalsIgnoreCase("SubscriberMiddleName")) {
                columnName = "SubscriberMiddleName";
            }
            if (columnName.equalsIgnoreCase("SubscriberBirthDate")) {
                columnName = "SubscriberBirthDate";
            }
            if (columnName.equalsIgnoreCase("SubscriberGender")) {
                columnName = "SubscriberGender";
            }
            if (columnName.equalsIgnoreCase("SubscriberAddressLine")) {
                columnName = "SubscriberAddressLine";
            }
            if (columnName.equalsIgnoreCase("SubscriberAddressLine2")) {
                columnName = "SubscriberAddressLine2";
            }
            if (columnName.equalsIgnoreCase("SubscriberAddressCity")) {
                columnName = "SubscriberAddressCity";
            }
            if (columnName.equalsIgnoreCase("SubscriberAddressStateCode")) {
                columnName = "SubscriberAddressStateCode";
            }
            if (columnName.equalsIgnoreCase("SubscriberAddressZipCode")) {
                columnName = "SubscriberAddressZipCode";
            }
            if (columnName.equalsIgnoreCase("SubscriberDeathDate")) {
                columnName = "SubscriberDeathDate";
            }
            if (columnName.equalsIgnoreCase("SubscriberWeight")) {
                columnName = "SubscriberWeight";
            }
            if (columnName.equalsIgnoreCase("SubscriberPregnancyIndicator")) {
                columnName = "SubscriberPregnancyIndicator";
            }
            if (columnName.equalsIgnoreCase("SubscriberPayerIdentificationType")) {
                columnName = "SubscriberPayerIdentificationType";
            }
            if (columnName.equalsIgnoreCase("SubscriberPayerIdentifier")) {
                columnName = "SubscriberPayerIdentifier";
            }
            if (columnName.equalsIgnoreCase("SubscriberPayerTaxId")) {
                columnName = "SubscriberPayerTaxId";
            }
            if (columnName.equalsIgnoreCase("SubscriberPayerName")) {
                columnName = "SubscriberPayerName";
            }
            if (columnName.equalsIgnoreCase("SubscriberPayerAddressLine")) {
                columnName = "SubscriberPayerAddressLine";
            }
            if (columnName.equalsIgnoreCase("SubscriberPayerAddressLine2")) {
                columnName = "SubscriberPayerAddressLine2";
            }
            if (columnName.equalsIgnoreCase("SubscriberPayerAddressCity")) {
                columnName = "SubscriberPayerAddressCity";
            }
            if (columnName.equalsIgnoreCase("SubscriberPayerAddressStateCode")) {
                columnName = "SubscriberPayerAddressStateCode";
            }
            if (columnName.equalsIgnoreCase("SubscriberPayerAddressZipCode")) {
                columnName = "SubscriberPayerAddressZipCode";
            }
            if (columnName.equalsIgnoreCase("SubscriberPayerAdditionalId1Type")) {
                columnName = "SubscriberPayerAdditionalId1Type";
            }
            if (columnName.equalsIgnoreCase("SubscriberPayerAdditionalId1Identification")) {
                columnName = "SubscriberPayerAdditionalId1Identification";
            }
            if (columnName.equalsIgnoreCase("SubscriberPayerAdditionalId2Type")) {
                columnName = "SubscriberPayerAdditionalId2Type";
            }
            if (columnName.equalsIgnoreCase("SubscriberPayerAdditionalId2Identification")) {
                columnName = "SubscriberPayerAdditionalId2Identification";
            }
            if (columnName.equalsIgnoreCase("PatientRelationshipType")) {
                columnName = "PatientRelationshipType";
            }
            if (columnName.equalsIgnoreCase("PatientLastName")) {
                columnName = "PatientLastName";
            }
            if (columnName.equalsIgnoreCase("PatientFirstName")) {
                columnName = "PatientFirstName";
            }
            if (columnName.equalsIgnoreCase("PatientMiddleName")) {
                columnName = "PatientMiddleName";
            }
            if (columnName.equalsIgnoreCase("PatientBirthDate")) {
                columnName = "PatientBirthDate";
            }
            if (columnName.equalsIgnoreCase("PatientGender")) {
                columnName = "PatientGender";
            }
            if (columnName.equalsIgnoreCase("PatientAddressLine")) {
                columnName = "PatientAddressLine";
            }
            if (columnName.equalsIgnoreCase("PatientAddressLine2")) {
                columnName = "PatientAddressLine2";
            }
            if (columnName.equalsIgnoreCase("PatientAddressCity")) {
                columnName = "PatientAddressCity";
            }
            if (columnName.equalsIgnoreCase("PatientAddressStateCode")) {
                columnName = "PatientAddressStateCode";
            }
            if (columnName.equalsIgnoreCase("PatientAddressZipCode")) {
                columnName = "PatientAddressZipCode";
            }
            if (columnName.equalsIgnoreCase("PatientDeathDate")) {
                columnName = "PatientDeathDate";
            }
            if (columnName.equalsIgnoreCase("PatientWeight")) {
                columnName = "PatientWeight";
            }
            if (columnName.equalsIgnoreCase("PatientPregnancyIndicator")) {
                columnName = "PatientPregnancyIndicator";
            }
            if (columnName.equalsIgnoreCase("ServiceDateFrom")) {
                columnName = "ServiceDateFrom";
            }
            if (columnName.equalsIgnoreCase("ServiceDateTo")) {
                columnName = "ServiceDateTo";
            }
            if (columnName.equalsIgnoreCase("OnsetOfCurrentIllnessOrInjuryDate")) {
                columnName = "OnsetOfCurrentIllnessOrInjuryDate";
            }
            if (columnName.equalsIgnoreCase("InitialTreatmentDate")) {
                columnName = "InitialTreatmentDate";
            }
            if (columnName.equalsIgnoreCase("LastSeenDate")) {
                columnName = "LastSeenDate";
            }
            if (columnName.equalsIgnoreCase("AcuteManifestationDate")) {
                columnName = "AcuteManifestationDate";
            }
            if (columnName.equalsIgnoreCase("AccidentDate")) {
                columnName = "AccidentDate";
            }
            if (columnName.equalsIgnoreCase("LastMenstrualPeriodDate")) {
                columnName = "LastMenstrualPeriodDate";
            }
            if (columnName.equalsIgnoreCase("LastXRayDate")) {
                columnName = "LastXRayDate";
            }
            if (columnName.equalsIgnoreCase("PrescriptionDate")) {
                columnName = "PrescriptionDate";
            }
            if (columnName.equalsIgnoreCase("AssumedCareDate")) {
                columnName = "AssumedCareDate";
            }
            if (columnName.equalsIgnoreCase("RelinquishedCareDate")) {
                columnName = "RelinquishedCareDate";
            }
            if (columnName.equalsIgnoreCase("AdmissionDate")) {
                columnName = "AdmissionDate";
            }
            if (columnName.equalsIgnoreCase("DischargeDate")) {
                columnName = "DischargeDate";
            }
            if (columnName.equalsIgnoreCase("PatientPaidAmount")) {
                columnName = "PatientPaidAmount";
            }
            if (columnName.equalsIgnoreCase("ServiceAuthorizationExceptionCode")) {
                columnName = "ServiceAuthorizationExceptionCode";
            }
            if (columnName.equalsIgnoreCase("ReferralNumber")) {
                columnName = "ReferralNumber";
            }
            if (columnName.equalsIgnoreCase("PriorAuthorizationNumber")) {
                columnName = "PriorAuthorizationNumber";
            }
            if (columnName.equalsIgnoreCase("PayerClaimControlNumber")) {
                columnName = "PayerClaimControlNumber";
            }
            if (columnName.equalsIgnoreCase("ClearinghouseTraceNumber")) {
                columnName = "ClearinghouseTraceNumber";
            }
            if (columnName.equalsIgnoreCase("RepricedReferenceNumber")) {
                columnName = "RepricedReferenceNumber";
            }
            if (columnName.equalsIgnoreCase("AdjustedRepricedReferenceNumber")) {
                columnName = "AdjustedRepricedReferenceNumber";
            }
            if (columnName.equalsIgnoreCase("MedicalRecordNumber")) {
                columnName = "MedicalRecordNumber";
            }
            if (columnName.equalsIgnoreCase("Note")) {
                columnName = "Note";
            }
            if (columnName.equalsIgnoreCase("Diag1Code")) {
                columnName = "Diag1Code";
            }
            if (columnName.equalsIgnoreCase("Diag2Code")) {
                columnName = "Diag2Code";
            }
            if (columnName.equalsIgnoreCase("Diag3Code")) {
                columnName = "Diag3Code";
            }
            if (columnName.equalsIgnoreCase("Diag4Code")) {
                columnName = "Diag4Code";
            }
            if (columnName.equalsIgnoreCase("Diag5Code")) {
                columnName = "Diag5Code";
            }
            if (columnName.equalsIgnoreCase("AnesthesiaProcedureCode")) {
                columnName = "AnesthesiaProcedureCode";
            }
            if (columnName.equalsIgnoreCase("Condition1Code")) {
                columnName = "Condition1Code";
            }
            if (columnName.equalsIgnoreCase("Condition2Code")) {
                columnName = "Condition2Code";
            }
            if (columnName.equalsIgnoreCase("Condition3Code")) {
                columnName = "Condition3Code";
            }
            if (columnName.equalsIgnoreCase("Attachment1ReportTypeCode")) {
                columnName = "Attachment1ReportTypeCode";
            }
            if (columnName.equalsIgnoreCase("Attachment1ReportTransmissionCode")) {
                columnName = "Attachment1ReportTransmissionCode";
            }
            if (columnName.equalsIgnoreCase("Attachment1ControlNumber")) {
                columnName = "Attachment1ControlNumber";
            }
            if (columnName.equalsIgnoreCase("Attachment2ReportTypeCode")) {
                columnName = "Attachment2ReportTypeCode";
            }
            if (columnName.equalsIgnoreCase("Attachment2ReportTransmissionCode")) {
                columnName = "Attachment2ReportTransmissionCode";
            }
            if (columnName.equalsIgnoreCase("Attachment2ControlNumber")) {
                columnName = "Attachment2ControlNumber";
            }
            if (columnName.equalsIgnoreCase("Attachment3ReportTypeCode")) {
                columnName = "Attachment3ReportTypeCode";
            }
            if (columnName.equalsIgnoreCase("Attachment3ReportTransmissionCode")) {
                columnName = "Attachment3ReportTransmissionCode";
            }
            if (columnName.equalsIgnoreCase("Attachment3ControlNumber")) {
                columnName = "Attachment3ControlNumber";
            }
            if (columnName.equalsIgnoreCase("ReferringProviderIdentifier")) {
                columnName = "ReferringProviderIdentifier";
            }
            if (columnName.equalsIgnoreCase("ReferringProviderLastNameOrOrgName")) {
                columnName = "ReferringProviderLastNameOrOrgName";
            }
            if (columnName.equalsIgnoreCase("ReferringProviderFirstName")) {
                columnName = "ReferringProviderFirstName";
            }
            if (columnName.equalsIgnoreCase("ReferringProviderMiddleName")) {
                columnName = "ReferringProviderMiddleName";
            }
            if (columnName.equalsIgnoreCase("ReferringProviderAdditionalId1Type")) {
                columnName = "ReferringProviderAdditionalId1Type";
            }
            if (columnName.equalsIgnoreCase("ReferringProviderAdditionalId1Identification")) {
                columnName = "ReferringProviderAdditionalId1Identification";
            }
            if (columnName.equalsIgnoreCase("ReferringProviderAdditionalId2Type")) {
                columnName = "ReferringProviderAdditionalId2Type";
            }
            if (columnName.equalsIgnoreCase("ReferringProviderAdditionalId2Identification")) {
                columnName = "ReferringProviderAdditionalId2Identification";
            }
            if (columnName.equalsIgnoreCase("RenderingProviderIdentifier")) {
                columnName = "RenderingProviderIdentifier";
            }
            if (columnName.equalsIgnoreCase("RenderingProviderLastNameOrOrgName")) {
                columnName = "RenderingProviderLastNameOrOrgName";
            }
            if (columnName.equalsIgnoreCase("RenderingProviderFirstName")) {
                columnName = "RenderingProviderFirstName";
            }
            if (columnName.equalsIgnoreCase("RenderingProviderMiddleName")) {
                columnName = "RenderingProviderMiddleName";
            }
            if (columnName.equalsIgnoreCase("RenderingProviderProviderTaxonomyCode")) {
                columnName = "RenderingProviderProviderTaxonomyCode";
            }
            if (columnName.equalsIgnoreCase("RenderingProviderAdditionalId1Type")) {
                columnName = "RenderingProviderAdditionalId1Type";
            }
            if (columnName.equalsIgnoreCase("RenderingProviderAdditionalId1Identification")) {
                columnName = "RenderingProviderAdditionalId1Identification";
            }
            if (columnName.equalsIgnoreCase("RenderingProviderAdditionalId2Type")) {
                columnName = "RenderingProviderAdditionalId2Type";
            }
            if (columnName.equalsIgnoreCase("RenderingProviderAdditionalId2Identification")) {
                columnName = "RenderingProviderAdditionalId2Identification";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityIdentifier")) {
                columnName = "ServiceFacilityIdentifier";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityName")) {
                columnName = "ServiceFacilityName";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityAddressLine")) {
                columnName = "ServiceFacilityAddressLine";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityAddressLine2")) {
                columnName = "ServiceFacilityAddressLine2";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityAddressCity")) {
                columnName = "ServiceFacilityAddressCity";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityAddressStateCode")) {
                columnName = "ServiceFacilityAddressStateCode";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityAddressZipCode")) {
                columnName = "ServiceFacilityAddressZipCode";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityContactName")) {
                columnName = "ServiceFacilityContactName";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityContactContactNumber1Type")) {
                columnName = "ServiceFacilityContactContactNumber1Type";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityContactContactNumber1Number")) {
                columnName = "ServiceFacilityContactContactNumber1Number";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityContactContactNumber2Type")) {
                columnName = "ServiceFacilityContactContactNumber2Type";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityContactContactNumber2Number")) {
                columnName = "ServiceFacilityContactContactNumber2Number";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityAdditionalId1Type")) {
                columnName = "ServiceFacilityAdditionalId1Type";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityAdditionalId1Identification")) {
                columnName = "ServiceFacilityAdditionalId1Identification";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityAdditionalId2Type")) {
                columnName = "ServiceFacilityAdditionalId2Type";
            }
            if (columnName.equalsIgnoreCase("ServiceFacilityAdditionalId2Identification")) {
                columnName = "ServiceFacilityAdditionalId2Identification";
            }
            if (columnName.equalsIgnoreCase("SupervisingProviderIdentifier")) {
                columnName = "SupervisingProviderIdentifier";
            }
            if (columnName.equalsIgnoreCase("SupervisingProviderLastNameOrOrgName")) {
                columnName = "SupervisingProviderLastNameOrOrgName";
            }
            if (columnName.equalsIgnoreCase("SupervisingProviderFirstName")) {
                columnName = "SupervisingProviderFirstName";
            }
            if (columnName.equalsIgnoreCase("SupervisingProviderMiddleName")) {
                columnName = "SupervisingProviderMiddleName";
            }
            if (columnName.equalsIgnoreCase("SupervisingProviderAdditionalId1Type")) {
                columnName = "SupervisingProviderAdditionalId1Type";
            }
            if (columnName.equalsIgnoreCase("SupervisingProviderAdditionalId1Identification")) {
                columnName = "SupervisingProviderAdditionalId1Identification";
            }
            if (columnName.equalsIgnoreCase("SupervisingProviderAdditionalId2Type")) {
                columnName = "SupervisingProviderAdditionalId2Type";
            }
            if (columnName.equalsIgnoreCase("SupervisingProviderAdditionalId2Identification")) {
                columnName = "SupervisingProviderAdditionalId2Identification";
            }
            if (columnName.equalsIgnoreCase("AmbulancePickUpAddressLine")) {
                columnName = "AmbulancePickUpAddressLine";
            }
            if (columnName.equalsIgnoreCase("AmbulancePickUpAddressLine2")) {
                columnName = "AmbulancePickUpAddressLine2";
            }
            if (columnName.equalsIgnoreCase("AmbulancePickUpAddressCity")) {
                columnName = "AmbulancePickUpAddressCity";
            }
            if (columnName.equalsIgnoreCase("AmbulancePickUpAddressStateCode")) {
                columnName = "AmbulancePickUpAddressStateCode";
            }
            if (columnName.equalsIgnoreCase("AmbulancePickUpAddressZipCode")) {
                columnName = "AmbulancePickUpAddressZipCode";
            }
            if (columnName.equalsIgnoreCase("AmbulanceDropOffLastNameOrOrgName")) {
                columnName = "AmbulanceDropOffLastNameOrOrgName";
            }
            if (columnName.equalsIgnoreCase("AmbulanceDropOffAddressLine")) {
                columnName = "AmbulanceDropOffAddressLine";
            }
            if (columnName.equalsIgnoreCase("AmbulanceDropOffAddressLine2")) {
                columnName = "AmbulanceDropOffAddressLine2";
            }
            if (columnName.equalsIgnoreCase("AmbulanceDropOffAddressCity")) {
                columnName = "AmbulanceDropOffAddressCity";
            }
            if (columnName.equalsIgnoreCase("AmbulanceDropOffAddressStateCode")) {
                columnName = "AmbulanceDropOffAddressStateCode";
            }
            if (columnName.equalsIgnoreCase("AmbulanceDropOffAddressZipCode")) {
                columnName = "AmbulanceDropOffAddressZipCode";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerResponsibilitySequence")) {
                columnName = "OtherSubscriberPayerResponsibilitySequence";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberRelationshipType")) {
                columnName = "OtherSubscriberRelationshipType";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberGroupOrPolicyNumber")) {
                columnName = "OtherSubscriberGroupOrPolicyNumber";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberGroupName")) {
                columnName = "OtherSubscriberGroupName";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberClaimFilingIndicatorCode")) {
                columnName = "OtherSubscriberClaimFilingIndicatorCode";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberIdentificationType")) {
                columnName = "OtherSubscriberIdentificationType";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberIdentifier")) {
                columnName = "OtherSubscriberIdentifier";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberTaxId")) {
                columnName = "OtherSubscriberTaxId";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberLastName")) {
                columnName = "OtherSubscriberLastName";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberFirstName")) {
                columnName = "OtherSubscriberFirstName";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberMiddleName")) {
                columnName = "OtherSubscriberMiddleName";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAddressLine")) {
                columnName = "OtherSubscriberAddressLine";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAddressLine2")) {
                columnName = "OtherSubscriberAddressLine2";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAddressCity")) {
                columnName = "OtherSubscriberAddressCity";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAddressStateCode")) {
                columnName = "OtherSubscriberAddressStateCode";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAddressZipCode")) {
                columnName = "OtherSubscriberAddressZipCode";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAdjustment1Group")) {
                columnName = "OtherSubscriberAdjustment1Group";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAdjustment1ReasonCode")) {
                columnName = "OtherSubscriberAdjustment1ReasonCode";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAdjustment1Amount")) {
                columnName = "OtherSubscriberAdjustment1Amount";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAdjustment1Quantity")) {
                columnName = "OtherSubscriberAdjustment1Quantity";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAdjustment2Group")) {
                columnName = "OtherSubscriberAdjustment2Group";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAdjustment2ReasonCode")) {
                columnName = "OtherSubscriberAdjustment2ReasonCode";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAdjustment2Amount")) {
                columnName = "OtherSubscriberAdjustment2Amount";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAdjustment2Quantity")) {
                columnName = "OtherSubscriberAdjustment2Quantity";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAdjustment3Group")) {
                columnName = "OtherSubscriberAdjustment3Group";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAdjustment3ReasonCode")) {
                columnName = "OtherSubscriberAdjustment3ReasonCode";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAdjustment3Amount")) {
                columnName = "OtherSubscriberAdjustment3Amount";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberAdjustment3Quantity")) {
                columnName = "OtherSubscriberAdjustment3Quantity";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerPaidAmount")) {
                columnName = "OtherSubscriberPayerPaidAmount";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberNonCoveredAmount")) {
                columnName = "OtherSubscriberNonCoveredAmount";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberRemainingPatientLiabilityAmount")) {
                columnName = "OtherSubscriberRemainingPatientLiabilityAmount";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerClaimControlNumber")) {
                columnName = "OtherSubscriberPayerClaimControlNumber";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerIdentificationType")) {
                columnName = "OtherSubscriberPayerIdentificationType";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerIdentifier")) {
                columnName = "OtherSubscriberPayerIdentifier";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerTaxId")) {
                columnName = "OtherSubscriberPayerTaxId";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerName")) {
                columnName = "OtherSubscriberPayerName";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerAddressLine")) {
                columnName = "OtherSubscriberPayerAddressLine";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerAddressLine2")) {
                columnName = "OtherSubscriberPayerAddressLine2";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerAddressCity")) {
                columnName = "OtherSubscriberPayerAddressCity";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerAddressStateCode")) {
                columnName = "OtherSubscriberPayerAddressStateCode";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerAddressZipCode")) {
                columnName = "OtherSubscriberPayerAddressZipCode";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerAdditionalId1Type")) {
                columnName = "OtherSubscriberPayerAdditionalId1Type";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerAdditionalId1Identification")) {
                columnName = "OtherSubscriberPayerAdditionalId1Identification";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerAdditionalId2Type")) {
                columnName = "OtherSubscriberPayerAdditionalId2Type";
            }
            if (columnName.equalsIgnoreCase("OtherSubscriberPayerAdditionalId2Identification")) {
                columnName = "OtherSubscriberPayerAdditionalId2Identification";
            }

            //if (columnName.equalsIgnoreCase("DataSourceName")) { columnName = "DataSourceName"; }
            //if (columnName.equalsIgnoreCase("ProcessedFlag")) { columnName = "ProcessedFlag"; }
            //if (columnName.equalsIgnoreCase("HashKeyForDuplicateClaim")) { columnName = "HashKeyForDuplicateClaim"; }
            //if (columnName.equalsIgnoreCase("EtlSourceID")) { columnName = "EtlSourceID"; }


            columnNames.add(columnName);
        }
        columnNames.add("EtlSourceID"); // This is File source id that will come from Source Manager Entry. = Table = cz_source_manager (etl_source_id)
        columnNames.add("TransactionID"); // This will come from file Transaction table. --> Table = CI_CLAIM_FILE_TRANSACTION (Id)

        return columnNames;
    }

    /**
     // OPTION A: All columns are matching with Database
     private List<String> createColumnNames(String listName) {
     var headers = schema.headers().get(listName);
     List<String> columnNames = new ArrayList<>();

     for (var header : headers) {
     String columnName = ((String) header).trim();

     // Everything else passes directly
     columnNames.add(columnName);
     }

     return columnNames;
     }
     **/


    /**
     * Creates a list of database column names from the schema headers for a given list.
     * Applies special transformations, such as renaming "Id" to "converterClaimId".
     *
     * @param listName the name of the list to get column names for
     * @return a list of column names to use in SQL statements
     */
    private List<String> createColumnNamesLines(String listName) {
        var headers = schema.headers().get(listName);
        List<String> columnNames = new ArrayList<>();
        for (var header : headers) {
            String columnName = (String) header;

            if (columnName.equalsIgnoreCase("Id")) {
                columnName = "Id";
            }
            if (columnName.equalsIgnoreCase("PatientControlNumber")) {
                columnName = "PatientControlNumber";
            }
            if (columnName.equalsIgnoreCase("LineControlNumber")) {
                columnName = "LineControlNumber";
            }
            if (columnName.equalsIgnoreCase("LineProcedureCode")) {
                columnName = "LineProcedureCode";
            }
            if (columnName.equalsIgnoreCase("LineProcedureDescFromClaim")) {
                columnName = "LineProcedureDescFromClaim";
            }
            if (columnName.equalsIgnoreCase("LineProcedureModifier1Code")) {
                columnName = "LineProcedureModifier1Code";
            }
            if (columnName.equalsIgnoreCase("LineProcedureModifier2Code")) {
                columnName = "LineProcedureModifier2Code";
            }
            if (columnName.equalsIgnoreCase("LineProcedureModifier3Code")) {
                columnName = "LineProcedureModifier3Code";
            }
            if (columnName.equalsIgnoreCase("LineProcedureModifier4Code")) {
                columnName = "LineProcedureModifier4Code";
            }
            if (columnName.equalsIgnoreCase("LineChargeAmount")) {
                columnName = "LineChargeAmount";
            }
            if (columnName.equalsIgnoreCase("LineUnitType")) {
                columnName = "LineUnitType";
            }
            if (columnName.equalsIgnoreCase("LineUnitCount")) {
                columnName = "LineUnitCount";
            }
            if (columnName.equalsIgnoreCase("LinePlaceOfService")) {
                columnName = "LinePlaceOfService";
            }
            if (columnName.equalsIgnoreCase("LinePlaceOfServiceCode")) {
                columnName = "LinePlaceOfServiceCode";
            }
            if (columnName.equalsIgnoreCase("LineDiagPointer1")) {
                columnName = "LineDiagPointer1";
            }
            if (columnName.equalsIgnoreCase("LineDiagPointer2")) {
                columnName = "LineDiagPointer2";
            }
            if (columnName.equalsIgnoreCase("LineDiagPointer3")) {
                columnName = "LineDiagPointer3";
            }
            if (columnName.equalsIgnoreCase("LineEmergencyIndicator")) {
                columnName = "LineEmergencyIndicator";
            }
            if (columnName.equalsIgnoreCase("LineEpsdtIndicator")) {
                columnName = "LineEpsdtIndicator";
            }
            if (columnName.equalsIgnoreCase("LineFamilyPlanningIndicator")) {
                columnName = "LineFamilyPlanningIndicator";
            }
            if (columnName.equalsIgnoreCase("LineCopayStatusCode")) {
                columnName = "LineCopayStatusCode";
            }
            if (columnName.equalsIgnoreCase("LineServiceDateFrom")) {
                columnName = "LineServiceDateFrom";
            }
            if (columnName.equalsIgnoreCase("LineServiceDateTo")) {
                columnName = "LineServiceDateTo";
            }
            if (columnName.equalsIgnoreCase("LinePrescriptionDate")) {
                columnName = "LinePrescriptionDate";
            }
            if (columnName.equalsIgnoreCase("LineBeginTherapyDate")) {
                columnName = "LineBeginTherapyDate";
            }
            if (columnName.equalsIgnoreCase("LineLastSeenDate")) {
                columnName = "LineLastSeenDate";
            }
            if (columnName.equalsIgnoreCase("LineTestPerformedDate")) {
                columnName = "LineTestPerformedDate";
            }
            if (columnName.equalsIgnoreCase("LineLastXRayDate")) {
                columnName = "LineLastXRayDate";
            }
            if (columnName.equalsIgnoreCase("LineInitialTreatmentDate")) {
                columnName = "LineInitialTreatmentDate";
            }
            if (columnName.equalsIgnoreCase("LinePriorAuthorization")) {
                columnName = "LinePriorAuthorization";
            }
            if (columnName.equalsIgnoreCase("LineReferralNumber")) {
                columnName = "LineReferralNumber";
            }
            if (columnName.equalsIgnoreCase("LineRepricedReferenceNumber")) {
                columnName = "LineRepricedReferenceNumber";
            }
            if (columnName.equalsIgnoreCase("LineAdjustedRepricedReferenceNumber")) {
                columnName = "LineAdjustedRepricedReferenceNumber";
            }
            if (columnName.equalsIgnoreCase("LineNote")) {
                columnName = "LineNote";
            }
            if (columnName.equalsIgnoreCase("LineThirdPartyNote")) {
                columnName = "LineThirdPartyNote";
            }
            if (columnName.equalsIgnoreCase("LineDrugCode")) {
                columnName = "LineDrugCode";
            }
            if (columnName.equalsIgnoreCase("LineDrugQuantity")) {
                columnName = "LineDrugQuantity";
            }
            if (columnName.equalsIgnoreCase("LineDrugUnitType")) {
                columnName = "LineDrugUnitType";
            }
            if (columnName.equalsIgnoreCase("LinePrescriptionNumber")) {
                columnName = "LinePrescriptionNumber";
            }
            if (columnName.equalsIgnoreCase("LineAttachment1ReportTypeCode")) {
                columnName = "LineAttachment1ReportTypeCode";
            }
            if (columnName.equalsIgnoreCase("LineAttachment1ReportTransmissionCode")) {
                columnName = "LineAttachment1ReportTransmissionCode";
            }
            if (columnName.equalsIgnoreCase("LineAttachment1ControlNumber")) {
                columnName = "LineAttachment1ControlNumber";
            }
            if (columnName.equalsIgnoreCase("LineAttachment2ReportTypeCode")) {
                columnName = "LineAttachment2ReportTypeCode";
            }
            if (columnName.equalsIgnoreCase("LineAttachment2ReportTransmissionCode")) {
                columnName = "LineAttachment2ReportTransmissionCode";
            }
            if (columnName.equalsIgnoreCase("LineAttachment2ControlNumber")) {
                columnName = "LineAttachment2ControlNumber";
            }
            if (columnName.equalsIgnoreCase("LineAttachment3ReportTypeCode")) {
                columnName = "LineAttachment3ReportTypeCode";
            }
            if (columnName.equalsIgnoreCase("LineAttachment3ReportTransmissionCode")) {
                columnName = "LineAttachment3ReportTransmissionCode";
            }
            if (columnName.equalsIgnoreCase("LineAttachment3ControlNumber")) {
                columnName = "LineAttachment3ControlNumber";
            }
            if (columnName.equalsIgnoreCase("LineRenderingProviderIdentifier")) {
                columnName = "LineRenderingProviderIdentifier";
            }
            if (columnName.equalsIgnoreCase("LineRenderingProviderLastNameOrOrgName")) {
                columnName = "LineRenderingProviderLastNameOrOrgName";
            }
            if (columnName.equalsIgnoreCase("LineRenderingProviderFirstName")) {
                columnName = "LineRenderingProviderFirstName";
            }
            if (columnName.equalsIgnoreCase("LineRenderingProviderMiddleName")) {
                columnName = "LineRenderingProviderMiddleName";
            }
            if (columnName.equalsIgnoreCase("LineRenderingProviderProviderTaxonomyCode")) {
                columnName = "LineRenderingProviderProviderTaxonomyCode";
            }
            if (columnName.equalsIgnoreCase("LineRenderingProviderAdditionalId1Type")) {
                columnName = "LineRenderingProviderAdditionalId1Type";
            }
            if (columnName.equalsIgnoreCase("LineRenderingProviderAdditionalId1Identification")) {
                columnName = "LineRenderingProviderAdditionalId1Identification";
            }
            if (columnName.equalsIgnoreCase("LineRenderingProviderAdditionalId2Type")) {
                columnName = "LineRenderingProviderAdditionalId2Type";
            }
            if (columnName.equalsIgnoreCase("LineRenderingProviderAdditionalId2Identification")) {
                columnName = "LineRenderingProviderAdditionalId2Identification";
            }
            if (columnName.equalsIgnoreCase("LinePurchasedServiceProviderIdentifier")) {
                columnName = "LinePurchasedServiceProviderIdentifier";
            }
            if (columnName.equalsIgnoreCase("LinePurchasedServiceProviderAdditionalId1Type")) {
                columnName = "LinePurchasedServiceProviderAdditionalId1Type";
            }
            if (columnName.equalsIgnoreCase("LinePurchasedServiceProviderAdditionalId1Identification")) {
                columnName = "LinePurchasedServiceProviderAdditionalId1Identification";
            }
            if (columnName.equalsIgnoreCase("LinePurchasedServiceProviderAdditionalId2Type")) {
                columnName = "LinePurchasedServiceProviderAdditionalId2Type";
            }
            if (columnName.equalsIgnoreCase("LinePurchasedServiceProviderAdditionalId2Identification")) {
                columnName = "LinePurchasedServiceProviderAdditionalId2Identification";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityIdentifier")) {
                columnName = "LineServiceFacilityIdentifier";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityName")) {
                columnName = "LineServiceFacilityName";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityAddressLine")) {
                columnName = "LineServiceFacilityAddressLine";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityAddressLine2")) {
                columnName = "LineServiceFacilityAddressLine2";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityAddressCity")) {
                columnName = "LineServiceFacilityAddressCity";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityAddressStateCode")) {
                columnName = "LineServiceFacilityAddressStateCode";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityAddressZipCode")) {
                columnName = "LineServiceFacilityAddressZipCode";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityContactName")) {
                columnName = "LineServiceFacilityContactName";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityContactContactNumber1Type")) {
                columnName = "LineServiceFacilityContactContactNumber1Type";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityContactContactNumber1Number")) {
                columnName = "LineServiceFacilityContactContactNumber1Number";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityContactContactNumber2Type")) {
                columnName = "LineServiceFacilityContactContactNumber2Type";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityContactContactNumber2Number")) {
                columnName = "LineServiceFacilityContactContactNumber2Number";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityAdditionalId1Type")) {
                columnName = "LineServiceFacilityAdditionalId1Type";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityAdditionalId1Identification")) {
                columnName = "LineServiceFacilityAdditionalId1Identification";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityAdditionalId2Type")) {
                columnName = "LineServiceFacilityAdditionalId2Type";
            }
            if (columnName.equalsIgnoreCase("LineServiceFacilityAdditionalId2Identification")) {
                columnName = "LineServiceFacilityAdditionalId2Identification";
            }
            if (columnName.equalsIgnoreCase("LineSupervisingProviderIdentifier")) {
                columnName = "LineSupervisingProviderIdentifier";
            }
            if (columnName.equalsIgnoreCase("LineSupervisingProviderLastNameOrOrgName")) {
                columnName = "LineSupervisingProviderLastNameOrOrgName";
            }
            if (columnName.equalsIgnoreCase("LineSupervisingProviderFirstName")) {
                columnName = "LineSupervisingProviderFirstName";
            }
            if (columnName.equalsIgnoreCase("LineSupervisingProviderMiddleName")) {
                columnName = "LineSupervisingProviderMiddleName";
            }
            if (columnName.equalsIgnoreCase("LineSupervisingProviderAdditionalId1Type")) {
                columnName = "LineSupervisingProviderAdditionalId1Type";
            }
            if (columnName.equalsIgnoreCase("LineSupervisingProviderAdditionalId1Identification")) {
                columnName = "LineSupervisingProviderAdditionalId1Identification";
            }
            if (columnName.equalsIgnoreCase("LineSupervisingProviderAdditionalId2Type")) {
                columnName = "LineSupervisingProviderAdditionalId2Type";
            }
            if (columnName.equalsIgnoreCase("LineSupervisingProviderAdditionalId2Identification")) {
                columnName = "LineSupervisingProviderAdditionalId2Identification";
            }
            if (columnName.equalsIgnoreCase("LineReferringProviderIdentifier")) {
                columnName = "LineReferringProviderIdentifier";
            }
            if (columnName.equalsIgnoreCase("LineReferringProviderLastNameOrOrgName")) {
                columnName = "LineReferringProviderLastNameOrOrgName";
            }
            if (columnName.equalsIgnoreCase("LineReferringProviderFirstName")) {
                columnName = "LineReferringProviderFirstName";
            }
            if (columnName.equalsIgnoreCase("LineReferringProviderMiddleName")) {
                columnName = "LineReferringProviderMiddleName";
            }
            if (columnName.equalsIgnoreCase("LineReferringProviderAdditionalId1Type")) {
                columnName = "LineReferringProviderAdditionalId1Type";
            }
            if (columnName.equalsIgnoreCase("LineReferringProviderAdditionalId1Identification")) {
                columnName = "LineReferringProviderAdditionalId1Identification";
            }
            if (columnName.equalsIgnoreCase("LineReferringProviderAdditionalId2Type")) {
                columnName = "LineReferringProviderAdditionalId2Type";
            }
            if (columnName.equalsIgnoreCase("LineReferringProviderAdditionalId2Identification")) {
                columnName = "LineReferringProviderAdditionalId2Identification";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderIdentifier")) {
                columnName = "LineOrderingProviderIdentifier";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderLastNameOrOrgName")) {
                columnName = "LineOrderingProviderLastNameOrOrgName";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderFirstName")) {
                columnName = "LineOrderingProviderFirstName";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderMiddleName")) {
                columnName = "LineOrderingProviderMiddleName";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderAddressLine")) {
                columnName = "LineOrderingProviderAddressLine";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderAddressLine2")) {
                columnName = "LineOrderingProviderAddressLine2";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderAddressCity")) {
                columnName = "LineOrderingProviderAddressCity";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderAddressStateCode")) {
                columnName = "LineOrderingProviderAddressStateCode";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderAddressZipCode")) {
                columnName = "LineOrderingProviderAddressZipCode";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderContactName")) {
                columnName = "LineOrderingProviderContactName";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderContactContactNumber1Type")) {
                columnName = "LineOrderingProviderContactContactNumber1Type";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderContactContactNumber1Number")) {
                columnName = "LineOrderingProviderContactContactNumber1Number";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderContactContactNumber2Type")) {
                columnName = "LineOrderingProviderContactContactNumber2Type";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderContactContactNumber2Number")) {
                columnName = "LineOrderingProviderContactContactNumber2Number";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderAdditionalId1Type")) {
                columnName = "LineOrderingProviderAdditionalId1Type";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderAdditionalId1Identification")) {
                columnName = "LineOrderingProviderAdditionalId1Identification";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderAdditionalId2Type")) {
                columnName = "LineOrderingProviderAdditionalId2Type";
            }
            if (columnName.equalsIgnoreCase("LineOrderingProviderAdditionalId2Identification")) {
                columnName = "LineOrderingProviderAdditionalId2Identification";
            }
            if (columnName.equalsIgnoreCase("LineAmbulancePickUpAddressLine")) {
                columnName = "LineAmbulancePickUpAddressLine";
            }
            if (columnName.equalsIgnoreCase("LineAmbulancePickUpAddressLine2")) {
                columnName = "LineAmbulancePickUpAddressLine2";
            }
            if (columnName.equalsIgnoreCase("LineAmbulancePickUpAddressCity")) {
                columnName = "LineAmbulancePickUpAddressCity";
            }
            if (columnName.equalsIgnoreCase("LineAmbulancePickUpAddressStateCode")) {
                columnName = "LineAmbulancePickUpAddressStateCode";
            }
            if (columnName.equalsIgnoreCase("LineAmbulancePickUpAddressZipCode")) {
                columnName = "LineAmbulancePickUpAddressZipCode";
            }
            if (columnName.equalsIgnoreCase("LineAmbulanceDropOffLastNameOrOrgName")) {
                columnName = "LineAmbulanceDropOffLastNameOrOrgName";
            }
            if (columnName.equalsIgnoreCase("LineAmbulanceDropOffAddressLine")) {
                columnName = "LineAmbulanceDropOffAddressLine";
            }
            if (columnName.equalsIgnoreCase("LineAmbulanceDropOffAddressLine2")) {
                columnName = "LineAmbulanceDropOffAddressLine2";
            }
            if (columnName.equalsIgnoreCase("LineAmbulanceDropOffAddressCity")) {
                columnName = "LineAmbulanceDropOffAddressCity";
            }
            if (columnName.equalsIgnoreCase("LineAmbulanceDropOffAddressStateCode")) {
                columnName = "LineAmbulanceDropOffAddressStateCode";
            }
            if (columnName.equalsIgnoreCase("LineAmbulanceDropOffAddressZipCode")) {
                columnName = "LineAmbulanceDropOffAddressZipCode";
            }

            columnNames.add(columnName);
        }
        columnNames.add("claimid");
        //columnNames.add("EtlId"); Not needed, Duplicate 

        return columnNames;
    }


    /**
     * Writes a data row to the database for the specified list type.
     * Uses the prepared statement associated with the list name and increments the row counter.
     *
     * @param listName the name of the list (e.g., "header", "line")
     * @param row      the data values to insert
     * @throws SQLException             if the insert operation fails
     * @throws IllegalArgumentException if no prepared statement exists for the list name
     */
    @Override
    public void writeRow(String listName, List<Object> row) {
        log.debug("Writing row for list: " + listName);

        if (listName.equalsIgnoreCase(HEADER_LIST_NAME)) {
            row.add(etlSourceId);
            row.add(transactionId);
        }

        if (listName.equalsIgnoreCase(LINE_LIST_NAME)) {
            row.add(generatedKey);
        }

        var insertStmt = insertStmts.get(listName);
        if (insertStmt == null) {
            throw new IllegalArgumentException("No insert statement for list: " + listName);
        }
        try {
            insertRow(insertStmt, row);
        } catch (SQLException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        counts.merge(listName, 1, Integer::sum);
    }

    /**
     * Executes an INSERT statement with the provided row data.
     * Sets each value in the prepared statement and executes the update.
     *
     * @param insertStmt the prepared INSERT statement to execute
     * @param row        the data values to bind to the statement parameters
     * @throws SQLException if parameter binding or statement execution fails
     */
    private void insertRow(PreparedStatement insertStmt, List<Object> row) throws SQLException {
        log.debug("Inserting row: " + row);

        for (int i = 0; i < row.size(); i++) {
            Object val = row.get(i);
            insertStmt.setObject(i + 1, val);
        }
        int updated = insertStmt.executeUpdate();

        log.debug("Inserted row, updated=" + updated);

        // generatedKeys = new HashMap<>() ;
        generatedKey = null;

        // Attempt to read generated keys if any
        try (ResultSet rs = insertStmt.getGeneratedKeys()) {
            if (rs != null && rs.next()) {
                long key = rs.getLong(1);
                generatedKey = key;
                log.debug("Inserted row, generated key=" + key + " (updated=" + updated + ")");
            }
        }
    }

    /**
     * Closes all prepared statements held by this output manager.
     * Should be called when the output manager is no longer needed to release database resources.
     *
     * @throws IOException  if an I/O error occurs during closing
     * @throws SQLException if closing any prepared statement fails
     */
    @Override
    public void close() throws IOException {
        for (var stmt : insertStmts.values()) {
            try {
                stmt.close();
            } catch (SQLException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }

    public ConversionSchema getSchema() {
        return schema;
    }

    public Connection getConnection() {
        return connection;
    }

    public Map<String, PreparedStatement> getInsertStmts() {
        return insertStmts;
    }

    public Map<String, Integer> getCounts() {
        return counts;
    }

    /**
     * Returns a map of the last autogenerated key for each list name (if any).
     */
//    public Map<String, Long> getGeneratedKeys() {
//        return generatedKeys;
//    }

    /**
     * Revised by M365 Copilot
     * Returns the last generated lz_claim.id value.
     */
    public Long getGeneratedKey() {
        return generatedKey;
    }

    /**
     * Revised by M365 Copilot
     * Returns CI_CLAIM_FILE_TRANSACTION.id passed into this manager.
     */
    public Long getTransactionId() {
        return transactionId;
    }

    /**
     * Revised by M365 Copilot
     * Returns EtlSourceID passed into this manager.
     */
    public Long getEtlSourceId() {
        return etlSourceId;
    }

}