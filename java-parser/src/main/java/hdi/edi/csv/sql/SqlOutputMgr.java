package hdi.edi.csv.sql;

import hdi.edi.csv.ConversionSchema;
import hdi.edi.csv.OutputMgr;
import lombok.Getter;
import lombok.SneakyThrows;
import lombok.experimental.Accessors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;

import java.io.Closeable;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
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
@Accessors(fluent = true)
@Slf4j
public class SqlOutputMgr implements Closeable, OutputMgr {
    /**
     * The conversion schema that defines the structure and mapping rules for the data.
     */
    @Getter
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
    @Getter
    final Map<String, Integer> counts = new HashMap<>();

    /**
     * Constructs a new SQL output manager.
     *
     * @param schema     the conversion schema defining data structure and mappings
     * @param connection the JDBC database connection to use for inserts
     */
    public SqlOutputMgr(ConversionSchema schema, Connection connection) {
        this.schema = schema;
        this.connection = connection;
    }

    /**
     * Processes headers for a given list and generates the corresponding SQL INSERT statement.
     * This method is invoked once for each list type before any data rows are written.
     *
     * @param listName the name of the list (e.g., "header", "line")
     * @param row      the header row containing column names (not used in current implementation)
     * @throws SQLException if SQL generation or statement preparation fails
     */
    @SneakyThrows(SQLException.class)
    public void writeHeaders(String listName, List<String> row) {
        generateSql(listName);
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
        var tableName = switch (listName) {
            case HEADER_LIST_NAME -> "claim";
            case LINE_LIST_NAME -> "claim_line";
            default -> throw new IllegalArgumentException("Unknown list name: " + listName);
        };

        List<String> columnNames = createColumnNames(listName);
        String columns = StringUtils.join(columnNames, ",");
        String placeholders = StringUtils.repeat("?", ",", columnNames.size());
        var sql = "insert into " + tableName + " (" + columns + ") values (" + placeholders + ")";
        log.info("Generated SQL for list {}:\n{}", listName, sql);
        var stmt = connection.prepareStatement(sql);
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
            String columnName = header;
            if (columnName.equals("Id")) {
                columnName = "converterClaimId";
            }
            columnNames.add(columnName);
        }
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
    @SneakyThrows(SQLException.class)
    @Override
    public void writeRow(String listName, List<Object> row) {
        log.debug("Writing row for list: {}", listName);
        var insertStmt = insertStmts.get(listName);
        if (insertStmt == null) {
            throw new IllegalArgumentException("No insert statement for list: " + listName);
        }
        insertRow(insertStmt, row);
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
        for (int i = 0; i < row.size(); i++) {
            Object val = row.get(i);
            insertStmt.setObject(i + 1, val);
        }
        insertStmt.executeUpdate();
    }

    /**
     * Closes all prepared statements held by this output manager.
     * Should be called when the output manager is no longer needed to release database resources.
     *
     * @throws IOException  if an I/O error occurs during closing
     * @throws SQLException if closing any prepared statement fails
     */
    @Override
    @SneakyThrows(SQLException.class)
    public void close() throws IOException {
        for (var stmt : insertStmts.values()) {
            stmt.close();
        }
    }
}