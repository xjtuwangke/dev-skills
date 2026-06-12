# Dependencies

## Runtime

| Dependency | Why it matters |
| --- | --- |
| `spring-boot-starter-webflux` | Reactive HTTP endpoints and WebClient support |
| `spring-boot-starter-data-r2dbc` | Reactive PostgreSQL repository access |
| `r2dbc-postgresql` | PostgreSQL R2DBC runtime driver |
| `postgresql` | JDBC driver for tooling/migration compatibility |
| `spring-boot-starter-data-redis-reactive` | Reactive Redis cache for order views |
| `spring-boot-starter-validation` | Request validation annotations |
| `spring-cloud-gcp-starter-pubsub` | GCP Pub/Sub publishing/subscribing |
| `springfox-boot-starter` | Legacy Swagger/OpenAPI docs integration |

## Test

| Dependency | Why it matters |
| --- | --- |
| `spring-boot-starter-test` | JUnit, Spring test support, WebFlux test support |
| `reactor-test` | `StepVerifier` and Reactor assertions |

## Version Notes

- Java is pinned to 17.
- Maven wrapper is pinned to 3.4.0 and enforcer requires Maven `>=3.4.0`.
- Spring Boot is 2.7.18 because Springfox 3 is legacy and is not a good fit for Spring Boot 3/Jakarta packages.
- If this fixture is migrated to Spring Boot 3.x, prefer replacing Springfox with springdoc-openapi and update expected docs accordingly.

