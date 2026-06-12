# Persistence Technical Reference

## Source Areas
- `src/main/java/com/acme/skillplayground/database/`
- `src/main/resources/db/migration/`
- `src/main/resources/application*.yml`
- Persistence-related tests under `src/test/java/`

## Current Migrations
- `V1__create_orders.sql`: order intake table used by `OrderEntity`.
- `V2__retail_platform_schema.sql`: 36-table retail platform schema for customer, catalog, supplier, inventory, pricing, promotion, sales order, payment, fulfillment, returns, support, audit, outbox, and feature flags.
- `V3__add_order_shipping_priority.sql`: adds order shipping priority, requested ship date, and manual review fields.

## Table Count
- 37 tables total across V1 and V2.
- Only `orders` currently has a JPA entity/repository in this fixture.
- Most V2 tables are schema evidence for project complexity and future repository work.

## Concerns
- JPA entity fields, table names, indexes, constraints, generated values, and enum storage.
- Spring Data repository methods and query assumptions.
- Flyway migration compatibility with the entity model.
- Postgres profile config, environment variables, and secret placeholders.
- WebFlux plus Hibernate/JPA blocking behavior.
- Distinguish implemented JPA surfaces from schema-only tables when planning changes.

## Related Context
- Service behavior: `agents/references/technical/services.md`
- Build/test commands: `agents/references/technical/maven.md`
