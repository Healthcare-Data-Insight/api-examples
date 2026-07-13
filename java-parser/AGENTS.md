# Java Parser Example Project Instructions

## Scope

These instructions apply to the
`java-parser` project and everything below this directory. The project contains JUnit-based examples for the Healthcare Data Insight EDI parser, converter, and generator.

## Prerequisites

- Use Java 17 or later. The Gradle build sets `sourceCompatibility` to Java 17.
- Use the checked-in Gradle wrapper; do not require a separately installed Gradle distribution.
- Run Gradle commands from the `java-parser` directory so relative sample and output paths resolve correctly.
- A valid EDI license is required to execute the examples. Configure one of:
    - `etc/edi-license.txt`
    - `EDI_LICENSE_FILE` with the absolute license-file path
    - `EDI_LICENSE_KEY` with the license contents
    - The equivalent `edi-license-file` or `edi-license-key` Java system property
- Never commit or print license-key contents.

## Build

From the repository root:

```shell
cd java-parser
./gradlew clean build
```

On Windows:

```powershell
cd java-parser
gradlew.bat clean build
```

Dependencies are resolved from Maven Central and
`https://repo.datainsight.health/repository/maven-releases/` as configured in `build.gradle`.

Note: the license file is already set in `~/.ediconvert`

## Run the Examples

The examples are JUnit 4 tests under `src/test/java`. Run the configured example suite with:

```shell
./gradlew test
```

The Gradle `test` task is filtered to
`hdi.edi.parser.TestSuite`. Add every new runnable example that should be part of the standard verification to
`src/test/java/hdi/edi/parser/TestSuite.java`.

`TransformClaimExample` is currently an opt-in example and is not included in
`TestSuite`; run it directly from an IDE when needed.

Sample inputs are read from the repository-level `../edi_files` directory. Generator examples write to
`../out_edi_files`, and converter examples write to `converted` under this project.

## Required Verification

`TestSuite` must succeed for every build. Before considering any change in this project complete, run:

```shell
./gradlew clean test
```

Do not report a successful build if
`TestSuite` was skipped, filtered out, or failed. If the suite cannot run because a license or dependency is unavailable, report that as an environment blocker rather than treating the change as verified.