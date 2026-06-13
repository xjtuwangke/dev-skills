# Testing Technical Reference

## Source Areas
- `pom.xml`
- `config/checkstyle/checkstyle.xml`
- `src/test/java/`
- `src/test/resources/`
- `agents/technical.md`

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
- `DownstreamClientsTest`: WebClient downstream host, path, method, and response DTO mapping.

## Command Ownership
- Choose commands from `agents/technical.md`.
- Run Maven directly when verification is required; use the low-context log pattern for noisy commands.
- Do not add subagent or tool-wrapper files unless the user explicitly asks.

## Best Practices
- Prefer targeted tests for the changed surface before running the full gate.
- Use `WebTestClient` for endpoint contracts and `StepVerifier` for reactive service/client behavior.
- Mock collaborators at the layer boundary; avoid full Spring context tests unless wiring/config is the behavior.
- Keep full Maven logs under `target/agent-maven-logs/` and return only concise summaries.

```java
StepVerifier.create(client.getAvailability("SKU-1"))
        .expectNext(new CatalogAvailabilityResponse("SKU-1", true, 42))
        .verifyComplete();
```

```bash
mkdir -p target/agent-maven-logs
mvn -B -ntp -Dtest=DownstreamClientsTest test > target/agent-maven-logs/downstream-clients-test.log 2>&1
grep -E "Tests run:|BUILD SUCCESS|BUILD FAILURE|ERROR|FAILURE" target/agent-maven-logs/downstream-clients-test.log | tail -40
```
