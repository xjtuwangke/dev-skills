# Endpoints Technical Reference

## Source Areas
- `src/main/java/com/acme/skillplayground/endpoint/`
- `src/main/java/com/acme/skillplayground/model/`
- `src/main/java/com/acme/skillplayground/exception/`
- `src/test/java/com/acme/skillplayground/endpoint/`

## Current Surface
- `POST /api/orders`
- `GET /api/orders/{id}`
- `GET /api/orders/customers/{customerId}`
- `PATCH /api/orders/{id}/status`
- `GET /api/retail/customers/{customerId}/profile`
- `GET /api/retail/catalog/items/{sku}`
- `POST /api/retail/inventory/reservations`
- `POST /api/retail/pricing/quotes`
- `GET /api/retail/promotions/{couponCode}/eligibility`
- `POST /api/retail/payments/authorizations`
- `POST /api/retail/fulfillment/plans`
- `POST /api/retail/returns/authorizations`
- `POST /api/retail/support/tickets`
- `GET /api/retail/audit/orders/{orderId}`

## Concerns
- Route methods, paths, path variables, request bodies, and response status codes.
- Validation annotations and exception mapping.
- WebFlux return types and blocking boundaries.
- SpringDoc/OpenAPI annotations when present.
- Endpoint tests for success, validation, not-found, and error paths.
- Retail operation endpoints route to many focused services; do not assume all business logic is in the endpoint.

## Related Context
- Business behavior: `agents/references/business/order-api-use-cases.md`
- Domain terms: `agents/references/business/order-domain.md`
- Retail domain map: `agents/BACKEND_SURFACES.md`
- Runtime call chains: `agents/CALL_CHAINS.md`
