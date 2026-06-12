# Architecture Notes

## Primary Flow
```text
HTTP route/controller -> handler/service -> client/repository -> external dependency
```

## Spring Boot WebFlux Evidence
### Application classes
- `src/main/java/com/acme/skillplayground/SkillPlaygroundApplication.java`
### Controllers, handlers, or router functions
- `src/main/java/com/acme/skillplayground/endpoint/OrderEndpoint.java`
- `src/main/java/com/acme/skillplayground/exception/ApiExceptionHandler.java`
### Web clients or HTTP clients
- None detected
### Reactive sources
- `src/main/java/com/acme/skillplayground/endpoint/OrderEndpoint.java`
- `src/main/java/com/acme/skillplayground/pubsub/GcpPubSubOrderEventPublisher.java`
- `src/main/java/com/acme/skillplayground/pubsub/NoopOrderEventPublisher.java`
- `src/main/java/com/acme/skillplayground/pubsub/OrderEventPublisher.java`
- `src/main/java/com/acme/skillplayground/service/OrderService.java`
- `src/main/java/com/acme/skillplayground/service/OrderUseCase.java`
- `src/test/java/com/acme/skillplayground/endpoint/OrderEndpointTest.java`
- `src/test/java/com/acme/skillplayground/service/OrderServiceTest.java`
### Configuration/property classes
- `src/main/java/com/acme/skillplayground/SkillPlaygroundApplication.java`
- `src/main/java/com/acme/skillplayground/config/OrderProperties.java`
### WebFlux tests
- `src/test/java/com/acme/skillplayground/endpoint/OrderEndpointTest.java`
- `src/test/java/com/acme/skillplayground/pubsub/GcpPubSubOrderEventPublisherTest.java`
- `src/test/java/com/acme/skillplayground/pubsub/NoopOrderEventPublisherTest.java`
- `src/test/java/com/acme/skillplayground/service/OrderServiceTest.java`
### Flyway migrations
- `src/main/resources/db/migration/V1__create_orders.sql`
- `src/main/resources/db/migration/V2__retail_platform_schema.sql`
- `src/main/resources/db/migration/V3__add_order_shipping_priority.sql`

### Surface Counts
- Endpoints: 4
- Services: 1
- Repositories: 1
- Entities: 1
- Pub/Sub classes: 6


## Representative Java Files
- `src/main/java/com/acme/skillplayground/SkillPlaygroundApplication.java`
- `src/main/java/com/acme/skillplayground/config/OrderProperties.java`
- `src/main/java/com/acme/skillplayground/database/entity/OrderEntity.java`
- `src/main/java/com/acme/skillplayground/database/repository/OrderRepository.java`
- `src/main/java/com/acme/skillplayground/endpoint/OrderEndpoint.java`
- `src/main/java/com/acme/skillplayground/exception/ApiExceptionHandler.java`
- `src/main/java/com/acme/skillplayground/exception/OrderNotFoundException.java`
- `src/main/java/com/acme/skillplayground/model/CreateOrderRequest.java`
- `src/main/java/com/acme/skillplayground/model/OrderResponse.java`
- `src/main/java/com/acme/skillplayground/model/OrderStatus.java`
- `src/main/java/com/acme/skillplayground/model/UpdateOrderStatusRequest.java`
- `src/main/java/com/acme/skillplayground/pubsub/GcpPubSubGateway.java`
- `src/main/java/com/acme/skillplayground/pubsub/GcpPubSubOrderEventPublisher.java`
- `src/main/java/com/acme/skillplayground/pubsub/NoopOrderEventPublisher.java`
- `src/main/java/com/acme/skillplayground/pubsub/OrderEvent.java`
- `src/main/java/com/acme/skillplayground/pubsub/OrderEventPublisher.java`
- `src/main/java/com/acme/skillplayground/pubsub/PubSubGateway.java`
- `src/main/java/com/acme/skillplayground/service/OrderService.java`
- `src/main/java/com/acme/skillplayground/service/OrderUseCase.java`
- `src/test/java/com/acme/skillplayground/endpoint/OrderEndpointTest.java`
- `src/test/java/com/acme/skillplayground/pubsub/GcpPubSubOrderEventPublisherTest.java`
- `src/test/java/com/acme/skillplayground/pubsub/NoopOrderEventPublisherTest.java`
- `src/test/java/com/acme/skillplayground/service/OrderServiceTest.java`

## Representative Feature Files
- None detected

## Risk Areas
- Generated files, fixtures, contracts, shared helpers, and environment-specific config.
- Public APIs and serialization/deserialization behavior.
- Authentication, authorization, secrets handling, file paths, shell execution, XML/JSON parsing, and network calls.
