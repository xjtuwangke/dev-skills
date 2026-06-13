# Order Domain Reference

## Concepts
- An order belongs to a customer.
- An order has a SKU, quantity, shipping priority, status, and timestamps.
- Order identifiers are UUIDs.
- Shipping priority is `STANDARD` by default and can be `EXPEDITED`.
- `requestedShipDate` is optional and is echoed when supplied.
- `manualReviewRequired` marks accepted orders that need human review before downstream fulfillment.

## Statuses
- `CREATED`: newly accepted by order intake.
- `ACCEPTED`: accepted by a downstream business process.
- `FULFILLED`: completed by fulfillment.
- `CANCELLED`: stopped before completion.

## Behavioral Notes
- Creation should persist an order and publish a created event.
- Expedited shipping is rejected for SKUs that start with `HAZ-`.
- Orders with quantity greater than 10 are accepted but require manual review.
- Status changes should persist the new status and publish a status-changed event.
- Reads should not publish events.

Confirm production business rules with product/domain owners before changing lifecycle semantics.
