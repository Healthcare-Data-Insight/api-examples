# EDI Parser and Generator Java Examples

This project contains runnable examples for parsing, validating, converting, and generating X12 EDI with the [EDI Parser for Java](https://datainsight.health/docs/java-edi-parser/).

## Getting Started

### Prerequisites

- Java 17 or later
- A license key

The included [Gradle build](build.gradle) already configures the Healthcare Data Insight Maven repository and the parser dependencies. It currently uses
`hdi:edi:2.15.1`, along with Jackson and test-only libraries used by the examples.

### Get a License Key

[Request a trial license key](https://datainsight.health/products/edi-license/), then configure it in one of these ways:

- Save the license file as
  `etc/edi-license.txt` in this project. This is the default location when commands are run from the
  `java-parser` directory.
- Set the `EDI_LICENSE_FILE` environment variable to the license file's absolute path.
- Set the `EDI_LICENSE_KEY` environment variable to the contents of the license file.
- Use the equivalent Java system properties: `edi-license-file` or `edi-license-key`.
- Linux/macOS: you can also copy the license file to `~/.ediconvert`

Do not commit your license key to source control.

### Run the Examples

From this directory, run the JUnit example suite with the included Gradle wrapper:

```shell
cd java-parser
./gradlew test
```

On Windows, use:

```powershell
cd java-parser
gradlew.bat test
```

The build downloads dependencies from Maven Central and the DataInsight Maven repository. Sample input files are read from the repository's top-level
`edi_files` directory. Generated EDI is written to the top-level
`out_edi_files` directory, while converter examples write to `java-parser/converted`.

The Gradle `test` task runs [
`TestSuite`](src/test/java/hdi/edi/parser/TestSuite.java), which collects the main examples. Open any example class in your IDE to run or adapt a specific test method. [
`TransformClaimExample`](src/test/java/hdi/edi/gen/TransformClaimExample.java) is intentionally not part of
`TestSuite` and can be run directly from an IDE when you want to try the parse-modify-generate workflow.

## Examples

### Parsing and Validation

- [
  `Claim837ParsingExample`](src/test/java/hdi/edi/parser/Claim837ParsingExample.java) parses 837P and 837I claims in chunks, reads transactions, providers, subscribers, diagnoses, service lines, and validation issues, and demonstrates parser-backed Java enums.
- [
  `Payment835ParsingExample`](src/test/java/hdi/edi/parser/Payment835ParsingExample.java) parses 835 remittances, including payment transactions, adjudicated claims, claim and line adjustments, remark codes, and provider-level adjustments.
- [
  `Member834ParsingExample`](src/test/java/hdi/edi/parser/Member834ParsingExample.java) parses 834 enrollment data into members, coverage records, sponsors, and insurers while collecting validation issues.
- [
  `ClaimStatus277CAParsingExample`](src/test/java/hdi/edi/parser/ClaimStatus277CAParsingExample.java) handles 277CA claim, service-line, provider, and receiver-level acknowledgment statuses, including whole-transaction rejections.
- [
  `SegmentParsingExample`](src/test/java/hdi/edi/parser/SegmentParsingExample.java) works with the raw segment tree: finding segments and loops, reading elements by position or name, formatting segments, and converting segments to Jackson JSON nodes.
- [
  `VersionAndLicenseInfoExample`](src/test/java/hdi/edi/parser/VersionAndLicenseInfoExample.java) prints the parser version and active license information.

### File Conversion

- [
  `ConverterExample`](src/test/java/hdi/edi/parser/ConverterExample.java) converts one or many EDI files to JSON, JSON Lines, or CSV. It also demonstrates validation output, CSV schemas, combined output files, and writing converted data to a custom
  `Writer`.

### EDI Generation and Transformation

- [
  `Generate837EdiExample`](src/test/java/hdi/edi/gen/Generate837EdiExample.java) builds and writes simple professional 837P and institutional 837I claims, including interchange, transaction, provider, subscriber, diagnosis, and service-line data.
- [
  `Generate835EdiExample`](src/test/java/hdi/edi/gen/Generate835EdiExample.java) builds an 835 payment transaction with payer/payee details, a paid claim, service-line amounts, and adjustments.
- [
  `TransformClaimExample`](src/test/java/hdi/edi/gen/TransformClaimExample.java) parses an 837P, updates transaction metadata and claim amounts, validates the modified claims, and writes a new EDI file.
- [
  `GenerateEdiExampleHelper`](src/test/java/hdi/edi/gen/GenerateEdiExampleHelper.java) shows the shared setup for ISA interchange and GS functional-group envelopes used by the generation examples.

## Documentation

- [EDI Parser for Java documentation](https://datainsight.health/docs/java-edi-parser/)
- [Installation and license configuration](https://datainsight.health/docs/java-edi-parser/install/)
- [EDI schemas and Java object model](https://datainsight.health/docs/schemas/intro/)

The source files are deliberately written as JUnit examples so they can be run as-is, debugged in an IDE, and copied into an application as a starting point.