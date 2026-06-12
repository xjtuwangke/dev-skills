# Backend Surfaces

Use this before changing endpoints, persistence, service behavior, Pub/Sub publication, or profile-specific config. This file is a navigation aid; confirm exact behavior in source code before editing.

## Domain Map
| Domain | Endpoint/service entry points | Main reference |
| --- | --- | --- |
| Customer | `RetailOperationsEndpoint#getCustomerProfile`, `CustomerProfileService` | `agents/references/business/customer-domain.md` |
| Catalog | `RetailOperationsEndpoint#getCatalogItem`, `CatalogQueryService` | `agents/references/technical/endpoints.md` |
| Inventory | `RetailOperationsEndpoint#reserveInventory`, `InventoryReservationService` | `agents/references/technical/persistence.md` |
| Pricing | `RetailOperationsEndpoint#quotePrice`, `PricingService`, `MoneyMapper` | `agents/references/business/pricing-promotions.md` |
| Promotion | `RetailOperationsEndpoint#evaluatePromotion`, `PromotionService` | `agents/references/business/pricing-promotions.md` |
| Order | `OrderEndpoint`, `OrderService` | `agents/references/business/order-domain.md` |
| Payment | `RetailOperationsEndpoint#authorizePayment`, `PaymentAuthorizationService` | `agents/references/business/payment-fulfillment-returns.md` |
| Fulfillment | `RetailOperationsEndpoint#planShipment`, `FulfillmentPlanningService`, `FulfillmentMapper` | `agents/references/business/payment-fulfillment-returns.md` |
| Returns | `RetailOperationsEndpoint#authorizeReturn`, `ReturnPolicyService` | `agents/references/business/payment-fulfillment-returns.md` |
| Support | `RetailOperationsEndpoint#createTicket`, `SupportTicketService` | `agents/references/business/support-audit.md` |
| Audit | `RetailOperationsEndpoint#getOrderAuditTrail`, `AuditTrailService` | `agents/references/business/support-audit.md` |

## Endpoints
| Method | Path | Handler | Request | Response | Source |
| --- | --- | --- | --- | --- | --- |
| POST | `/api/orders` | `OrderEndpoint#create` | `CreateOrderRequest` | `Mono<ResponseEntity<OrderResponse>>` | `src/main/java/com/acme/skillplayground/endpoint/OrderEndpoint.java` |
| GET | `/api/orders/{id}` | `OrderEndpoint#getById` | None | `Mono<OrderResponse>` | `src/main/java/com/acme/skillplayground/endpoint/OrderEndpoint.java` |
| GET | `/api/orders/customers/{customerId}` | `OrderEndpoint#listByCustomer` | None | `Mono<List<OrderResponse>>` | `src/main/java/com/acme/skillplayground/endpoint/OrderEndpoint.java` |
| PATCH | `/api/orders/{id}/status` | `OrderEndpoint#updateStatus` | `UpdateOrderStatusRequest` | `Mono<OrderResponse>` | `src/main/java/com/acme/skillplayground/endpoint/OrderEndpoint.java` |
| GET | `/api/retail/customers/{customerId}/profile` | `RetailOperationsEndpoint#getCustomerProfile` | None | `Mono<CustomerProfileResponse>` | `src/main/java/com/acme/skillplayground/endpoint/RetailOperationsEndpoint.java` |
| GET | `/api/retail/catalog/items/{sku}` | `RetailOperationsEndpoint#getCatalogItem` | None | `Mono<CatalogItemResponse>` | `src/main/java/com/acme/skillplayground/endpoint/RetailOperationsEndpoint.java` |
| POST | `/api/retail/inventory/reservations` | `RetailOperationsEndpoint#reserveInventory` | `InventoryReservationRequest` | `Mono<InventoryReservationResponse>` | `src/main/java/com/acme/skillplayground/endpoint/RetailOperationsEndpoint.java` |
| POST | `/api/retail/pricing/quotes` | `RetailOperationsEndpoint#quotePrice` | `PriceQuoteRequest` | `Mono<PriceQuoteResponse>` | `src/main/java/com/acme/skillplayground/endpoint/RetailOperationsEndpoint.java` |
| GET | `/api/retail/promotions/{couponCode}/eligibility` | `RetailOperationsEndpoint#evaluatePromotion` | Query params | `Mono<PromotionDecisionResponse>` | `src/main/java/com/acme/skillplayground/endpoint/RetailOperationsEndpoint.java` |
| POST | `/api/retail/payments/authorizations` | `RetailOperationsEndpoint#authorizePayment` | `PaymentAuthorizationRequest` | `Mono<PaymentAuthorizationResponse>` | `src/main/java/com/acme/skillplayground/endpoint/RetailOperationsEndpoint.java` |
| POST | `/api/retail/fulfillment/plans` | `RetailOperationsEndpoint#planShipment` | `ShipmentPlanRequest` | `Mono<ShipmentPlanResponse>` | `src/main/java/com/acme/skillplayground/endpoint/RetailOperationsEndpoint.java` |
| POST | `/api/retail/returns/authorizations` | `RetailOperationsEndpoint#authorizeReturn` | `ReturnAuthorizationRequest` | `Mono<ReturnAuthorizationResponse>` | `src/main/java/com/acme/skillplayground/endpoint/RetailOperationsEndpoint.java` |
| POST | `/api/retail/support/tickets` | `RetailOperationsEndpoint#createTicket` | `CreateTicketRequest` | `Mono<TicketResponse>` | `src/main/java/com/acme/skillplayground/endpoint/RetailOperationsEndpoint.java` |
| GET | `/api/retail/audit/orders/{orderId}` | `RetailOperationsEndpoint#getOrderAuditTrail` | None | `Mono<AuditTrailResponse>` | `src/main/java/com/acme/skillplayground/endpoint/RetailOperationsEndpoint.java` |

