# Karate AT Template

Use this template when the project or a meaningful part of the project uses Karate for acceptance tests, API tests, contract tests, smoke tests, or regression suites. It usually combines with `maven-java`.

## Detection Checklist

Strong signals:

- Dependencies include `com.intuit.karate`, `io.karatelabs`, `karate-core`, `karate-junit5`, or related Karate artifacts.
- `.feature` files exist, usually under `src/test/java` or `src/test/resources`.
- Java runner classes invoke Karate.
- Project naming, README, or CI labels mention AT, acceptance tests, API tests, contract tests, regression tests, or Karate.

Supporting signals:

- `karate-config.js`.
- Environment-specific config files.
- Test data under `src/test/resources`, `data`, `payloads`, `schemas`, or `fixtures`.
- CI jobs that run tagged suites or environment-specific smoke/regression commands.

## Files To Inspect

```text
pom.xml
README.md
src/test/java/
src/test/resources/
karate-config.js
.github/workflows/
Jenkinsfile
```

Read representative files:

- One or two `.feature` files from core suites.
- The main Karate runner class.
- `karate-config.js`.
- README/CI commands for environments and tags.
- Shared helpers, schemas, or payload fixtures if referenced by features.

## Template Scripts

After `karate-at` matches, use the static inspector to collect test-suite evidence:

```bash
python3 /path/to/init-project/scripts/templates/karate-at/inspect_karate_project.py /path/to/project
```

It emits JSON for feature files, tags, runner classes, `karate-config.js`, environment hints, and fixtures/schemas/payloads. Use this output to refine `PROJECT_PROFILE.md`, `BUILD_AND_TEST.md`, `CODE_STYLE.md`, `ARCHITECTURE_NOTES.md`, and `TEMPLATE_NOTES.md`.

## AGENTS.md Guidance

Add these Karate-specific facts:

```markdown
## Project
- Primary purpose: [Karate acceptance-test project / service repo with Karate tests]
- Template facets: maven-java, karate-at[, additional facets]
- Feature roots: [discovered roots]
- Runner roots: [discovered roots]

## Working Rules
- Keep scenarios readable and behavior-focused.
- Reuse existing helpers, payload fixtures, schemas, and tag conventions.
- Do not hard-code credentials, tokens, hostnames, or environment-specific secrets.
- Preserve environment/tag behavior when adding or changing tests.
```

## PROJECT_PROFILE.md Content

Capture:

- Feature file roots and naming conventions.
- Runner classes and suite entrypoints.
- Environment model: `karate.env`, config files, profile flags, base URLs.
- Shared utilities: JS helpers, Java helpers, reusable feature calls, schemas, payload fixtures.
- External systems under test and safe test data assumptions.
- CI jobs, tags, and suite names.

Mark anything environment-specific as "Needs confirmation" unless verified in docs/config.

## BUILD_AND_TEST.md Content

Typical commands to adapt:

```bash
./mvnw test
./mvnw test -Dkarate.env=dev
./mvnw test -Dkarate.options="--tags @smoke"
./mvnw test -Dtest=SomeRunner
```

Document:

- Safe local smoke command.
- Full regression command.
- How to run one runner, one feature, or one tag.
- Required env vars and secrets handling.
- Commands that call real shared environments and should be used carefully.

## CODE_STYLE.md Content

Infer style from existing features:

- Feature naming and folder grouping.
- Scenario names and Given/When/Then style.
- Tag naming and placement.
- Payload and schema fixture conventions.
- Common variables and helper calls.
- Assertion style: status, response fields, schema matching, headers, side effects.
- Java runner naming and package conventions.

Karate tests are executable specs; keep intent clear for humans.

## ARCHITECTURE_NOTES.md Content

Document the test flow:

```text
Maven command -> JUnit/Karate runner -> karate-config.js -> feature files -> shared helpers/fixtures -> system under test
```

Add project-specific notes:

- Which suites are smoke, regression, contract, or environment-specific.
- Where authentication/session setup happens.
- Where base URLs and per-environment config are defined.
- How test data is created, reused, and cleaned up.
- How reports are generated and where they land.
- Risks around shared environments, flaky dependencies, and data coupling.

## TEMPLATE_NOTES.md Content

```markdown
# Karate AT Agent Notes

## Scenario Guidelines
- Keep scenarios behavior-focused and readable.
- Reuse existing `Background`, helper features, JS utilities, and fixtures before adding new ones.
- Use tags consistently so CI suites continue to select the right tests.
- Prefer meaningful assertions on response body, schema, headers, and business fields.

## Environment Guidelines
- Respect `karate.env` and existing config resolution.
- Do not hard-code secrets, tokens, or personal endpoints.
- Treat shared test environments as stateful and potentially fragile.
- Document any required test data setup or cleanup.

## Maintenance Guidelines
- Add new fixtures near related features and name them clearly.
- Keep generated reports, target output, and local logs out of source control.
- When changing common helpers, run or identify all affected suites.

## Common Risks
- A scenario passes only because it checks status code and ignores response content.
- Tags drift from CI expectations.
- Tests depend on mutable shared data without setup/cleanup.
- Environment-specific values are baked into feature files.
```
