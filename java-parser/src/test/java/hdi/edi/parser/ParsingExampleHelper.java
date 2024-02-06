package hdi.edi.parser;

import static org.assertj.core.api.Assertions.assertThat;

public interface ParsingExampleHelper {
    String EDI_FILES_DIR = "../edi_files";

    default void assertNotNull(Object... vals) {
        for (var val : vals) {
            assertThat(val).isNotNull();
        }
    }
}