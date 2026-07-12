package hdi.edi.parser;

import lombok.extern.slf4j.Slf4j;
import org.junit.Test;

@SuppressWarnings("NewClassNamingConvention")
@Slf4j
public class VersionAndLicenseInfoExample implements ParsingExampleHelper {

    @Test
    public void printParserVersionAndLicenseInfo() {
        System.out.println(EdiParser.getVersion());
        var licenseInfo = EdiParser.getLicenseInfo();
        // License will be null if not set
        System.out.println(licenseInfo);
    }
}