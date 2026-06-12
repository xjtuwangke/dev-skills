# Commerce Fulfillment Demo

This fixture is a realistic Spring WebFlux backend used to evaluate the
`init-project` skill. It models an order fulfillment service with PostgreSQL,
Redis, outbound clients, GCP Pub/Sub, Springfox API docs, and multiple runtime
environments.

The fixture intentionally includes enough surface area for agent documentation:

- 20+ HTTP endpoints.
- Endpoint, service, persistence, client, and pub/sub layers.
- Request-driven and event-driven call chains.
- `src/main/resources/openapi.yaml` as the expected API contract artifact.
- Expected generated agent docs under `expected/`.

This is a documentation/eval fixture, not a production service.

