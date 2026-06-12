# Agent Instructions

## Project

- Maven Java 17 reactive backend service.
- Business domain: commerce order fulfillment across orders, customers, inventory, payments, fulfillment plans, shipments, returns, reconciliation, and order events.
- Primary runtime stack: Spring WebFlux, PostgreSQL via R2DBC, Reactive Redis, GCP Pub/Sub, Springfox API docs.
- Maven wrapper is pinned to Maven 3.4.0. The POM enforces Maven `>=3.4.0` and Java `[17,18)`.
- Springfox is a legacy docs dependency. This fixture keeps Spring Boot 2.7.18 to make Springfox 3 usable with WebFlux and Java 17.

## Read First

- `agents/PROJECT_PROFILE.md` for modules, packages, envs, and important files.
- `agents/BACKEND_SURFACES.md` before changing endpoints, persistence, clients, Redis, or pub/sub.
- `agents/CALL_CHAINS.md` before changing behavior behind an existing API or message handler.
- `agents/BUILD_AND_TEST.md` before running verification.
- `agents/DEPENDENCIES.md` before changing the POM or dependency versions.

## Common Commands

- Compile: `./mvnw compile`
- Run tests: `./mvnw test`
- Package: `./mvnw package`
- Run locally: `SPRING_PROFILES_ACTIVE=dev ./mvnw spring-boot:run`
- Export Springfox docs without an HTTP server: add a Spring test that reads Springfox `DocumentationCache` and writes `target/openapi.yaml`; do not assume Springfox can generate OpenAPI without starting a Spring context.

## Change Rules

- Keep HTTP handlers in `endpoint/`; keep business decisions in `service/`.
- Keep storage access behind `database/` repositories.
- Keep outbound HTTP calls in `client/`; document base URL config keys, timeout, retry, and error mapping.
- Keep GCP Pub/Sub publish/consume behavior in `pubsub/`; document topic/subscription, payload, idempotency, and ack behavior.
- When changing an endpoint, update `src/main/resources/openapi.yaml`, endpoint tests, `agents/BACKEND_SURFACES.md`, and the relevant chain in `agents/CALL_CHAINS.md`.
- When changing order, payment, inventory, or shipment behavior, check both request-driven and event-driven chains.
- Never write secrets to generated agent docs. Reference environment variable names such as `DB_USER` and `DB_PASSWORD` only.

