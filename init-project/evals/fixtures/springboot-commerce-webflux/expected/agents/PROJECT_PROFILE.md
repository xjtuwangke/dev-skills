# Project Profile

## Identity

- Name: `commerce-fulfillment-service`
- Group/artifact: `com.acme.commerce:commerce-fulfillment-service`
- Packaging: Spring Boot executable jar.
- Java: 17.
- Maven: wrapper distribution `3.4.0`, enforcer requires `[3.4.0,)`.
- Primary package: `com.acme.commerce`.

## Source Layout

```text
src/main/java/com/acme/commerce/
  config/      runtime properties, WebClient, Redis, Springfox
  model/       request, response, and event records
  database/    reactive repository interfaces and row models
  client/      outbound inventory, payment, and shipping clients
  pubsub/      GCP Pub/Sub publisher and subscribers
  service/     business use cases and call-chain orchestration
  endpoint/    WebFlux REST endpoints
src/main/resources/
  application.yml
  application-dev.yml
  application-sit.yml
  application-uat.yml
  application-ppd.yml
  application-prd.yml
  openapi.yaml
  db/migration/V1__commerce_schema.sql
```

## Environments

| Profile | Purpose | PostgreSQL | Redis | Downstream hosts |
| --- | --- | --- | --- | --- |
| `dev` | local developer profile | `localhost:5432/commerce_dev` | `localhost:6379` | localhost inventory/payment/shipping |
| `sit` | system integration | `postgres-sit.internal` | `redis-sit.internal` | `*.sit.example.com` |
| `uat` | user acceptance | `postgres-uat.internal` | `redis-uat.internal` | `*.uat.example.com` |
| `ppd` | pre-production | `postgres-ppd.internal` | `redis-ppd.internal` | `*.ppd.example.com` |
| `prd` | production | `postgres-prd.internal` | `redis-prd.internal` | production domains |

## Important Config

- PostgreSQL/R2DBC: `spring.r2dbc.*`.
- Redis: `spring.redis.*`.
- Downstream clients:
  - `commerce.clients.inventory.base-url`
  - `commerce.clients.payment.base-url`
  - `commerce.clients.shipping.base-url`
- Pub/Sub:
  - `commerce.pubsub.order-created-topic`
  - `commerce.pubsub.order-cancelled-topic`
  - `commerce.pubsub.payment-authorized-topic`
  - `commerce.pubsub.inventory-reserved-subscription`
  - `commerce.pubsub.shipment-updated-subscription`
- API contract: `src/main/resources/openapi.yaml`.
- Springfox config: `config/SpringfoxConfig.java`.

## Matched Templates

- `baseline`
- `maven-java`
- `springboot3-webflux`

Karate is not part of this fixture.

