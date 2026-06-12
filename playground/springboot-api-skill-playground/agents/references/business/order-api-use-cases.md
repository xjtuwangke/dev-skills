# Order API Use Cases

## Create Order
- Client sends customer, SKU, quantity, and optional shipping fields to `POST /api/orders`.
- API validates the request, creates a `CREATED` order, and returns the created resource.
- `shippingPriority` defaults to `STANDARD` when omitted.
- `EXPEDITED` orders for `HAZ-` SKUs should return the project 422 problem-detail contract.
- Quantity greater than 10 should still create the order with `manualReviewRequired=true`.
- A created event is expected after successful persistence.

## Get Order
- Client fetches one order by ID with `GET /api/orders/{id}`.
- Missing orders should map to the project error contract.

## List Customer Orders
- Client fetches a customer's orders with `GET /api/orders/customers/{customerId}`.
- Response ordering should be confirmed before promising it to consumers.

## Update Status
- Client changes an order status with `PATCH /api/orders/{id}/status`.
- A status-changed event is expected after successful persistence.
