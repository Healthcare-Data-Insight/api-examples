package hdi.edi.parser.edi810;

import hdi.edi.objmapper.EdiObjectMapper;
import hdi.edi.objmapper.annotations.EdiElt;
import lombok.Data;
import lombok.experimental.Accessors;

import java.math.BigDecimal;

@Accessors(fluent = true)
@Data
public class AdditionalItemData {
    public static EdiObjectMapper<AdditionalItemData> mapper = new EdiObjectMapper<>();

    @EdiElt(seg = "IT3", pos = 1)
    private BigDecimal numberOfUnits;
    @EdiElt(seg = "IT3", pos = 2)
    private String unitTypeCode;
    @EdiElt(seg = "IT3", pos = 3)
    private String statusCode;
    @EdiElt(seg = "IT3", pos = 4)
    private BigDecimal quantityDifference;
    @EdiElt(seg = "IT3", pos = 5)
    private String changeReasonCode;

}