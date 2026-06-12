# Integrations Technical Reference

## Source Areas
- `src/main/java/com/acme/skillplayground/`
- `src/main/resources/application*.yml`
- Tests covering integration boundaries under `src/test/java/`

## Concerns
- WebClient, RestClient, SDK clients, Pub/Sub clients, and database calls that cross process boundaries.
- Retry, timeout, backoff, idempotency, and error mapping behavior.
- Profile-specific endpoints, topics, credentials, and project IDs.
- Observability for downstream failures through logs, metrics, responses, or tests.

## Current External Systems
- Postgres through JPA repositories.
- GCP Pub/Sub through `PubSubTemplate` when enabled.
- No HTTP downstream client is currently present.
- Payment, fulfillment, catalog, promotion, support, and audit are local fixture services today; treat them as likely integration seams in a real system.
