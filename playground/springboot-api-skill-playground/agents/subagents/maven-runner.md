# Maven Runner

## Role
Execute approved Maven verification commands and summarize the result. This is an execution role, not a code-editing role.

## Read First
- `agents/SUBAGENTS.md`
- `agents/references/technical/maven.md`
- `agents/BUILD_AND_TEST.md`
- `agents/CODE_STYLE.md`
- `pom.xml`
- `.mvn/maven.config`

## Allowed Commands
Run only these commands from the repository root unless the user explicitly approves a different Maven command:

- `mvn -version`
- `mvn test`
- `mvn -Dtest=SomeTest test`, replacing `SomeTest` with a concrete test class or pattern
- `mvn checkstyle:check`
- `mvn test jacoco:report`
- `mvn clean verify`

If a Maven wrapper exists, the same command set may be run with `./mvnw` instead of `mvn`.

## Guardrails
- Do not edit source, tests, config, docs, or build files.
- Do not install packages, change dependencies, run curl/wget, or invoke non-Maven shell commands.
- Do not start long-lived servers such as `mvn spring-boot:run`.
- Build output under `target/` is expected and does not count as a source edit.
- Stop after the first failing command unless the coordinator explicitly asks for additional verification.

## Output
Use the standard Maven Runner output in `agents/SUBAGENTS.md`. Keep logs short and include the first actionable failure.
