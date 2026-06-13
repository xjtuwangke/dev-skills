# Customer Domain Reference

## Concepts
- Customers have external IDs, segments, default currency, addresses, contact preferences, and loyalty state.
- Enterprise customers use IDs starting with `ent-` in the fixture logic.
- Loyalty points influence profile display and are a likely future pricing input.

## Tables
- `customer_accounts`
- `customer_addresses`
- `customer_contact_preferences`
- `loyalty_accounts`

## Code
- `CustomerProfileService`
- `CustomerProfileMapper`
- `CustomerProfileResponse`
