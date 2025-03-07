package hdi.edi.parser.edi810;

import hdi.edi.objmapper.EdiObjectMapper;
import hdi.edi.objmapper.annotations.EdiElt;
import lombok.Data;
import lombok.experimental.Accessors;

import java.time.LocalDate;

@Data
@Accessors(fluent = true)
public class InvoiceHeader {
    // Mapper will match fields based on element names
    // Alternatively, we can provide EdiElt annotation to match based on segment name/element position
    public static EdiObjectMapper<InvoiceHeader> mapper = new EdiObjectMapper<>();

    private LocalDate date;
    private String invoiceNumber;
    @EdiElt(segType = "BIG", pos = 4)
    private String purchaseOrderNumber;
}