## Services And Mappers
| Surface | Public behavior | Collaborators | Source |
| --- | --- | --- | --- |
| `OrderService` | create/read/list/update orders, shipping priority rules, manual review flagging | `OrderRepository`, `OrderEventPublisher` | `src/main/java/com/acme/skillplayground/service/OrderService.java` |
| `CustomerProfileService` | customer profile lookup | `CustomerProfileMapper` | `src/main/java/com/acme/skillplayground/service/CustomerProfileService.java` |
| `CatalogQueryService` | catalog item lookup | `CatalogMapper` | `src/main/java/com/acme/skillplayground/service/CatalogQueryService.java` |
| `InventoryReservationService` | stock reservation and conflict handling | none | `src/main/java/com/acme/skillplayground/service/InventoryReservationService.java` |
| `PricingService` | quote subtotal, discount, tax, total | `CatalogMapper`, `MoneyMapper` | `src/main/java/com/acme/skillplayground/service/PricingService.java` |
| `PromotionService` | coupon and enterprise eligibility | none | `src/main/java/com/acme/skillplayground/service/PromotionService.java` |
| `PaymentAuthorizationService` | currency validation and manual review | none | `src/main/java/com/acme/skillplayground/service/PaymentAuthorizationService.java` |
| `FulfillmentPlanningService` | shipment plan and hazmat rules | `FulfillmentMapper` | `src/main/java/com/acme/skillplayground/service/FulfillmentPlanningService.java` |
| `ReturnPolicyService` | return disposition decisions | none | `src/main/java/com/acme/skillplayground/service/ReturnPolicyService.java` |
| `SupportTicketService` | ticket priority and timestamping | `Clock` | `src/main/java/com/acme/skillplayground/service/SupportTicketService.java` |
| `AuditTrailService` | order audit trail fixture | `Clock` | `src/main/java/com/acme/skillplayground/service/AuditTrailService.java` |
| `MoneyMapper` | money rounding, discount, tax mapping | none | `src/main/java/com/acme/skillplayground/mapper/MoneyMapper.java` |
| `CustomerProfileMapper` | customer id to profile mapping | none | `src/main/java/com/acme/skillplayground/mapper/CustomerProfileMapper.java` |
| `CatalogMapper` | SKU to catalog item mapping | none | `src/main/java/com/acme/skillplayground/mapper/CatalogMapper.java` |
| `FulfillmentMapper` | postal code to warehouse/service dates | `Clock` | `src/main/java/com/acme/skillplayground/mapper/FulfillmentMapper.java` |

