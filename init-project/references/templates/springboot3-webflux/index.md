# Spring Boot 3 WebFlux Template

Use this template when a project is a Spring Boot 3 service using reactive WebFlux/Reactor. It usually combines with `maven-java`.

## Detection Checklist

Strong signals:

- Spring Boot 3 appears in a parent, dependency management, property, or plugin.
- `spring-boot-starter-webflux` is present.
- Java 17 or newer is configured, or Spring Boot 3 implies Java 17+.
- Source tree contains an application entrypoint, controllers/handlers/routers, services, clients, or reactive pipelines.

Supporting signals:

- Reactor types such as `Mono`, `Flux`, `Scheduler`, `WebClient`.
- `application.yml`, `application.yaml`, or profile-specific config under `src/main/resources`.
- Tests using JUnit 5, Mockito, Spring Boot Test, WebTestClient, StepVerifier, or Reactor test.

## Files To Inspect

```text
pom.xml
src/main/java/
src/main/resources/application*.yml
src/main/resources/application*.yaml
src/test/java/
src/test/resources/
Dockerfile
```

Read representative code only:

- The main `@SpringBootApplication` class.
- One route/controller/handler.
- One service containing reactive logic.
- One outbound client using `WebClient` or generated clients.
- One unit test and one Spring/WebFlux integration test if present.

## Template Scripts

After `springboot3-webflux` matches, use the static inspector to collect service-specific evidence without running the app:

```bash
python3 /path/to/init-project/scripts/templates/springboot3-webflux/inspect_springboot_webflux.py /path/to/project
```

The top-level inspector is intentionally only an orchestrator. Keep extraction
logic split by technology point under
`scripts/templates/springboot3-webflux/inspectors/`:

```text
inspectors/
  java_summary.py   # application classes, package roots, WebFlux/reactive clues
  endpoint.py       # HTTP mappings and handler signatures
  service.py        # @Service classes, public methods, constructor collaborators
  persistence.py    # Spring Data repositories, JPA entities/tables, migrations
  config.py         # application*.yml profiles, env vars, topic hints
  pubsub.py         # Pub/Sub publishers, gateways, adapters
  tests.py          # WebTestClient, StepVerifier, Mockito, Spring test clues
```

When adding new Spring backend extraction, add a focused inspector module for
that concern instead of growing `inspect_springboot_webflux.py`. Examples:
`security.py`, `scheduler.py`, `r2dbc.py`, `kafka.py`, or `openapi.py`.

It emits JSON for application classes, controllers/handlers, WebClient usage,
Reactor sources, configuration/property classes, WebFlux tests, package roots,
application config files, profile names, environment variable placeholders,
HTTP endpoint mappings, services and constructor collaborators, Spring Data
repositories, JPA/Hibernate entities and tables, Flyway migrations, Pub/Sub
classes/topic hints, and test catalogs. Use this output to refine
`AGENTS.md`, `agents/technical.md`, focused `agents/technical/*.md` cards, and
focused `agents/business/*.md` cards.

For backend projects that need reusable context, create a compact
reference-first layout:

```text
AGENTS.md
agents/technical.md
agents/technical/
  endpoints.md
  services.md
  persistence.md
  clients.md
  pubsub.md
  integrations.md
  testing.md
agents/business/
  *.md
```

Generate only files backed by useful project evidence. Do not create subagent
wrappers, workflow files, evidence dumps, or global architecture catalogs by
default.

## AGENTS.md Guidance

Keep root `AGENTS.md` to one-sentence project positioning and `Where To Look`.
Put working rules, commands, coding standards, and verification detail in
`agents/technical.md`.

```markdown
## Project
- Spring Boot 3 WebFlux service using Java [version], Maven, [persistence], and [integrations].

## Where To Look

| Task | Start Here | Notes |
| --- | --- | --- |
| Technical change, review, build, or test | `agents/technical.md` | Directory page with commands, coding standards, and focused technical links. |
| Analyze business logic | `agents/business/` | Read only the relevant domain card before changing semantics. |
```

## agents/technical.md Content

Use `agents/technical.md` as the technical directory page and common technical
rules page. It should link to focused technical cards and include:

