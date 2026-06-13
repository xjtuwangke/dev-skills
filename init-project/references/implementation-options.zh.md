# init-project 实施方案调研

这份文档整理 `init-project` skill 后续演进时可以采用的公开实践和落地方案。核心目标是：为 coding agent 生成有用的项目上下文，但不要把仓库说明膨胀成第二套嘈杂代码库。

## 当前基线

`init-project` 当前已经具备：

- 一个偏薄的 `AGENTS.md`，聚焦项目命令、目录结构和协作约束。
- `references/templates/{name}/index.md` 下的模板片段，一个项目可以命中多个模板。
- `scripts/templates/{name}/` 下的模板专属脚本。
- 检测和渲染脚本，按命中的模板渐进加载内容。
- Java/Maven 检查、依赖树生成、Spring Boot WebFlux 检查、Karate AT 检查，以及 skill 自校验。

## 公开实践

### AGENTS.md 作为共享仓库说明

OpenAI Codex 文档把 `AGENTS.md` 定义为 Codex 开始工作前读取的项目说明文件。同时它支持分层加载：先全局说明，再仓库说明，再更靠近当前文件的嵌套说明；越后加载、越具体的说明优先级越高。Codex 对组合后的指令大小也有默认上限，因此生成文件不宜过大。

参考：[OpenAI Codex AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)

开放的 AGENTS.md 格式把 `AGENTS.md` 视为工具中立的 agent 指令入口。

