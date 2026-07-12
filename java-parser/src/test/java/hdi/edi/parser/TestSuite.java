package hdi.edi.parser;


import hdi.edi.gen.Generate835EdiExample;
import hdi.edi.gen.Generate837EdiExample;
import hdi.edi.parser.edi810.Edi810ParsingExample;
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
        Generate837EdiExample.class,
        Generate835EdiExample.class
})

public class TestSuite {
}