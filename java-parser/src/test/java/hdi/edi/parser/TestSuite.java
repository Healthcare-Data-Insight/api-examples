package hdi.edi.parser;


import hdi.edi.parser.edi810.Edi810ParsingExample;
import hdi.edi.writer.ClaimToEdiExample;
import org.junit.runner.RunWith;
import org.junit.runners.Suite;

@RunWith(Suite.class)
@Suite.SuiteClasses({
        ConverterExample.class,
        Claim837ParsingExample.class,
        Payment835ParsingExample.class,
        Member834ParsingExample.class,
        ClaimStatus277CAParsingExample.class,
        SegmentParsingExample.class,
        Edi810ParsingExample.class,
        ClaimToEdiExample.class
})

public class TestSuite {
}