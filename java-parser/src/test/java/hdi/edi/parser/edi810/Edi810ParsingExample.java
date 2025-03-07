package hdi.edi.parser.edi810;

import hdi.edi.parser.EdiParser;
import hdi.edi.parser.EdiSeg;
import hdi.edi.parser.SegmentType;
import hdi.model.orgperson.OrgOrPerson;
import org.junit.Test;

import java.io.File;

import static hdi.edi.parser.ParsingExampleHelper.EDI_FILES_DIR;

public class Edi810ParsingExample {

    public static final int CHUNK_SIZE = 1;
    public static final File TEST_FILE = new File(EDI_FILES_DIR + "/810/810-test.edi");

    @Test
    public void parse810() {
        try (var parser = new EdiParser(TEST_FILE)) {
            while (true) {
                var results = parser.parse(CHUNK_SIZE);
                if (results.isDone()) {
                    break;
                }
                for (var tranSeg : results.segs()) {
                    var invoice = parseInvoice(tranSeg);
                    System.err.println(invoice);
                }
            }
        }
    }

    @Test
    public void printTestFile() {
        try (var parser = new EdiParser(TEST_FILE)) {
            int i = 0;
            while (true) {
                var results = parser.parse(CHUNK_SIZE);
                if (results.isDone()) {
                    break;
                }
                for (var tranSeg : results.segs()) {
                    System.err.println("** Transaction " + i);
                    System.err.println(tranSeg.toFormattedStringWithChildren());
                }
                ++i;
            }
        }
    }

    private Invoice parseInvoice(EdiSeg tran) {
        var invoice = new Invoice();
        var bigSeg = tran.findFirstChildSeg(SegmentType.BIG);
        if (bigSeg != null) {
            var invoiceHeader = new InvoiceHeader();
            InvoiceHeader.mapper.populate(invoiceHeader, bigSeg);
            invoice.invoiceHeader(invoiceHeader);
        }
        var nameSegs = tran.findChildSegs(SegmentType.N1);
        for (var seg : nameSegs) {
            if (seg.entity() instanceof OrgOrPerson org) {
                invoice.orgs().add(org);
            }
        }
        var it1Segs = tran.findChildSegs(SegmentType.IT1);
        for (var seg : it1Segs) {
            parseDetailsLoop(invoice, seg);
        }
        return invoice;
    }

    private void parseDetailsLoop(Invoice invoice, EdiSeg it1Seg) {
//        System.err.println(it1Seg.toFormattedStringWithChildren());
        var invoiceDetails = new InvoiceDetail();
        invoice.invoiceDetails().add(invoiceDetails);
        InvoiceDetail.mapper.populateFromLoop(invoiceDetails, it1Seg);
        var itdSegs = it1Seg.findChildSegs(SegmentType.IT3);
        for (var seg : itdSegs) {
            var additionalItemData = new AdditionalItemData();
            AdditionalItemData.mapper.populate(additionalItemData, seg);
            invoiceDetails.additionalItems().add(additionalItemData);
        }
    }

}