# 依赖

## Runtime

| 依赖 | 作用 |
| --- | --- |
| `spring-boot-starter-webflux` | 响应式 HTTP endpoints 和 WebClient 支持 |
| `spring-boot-starter-data-r2dbc` | 响应式 PostgreSQL repository 访问 |
| `r2dbc-postgresql` | PostgreSQL R2DBC runtime driver |
| `postgresql` | JDBC driver，用于工具和 migration 兼容 |
| `spring-boot-starter-data-redis-reactive` | 用于 order view 的 Reactive Redis cache |
| `spring-boot-starter-validation` | Request validation annotations |
| `spring-cloud-gcp-starter-pubsub` | GCP Pub/Sub publish/subscribe |
| `springfox-boot-starter` | 遗留 Swagger/OpenAPI docs 集成 |

## Test

| 依赖 | 作用 |
| --- | --- |
| `spring-boot-starter-test` | JUnit、Spring test support、WebFlux test support |
| `reactor-test` | `StepVerifier` 和 Reactor assertions |

## 版本说明

- Java 固定为 17。
- Maven wrapper 固定为 3.4.0，enforcer 要求 Maven `>=3.4.0`。
- Spring Boot 使用 2.7.18，因为 Springfox 3 是遗留方案，不适合 Spring Boot 3/Jakarta packages。
- 如果这个 fixture 迁移到 Spring Boot 3.x，优先用 springdoc-openapi 替换 Springfox，并同步更新 expected docs。

