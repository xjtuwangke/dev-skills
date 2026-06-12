# Backend Surfaces

## Endpoints

| Method | Path | Handler | Service | Notes |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/orders` | `OrderEndpoint#listOrders` | `OrderService#listOrders` | list all orders |
| POST | `/api/v1/orders` | `OrderEndpoint#createOrder` | `OrderService#createOrder` | creates draft order |
| GET | `/api/v1/orders/{orderId}` | `OrderEndpoint#getOrder` | `OrderService#getOrder` | Redis read-through cache |
| PATCH | `/api/v1/orders/{orderId}/status` | `OrderEndpoint#updateStatus` | `OrderService#updateStatus` | invalidates order cache |
| POST | `/api/v1/orders/{orderId}/submit` | `OrderEndpoint#submitOrder` | `OrderService#submitOrder` | publishes order-created event |
| POST | `/api/v1/orders/{orderId}/cancel` | `OrderEndpoint#cancelOrder` | `OrderService#cancelOrder` | publishes order-cancelled event |
| GET | `/api/v1/customers/{customerId}` | `CustomerEndpoint#getCustomer` | `CustomerService#getCustomer` | customer lookup |
| GET | `/api/v1/customers/{customerId}/orders` | `CustomerEndpoint#listCustomerOrders` | `OrderService#listCustomerOrders` | customer order history |
| POST | `/api/v1/inventory/reservations` | `InventoryEndpoint#reserve` | `InventoryService#reserve` | calls inventory downstream |
| GET | `/api/v1/inventory/reservations/{reservationId}` | `InventoryEndpoint#getReservation` | `InventoryService#getReservation` | reservation lookup |
| POST | `/api/v1/inventory/reservations/{reservationId}/release` | `InventoryEndpoint#release` | `InventoryService#releaseReservation` | calls inventory downstream |
| POST | `/api/v1/payments/authorize` | `PaymentEndpoint#authorize` | `PaymentService#authorize` | calls payment downstream and publishes event |
| GET | `/api/v1/payments/{paymentId}` | `PaymentEndpoint#getPayment` | `PaymentService#getPayment` | payment lookup |
| POST | `/api/v1/payments/{paymentId}/capture` | `PaymentEndpoint#capture` | `PaymentService#capture` | calls payment downstream |
| POST | `/api/v1/fulfillment/plans` | `FulfillmentEndpoint#createPlan` | `FulfillmentService#createPlan` | creates plan |
| GET | `/api/v1/fulfillment/plans/{planId}` | `FulfillmentEndpoint#getPlan` | `FulfillmentService#getPlan` | plan lookup |
| POST | `/api/v1/shipments` | `ShipmentEndpoint#createShipment` | `ShipmentService#createShipment` | calls shipping downstream |
| GET | `/api/v1/shipments/{shipmentId}` | `ShipmentEndpoint#getShipment` | `ShipmentService#getShipment` | cached/downstream lookup |
| POST | `/api/v1/returns` | `ReturnEndpoint#createReturn` | `ReturnService#createReturn` | creates return request |
| GET | `/api/v1/returns/{returnId}` | `ReturnEndpoint#getReturn` | `ReturnService#getReturn` | return lookup |
| POST | `/api/v1/operations/reconciliation/jobs` | `OperationsEndpoint#start` | `ReconciliationService#start` | queues reconciliation |
| GET | `/api/v1/operations/reconciliation/jobs/{jobId}` | `OperationsEndpoint#get` | `ReconciliationService#get` | job status |
| GET | `/api/v1/events/orders/{orderId}` | `EventEndpoint#listOrderEvents` | `EventQueryService#listOrderEvents` | event stream lookup |

## Persistence

| Repository | Storage | Row/entity | Used by |
| --- | --- | --- | --- |
| `OrderRepository` | PostgreSQL/R2DBC table `orders` | `OrderRow` | `OrderService` |
| `CustomerRepository` | PostgreSQL/R2DBC table `customers` | `CustomerRow` | `CustomerService` |
| `InventoryReservationRepository` | PostgreSQL/R2DBC table `inventory_reservations` | `InventoryReservationRow` | `InventoryService` |
| `PaymentRepository` | PostgreSQL/R2DBC table `payments` | `PaymentRow` | `PaymentService` |

Migration source: `src/main/resources/db/migration/V1__commerce_schema.sql`.

## Redis

| Template | Key | Value | Used by |
| --- | --- | --- | --- |
| `ReactiveRedisTemplate<String, OrderView>` | `orders:{orderId}` | `OrderView` | `OrderService#getOrder`, `OrderService#updateStatus` |

## Outbound Clients

| Client | Bean | Base URL key | Calls | Used by |
| --- | --- | --- | --- | --- |
| `InventoryClient` | `inventoryWebClient` | `commerce.clients.inventory.base-url` | reserve, release | `InventoryService` |
| `PaymentGatewayClient` | `paymentWebClient` | `commerce.clients.payment.base-url` | authorize, capture | `PaymentService` |
| `ShippingClient` | `shippingWebClient` | `commerce.clients.shipping.base-url` | create/get shipment | `ShipmentService` |

## Pub/Sub

| Direction | Topic/subscription config | Handler | Payload | Notes |
| --- | --- | --- | --- | --- |
| publish | `commerce.pubsub.order-created-topic` | `CommerceEventPublisher#publishOrderCreated` | `OrderCreatedEvent` | after order submitted |
| publish | `commerce.pubsub.order-cancelled-topic` | `CommerceEventPublisher#publishOrderCancelled` | `OrderCancelledEvent` | after order cancelled |
| publish | `commerce.pubsub.payment-authorized-topic` | `CommerceEventPublisher#publishPaymentAuthorized` | `PaymentAuthorizedEvent` | after payment saved |
| consume | `commerce.pubsub.inventory-reserved-subscription` | `CommerceEventSubscriber#handleInventoryReserved` | `InventoryReservedEvent` | writes reservation and acks |
| consume | `commerce.pubsub.shipment-updated-subscription` | `CommerceEventSubscriber#handleShipmentUpdated` | `ShipmentUpdatedEvent` | updates shipment cache and acks |

## API Docs

- Static contract: `src/main/resources/openapi.yaml`.
- Springfox runtime config: `config/SpringfoxConfig.java`.
- Expected docs endpoint when app runs: Swagger UI from Springfox.

