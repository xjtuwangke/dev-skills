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
- WebClient downstream hosts configured under `clients.*.base-url`.
- Current downstream WebClient calls cover customer profile, catalog, inventory, payment gateway, and shipping hosts.
- Payment, fulfillment, catalog, promotion, support, and audit remain local fixture services too; treat them as likely integration seams in a real system.

## Best Practices
- Keep external system addresses in typed configuration properties.
- Give each integration an owner class and a focused test.
- Document timeout, retry, idempotency, and error behavior when adding it; write "not configured" when absent.
- Do not let profile-specific credentials or secrets leak into agent docs.

```java
@ConfigurationProperties(prefix = "clients")
public record DownstreamClientProperties(
        Service customerProfile,
        Service catalog,
        Service inventory,
        Service paymentGateway,
        Service shipping) {

    public record Service(String baseUrl) {
    }
}
```