## Error Handling
| Exception | Status | Typical trigger | Source |
| --- | --- | --- | --- |
| `OrderNotFoundException` | 404 | missing order read/update | `src/main/java/com/acme/skillplayground/exception/ApiExceptionHandler.java` |
| `ResourceConflictException` | 409 | insufficient inventory | `src/main/java/com/acme/skillplayground/exception/ApiExceptionHandler.java` |
| `DomainRuleViolationException` | 422 | unsupported currency, hazmat shipping rule, expedited `HAZ-` order intake | `src/main/java/com/acme/skillplayground/exception/ApiExceptionHandler.java` |

## Persistence

### JPA Surface
| Repository | Entity | ID | Source |
| --- | --- | --- | --- |
| `OrderRepository` | `OrderEntity` | `UUID` | `src/main/java/com/acme/skillplayground/database/repository/OrderRepository.java` |

### Flyway Migrations
- `src/main/resources/db/migration/V1__create_orders.sql`
- `src/main/resources/db/migration/V2__retail_platform_schema.sql`
- `src/main/resources/db/migration/V3__add_order_shipping_priority.sql`

### Table Groups
- Order intake: `orders`
- Customer: `customer_accounts`, `customer_addresses`, `customer_contact_preferences`, `loyalty_accounts`
- Catalog/supplier: `product_categories`, `products`, `product_variants`, `suppliers`, `product_supplier_contracts`
- Inventory: `inventory_locations`, `inventory_stocks`, `inventory_reservations`, `warehouse_transfers`, `warehouse_transfer_lines`
- Pricing/promotion/tax: `price_lists`, `price_list_items`, `tax_rates`, `promotion_campaigns`, `coupons`, `coupon_redemptions`
- Sales order: `sales_orders`, `order_lines`, `order_status_history`, `idempotency_keys`
- Payment: `payment_methods`, `payments`, `payment_attempts`
- Fulfillment/returns: `shipments`, `shipment_items`, `return_requests`, `return_items`
- Support/audit/outbox/ops: `support_tickets`, `ticket_messages`, `audit_logs`, `outbox_events`, `feature_flags`

## Pub/Sub
| Class | Signals | Source |
| --- | --- | --- |
| `GcpPubSubGateway` | PubSubTemplate, publisher interface/gateway, conditional pubsub bean | `src/main/java/com/acme/skillplayground/pubsub/GcpPubSubGateway.java` |
| `GcpPubSubOrderEventPublisher` | publisher interface/gateway, conditional pubsub bean | `src/main/java/com/acme/skillplayground/pubsub/GcpPubSubOrderEventPublisher.java` |
| `NoopOrderEventPublisher` | publisher interface/gateway, conditional pubsub bean | `src/main/java/com/acme/skillplayground/pubsub/NoopOrderEventPublisher.java` |
| `OrderEvent` | event payload | `src/main/java/com/acme/skillplayground/pubsub/OrderEvent.java` |
| `OrderEventPublisher` | publisher interface | `src/main/java/com/acme/skillplayground/pubsub/OrderEventPublisher.java` |
| `PubSubGateway` | gateway interface | `src/main/java/com/acme/skillplayground/pubsub/PubSubGateway.java` |

### Topic Hints
- `orders.created.*`
- `orders.status-changed.*`

## Tests
- `src/test/java/com/acme/skillplayground/endpoint/OrderEndpointTest.java`: order endpoint WebTestClient coverage.
- `src/test/java/com/acme/skillplayground/endpoint/RetailOperationsEndpointTest.java`: retail operations endpoint and problem-detail coverage.
- `src/test/java/com/acme/skillplayground/service/OrderServiceTest.java`: order service and Pub/Sub interactions.
- `src/test/java/com/acme/skillplayground/service/RetailDomainServicesTest.java`: customer, catalog, inventory, pricing, promotion, payment, fulfillment, returns, support, audit logic.
- `src/test/java/com/acme/skillplayground/pubsub/GcpPubSubOrderEventPublisherTest.java`: GCP publisher behavior.
- `src/test/java/com/acme/skillplayground/pubsub/NoopOrderEventPublisherTest.java`: no-op publisher behavior.