参考：[AGENTS.md open format](https://agents.md/)

### Copilot 风格的路径级说明

GitHub Copilot 支持仓库级说明，也支持 `.github/instructions/*.instructions.md` 这种带 `applyTo` glob 的路径级说明。GitHub 也识别嵌套 `AGENTS.md`，编辑某个文件时，离该文件最近的 `AGENTS.md` 可以优先生效。

参考：[GitHub Copilot repository instructions](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions)

### Claude Code 的记忆桥接

Claude Code 主要读取 `CLAUDE.md`，不是直接读取 `AGENTS.md`。但官方文档推荐用一个 `CLAUDE.md` 导入 `@AGENTS.md`，从而复用同一份仓库说明。该文档也强调：具体、简洁的指令更容易被稳定遵循。

参考：[Claude Code memory](https://code.claude.com/docs/en/memory)

### 小型约定文件和 repo map

Aider 推荐维护小型 markdown 约定文件，并以只读上下文方式持续加载。它的 repo map 方案也很有启发：与其让 agent 从原始文件树里自行猜测，不如提供一份紧凑的类、函数、签名、重要文件地图。

参考：

- [Aider conventions](https://aider.chat/docs/usage/conventions.html)
- [Aider repo map](https://aider.chat/docs/repomap.html)

### 可复用指令目录

`awesome-copilot` 把 prompts、instructions、skills、hooks、workflows 组织成类似 marketplace 的目录。等 `init-project` 模板数量变多后，这种目录化元数据会很适合用来管理模板发现和扩展。

参考：[github/awesome-copilot](https://github.com/github/awesome-copilot)

## 研究信号

近期公开研究给出的信号是双向的：

- 仓库上下文文件可能提升效率。有研究观察到，存在 `AGENTS.md` 时，中位运行时间和输出 token 会下降，同时任务完成行为大体保持可比。
- 上下文文件也可能伤害任务成功率和成本，尤其是其中包含过宽泛的探索建议、无关要求或过多规则时。相比大段规则，最小且任务相关的上下文更安全。
- 配置文件仍是当前定制 coding agent 的主流方式，而 `AGENTS.md` 正在成为跨工具的互操作标准。

参考：

- [On the Impact of AGENTS.md Files on the Efficiency of AI Coding Agents](https://arxiv.org/abs/2601.20404)
- [Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?](https://arxiv.org/abs/2602.11988)
- [Configuring Agentic AI Coding Tools: An Exploratory Study](https://arxiv.org/abs/2602.14690)

## 方案 V1：薄根文件 + 证据文件

生成一份简洁的根目录 `AGENTS.md`，把大部分技术栈细节放到 `agents/` 或其他生成支持目录里的引用文件中。

变化点：

- 保持 `AGENTS.md` 简短，只包含命令、目录结构、测试策略、生成证据文件链接。
- 在生成流程或校验器里加入长度预算和噪音预算。
- 优先写入项目扫描得到的事实，而不是通用规则。

优点：

- 最符合 Codex 指令大小限制，也符合研究里对上下文膨胀的警告。
- 基于当前模板引用和 inspectors 很容易实现。
- 初始加载成本低，稳定性好。

缺点：

- agent 需要在必要时主动打开被引用的文件。
- 有些工具不一定像直接加载文本那样可靠地跟随引用。

实施计划：

1. 在校验中加入 `max_root_lines`、`max_root_bytes`、`max_template_summary_lines`。
2. 生成 `agents/project-evidence.md`，包含检测输出、Maven 坐标、模块列表、依赖树位置、命中模板。
3. 模板片段只写短的、局部的事实和命令。

测试计划：

- 对 Maven、Spring WebFlux、Karate 示例项目做渲染快照。
- 校验根文件大小，以及是否存在空模板段落。
- 校验被引用的证据文件确实存在。

实际例子，Maven + Spring Boot 纯后端项目：

假设项目结构如下：

```text
pom.xml
src/main/java/com/acme/order/OrderApplication.java
src/main/java/com/acme/order/api/OrderController.java
src/main/java/com/acme/order/service/OrderService.java
src/test/java/com/acme/order/service/OrderServiceTest.java
```

V1 会生成一个很短的根目录 `AGENTS.md`：

```markdown
# Agent Instructions

## Project facts

- Java Maven backend service.
- Spring Boot 3 application detected.
- Primary build file: `pom.xml`.
- Generated project evidence: `agents/project-evidence.md`.

## Common commands

- Compile: `mvn compile`
- Run tests: `mvn test`
- Package: `mvn package`

## Working rules

- Prefer Maven wrapper if `mvnw` exists.
- Keep changes scoped to the module and package being edited.
- Read `agents/project-evidence.md` before changing dependencies or build configuration.
```

同时生成 `agents/project-evidence.md`：

```markdown
# Project Evidence

## Maven coordinates

- groupId: `com.acme`
- artifactId: `order-service`
- version: `0.1.0-SNAPSHOT`
- packaging: `jar`

## Detected templates

- `maven-java`
- `springboot3-webflux` or `springboot3-web`

## Key dependencies

- `org.springframework.boot:spring-boot-starter-web`
- `org.springframework.boot:spring-boot-starter-validation`
- `org.springframework.boot:spring-boot-starter-test`

## Dependency tree

- Generated file: `agents/maven-dependency-tree.txt`
```

这个例子里，根文件只给 agent 第一屏必读信息；依赖详情和扫描事实留在 evidence 文件里，避免每次任务都加载过多上下文。

## 方案 V2：路径级 instruction pack

当仓库目录结构足够明确时，除了根说明，还生成路径级指令文件。

变化点：

- 对 `src/test`、`src/it`、`features`、service module 等高信号子树生成嵌套 `AGENTS.md`。
- 可选生成 `.github/instructions/*.instructions.md`，并用 `applyTo` glob 适配 Copilot。

优点：

- 符合 Codex 和 GitHub 文档里的就近优先模型。
- agent 只编辑测试、WebFlux handler 或 Karate feature 时，不会被无关规则干扰。
- 很契合“一个项目命中多个模板”的设计。

缺点：

- 生成文件更多，需要 review。
- Codex、Copilot、Claude 对 scoped 文件的加载行为并不完全一致。
- 路径识别错误时，规则可能落到错误作用域。

实施计划：

1. 扩展 inspectors，返回候选作用域：`main_sources`、`test_sources`、`karate_features`、`webflux_handlers`。
2. 只把模板指导应用到匹配作用域中。
3. 输出人工检查清单，说明建议创建哪些文件以及原因。

测试计划：

- 多模块 Maven fixture。
- Karate feature 位于非标准路径的 fixture。
- 校验 scoped 文件不重复根文件内容。

实际例子，Maven + Spring Boot 纯后端项目：

假设项目中存在 controller、service、repository 和 test 目录：

```text
src/main/java/com/acme/order/api/
src/main/java/com/acme/order/service/
src/main/java/com/acme/order/repository/
src/test/java/com/acme/order/
```

V2 可以生成根 `AGENTS.md`，再生成靠近代码的嵌套说明：

```text
AGENTS.md
src/main/java/com/acme/order/api/AGENTS.md
src/main/java/com/acme/order/service/AGENTS.md
src/test/java/com/acme/order/AGENTS.md
```

`src/main/java/com/acme/order/api/AGENTS.md` 示例：

```markdown
# API Layer Instructions

- This package contains Spring HTTP entry points.
- Keep request and response DTOs explicit.
- Validate inbound payloads with Jakarta Validation annotations.
- Do not put business decisions in controllers; delegate to service classes.
- When adding endpoints, update controller tests or web slice tests.
```

`src/main/java/com/acme/order/service/AGENTS.md` 示例：

```markdown
# Service Layer Instructions

- This package owns application use cases and transaction boundaries.
- Keep persistence details behind repository interfaces.
- Prefer constructor injection.
- Add focused unit tests for new branches or error paths.
```

`src/test/java/com/acme/order/AGENTS.md` 示例：

```markdown
# Test Instructions

- Use JUnit 5 and AssertJ conventions already present in this project.
- Prefer fast unit tests unless the change crosses Spring wiring boundaries.
- Use `mvn test` for the default verification path.
```

如果启用 Copilot 兼容输出，也可以生成：

```text
.github/instructions/api.instructions.md
.github/instructions/tests.instructions.md
```

其中 `api.instructions.md` 带 frontmatter：

```markdown
---
applyTo: "src/main/java/**/api/**/*.java"
---

# API Layer Instructions

- Keep controllers thin and delegate business logic to services.
```

这个例子里，agent 编辑 controller 时只吃到 API 层规则；编辑测试时只吃到测试规则，减少无关模板内容。

## 方案 V3：跨 agent 桥接

以 `AGENTS.md` 作为唯一事实源，再按需生成其他工具的小型桥接文件。

变化点：

- 生成包含 `@AGENTS.md` 的 `CLAUDE.md`。
- 可选生成 `.github/copilot-instructions.md` 或 `.github/instructions/*.instructions.md`。
- 增加 manifest，记录生成文件和来源模板 hash。

优点：

- 一次初始化可以服务 Codex、Claude Code、Copilot。
- 减少手工重复维护。
- 与公开工具文档保持一致。

缺点：

- 如果用户手改生成文件，桥接文件可能漂移。
- 当仓库已有多个工具文件时，优先级可能冲突。
- 需要非常谨慎的覆盖策略。

实施计划：

1. 增加 `--emit-bridge claude,copilot`，默认不启用。
2. 检测已有 `CLAUDE.md`、`.github/copilot-instructions.md` 和 scoped instruction 文件。
3. 使用保守 merge 模式：缺失则创建，只在标记的 generated region 内追加，默认不覆盖用户手写内容。
4. 在 `agents/init-project-manifest.json` 记录生成文件元数据。

测试计划：

- 已存在 bridge 文件且没有 generated region。
- 已存在 bridge 文件且有 generated region。
- 同时存在根目录和嵌套 `AGENTS.md` 的仓库。

实际例子，Maven + Spring Boot 纯后端项目：

V3 仍然以根目录 `AGENTS.md` 为唯一主要说明：

```text
AGENTS.md
agents/project-evidence.md
```

如果用户选择 `--emit-bridge claude,copilot`，再生成：

```text
CLAUDE.md
.github/copilot-instructions.md
agents/init-project-manifest.json
```

`CLAUDE.md` 示例：

```markdown
# Claude Project Memory

@AGENTS.md

<!-- init-project:generated:start -->
This file delegates project instructions to `AGENTS.md`.
Regenerate with `init-project` when Maven or Spring project structure changes.
<!-- init-project:generated:end -->
```

`.github/copilot-instructions.md` 示例：

```markdown
# Repository Instructions

Follow the source of truth in `AGENTS.md`.

For this Maven Spring Boot backend:

- Use Maven commands from `AGENTS.md`.
- Keep Spring controllers thin.
- Add or update tests for changed service behavior.
```

`agents/init-project-manifest.json` 示例：

```json
{
  "source": "init-project",
  "project": {
    "build": "maven",
    "language": "java",
    "frameworks": ["spring-boot"]
  },
  "generatedFiles": [
    "AGENTS.md",
    "CLAUDE.md",
    ".github/copilot-instructions.md",
    "agents/project-evidence.md"
  ],
  "templates": ["maven-java", "springboot3-web"]
}
```

这个例子里，不同 agent 都能读到同一套项目约束，但实际维护中心仍是 `AGENTS.md`，降低多文件漂移风险。

## 方案 V4：repo map 增强

借鉴 Aider，生成一份紧凑的 repo map：重要文件、Java package、class、method、Spring component、route、Karate feature、构建模块等。

变化点：

- 生成 `agents/repo-map.md` 或 `agents/repo-map.json`。
- 放入顶层符号和关系，而不是完整源码摘录。
- 通过技术栈 inspector 丰富 map 内容。

优点：

- 不加载大量文件，也能给 agent 足够的项目拓扑。
- 帮助 agent 找到正确抽象，减少重复实现。
- 能补充 Maven 和依赖树事实。

缺点：

- Java 解析会变复杂，尤其遇到 annotation processor 和 generated code。
- repo map 如果不重新生成就会过期。
- map 太大时会重新制造上下文膨胀问题。

实施计划：

1. 先用简单 regex 或 XML-backed 方式生成 Java map：package、public class、annotation、method name。
2. 加入 Spring WebFlux route 提取：`@RestController`、functional router bean、WebClient bean。
3. 加入 Karate feature map：feature 文件、scenario 名、tag、被调用 helper。
4. 限制每个 module 和文件数量，超限时写入 warning。

测试计划：

- 校验 repo-map JSON schema。
- 为代表性项目生成 map 快照。
- 确认生成 Markdown 低于配置的大小预算。

实际例子，Maven + Spring Boot 纯后端项目：

对于下面的项目：

```text
src/main/java/com/acme/order/OrderApplication.java
src/main/java/com/acme/order/api/OrderController.java
src/main/java/com/acme/order/api/CreateOrderRequest.java
src/main/java/com/acme/order/service/OrderService.java
src/main/java/com/acme/order/repository/OrderRepository.java
src/main/java/com/acme/order/domain/Order.java
```

V4 生成 `agents/repo-map.md`：

```markdown
# Repo Map

## Maven module

- root module: `com.acme:order-service`
- packaging: `jar`
- Java source root: `src/main/java`
- Test source root: `src/test/java`

## Spring Boot entrypoint

- `com.acme.order.OrderApplication`

## HTTP API

- `OrderController`
  - package: `com.acme.order.api`
  - annotations: `@RestController`, `@RequestMapping("/orders")`
  - methods:
    - `create(CreateOrderRequest request)`
    - `getById(String id)`

## Application services

- `OrderService`
  - package: `com.acme.order.service`
  - methods:
    - `createOrder(...)`
    - `findOrder(...)`

## Persistence

- `OrderRepository`
  - package: `com.acme.order.repository`
  - likely Spring Data repository

## Domain

- `Order`
  - package: `com.acme.order.domain`
```

也可以生成机器可读的 `agents/repo-map.json`：

```json
{
  "entrypoints": ["com.acme.order.OrderApplication"],
  "controllers": [
    {
      "class": "OrderController",
      "path": "src/main/java/com/acme/order/api/OrderController.java",
      "routes": ["/orders"]
    }
  ],
  "services": [
    {
      "class": "OrderService",
      "path": "src/main/java/com/acme/order/service/OrderService.java"
    }
  ]
}
```

这个例子里，agent 想改新增订单逻辑时，可以先从 repo map 找到 controller、service、repository、domain 的关系，而不是全仓库搜索一遍。

## 方案 V5：验证和 eval 回路

把 `init-project` 输出变成可测试产物，而不仅是生成文档。

变化点：

- 扩展 `validate_skill.py`，让它成为模板、脚本和渲染输出的质量门。
- 增加 fixtures 和 expected outputs。
- 检查缺失命令、断链、空段落、过多通用建议。

优点：

- 模板越来越多时，可以防止漂移。
- commit 和 push 前更安全。
- 让质量评估从主观 prompt tuning 变成可测规则。

缺点：

- 需要样例仓库或合成 fixtures。
- 如果输出格式经常变，快照测试可能比较吵。

实施计划：

1. 在 `init-project/evals/fixtures/` 增加 fixtures。
2. 添加 expected rendered file manifests，不保存完整大快照。
3. 检查不变量：命中模板、生成文件、文件大小、命令提取、无断链。
4. 增加 README 段落说明 validation workflow。

测试计划：

- 对每个 fixture 跑 validation。
- 相对链接断裂、模板脚本引用缺失时失败。
- 将 detector JSON 与期望模板命中结果对比。

实际例子，Maven + Spring Boot 纯后端项目：

增加一个 fixture：

```text
init-project/evals/fixtures/springboot-maven-backend/
  pom.xml
  src/main/java/com/acme/order/OrderApplication.java
  src/main/java/com/acme/order/api/OrderController.java
  src/test/java/com/acme/order/OrderApplicationTests.java
  expected/
    detector.json
    generated-files.json
```

`expected/detector.json` 示例：

```json
{
  "templates": ["maven-java", "springboot3-web"],
  "build": {
    "tool": "maven",
    "rootPom": "pom.xml"
  },
  "java": {
    "sourceRoots": ["src/main/java"],
    "testRoots": ["src/test/java"]
  },
  "spring": {
    "bootVersionMajor": 3,
    "applicationClasses": [
      "src/main/java/com/acme/order/OrderApplication.java"
    ]
  }
}
```

`expected/generated-files.json` 示例：

```json
{
  "required": [
    "AGENTS.md",
    "agents/project-evidence.md"
  ],
  "optionalWhenEnabled": [
    "CLAUDE.md",
    ".github/copilot-instructions.md",
    "agents/repo-map.md"
  ],
  "budgets": {
    "AGENTS.md": {
      "maxBytes": 6000,
      "maxLines": 120
    }
  }
}
```

validation 可以检查：

```text
- detector 是否命中 `maven-java` 和 `springboot3-web`
- `AGENTS.md` 是否包含 `mvn test`
- `agents/project-evidence.md` 是否包含 Maven 坐标
- 根文件是否超过大小预算
- 所有 markdown 链接是否能解析到真实文件
```

这个例子里，每次修改模板或 inspectors，都能用固定 Spring Boot Maven fixture 验证不会把项目初始化结果弄坏。

## 方案 V6：模板注册表

当模板数量增长后，引入机器可读的 registry。

变化点：

- 增加 `references/templates/index.json`。
- 每个模板声明 name、description、detector hints、scripts、emitted sections、兼容的 bridge outputs、依赖模板。

优点：

- 比手工扫描目录更适合扩展到大量模板。
- 让模板发现、文档生成、校验更容易。
- 支持类似 Copilot instruction catalog 的 marketplace 浏览方式。

缺点：

- 太早引入结构会拖慢模板编写。
- registry/schema 维护会变成每次改动的一部分。

实施计划：

1. 在模板达到 6-8 个之前，保持 registry 可选。
2. 定义最小 schema：`name`、`summary`、`detects`、`scripts`、`outputs`、`dependencies`。
3. detector 和 validator 在 registry 存在时读取它。
4. 从 registry 元数据生成 template index page。

测试计划：

- 校验每个注册路径都存在。
- 校验 dependencies 指向已知模板。
- 迁移期内，未注册的旧模板仍然可用。

实际例子，Maven + Spring Boot 纯后端项目：

当模板变多后，可以把当前目录扫描升级为显式 registry：

```text
references/templates/index.json
references/templates/maven-java/index.md
references/templates/springboot3-web/index.md
references/templates/springboot3-webflux/index.md
references/templates/karate-at/index.md
```

`references/templates/index.json` 示例：

```json
{
  "templates": [
    {
      "name": "maven-java",
      "summary": "Java project built with Maven",
      "detects": {
        "files": ["pom.xml"],
        "pomPackaging": ["jar", "war", "pom"]
      },
      "scripts": [
        "scripts/templates/maven-java/inspect_maven_project.py",
        "scripts/templates/maven-java/generate_dependency_tree.py"
      ],
      "outputs": [
        "agents/project-evidence.md",
        "agents/maven-dependency-tree.txt"
      ]
    },
    {
      "name": "springboot3-web",
      "summary": "Spring Boot 3 backend service using servlet web stack",
      "dependsOn": ["maven-java"],
      "detects": {
        "pomDependencies": [
          "org.springframework.boot:spring-boot-starter-web"
        ],
        "javaAnnotations": ["SpringBootApplication", "RestController"]
      },
      "outputs": [
        "AGENTS.md",
        "agents/repo-map.md"
      ]
    }
  ]
}
```

对一个 `pom.xml` 包含下面依赖的项目：

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
</dependency>
```

detector 可以稳定得到：

```json
{
  "matchedTemplates": [
    "maven-java",
    "springboot3-web"
  ],
  "templateReasons": {
    "maven-java": ["found pom.xml"],
    "springboot3-web": [
      "found spring-boot-starter-web",
      "found @SpringBootApplication"
    ]
  }
}
```

这个例子里，模板是否适用、依赖哪个基础模板、会生成哪些文件都由 registry 显式声明；等模板数量增加时，维护成本会比隐式目录扫描更可控。

## 推荐路线

1. 先做 V1 hardening。它能增强当前设计，而且不改变用户工作流。
2. 再做 V2 scoped instruction generation，覆盖 Maven、Spring WebFlux、Karate 项目。这最贴合“一个项目命中多个模板”的设计。
3. 增加 V3 bridge output，支持 Claude 和 Copilot，但默认关闭。
4. 在继续增加大量模板前，先做 V5 quality gates。
5. 有 fixture 覆盖后，再做 V4 repo map。
6. 只有当模板数量大到目录扫描难以维护时，再做 V6 registry。

## 决策矩阵

| 方案 | 当前适配度 | 成本 | 主要风险 | 优先级 |
| --- | --- | --- | --- | --- |
| V1 薄根文件 + 证据文件 | 高 | 低 | agent 可能跳过引用证据 | 1 |
| V2 路径级 instruction pack | 高 | 中 | 路径作用域判断错误 | 2 |
| V3 跨 agent 桥接 | 中 | 中 | 漂移和优先级冲突 | 3 |
| V5 验证和 eval 回路 | 高 | 中 | fixture 维护成本 | 4 |
| V4 repo map 增强 | 中 | 高 | 解析复杂且容易过期 | 5 |
| V6 模板注册表 | 当前低，后续高 | 中 | 过早 schema 化 | 6 |
