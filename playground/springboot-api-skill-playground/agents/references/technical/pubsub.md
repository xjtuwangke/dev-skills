# Pub/Sub Technical Reference

## Source Areas
- `src/main/java/com/acme/skillplayground/pubsub/`
- `src/main/java/com/acme/skillplayground/config/`
- `src/main/resources/application*.yml`
- `src/test/java/com/acme/skillplayground/pubsub/`

## Concerns
- Publisher interfaces, gateway implementations, and conditional beans.
- Topic names per profile and environment variable requirements.
- Event payload shape, identifiers, timestamps, shipping priority, and manual review flags.
- Publish success/failure behavior and whether failures affect API responses.
- Tests for payload serialization, no-op behavior, and reactive completion.

## Related Context
- Business event meaning: `agents/references/business/order-events.md`
- Service trigger points: `agents/references/technical/services.md`
