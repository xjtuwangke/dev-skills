# Services Technical Reference

## Source Areas
- `src/main/java/com/acme/skillplayground/service/`
- `src/main/java/com/acme/skillplayground/mapper/`
- `src/main/java/com/acme/skillplayground/model/`
- `src/main/java/com/acme/skillplayground/exception/`
- `src/test/java/com/acme/skillplayground/service/`

## Current Services
- `OrderService`
- `CustomerProfileService`
- `CatalogQueryService`
- `InventoryReservationService`
- `PricingService`
- `PromotionService`
- `PaymentAuthorizationService`
- `FulfillmentPlanningService`
- `ReturnPolicyService`
- `SupportTicketService`
- `AuditTrailService`

## Current Mappers
- `MoneyMapper`
- `CustomerProfileMapper`
- `CatalogMapper`
- `FulfillmentMapper`

## Concerns
- Public use-case methods and collaborator boundaries.
- Entity/model conversion, defaults, and enum transitions.
- Not-found, validation, duplicate, and failure behavior.
- Transactional assumptions and blocking calls inside reactive wrappers.
- Event publication timing relative to persistence changes.
- Manual type mapping, rounding, date, and domain-rule decisions.

## Best Practices
- Keep service methods responsible for business decisions, state changes, and side-effect ordering.
- Validate domain rules before persistence when the rule does not need a saved entity.
- Persist first, map to response, then publish events for successful state changes.
- Keep blocking repository access isolated on `Schedulers.boundedElastic()`.

```java
public Mono<OrderResponse> create(final CreateOrderRequest request) {
    return Mono.fromCallable(() -> {
                validateCreateRequest(request);
                return orderRepository.save(OrderEntity.create(request, requiresManualReview(request)));
            })
            .subscribeOn(Schedulers.boundedElastic())
            .map(this::toResponse)
            .flatMap((final OrderResponse response) -> orderEventPublisher.publishCreated(response)
                    .thenReturn(response));
}
```
