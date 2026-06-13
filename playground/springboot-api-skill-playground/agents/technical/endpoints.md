# Endpoints Technical Reference

## Source Areas
- Endpoints: `src/main/java/com/acme/skillplayground/endpoint/`
- API models: `src/main/java/com/acme/skillplayground/model/`
- Error mapping: `src/main/java/com/acme/skillplayground/exception/ApiExceptionHandler.java`
- Endpoint tests: `src/test/java/com/acme/skillplayground/endpoint/`

## API Docs
- Swagger UI when the app runs locally: `http://localhost:8080/swagger-ui.html`
- OpenAPI JSON when the app runs locally: `http://localhost:8080/v3/api-docs`
- Paths come from `springdoc.swagger-ui.path` and `springdoc.api-docs.path` in `src/main/resources/application.yml`.
- Endpoint docs are generated from SpringDoc annotations. Current tags are `Orders` and `Retail operations`.
- No static checked-in OpenAPI file is present.

## Common Endpoint Rules
- Endpoint classes use `@RestController` under `com.acme.skillplayground.endpoint`.
- Request bodies use Java `record` models and `@Valid @RequestBody` when validation annotations exist.
- No endpoint currently declares `@RequestHeader`; there are no explicit header validations yet.
- No endpoint currently declares explicit `consumes` or `produces`; tests send JSON for request bodies.
- Missing required request parameters, invalid UUID path variables, and body validation failures are handled by Spring WebFlux default 400 behavior.
- `ApiExceptionHandler` maps `OrderNotFoundException` to 404, `ResourceConflictException` to 409, and `DomainRuleViolationException` to 422 Problem Details.

## Best Practices
- Keep endpoints thin: validate transport input, call a use case/service, return transport shape.
- Put business rules in services; do not calculate domain decisions in endpoint methods.
- Add/update a `WebTestClient` route test with every request/response or validation change.
- Use `record` DTOs and Bean Validation annotations for request bodies.

```java
@PostMapping
@Operation(summary = "Create an order")
public Mono<ResponseEntity<OrderResponse>> create(@Valid @RequestBody final CreateOrderRequest request) {
    return orderUseCase.create(request)
            .map((final OrderResponse response) -> ResponseEntity
                    .created(URI.create("/api/orders/" + response.id()))
                    .body(response));
}
```

## Endpoints

### POST /api/orders
- Docs: `Orders` tag, "Create an order".
- Class/method: `OrderEndpoint#create`.
- Request: body.
- Request POJO: `com.acme.skillplayground.model.CreateOrderRequest`.
- Response: `201 Created`, `Location: /api/orders/{id}`.
- Response POJO: `com.acme.skillplayground.model.OrderResponse`.

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Body | `customerId` | `@NotBlank` |
| Body | `sku` | `@NotBlank` |
| Body | `quantity` | `@Positive` |
| Body | `shippingPriority` | Optional `ShippingPriority` enum |
| Body | `requestedShipDate` | Optional `LocalDate`, JSON string |
| Header | none | No `@RequestHeader` declared |

- Errors/tests: `OrderEndpointTest#createReturnsCreatedOrder`; domain rule failures map to 422 in `createMapsDomainRuleViolation`.

### GET /api/orders/{id}
- Docs: `Orders` tag, "Get an order by id".
- Class/method: `OrderEndpoint#getById`.
- Request: path `id: UUID`.
- Request POJO: none.
- Response: `200 OK`.
- Response POJO: `com.acme.skillplayground.model.OrderResponse`.

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Path | `id` | UUID path conversion |
| Header | none | No `@RequestHeader` declared |

- Errors/tests: `OrderEndpointTest#getByIdReturnsOrder`; `OrderNotFoundException` maps to 404 in `getByIdMapsNotFound`.

### GET /api/orders/customers/{customerId}
- Docs: `Orders` tag, "List orders by customer id".
- Class/method: `OrderEndpoint#listByCustomer`.
- Request: path `customerId: String`.
- Request POJO: none.
- Response: `200 OK`.
- Response POJO: `java.util.List<com.acme.skillplayground.model.OrderResponse>`.

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Path | `customerId` | `String`; no Bean Validation annotation |
| Header | none | No `@RequestHeader` declared |

- Errors/tests: `OrderEndpointTest#listByCustomerReturnsOrders`.

### PATCH /api/orders/{id}/status
- Docs: `Orders` tag, "Update order status".
- Class/method: `OrderEndpoint#updateStatus`.
- Request: path `id: UUID`; body.
- Request POJO: `com.acme.skillplayground.model.UpdateOrderStatusRequest`.
- Response: `200 OK`.
- Response POJO: `com.acme.skillplayground.model.OrderResponse`.

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Path | `id` | UUID path conversion |
| Body | `status` | `@NotNull`; `OrderStatus` enum: `CREATED`, `ACCEPTED`, `FULFILLED`, `CANCELLED` |
| Header | none | No `@RequestHeader` declared |

