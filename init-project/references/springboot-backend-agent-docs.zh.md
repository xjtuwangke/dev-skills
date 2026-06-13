# Spring Boot 后端 Agent 文档组织建议

这份参考用于指导 `init-project` 为 Spring Boot 后端项目生成
`AGENTS.md` 和 `agents/` 支撑文档。目标不是写项目 Wiki，也不是保存
完整证据库，而是给后续 coding agent 一张低维护成本的工作地图。

## 核心原则

- 根目录 `AGENTS.md` 保持短，只负责一句话定位项目和 `Where To Look` 路由。
- 可复用上下文直接放在 `agents/technical/` 和 `agents/business/`。
- 不再默认生成额外的 `references` 中间层目录。
- 不默认生成 `PROJECT_PROFILE.md`、`PROJECT_EVIDENCE.md`、
  `ARCHITECTURE_NOTES.md`、`BACKEND_SURFACES.md`、`CALL_CHAINS.md`、
  `SUBAGENTS.md` 或 tool wrapper。
- 证据要够用，不追求堆满。能指向源码、测试、配置或 OpenAPI 的事实才写入。
- 业务语义和技术结构分开。代码需求变更、review、业务逻辑梳理应该能各读所需。

## 推荐输出结构

```text
AGENTS.md
agents/
  technical.md
  technical/
    endpoints.md
    services.md
    persistence.md
    clients.md
    integrations.md
    pubsub.md
    testing.md
  business/
    domain-overview.md
    business-rules.md
    events.md
```

实际生成时按项目证据裁剪。没有 Pub/Sub 就不生成 `pubsub.md`；没有清晰业务
规则就不硬写业务卡片。

## 主要使用场景

代码需求变更、分析和实施：

- 先读 `AGENTS.md`。
- 技术类任务先读 `agents/technical.md`，再根据变更面读取一个或几个
  `agents/technical/*.md`。
- 如果涉及业务含义、状态流转、价格、支付、履约、审计或事件 payload，再读相关
  `agents/business/*.md`。
- 最后看源码和测试。文档只能导航，不能替代源码确认。

当前代码 review：

- 先用 `AGENTS.md` 判断项目边界，再进入 `agents/technical.md` 看验证命令。
- 读 touched area 对应的 technical card。
- review 行为变化时读 business card。
- 不要求 reviewer 先读完整项目文档。

业务逻辑梳理：

- 优先读 `agents/business/`。
- 技术卡片只用于定位实现入口、测试和持久化/消息副作用。
- 业务事实不确定时写 `Needs confirmation`，不要把推测写成规则。

## AGENTS.md 建议内容

根 `AGENTS.md` 建议包含：

- 项目一句话定位。
- `Where To Look` 表格，把技术任务映射到 `agents/technical.md`，把业务任务映射到
  `agents/business/`。
- 不放高频命令、coding standards、validation 细节或 best practice demo；这些内容下放到
  `agents/technical.md` 或 focused cards。

不建议包含：

- 完整 endpoint 列表。
- 完整依赖树。
- 大段通用 Spring 最佳实践。
- 推测出来的调用链。
- tool-specific subagent 配置。

## Technical Cards

每个 `agents/technical/*.md` 都应该有 `Best Practices` 小节，并给出一个短的
推荐写法 demo。demo 可以是 Java、YAML、SQL、Maven 命令或测试代码，但要贴近
项目已有风格，不要写成泛用教程。

`agents/technical.md`：

- technical 目录页，作为 `AGENTS.md` 之后的下一层渐进披露。
- 目录索引：按 endpoint、service、persistence、client、pubsub、integration、testing
  链接到 `agents/technical/*.md`。
- common Checkstyle：配置路径、`mvn -B -ntp checkstyle:check`、报告路径。
- 各类 Maven 命令：编译、测试、targeted tests、verify、本地启动。
- coding standards：constructor injection、`final`、records、imports、license
  header、exception/problem details、logging、mapper、test fixture 等本地风格。
- 需要 Docker/Testcontainers/profile/env var 的命令说明。
- Maven 低上下文日志模式。

`agents/technical/endpoints.md`：

- 按接口维度组织，一接口一个小节，例如 `### POST /api/orders`。
- 每个接口的方法和路径。
- 文档地址，如果项目配置了 SpringDoc/OpenAPI/Swagger UI。
- 所在 endpoint/controller/router class 和 method。
- Request POJO、Response POJO、状态码、重要响应 header。
- 每个接口用结构化 validation 表格整理 request body、path variable、query
  parameter、request header validations。
