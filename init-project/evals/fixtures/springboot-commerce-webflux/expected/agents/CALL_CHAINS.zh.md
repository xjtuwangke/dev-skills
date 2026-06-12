# 调用链

修改行为前先看这些链路。置信度基于静态源码扫描和配置证据。

## POST /api/v1/orders

置信度：`static`

```mermaid
sequenceDiagram
  participant API as OrderEndpoint#createOrder
  participant SVC as OrderService#createOrder
  participant DB as OrderRepository#save
  API->>SVC: CreateOrderRequest
  SVC->>SVC: calculate line totals
  SVC->>DB: save DRAFT order
```

证据：

- `endpoint/OrderEndpoint.java`
- `service/OrderService.java`
- `database/OrderRepository.java`

## POST /api/v1/orders/{orderId}/submit

置信度：`static + config`

```mermaid
sequenceDiagram
  participant API as OrderEndpoint#submitOrder
  participant SVC as OrderService#submitOrder
  participant DB as OrderRepository#save
  participant CACHE as Redis orders:{orderId}
  participant MQ as orders.created topic
  API->>SVC: submit order
  SVC->>DB: update status SUBMITTED
  SVC->>CACHE: delete cached OrderView
  SVC->>MQ: publish OrderCreatedEvent
```

变更清单：

- 更新订单状态相关测试。
- 检查所有环境里的 `order-created-topic` 配置。
- 保持 `OrderCreatedEvent` 向后兼容；如果不兼容，记录 consumer migration。

## POST /api/v1/payments/authorize

置信度：`static + config`

```mermaid
sequenceDiagram
  participant API as PaymentEndpoint#authorize
  participant SVC as PaymentService#authorize
  participant PAY as PaymentGatewayClient#authorize
  participant DB as PaymentRepository#save
  participant MQ as payments.authorized topic
  API->>SVC: AuthorizePaymentRequest
  SVC->>PAY: POST /internal/payments/authorizations
  SVC->>DB: save AUTHORIZED payment
  SVC->>MQ: publish PaymentAuthorizedEvent
```

变更清单：

- 检查 `commerce.clients.payment.base-url` 和 timeout 行为。
- 修改 retry/capture 语义前，先更新下游 error mapping tests。
- 添加 event 字段前，先更新 payment event payload 文档。

## POST /api/v1/inventory/reservations

置信度：`static + config`

```mermaid
sequenceDiagram
  participant API as InventoryEndpoint#reserve
  participant SVC as InventoryService#reserve
  participant INV as InventoryClient#reserve
  participant DB as InventoryReservationRepository#save
  API->>SVC: ReserveInventoryRequest
  SVC->>INV: POST /internal/inventory/reservations
  SVC->>DB: save downstream reservation result
```

## inventoryReservedInputChannel

置信度：`static + pubsub`

```mermaid
sequenceDiagram
  participant MQ as inventory.reserved subscription
  participant SUB as CommerceEventSubscriber#handleInventoryReserved
  participant SVC as InventoryService#markReserved
  participant DB as InventoryReservationRepository#save
  MQ->>SUB: InventoryReservedEvent
  SUB->>SVC: markReserved(event)
  SVC->>DB: upsert RESERVED reservation
  SUB->>MQ: ack
```

## shipmentUpdatedInputChannel

置信度：`static + pubsub`

```mermaid
sequenceDiagram
  participant MQ as shipment.updated subscription
  participant SUB as CommerceEventSubscriber#handleShipmentUpdated
  participant SVC as ShipmentService#recordShipmentUpdate
  MQ->>SUB: ShipmentUpdatedEvent
  SUB->>SVC: update in-memory shipment view
  SUB->>MQ: ack
```

## POST /api/v1/shipments

置信度：`static + config`

```mermaid
sequenceDiagram
  participant API as ShipmentEndpoint#createShipment
  participant SVC as ShipmentService#createShipment
  participant SHIP as ShippingClient#createShipment
  API->>SVC: CreateShipmentRequest
  SVC->>SHIP: POST /internal/shipments
  SVC->>SVC: cache ShipmentView in memory
```

## POST /api/v1/returns

置信度：`static`

```mermaid
sequenceDiagram
  participant API as ReturnEndpoint#createReturn
  participant SVC as ReturnService#createReturn
  API->>SVC: CreateReturnRequest
  SVC->>SVC: create REQUESTED return view
```

## POST /api/v1/operations/reconciliation/jobs

置信度：`static`

```mermaid
sequenceDiagram
  participant API as OperationsEndpoint#start
  participant SVC as ReconciliationService#start
  API->>SVC: ReconciliationRequest
  SVC->>SVC: create QUEUED reconciliation job
```

