# Architecture Notes

## Test Flow

```text
Maven Surefire -> DemoServiceAtRunner -> karate-config.js -> feature files -> payload fixtures -> running demo service
```

## Boundaries
- This project is a black-box HTTP AT suite.
- The service under test is the sibling Spring Boot project, not a Maven dependency.
- The AT suite verifies public API behavior through HTTP status codes, response bodies, headers, and problem-detail errors.

## Covered Surfaces
- Order lifecycle: create, fetch by id, list by customer, update status.
- Retail reads: customer profile, catalog item, promotion eligibility, audit trail.
- Retail writes: inventory reservation, price quote, payment authorization, shipment planning, return authorization, support ticket creation.
- Error mapping: order domain rule violation, inventory conflict, unsupported payment currency.

## Environment Risks
- Hosted tests depend on an already running service.
- Order lifecycle scenarios require service persistence to be healthy because `/api/orders` uses JPA/PostgreSQL.
- Retail read/write scenarios mostly use deterministic in-memory mapper/service behavior, but the Spring app still needs to start successfully.
- Shared environments may contain prior order data; assertions avoid assuming list endpoints return only one order.

## Extension Points
- Add new feature files under `features/<surface>/` and tag them by suite.
- Add new payload fixtures under `payloads/<surface>/`.
- Add service-specific setup/cleanup only when the demo API exposes safe endpoints for it.
