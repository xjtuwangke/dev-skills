# Services Technical Reference

## Source Areas
- `src/main/java/com/acme/skillplayground/service/`
- `src/main/java/com/acme/skillplayground/mapper/`
- `src/main/java/com/acme/skillplayground/model/`
- `src/main/java/com/acme/skillplayground/exception/`
- `src/test/java/com/acme/skillplayground/service/`

## Current Services
- `OrderService`
- `CustomerProfileService`
- `CatalogQueryService`
- `InventoryReservationService`
- `PricingService`
- `PromotionService`
- `PaymentAuthorizationService`
- `FulfillmentPlanningService`
- `ReturnPolicyService`
- `SupportTicketService`
- `AuditTrailService`

## Current Mappers
- `MoneyMapper`
- `CustomerProfileMapper`
- `CatalogMapper`
- `FulfillmentMapper`

## Concerns
- Public use-case methods and collaborator boundaries.
- Entity/model conversion, defaults, and enum transitions.
- Not-found, validation, duplicate, and failure behavior.
- Transactional assumptions and blocking calls inside reactive wrappers.
- Event publication timing relative to persistence changes.
- Manual type mapping, rounding, date, and domain-rule decisions.

## Related Context
- Persistence: `agents/references/technical/persistence.md`
- Pub/Sub side effects: `agents/references/technical/pubsub.md`
- Business domain: `agents/references/business/order-domain.md`
- Cross-domain behavior: `agents/BACKEND_SURFACES.md`
