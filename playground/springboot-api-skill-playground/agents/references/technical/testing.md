# Testing Technical Reference

## Source Areas
- `pom.xml`
- `config/checkstyle/checkstyle.xml`
- `src/test/java/`
- `src/test/resources/`

## Concerns
- JUnit 5, Mockito, Reactor `StepVerifier`, and `WebTestClient` coverage.
- Endpoint contracts, service state changes, persistence assumptions, Pub/Sub publication, and error paths.
- JaCoCo thresholds and Checkstyle rules that can block builds.
- Targeted Maven commands for the likely change area.

## Current Test Map
- `OrderEndpointTest`: order API routes and order error behavior.
- `RetailOperationsEndpointTest`: cross-domain retail routes and 409/422 problem details.
- `OrderServiceTest`: JPA-backed order service and Pub/Sub publication.
- `RetailDomainServicesTest`: customer, catalog, inventory, pricing, promotion, payment, fulfillment, returns, support, and audit service rules.
- `GcpPubSubOrderEventPublisherTest`: GCP Pub/Sub payload publishing.
- `NoopOrderEventPublisherTest`: disabled Pub/Sub behavior.

## Command Ownership
- Recommend commands here.
- Delegate actual Maven execution to `maven-runner` when subagents are available.
- Without subagents, run commands directly only when the user asked for verification or the task requires it.
