# 后端表面

## Endpoints

| Method | Path | Handler | Service | 说明 |
| --- | --- | --- | --- | --- |
| GET | `/api/v1/orders` | `OrderEndpoint#listOrders` | `OrderService#listOrders` | 列出全部订单 |
| POST | `/api/v1/orders` | `OrderEndpoint#createOrder` | `OrderService#createOrder` | 创建草稿订单 |
| GET | `/api/v1/orders/{orderId}` | `OrderEndpoint#getOrder` | `OrderService#getOrder` | Redis read-through cache |
| PATCH | `/api/v1/orders/{orderId}/status` | `OrderEndpoint#updateStatus` | `OrderService#updateStatus` | 更新状态并失效订单缓存 |
| POST | `/api/v1/orders/{orderId}/submit` | `OrderEndpoint#submitOrder` | `OrderService#submitOrder` | 提交订单并发布 order-created event |
| POST | `/api/v1/orders/{orderId}/cancel` | `OrderEndpoint#cancelOrder` | `OrderService#cancelOrder` | 取消订单并发布 order-cancelled event |
| GET | `/api/v1/customers/{customerId}` | `CustomerEndpoint#getCustomer` | `CustomerService#getCustomer` | 查询客户 |
| GET | `/api/v1/customers/{customerId}/orders` | `CustomerEndpoint#listCustomerOrders` | `OrderService#listCustomerOrders` | 查询客户订单历史 |
| POST | `/api/v1/inventory/reservations` | `InventoryEndpoint#reserve` | `InventoryService#reserve` | 调用库存下游并保存 reservation |
| GET | `/api/v1/inventory/reservations/{reservationId}` | `InventoryEndpoint#getReservation` | `InventoryService#getReservation` | 查询库存 reservation |
| POST | `/api/v1/inventory/reservations/{reservationId}/release` | `InventoryEndpoint#release` | `InventoryService#releaseReservation` | 调用库存下游释放 reservation |
| POST | `/api/v1/payments/authorize` | `PaymentEndpoint#authorize` | `PaymentService#authorize` | 调用支付下游、保存 payment、发布事件 |
| GET | `/api/v1/payments/{paymentId}` | `PaymentEndpoint#getPayment` | `PaymentService#getPayment` | 查询 payment |
| POST | `/api/v1/payments/{paymentId}/capture` | `PaymentEndpoint#capture` | `PaymentService#capture` | 调用支付下游 capture |
| POST | `/api/v1/fulfillment/plans` | `FulfillmentEndpoint#createPlan` | `FulfillmentService#createPlan` | 创建履约计划 |
| GET | `/api/v1/fulfillment/plans/{planId}` | `FulfillmentEndpoint#getPlan` | `FulfillmentService#getPlan` | 查询履约计划 |
| POST | `/api/v1/shipments` | `ShipmentEndpoint#createShipment` | `ShipmentService#createShipment` | 调用物流下游创建 shipment |
| GET | `/api/v1/shipments/{shipmentId}` | `ShipmentEndpoint#getShipment` | `ShipmentService#getShipment` | 从缓存或下游查询 shipment |
| POST | `/api/v1/returns` | `ReturnEndpoint#createReturn` | `ReturnService#createReturn` | 创建退货请求 |
| GET | `/api/v1/returns/{returnId}` | `ReturnEndpoint#getReturn` | `ReturnService#getReturn` | 查询退货请求 |
| POST | `/api/v1/operations/reconciliation/jobs` | `OperationsEndpoint#start` | `ReconciliationService#start` | 创建对账 job |
| GET | `/api/v1/operations/reconciliation/jobs/{jobId}` | `OperationsEndpoint#get` | `ReconciliationService#get` | 查询对账 job 状态 |
| GET | `/api/v1/events/orders/{orderId}` | `EventEndpoint#listOrderEvents` | `EventQueryService#listOrderEvents` | 查询订单事件流 |

## Persistence

| Repository | Storage | Row/entity | Used by |
| --- | --- | --- | --- |
| `OrderRepository` | PostgreSQL/R2DBC table `orders` | `OrderRow` | `OrderService` |
| `CustomerRepository` | PostgreSQL/R2DBC table `customers` | `CustomerRow` | `CustomerService` |
| `InventoryReservationRepository` | PostgreSQL/R2DBC table `inventory_reservations` | `InventoryReservationRow` | `InventoryService` |
| `PaymentRepository` | PostgreSQL/R2DBC table `payments` | `PaymentRow` | `PaymentService` |

Migration 来源：`src/main/resources/db/migration/V1__commerce_schema.sql`。

## Redis

| Template | Key | Value | Used by |
| --- | --- | --- | --- |
| `ReactiveRedisTemplate<String, OrderView>` | `orders:{orderId}` | `OrderView` | `OrderService#getOrder`, `OrderService#updateStatus` |

## 出站 Clients

| Client | Bean | Base URL key | 调用 | Used by |
| --- | --- | --- | --- | --- |
| `InventoryClient` | `inventoryWebClient` | `commerce.clients.inventory.base-url` | reserve, release | `InventoryService` |
| `PaymentGatewayClient` | `paymentWebClient` | `commerce.clients.payment.base-url` | authorize, capture | `PaymentService` |
| `ShippingClient` | `shippingWebClient` | `commerce.clients.shipping.base-url` | create/get shipment | `ShipmentService` |

## Pub/Sub

| 方向 | Topic/subscription config | Handler | Payload | 说明 |
| --- | --- | --- | --- | --- |
| publish | `commerce.pubsub.order-created-topic` | `CommerceEventPublisher#publishOrderCreated` | `OrderCreatedEvent` | 订单提交后发布 |
| publish | `commerce.pubsub.order-cancelled-topic` | `CommerceEventPublisher#publishOrderCancelled` | `OrderCancelledEvent` | 订单取消后发布 |
| publish | `commerce.pubsub.payment-authorized-topic` | `CommerceEventPublisher#publishPaymentAuthorized` | `PaymentAuthorizedEvent` | payment 保存后发布 |
| consume | `commerce.pubsub.inventory-reserved-subscription` | `CommerceEventSubscriber#handleInventoryReserved` | `InventoryReservedEvent` | 写入 reservation 后 ack |
| consume | `commerce.pubsub.shipment-updated-subscription` | `CommerceEventSubscriber#handleShipmentUpdated` | `ShipmentUpdatedEvent` | 更新 shipment cache 后 ack |

## API Docs

- 静态 contract：`src/main/resources/openapi.yaml`。
- Springfox runtime config：`config/SpringfoxConfig.java`。
- 应用运行时预期 docs endpoint：Springfox Swagger UI。

