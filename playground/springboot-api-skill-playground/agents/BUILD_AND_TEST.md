# Build And Test

## Core Commands
- Build: `mvn clean verify`
- Unit tests: `mvn test`
- Targeted test: `mvn -Dtest=SomeTest test`
- Endpoint tests: `mvn -Dtest=OrderEndpointTest,RetailOperationsEndpointTest test`
- Service/domain tests: `mvn -Dtest=OrderServiceTest,RetailDomainServicesTest test`
- Pub/Sub tests: `mvn -Dtest=GcpPubSubOrderEventPublisherTest,NoopOrderEventPublisherTest test`
- Package without tests: `mvn -DskipTests package`
- Checkstyle: `mvn checkstyle:check`
- Coverage report: `mvn test jacoco:report`

## Spring Boot Commands
- Run locally: `mvn spring-boot:run`
- Package without tests: `mvn -DskipTests package`
- Run with a profile: `mvn spring-boot:run -Dspring-boot.run.profiles=dev`
- Profiles detected: `dev`, `ppd`, `prd`, `sit`, `uat`

## Quality Gates Detected
- Checkstyle plugin: True
- JaCoCo plugin: True
- Spring Boot Maven plugin: True

## Verification Strategy
- Prefer targeted tests while editing.
- Run full build before finishing changes that affect shared behavior.
- If external services, shared environments, or slow dependency resolution block a command, record the command and reason.

## Low-Context Maven Output
When a Maven Runner subagent is not available, do not stream full Maven logs into the main agent context. Redirect full output to `target/agent-maven-logs/`, then return only a concise summary.

```bash
mkdir -p target/agent-maven-logs
mvn -B -ntp clean verify > target/agent-maven-logs/clean-verify.log 2>&1
grep -E "Tests run:|BUILD SUCCESS|BUILD FAILURE|Total time|ERROR|FAILURE" target/agent-maven-logs/clean-verify.log | tail -40
```

If the command fails, inspect focused reports before reading the full log:

- `target/surefire-reports/*.txt`
- `target/checkstyle-result.xml`
- `target/site/jacoco/jacoco.xml`
- `tail -80 target/agent-maven-logs/clean-verify.log`
