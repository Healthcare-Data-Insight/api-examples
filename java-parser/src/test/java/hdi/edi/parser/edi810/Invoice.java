package hdi.edi.parser.edi810;

import hdi.model.orgperson.OrgOrPerson;
import lombok.Data;
import lombok.experimental.Accessors;

import java.util.ArrayList;
import java.util.List;

@Accessors(fluent = true)
@Data
public class Invoice {
    private InvoiceHeader invoiceHeader;
    private List<OrgOrPerson> orgs = new ArrayList<>();
    private List<InvoiceDetail> invoiceDetails = new ArrayList<>();
}