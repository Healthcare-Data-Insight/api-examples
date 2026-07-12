package hdi.edi.parser;

import hdi.edi.validation.ValidationIssue;
import org.slf4j.LoggerFactory;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

public interface ParsingExampleHelper {
    String EDI_FILES_DIR = "../edi_files";
    String OUT_EDI_FILES_DIR = "../out_edi_files";
    int DEFAULT_CHUNK_SIZE = 20;

    default void assertNotNull(Object... vals) {
        for (var val : vals) {
            assertThat(val).isNotNull();
        }
    }

    default void logValidationIssues(List<ValidationIssue> issues) {
        var validationLogger = LoggerFactory.getLogger(ParsingExampleHelper.class.getName());
        for (var issue : issues) {
            validationLogger.warn(issue.toFullMessage());
        }
    }
}