package hdi.edi.parser;

import hdi.edi.validation.ValidationIssue;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

public interface ParsingExampleHelper {
    String EDI_FILES_DIR = "../edi_files";
    String OUT_EDI_FILES_DIR = "../out_edi_files";

    default void assertNotNull(Object... vals) {
        for (var val : vals) {
            assertThat(val).isNotNull();
        }
    }

    default void printValidationIssues(List<ValidationIssue> issues) {
        for (var issue : issues) {
            System.out.println(issue.toString());
        }
    }
}