- Errors/tests: `OrderEndpointTest#updateStatusReturnsUpdatedOrder`.

### GET /api/retail/customers/{customerId}/profile
- Docs: `Retail operations` tag, "Get a customer profile".
- Class/method: `RetailOperationsEndpoint#getCustomerProfile`.
- Request: path `customerId: String`.
- Request POJO: none.
- Response: `200 OK`.
- Response POJO: `com.acme.skillplayground.model.customer.CustomerProfileResponse`.

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Path | `customerId` | `String`; no Bean Validation annotation |
| Header | none | No `@RequestHeader` declared |

- Errors/tests: `RetailOperationsEndpointTest#routesCustomerCatalogPromotionAndAuditReads`.

### GET /api/retail/catalog/items/{sku}
- Docs: `Retail operations` tag, "Get a catalog item".
- Class/method: `RetailOperationsEndpoint#getCatalogItem`.
- Request: path `sku: String`.
- Request POJO: none.
- Response: `200 OK`.
- Response POJO: `com.acme.skillplayground.model.catalog.CatalogItemResponse`.

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Path | `sku` | `String`; no Bean Validation annotation |
| Header | none | No `@RequestHeader` declared |

- Errors/tests: `RetailOperationsEndpointTest#routesCustomerCatalogPromotionAndAuditReads`.

### POST /api/retail/inventory/reservations
- Docs: `Retail operations` tag, "Reserve inventory".
- Class/method: `RetailOperationsEndpoint#reserveInventory`.
- Request: body.
- Request POJO: `com.acme.skillplayground.model.inventory.InventoryReservationRequest`.
- Response: `200 OK`.
- Response POJO: `com.acme.skillplayground.model.inventory.InventoryReservationResponse`.

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Body | `orderId` | Optional `UUID` |
| Body | `sku` | `@NotBlank` |
| Body | `quantity` | `@Positive` |
| Header | none | No `@RequestHeader` declared |

- Errors/tests: `RetailOperationsEndpointTest#routesWriteOperations`; `ResourceConflictException` maps to 409 in `mapsDomainErrorsToProblemDetails`.

### POST /api/retail/pricing/quotes
- Docs: `Retail operations` tag, "Create a price quote".
- Class/method: `RetailOperationsEndpoint#quotePrice`.
- Request: body.
- Request POJO: `com.acme.skillplayground.model.pricing.PriceQuoteRequest`.
- Response: `200 OK`.
- Response POJO: `com.acme.skillplayground.model.pricing.PriceQuoteResponse`.

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Body | `customerId` | `@NotBlank` |
| Body | `sku` | `@NotBlank` |
| Body | `quantity` | `@Positive` |
| Body | `couponCode` | Optional `String` |
| Header | none | No `@RequestHeader` declared |

- Errors/tests: `RetailOperationsEndpointTest#routesWriteOperations`.

### GET /api/retail/promotions/{couponCode}/eligibility
- Docs: `Retail operations` tag, "Evaluate promotion eligibility".
- Class/method: `RetailOperationsEndpoint#evaluatePromotion`.
- Request: path `couponCode: String`; required query params `customerId`, `sku`.
- Request POJO: none.
- Response: `200 OK`.
- Response POJO: `com.acme.skillplayground.model.promotion.PromotionDecisionResponse`.

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Path | `couponCode` | `String`; no Bean Validation annotation |
| Query | `customerId` | Required by default; no Bean Validation annotation |
| Query | `sku` | Required by default; no Bean Validation annotation |
| Header | none | No `@RequestHeader` declared |

- Errors/tests: `RetailOperationsEndpointTest#routesCustomerCatalogPromotionAndAuditReads`.

### POST /api/retail/payments/authorizations
- Docs: `Retail operations` tag, "Authorize a payment".
- Class/method: `RetailOperationsEndpoint#authorizePayment`.
- Request: body.
- Request POJO: `com.acme.skillplayground.model.payment.PaymentAuthorizationRequest`.
- Response: `200 OK`.
- Response POJO: `com.acme.skillplayground.model.payment.PaymentAuthorizationResponse`.

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Body | `orderId` | Optional `UUID` |
| Body | `amount` | `@DecimalMin("0.01")` |
| Body | `currency` | `@NotBlank` |
| Body | `paymentToken` | `@NotBlank` |
| Header | none | No `@RequestHeader` declared |

- Errors/tests: `RetailOperationsEndpointTest#routesWriteOperations`; `DomainRuleViolationException` maps to 422 in `mapsDomainErrorsToProblemDetails`.

