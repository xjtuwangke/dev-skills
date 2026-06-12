# Call Chains

These chains are static reading guides. Confirm exact branches, transactions, reactive scheduling, and error behavior in code.

## Order Write Paths

```text
POST /api/orders
OrderEndpoint#create -> OrderService#create -> OrderRepository#save -> OrderEventPublisher#publishCreated
```

```text
PATCH /api/orders/{id}/status
OrderEndpoint#updateStatus -> OrderService#updateStatus -> OrderRepository#findById/save -> OrderEventPublisher#publishStatusChanged
```

Risks to inspect:
- Blocking JPA work is wrapped with `Schedulers.boundedElastic()`.
- Pub/Sub publication happens after mapping the saved entity.
- Status transition validation is intentionally light in this fixture and is a likely future improvement.

## Order Read Paths

```text
GET /api/orders/{id}
OrderEndpoint#getById -> OrderService#findById -> OrderRepository#findById
```

```text
GET /api/orders/customers/{customerId}
OrderEndpoint#listByCustomer -> OrderService#findByCustomerId -> OrderRepository#findByCustomerId
```

`OrderNotFoundException` maps to 404 through `ApiExceptionHandler`.

## Retail Operations Paths

| Endpoint | Chain | Key branches |
| --- | --- | --- |
| `GET /api/retail/customers/{customerId}/profile` | `RetailOperationsEndpoint#getCustomerProfile -> CustomerProfileService -> CustomerProfileMapper` | `ent-*` customers map to enterprise segment. |
| `GET /api/retail/catalog/items/{sku}` | `RetailOperationsEndpoint#getCatalogItem -> CatalogQueryService -> CatalogMapper` | `OLD*` discontinued, `HZ*` hazardous, blank SKU errors. |
| `POST /api/retail/inventory/reservations` | `RetailOperationsEndpoint#reserveInventory -> InventoryReservationService` | `LOW*` SKU with quantity > 1 throws `ResourceConflictException` and returns 409. |
| `POST /api/retail/pricing/quotes` | `RetailOperationsEndpoint#quotePrice -> PricingService -> CatalogMapper + MoneyMapper` | Applies max of loyalty vs coupon discount, then tax. |
| `GET /api/retail/promotions/{couponCode}/eligibility` | `RetailOperationsEndpoint#evaluatePromotion -> PromotionService` | `SAVE20` eligible except old SKUs; enterprise fallback. |
| `POST /api/retail/payments/authorizations` | `RetailOperationsEndpoint#authorizePayment -> PaymentAuthorizationService` | Non-USD throws 422; amount > 5000 returns manual-review denial. |
| `POST /api/retail/fulfillment/plans` | `RetailOperationsEndpoint#planShipment -> FulfillmentPlanningService -> FulfillmentMapper` | Hazardous SKUs can ship only from western postal codes. |
| `POST /api/retail/returns/authorizations` | `RetailOperationsEndpoint#authorizeReturn -> ReturnPolicyService` | Fraud reason denies; hazardous SKU gets special handling. |
| `POST /api/retail/support/tickets` | `RetailOperationsEndpoint#createTicket -> SupportTicketService` | Payment or chargeback text raises priority. |
| `GET /api/retail/audit/orders/{orderId}` | `RetailOperationsEndpoint#getOrderAuditTrail -> AuditTrailService` | Fixture returns order lifecycle events. |

## Persistence Map

```text
Flyway
V1__create_orders.sql -> orders
V2__retail_platform_schema.sql -> 36 retail platform tables
V3__add_order_shipping_priority.sql -> orders shipping priority/manual review fields
```

Important table clusters:
- Customer: accounts, addresses, contact preferences, loyalty.
- Catalog/supplier: categories, products, variants, suppliers, supplier contracts.
- Inventory: locations, stock, reservations, transfers.
- Pricing/promotion/tax: price lists, tax rates, campaigns, coupons, redemptions.
- Order/payment/fulfillment/returns: sales orders, order lines, payments, shipments, returns.
- Support/audit/outbox/ops: tickets, messages, audit logs, outbox events, feature flags.

## Pub/Sub Publication

```text
OrderService -> OrderEventPublisher
GcpPubSubOrderEventPublisher -> PubSubGateway
GcpPubSubGateway -> PubSubTemplate
```

Topic/config evidence:
- `orders.created.*`
- `orders.status-changed.*`

## Verification Map
- Endpoint changes: `mvn -Dtest=OrderEndpointTest,RetailOperationsEndpointTest test`
- Service logic changes: `mvn -Dtest=OrderServiceTest,RetailDomainServicesTest test`
- Pub/Sub changes: `mvn -Dtest=GcpPubSubOrderEventPublisherTest,NoopOrderEventPublisherTest test`
- Broad check: `mvn clean verify`
