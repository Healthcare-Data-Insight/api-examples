package hdi.edi.parser;

import hdi.edi.legacyparser.SegmentType;
import hdi.edi.parser.EdiParser;
import hdi.edi.parser.EdiParsingResults;
import hdi.edi.parser.EdiSeg;
import hdi.edi.parser.Elt;
import hdi.edi.parserhelper.SegMatcher;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.math.BigDecimal;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@SuppressWarnings("NewClassNamingConvention")
public class SegmentParsingExample {


    private EdiParser parser;

    @Test
    public void findSegments() {
        EdiParsingResults results = parser.parse();
        // find transactions
        List<EdiSeg> tranSegs = results.findSegsByType(SegmentType.ST);
        EdiSeg tran = tranSegs.get(0);

        List<EdiSeg> tranChildSegs = tran.childSegs();
        var segMatcher = new SegMatcher();
        // find claim segments for this transaction
        var claimSegs = segMatcher.findByType(tranChildSegs, SegmentType.CLM);
        assertThat(claimSegs).hasSize(1);
        // get the first claim
        var claimSeg = claimSegs.get(0);
        // find all dates for the claim
        var dateSegs = segMatcher.findByLoopAndType(claimSeg.childSegs(), "2300", SegmentType.DTP);
        assertThat(dateSegs).isNotEmpty();
    }

    @Test
    public void elementsForTheSegment() {

        EdiParsingResults results = parser.parse();
        var claimSeg = results.findFirstSegByType(SegmentType.CLM);
        assertThat(claimSeg).isNotNull();

        // iterate over elts and do something with them based on name or position (CLM01, CLM05, etc)
        // position is defined by the spec, elements could be omitted. for CLM, positions are 1, 2, 5, 7, 8,9
        String patientAccountNumber=null;
        BigDecimal chargeAmount=null;
        String medicareAssessmentCode = null;
        for (Elt elt : claimSeg.eltSet().elts()) {

            switch (elt.position()) {
                // CLM01
                case 1 -> patientAccountNumber=elt.stringVal();
                // CLM02, charge amount
                case 2 -> chargeAmount=elt.bigDecimalVal();
                // CLM07, medicare assignment code
                case 7 -> medicareAssessmentCode = elt.stringVal();
            }
        }
        assertThat(patientAccountNumber).isEqualTo("26462967");
        assertThat(chargeAmount).isEqualTo(new BigDecimal("100.00"));
        assertThat(medicareAssessmentCode).isEqualTo("A");

        // or by name
        chargeAmount = claimSeg.eltByName("total_claim_charge_amount").bigDecimalVal();
        assertThat(chargeAmount).isEqualTo(new BigDecimal("100.00"));

    }

    @Test
    public void printSegments() {
        EdiParsingResults results = parser.parse();
        List<EdiSeg> claimSegs = results.findSegsByType(SegmentType.CLM);
        EdiSeg claimSeg = claimSegs.get(0);
        System.out.println(claimSeg.toFormattedStringWithChildren());
        // or print all segments using the static method
        System.out.println(EdiSeg.toFormattedStringWithChildren(claimSegs));
    }


    @Before
    public void setup(){
        var ediFile837p = new File("../edi_files/837/prof-encounter.dat");
        parser = new EdiParser(ediFile837p);
    }

    private void assertNotNull(Object ... vals) {
        for(var val:vals){
            assertThat(val).isNotNull();
        }
    }

}