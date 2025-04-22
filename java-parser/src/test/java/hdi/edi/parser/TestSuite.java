package hdi.edi.parser;


import hdi.edi.parser.edi810.Edi810ParsingExample;
import org.junit.runner.RunWith;
import org.junit.runners.Suite;

@RunWith(Suite.class)
@Suite.SuiteClasses({
        ConverterExample.class,
        ClaimParsingExample.class,
        PaymentParsingExample.class,
        SegmentParsingExample.class,
        Edi810ParsingExample.class
})

public class TestSuite {
}