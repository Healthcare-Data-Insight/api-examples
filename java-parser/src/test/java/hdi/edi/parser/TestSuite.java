package hdi.edi.parser;


import org.junit.runner.RunWith;
import org.junit.runners.Suite;

@RunWith(Suite.class)
@Suite.SuiteClasses({
        ClaimParsingExample.class,
        PaymentParsingExample.class,
        SegmentParsingExample.class
})
public class TestSuite {
}