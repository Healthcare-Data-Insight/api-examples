package hdi.edi.parser.edi810;

import hdi.edi.objmapper.EdiObjectMapper;
import lombok.Data;
import lombok.experimental.Accessors;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;

@Accessors(fluent = true)
@Data
public class InvoiceDetail {
    public static EdiObjectMapper<InvoiceDetail> mapper = new EdiObjectMapper<>();

    private String assignedIdentification;
    private BigDecimal unitPrice;
    private List<AdditionalItemData> additionalItems = new ArrayList<>();
}