# Build And Test

## Commands

| Task | Command |
| --- | --- |
| Compile | `./mvnw compile` |
| Unit tests | `./mvnw test` |
| Package | `./mvnw package` |
| Run dev | `SPRING_PROFILES_ACTIVE=dev ./mvnw spring-boot:run` |

Use `mvn` only when the wrapper is unavailable. The wrapper is pinned to Maven 3.4.0 for this fixture.

## Expected Test Style

- Endpoint tests use `WebTestClient`.
- Service tests should use Reactor `StepVerifier`.
- Client tests should mock downstream HTTP with a fake server or WebClient exchange function.
- Pub/Sub tests should verify payload serialization, topic/subscription names, ack behavior, and idempotency decisions.

## Verification Checklist

- Endpoint changed: run endpoint tests and compare `openapi.yaml`.
- Service behavior changed: run service tests and update `CALL_CHAINS.md` if the orchestration changed.
- Repository changed: verify schema/migration and repository tests.
- Client changed: verify timeout, retry, error mapping, and base URL config.
- Pub/Sub changed: verify topic/subscription config, payload compatibility, ack behavior, retry/DLQ assumptions.

## Known Fixture Caveat

Springfox is runtime/context based. Do not claim it can produce `openapi.yaml` from Maven with no Spring context. A no-HTTP export can be implemented as a Spring test that starts `MOCK` web environment and writes Springfox model output to `target/openapi.yaml`.

