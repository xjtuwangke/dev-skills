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