### POST /api/retail/fulfillment/plans
- Docs: `Retail operations` tag, "Plan a shipment".
- Class/method: `RetailOperationsEndpoint#planShipment`.
- Request: body.
- Request POJO: `com.acme.skillplayground.model.fulfillment.ShipmentPlanRequest`.
- Response: `200 OK`.
- Response POJO: `com.acme.skillplayground.model.fulfillment.ShipmentPlanResponse`.

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Body | `orderId` | Optional `UUID` |
| Body | `postalCode` | `@NotBlank` |
| Body | `sku` | `@NotBlank` |
| Body | `quantity` | `@Positive` |
| Header | none | No `@RequestHeader` declared |

- Errors/tests: `RetailOperationsEndpointTest#routesWriteOperations`.

### POST /api/retail/returns/authorizations
- Docs: `Retail operations` tag, "Authorize a return".
- Class/method: `RetailOperationsEndpoint#authorizeReturn`.
- Request: body.
- Request POJO: `com.acme.skillplayground.model.returns.ReturnAuthorizationRequest`.
- Response: `200 OK`.
- Response POJO: `com.acme.skillplayground.model.returns.ReturnAuthorizationResponse`.

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Body | `orderId` | Optional `UUID` |
| Body | `sku` | `@NotBlank` |
| Body | `quantity` | `@Positive` |
| Body | `reasonCode` | `@NotBlank` |
| Header | none | No `@RequestHeader` declared |

- Errors/tests: `RetailOperationsEndpointTest#routesWriteOperations`.

### POST /api/retail/support/tickets
- Docs: `Retail operations` tag, "Create a support ticket".
- Class/method: `RetailOperationsEndpoint#createTicket`.
- Request: body.
- Request POJO: `com.acme.skillplayground.model.support.CreateTicketRequest`.
- Response: `200 OK`.
- Response POJO: `com.acme.skillplayground.model.support.TicketResponse`.

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Body | `customerId` | `@NotBlank` |
| Body | `orderId` | `@NotBlank` |
| Body | `subject` | `@NotBlank` |
| Body | `message` | `@NotBlank` |
| Header | none | No `@RequestHeader` declared |

- Errors/tests: `RetailOperationsEndpointTest#routesWriteOperations`.

### GET /api/retail/audit/orders/{orderId}
- Docs: `Retail operations` tag, "Get order audit trail".
- Class/method: `RetailOperationsEndpoint#getOrderAuditTrail`.
- Request: path `orderId: UUID`.
- Request POJO: none.
- Response: `200 OK`.
- Response POJO: `com.acme.skillplayground.model.audit.AuditTrailResponse`.

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Path | `orderId` | UUID path conversion |
| Header | none | No `@RequestHeader` declared |

- Errors/tests: `RetailOperationsEndpointTest#routesCustomerCatalogPromotionAndAuditReads`.

## API Models
- `CreateOrderRequest`: `customerId`, `sku`, `quantity`, optional `shippingPriority`, optional `requestedShipDate`. Default priority is `STANDARD`.
- `UpdateOrderStatusRequest`: `status` using `OrderStatus` values `CREATED`, `ACCEPTED`, `FULFILLED`, `CANCELLED`.
- `OrderResponse`: `id`, `customerId`, `sku`, `quantity`, `shippingPriority`, `requestedShipDate`, `manualReviewRequired`, `status`, `createdAt`, `updatedAt`.
- `InventoryReservationRequest` / `InventoryReservationResponse`: reserve SKU quantity for an optional order and return reservation status.
- `PriceQuoteRequest` / `PriceQuoteResponse`: quote customer/SKU quantity with optional coupon and return subtotal, discount, tax, total, currency, price rule.
- `PaymentAuthorizationRequest` / `PaymentAuthorizationResponse`: authorize an amount/currency/payment token for an optional order.
- `ShipmentPlanRequest` / `ShipmentPlanResponse`: plan fulfillment for an optional order/SKU/postal code/quantity.
- `ReturnAuthorizationRequest` / `ReturnAuthorizationResponse`: authorize return quantity and reason for an optional order/SKU.
- `CreateTicketRequest` / `TicketResponse`: create a support ticket for customer/order details.
- Read-only responses: `CustomerProfileResponse`, `CatalogItemResponse`, `PromotionDecisionResponse`, `AuditTrailResponse`.

## Test Coverage
- `OrderEndpointTest`: create, 201 `Location`, not-found mapping, list by customer, update status, 422 domain rule mapping.
- `RetailOperationsEndpointTest`: retail read routes, retail write routes, 409 resource conflict mapping, 422 domain rule mapping.
- Add endpoint tests for new request/header validations before changing service behavior.