- Build, test, checkstyle, local run, and low-context Maven log commands.
- Direct Checkstyle command, usually `mvn -B -ntp checkstyle:check`.
- Checkstyle config/report paths when present.
- Coding standards inferred from nearby code.
- Java, Spring, WebFlux/Reactor, DTO, exception, logging, and test conventions.
- Generated-output and local-log paths that agents must not commit.

Add service commands when supported by the repo:

```bash
./mvnw spring-boot:run
./mvnw test
./mvnw -Dtest=SomeWebFluxTest test
./mvnw checkstyle:check
./mvnw test jacoco:report
```

If integration tests require external services, profiles, Docker Compose, or Testcontainers, document the safe quick command separately from the full CI command.

## Focused Technical Card Content

Capture only the relevant facts in focused cards under `agents/technical/`:

- Application entrypoint.
- Main packages and layer/package organization.
- Configuration files and profile strategy.
- Important external integrations: databases, message brokers, HTTP clients, auth, service discovery.
- Runtime assumptions: ports, profiles, required env vars.
- Endpoint, service, persistence, client, Pub/Sub, and testing source areas.
- Business cards to read when code behavior encodes domain semantics.
- A `Best Practices` section with a compact code, config, SQL, shell, or test
  demo that matches the local project style.

For `agents/technical/endpoints.md`, organize content by individual API when
the project exposes HTTP endpoints. Use one section per interface, for example
`### POST /api/orders`, and include:

- API method and path.
- Documentation address when available, such as SpringDoc Swagger UI and
  OpenAPI JSON paths.
- Owning endpoint/controller/router class and method.
- Request POJO, response POJO, status code, and important response headers.
- A structured validation table per API covering body, path variable, query
  parameter, and header validations.
- Error/status mapping and endpoint tests that cover the route.
- State explicitly when no `@RequestHeader` or header validation is present.

For `agents/technical/clients.md`, organize content by individual downstream
API when the project has outbound HTTP clients. Use one section per downstream
interface, for example `### POST /v1/payments/authorizations`, and include:

- Host/base URL config key and default host when available.
- Owning client class and method.
- HTTP method and downstream path.
- Request POJO, response POJO, request headers, and response handling.
- A structured validation table covering body, path variable, query parameter,
  and header requirements.
- Timeout/retry/error mapping when present; write "not configured" when absent.
- Tests that cover host, path, method, serialization, or error handling.

Default strategy:

- Narrow technical task: read `AGENTS.md`, `agents/technical.md`, one focused
  technical card, then inspect the relevant source files.
- Business-semantic task: read `AGENTS.md`, the relevant business card, and
  `agents/technical.md` only when implementation details are needed.
- Broad or risky task: inspect `agents/technical.md`, multiple focused cards,
  and source areas before implementing. Add subagent or workflow files only
  when the user asks.

Coding standards to infer for `agents/technical.md`:

- Controller/router/handler style.
- DTO and validation conventions.
- Error handling and exception mapping.
- Logging, tracing, and metrics style.
- Reactive style: `Mono`/`Flux` composition, retries, timeouts, scheduler use.
- Test naming, fixture style, assertions, mocks.

## Spring Boot Notes

- Prefer composing `Mono` and `Flux` pipelines over blocking to extract values.
- Avoid `block()`, `toFuture().get()`, `Thread.sleep`, and blocking I/O inside request handling paths.
- If legacy blocking work is unavoidable, isolate it deliberately and document the scheduler choice.
- Preserve backpressure and cancellation behavior when changing streams.
- Use existing test patterns first.
- For WebFlux endpoints, prefer `WebTestClient` when the project already uses it.
- For Reactor pipelines, prefer `StepVerifier` when present.
- Keep unit tests focused; use Spring context tests only when wiring/configuration matters.
- Spring Boot 3 uses Jakarta namespaces for many APIs.
- Java 17+ is expected unless the project proves otherwise.
- Configuration properties, validation, security, and actuator behavior should follow existing project patterns.
- Accidentally adding servlet MVC dependencies to a WebFlux service.
- Introducing blocking calls on event-loop threads.
- Treating a WebFlux + Hibernate/JPA service as fully non-blocking. If JPA is
  present, document where blocking repository work is isolated.
- Changing API serialization/deserialization without updating tests.
- Adding config that works locally but fails in CI because env vars are undocumented.
