# 构建和测试

## 命令

| 任务 | 命令 |
| --- | --- |
| 编译 | `./mvnw compile` |
| 单元测试 | `./mvnw test` |
| 打包 | `./mvnw package` |
| 本地 dev 运行 | `SPRING_PROFILES_ACTIVE=dev ./mvnw spring-boot:run` |

只有 wrapper 不可用时才使用 `mvn`。这个 fixture 的 wrapper 固定为 Maven 3.4.0。

## 预期测试风格

- Endpoint tests 使用 `WebTestClient`。
- Service tests 使用 Reactor `StepVerifier`。
- Client tests 应该用 fake server 或 WebClient exchange function mock 下游 HTTP。
- Pub/Sub tests 应该验证 payload 序列化、topic/subscription 名称、ack 行为和幂等性决策。

## 验证清单

- Endpoint 变更：运行 endpoint tests，并对比 `openapi.yaml`。
- Service 行为变更：运行 service tests；如果编排变化，更新 `CALL_CHAINS.md`。
- Repository 变更：验证 schema/migration 和 repository tests。
- Client 变更：验证 timeout、retry、error mapping 和 base URL config。
- Pub/Sub 变更：验证 topic/subscription config、payload 兼容性、ack 行为、retry/DLQ 假设。

## Fixture 已知注意点

Springfox 基于 runtime/context 工作。不要声称它可以在没有 Spring context 的情况下从 Maven 直接产出 `openapi.yaml`。如果要实现不启动 HTTP 服务的导出，可以写一个 Spring test，使用 `MOCK` web environment 启动 context，并把 Springfox model 输出到 `target/openapi.yaml`。

