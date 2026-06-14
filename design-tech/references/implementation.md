# Implementation, Testing, And Rollout

Use this reference when the user needs a technical design that can become an
engineering plan.

## Implementation Plan

Break work into reviewable phases:

1. Data model or schema changes.
2. Internal interfaces and domain logic.
3. API, event, or integration changes.
4. Migration, backfill, or compatibility layer.
5. Observability and operational tooling.
6. Cleanup after rollout.

For each phase, note dependencies and validation.

## Migration And Compatibility

Include when data or interfaces change:

- Backwards-compatible schema changes.
- Versioned APIs or events.
- Dual-read, dual-write, or shadow mode if needed.
- Backfill plan.
- Cutover criteria.
- Cleanup plan.

## Testing Strategy

Select tests based on risk:

- Unit tests for pure domain logic.
- Integration tests for database, cache, queue, and external clients.
- Contract tests for APIs and events.
- Migration tests for schema and backfill.
- End-to-end tests for critical workflows.
- Load or soak tests for scale-sensitive changes.
- Failure-injection tests for retry, timeout, idempotency, and rollback paths.

## Rollout And Rollback

Cover:

- Feature flags or configuration gates.
- Progressive rollout stages.
- Pre-launch checks.
- Metrics to watch.
- Alert thresholds.
- Rollback command or procedure.
- Data repair steps if rollback is not enough.

## Output Shape

```markdown
## Implementation Plan
| Phase | Change | Validation |
| --- | --- | --- |

## Testing Strategy
| Risk | Test coverage |
| --- | --- |

## Rollout Plan
1. [Step]

## Rollback Plan
1. [Step]
```
