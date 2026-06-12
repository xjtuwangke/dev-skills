# Agent 指令

## 项目

- Maven Java 17 响应式后端服务。
- 业务域：电商订单履约，覆盖订单、客户、库存、支付、履约计划、物流、退货、对账和订单事件。
- 主要运行栈：Spring WebFlux、PostgreSQL via R2DBC、Reactive Redis、GCP Pub/Sub、Springfox API docs。
- Maven wrapper 固定为 Maven 3.4.0。POM 通过 enforcer 要求 Maven `>=3.4.0` 且 Java `[17,18)`。
- Springfox 是遗留 docs 依赖。这个 fixture 保持 Spring Boot 2.7.18，是为了让 Springfox 3 能配合 WebFlux 和 Java 17 使用。

## 优先阅读

- `agents/PROJECT_PROFILE.md`：模块、包、环境和关键文件。
- `agents/BACKEND_SURFACES.md`：修改 endpoint、persistence、client、Redis 或 pub/sub 前先读。
- `agents/CALL_CHAINS.md`：修改已有 API 或消息 handler 背后的行为前先读。
- `agents/BUILD_AND_TEST.md`：运行验证前先读。
- `agents/DEPENDENCIES.md`：修改 POM 或依赖版本前先读。

## 常用命令

- 编译：`./mvnw compile`
- 运行测试：`./mvnw test`
- 打包：`./mvnw package`
- 本地运行：`SPRING_PROFILES_ACTIVE=dev ./mvnw spring-boot:run`
- 不启动 HTTP 服务导出 Springfox 文档：增加一个 Spring test，读取 Springfox `DocumentationCache` 并写出 `target/openapi.yaml`；不要假设 Springfox 可以在不启动 Spring context 的情况下生成 OpenAPI。

## 变更规则

- HTTP handler 放在 `endpoint/`；业务决策放在 `service/`。
- 存储访问通过 `database/` repository 封装。
- 出站 HTTP 调用放在 `client/`；记录 base URL config key、timeout、retry 和 error mapping。
- GCP Pub/Sub 发布/消费行为放在 `pubsub/`；记录 topic/subscription、payload、idempotency 和 ack 行为。
- 修改 endpoint 时，同步更新 `src/main/resources/openapi.yaml`、endpoint tests、`agents/BACKEND_SURFACES.md`，以及 `agents/CALL_CHAINS.md` 中对应调用链。
- 修改订单、支付、库存或物流行为时，同时检查请求驱动链路和事件驱动链路。
- 不要把 secret 写进生成的 agent 文档。只引用 `DB_USER`、`DB_PASSWORD` 这类环境变量名。

