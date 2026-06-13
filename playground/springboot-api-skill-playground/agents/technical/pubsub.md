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

## Best Practices
- Keep topic names in `OrderProperties`; do not hard-code them in services.
- Publish events after successful persistence, not before repository state changes commit.
- Keep event payload records stable; treat field names as downstream contracts.
- Test both enabled publisher behavior and disabled no-op behavior.

```java
public Mono<Void> publishCreated(final OrderResponse order) {
    return publish(properties.pubsub().createdTopic(), OrderEvent.created(order));
}
```
