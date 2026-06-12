# Support And Audit Reference

## Support
- Tickets belong to a customer and can optionally reference an order.
- Payment or chargeback language raises priority to high.
- Other tickets default to normal priority.

## Audit
- Audit trail fixture returns order lifecycle events.
- Treat audit payload shape as consumer-sensitive when adding real persistence.

## Tables
- `support_tickets`
- `ticket_messages`
- `audit_logs`
- `outbox_events`
- `feature_flags`

## Code
- `SupportTicketService`
- `AuditTrailService`
