# Generate Python EDI Enums

Generate Python EDI Enums from Java enum.
Each enum inherits from EdiEnum in the edi_model.base module.
The value of the enum is the EDI code.

Example:

```python
class MeasurementType(EdiEnum):
    HEIGHT = "HT"
    HEMOGLOBIN = "R1"
    HEMATOCRIT = "R2"
    EPOETIN = "R3"
    CREATININE = "R4"
```

Corrsponging Java enum:

```java
public enum MeasurementType implements EdiQualifier {

    HEIGHT("HT", null),
    HEMOGLOBIN("R1", null),
    HEMATOCRIT("R2", null),
    EPOETIN("R3", null),
    CREATININE("R4", null),
    NONE("99999", "None"),
    ;

    final String ediValue;
    final String desc;
```

Take each Java enum and create a corresponding Python enum in the edi_model.enums module.

Ignore descriptions in the Java enum, transfer only the ediValue.
Do not create a Python enum for the NONE enum.

Java code base: ~/myarchdev/healthcaredata/claiminsight/clinsight/src

## List of enums to generate

Each section is a package in the Java code base.

### hdi.model.enumtype package

AmountType
DateType
ReferenceType
DrugIdentificationType
IdentificationType
MeasurementType
NoteType
QuantityType
UnitType
ClaimOrEncounterIdentifierType

### hdi.model.claim package

PatientSignatureSourceType.java
AssignmentCertificationType.java
AssignmentParticipationType.java
DelayReasonType.java
RelatedCauseType.java
ReleaseOfInformationType.java
SpecialProgramType.java
ConditionsIndicatorCategory

### hdi.model.claim.dme

DmeBillingFrequency

### hdi.model.claim.ambulance

AmbulanceConditionCode
AmbulanceTransportationReason

### hdi.model.orgperson package

ContactType.java
EntityRole.java
EntityType.java
GenderType.java

### hdi.model.patientsubscriber package

PayerRespSequenceType.java
RelationshipType.java

### hdi.model.payment package

AccountNumberQualifier.java
AdjustmentGroup.java
ClaimStatus.java
DfiQualifier.java
PaymentMethodType.java
TransactionHandlingType.java
InsurancePlanType

### hdi.model.status

StatusActionType

## Acceptance Criteria

Run py_compile for all generated/updated files.