- validation、status code、problem details、OpenAPI/SpringDoc 线索。
- 如果当前没有 `@RequestHeader` 或 header validation，要明确写“没有”。
- endpoint 层该保持薄还是承载业务逻辑，以现有代码为准。

`agents/technical/services.md`：

- service/application 层入口。
- collaborator 边界、transaction 假设、状态流转、事件发布时间点。
- blocking 调用在 reactive 项目里的隔离方式。

`agents/technical/persistence.md`：

- entity、repository、migration、profile config、table/column 线索。
- JPA/Hibernate、R2DBC、Flyway/Liquibase 等相关注意点。

`agents/technical/clients.md`：

- 按下游接口维度组织，一个 downstream API 一个小节。
- 每个下游接口写 host/base URL config key、默认 host、client class/method。
- HTTP method、path、Request POJO、Response POJO、request/response header。
- 用结构化 validation 表格整理 body、path variable、query parameter、header 要求。
- timeout/retry/error mapping 有证据才写；没有配置时明确写没有。
- 写明覆盖 host/path/method/serialization/error handling 的测试。

`agents/technical/integrations.md`：

- outbound HTTP/client、数据库、缓存、消息系统、外部配置。
- timeout/retry/error mapping/idempotency 只有有证据才写。

`agents/technical/pubsub.md`：

- topic/binding/config key、producer/consumer、payload、retry/DLQ 线索。
- 事件 payload 是跨系统契约，改动时同步测试和业务卡片。

`agents/technical/testing.md`：

- JUnit 5、Mockito、WebTestClient、StepVerifier、JaCoCo、Checkstyle。
- 每类变更应该优先跑哪些 targeted tests。

## Business Cards

业务卡片描述“系统为什么这样做”，不是重复代码结构。

适合写入：

- domain terms。
- 状态机和允许/禁止的状态迁移。
- 定价、促销、支付、履约、退货、客服、审计等规则。
- 事件含义和消费者依赖。
- API use case 的业务语义。

不适合写入：

- controller/service/repository 文件清单。
- 没有代码、测试、产品文档或用户确认支撑的政策规则。
- “可能”“应该”的猜测，除非明确标注 `Needs confirmation`。

## 可选深文档

只有在用户明确要求，或项目确实很大且维护收益高于成本时，才考虑增加：

- call chain map。
- backend surface catalog。
- raw evidence/audit trail。
- subagent role files。
- `.codex/`、`.opencode/`、`.github/` tool wrapper。

这些文件一旦默认生成，会增加每次代码变更后的同步成本，所以不作为默认产物。

## 可用事实来源

- Spring MVC/WebFlux mapping 注解：`@RequestMapping`、`@GetMapping`、
  `@PostMapping` 等。参考：
  [Spring Framework Mapping Requests](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-requestmapping.html)。
- Spring Boot Actuator mappings：运行后可通过 `/actuator/mappings` 查看映射。
  参考：
  [Spring Boot mappings endpoint](https://docs.spring.io/spring-boot/api/rest/actuator/mappings.html)。
- OpenAPI/SpringDoc：可从配置、类结构和注解推断 API 语义。参考：
  [springdoc-openapi](https://springdoc.org/)。
- Persistence：Spring Data repository interface 绑定 domain class 和 ID 类型。
  参考：
  [Spring Data JPA repositories](https://docs.spring.io/spring-data/jpa/reference/repositories/definition.html)。
- Client：Spring `RestClient`、`WebClient`、HTTP Service Clients。参考：
  [Spring REST Clients](https://docs.spring.io/spring-framework/reference/integration/rest-clients.html) 和
  [Spring WebClient](https://docs.spring.io/spring-framework/reference/web/webflux-webclient.html)。
- Pub/Sub：Spring Cloud Stream binder、binding、message、consumer group、
  partitioning。参考：
  [Spring Cloud Stream](https://spring.io/projects/spring-cloud-stream/)。

## 反模式

- 为了“看起来完整”生成一堆未来没人维护的大文档。
- 把 `BUILD_AND_TEST.md`、`CODE_STYLE.md` 放在 agents 根目录，和 focused
  technical cards 分裂。
- 把业务规则藏在 technical 文档里，导致业务梳理必须读技术细节。
- 只写证据，不写 agent 实际该去哪里改代码和跑测试。
- 生成 tool wrapper，却没有明确使用场景。
