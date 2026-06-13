# Order Events Reference

## Event Types
- Order created.
- Order status changed.

## Business Meaning
- Created events tell downstream consumers that a new order exists.
- Status-changed events tell consumers that fulfillment or customer-visible state may need to update.

## Consumer-Sensitive Fields
- Order ID.
- Customer ID.
- Shipping priority.
- Manual review flag.
- Event timestamp.

## Change Guidance
- Treat event payload shape and topic names as cross-service contracts.
- Coordinate business and consumer impact before renaming fields, removing values, or changing publish timing.
