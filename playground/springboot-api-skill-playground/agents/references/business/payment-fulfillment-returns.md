# Payment, Fulfillment, And Returns Reference

## Payment
- Only USD is supported in the fixture.
- Payments over 5000.00 require manual review instead of authorization.
- Unsupported currency maps to a 422 domain-rule response.

## Fulfillment
- Postal code controls warehouse selection.
- Hazardous SKUs can ship only from western-region postal codes.
- Large quantities use freight service level.

## Returns
- Fraud reason codes are denied and sent to review.
- Hazardous SKUs use special handling disposition.
- Standard returns are approved for restock.

## Tables
- `payment_methods`, `payments`, `payment_attempts`
- `shipments`, `shipment_items`
- `return_requests`, `return_items`

## Code
- `PaymentAuthorizationService`
- `FulfillmentPlanningService`
- `FulfillmentMapper`
- `ReturnPolicyService`
