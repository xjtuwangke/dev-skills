# Maven Technical Reference

## Core Commands
- `mvn -version`
- `mvn test`
- `mvn -Dtest=SomeTest test`
- `mvn -Dtest=OrderEndpointTest,RetailOperationsEndpointTest test`
- `mvn -Dtest=OrderServiceTest,RetailDomainServicesTest test`
- `mvn checkstyle:check`
- `mvn test jacoco:report`
- `mvn clean verify`

## Quality Gates
- Checkstyle enforces import, header, and final-variable style rules.
- JaCoCo monitors unit-test coverage.
- `mvn clean verify` is the broadest local verification command.

## Runner Boundary
- Use `agents/subagents/maven-runner.md` when a subagent should run Maven.
- Do not use Maven Runner for code edits, dependency changes, installs, or long-lived server commands.
- If no Maven Runner is available, the coordinator should use the low-context Maven protocol from `agents/BUILD_AND_TEST.md`.
- Prefer `-B -ntp` for agent-run Maven commands to reduce noise.
