# Call Chains

Use these chains before changing behavior. Confidence is based on static source inspection and configuration evidence.

## POST /api/v1/orders

Confidence: `static`

```mermaid
sequenceDiagram
  participant API as OrderEndpoint#createOrder
  participant SVC as OrderService#createOrder
  participant DB as OrderRepository#save
  API->>SVC: CreateOrderRequest
  SVC->>SVC: calculate line totals
  SVC->>DB: save DRAFT order
```

Evidence:

- `endpoint/OrderEndpoint.java`
- `service/OrderService.java`
- `database/OrderRepository.java`

## POST /api/v1/orders/{orderId}/submit

Confidence: `static + config`

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

Change checklist:

- Update order status tests.
- Verify `order-created-topic` config in all envs.
- Keep `OrderCreatedEvent` backwards compatible or document consumer migration.

## POST /api/v1/payments/authorize

Confidence: `static + config`

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

Change checklist:

- Check `commerce.clients.payment.base-url` and timeout behavior.
- Update downstream error mapping tests before changing retry/capture semantics.
- Update payment event payload docs before adding fields.

## POST /api/v1/inventory/reservations

Confidence: `static + config`

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

Confidence: `static + pubsub`

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

Confidence: `static + pubsub`

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

Confidence: `static + config`

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

Confidence: `static`

```mermaid
sequenceDiagram
  participant API as ReturnEndpoint#createReturn
  participant SVC as ReturnService#createReturn
  API->>SVC: CreateReturnRequest
  SVC->>SVC: create REQUESTED return view
```

## POST /api/v1/operations/reconciliation/jobs

Confidence: `static`

```mermaid
sequenceDiagram
  participant API as OperationsEndpoint#start
  participant SVC as ReconciliationService#start
  API->>SVC: ReconciliationRequest
  SVC->>SVC: create QUEUED reconciliation job
```

