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
`PROJECT_PROFILE.md`, `PROJECT_EVIDENCE.md`, `BACKEND_SURFACES.md`,
`CALL_CHAINS.md`, `ARCHITECTURE_NOTES.md`, `BUILD_AND_TEST.md`, and
`TEMPLATE_NOTES.md`.

For backend projects that need deeper context, create reference-first docs:

```text
agents/REFERENCES.md
agents/references/technical/
agents/references/business/
agents/SUBAGENTS.md
agents/subagents/*.md
agents/workflows/BACKEND_ANALYSIS.md
.codex/agents/*.toml
.opencode/agents/*.md
.github/agents/*.agent.md
```

Keep reusable project facts in `agents/references/`. Keep role behavior in
`agents/subagents/`. Keep tool-specific permissions in thin wrappers only.

## AGENTS.md Guidance

Add these service-specific facts:

```markdown
## Project
- Primary purpose: Spring Boot 3 WebFlux service
- Template facets: maven-java, springboot3-webflux[, additional facets]

## Working Rules
- Preserve reactive flow; do not introduce blocking calls in event-loop paths.
- Add or update focused tests with behavior changes.
- Keep configuration changes explicit and document required environment variables.
```

## PROJECT_PROFILE.md Content

Capture:

- Application entrypoint.
- Main packages and layer/package organization.
- Configuration files and profile strategy.
- Important external integrations: databases, message brokers, HTTP clients, auth, service discovery.
- Runtime assumptions: ports, profiles, required env vars.

For Boot API services with enough evidence, also create
`agents/REFERENCES.md`, focused technical/business reference files,
`agents/BACKEND_SURFACES.md`, and `agents/CALL_CHAINS.md` so the root
`AGENTS.md` can stay thin while still routing future agents to endpoint,
service, persistence, Pub/Sub, migration, and business-context facts.

Default strategy:

- Narrow task: read `AGENTS.md`, `agents/REFERENCES.md`, one focused reference,
  then inspect the relevant source files.
- Broad or risky task: use `agents/workflows/BACKEND_ANALYSIS.md` and specialist
  subagents when the current tool supports them.
- Subagents cost extra context and merge work; use them for independent
  cross-surface review, not for every edit.

## BUILD_AND_TEST.md Content

Add service commands when supported by the repo:

```bash
./mvnw spring-boot:run
./mvnw test
./mvnw -Dtest=SomeWebFluxTest test
./mvnw checkstyle:check
./mvnw test jacoco:report
```

If integration tests require external services, profiles, Docker Compose, or Testcontainers, document the safe quick command separately from the full CI command.

## CODE_STYLE.md Content

Infer:

- Controller/router/handler style.
- DTO and validation conventions.
- Error handling and exception mapping.
- Logging, tracing, and metrics style.
- Reactive style: `Mono`/`Flux` composition, retries, timeouts, scheduler use.
- Test naming, fixture style, assertions, mocks.

## ARCHITECTURE_NOTES.md Content

Document the request flow:

```text
HTTP route/controller -> handler/service -> client/repository -> external dependency
```

Add project-specific notes:

- Where routes/controllers live.
- Where business logic lives.
- Where outbound clients live.
- Where configuration properties are bound.
- Where cross-cutting concerns live: filters, security, tracing, metrics, error mapping.
- Where tests should be added for each layer.

## TEMPLATE_NOTES.md Content

```markdown
# Spring Boot 3 WebFlux Agent Notes

## Reactive Guidelines
- Prefer composing `Mono` and `Flux` pipelines over blocking to extract values.
- Avoid `block()`, `toFuture().get()`, `Thread.sleep`, and blocking I/O inside request handling paths.
- If legacy blocking work is unavoidable, isolate it deliberately and document the scheduler choice.
- Preserve backpressure and cancellation behavior when changing streams.

## Testing Guidelines
- Use existing test patterns first.
- For WebFlux endpoints, prefer `WebTestClient` when the project already uses it.
- For Reactor pipelines, prefer `StepVerifier` when present.
- Keep unit tests focused; use Spring context tests only when wiring/configuration matters.

## Spring Boot 3 Notes
- Spring Boot 3 uses Jakarta namespaces for many APIs.
- Java 17+ is expected unless the project proves otherwise.
- Configuration properties, validation, security, and actuator behavior should follow existing project patterns.

## Common Risks
- Accidentally adding servlet MVC dependencies to a WebFlux service.
- Introducing blocking calls on event-loop threads.
- Treating a WebFlux + Hibernate/JPA service as fully non-blocking. If JPA is
  present, document where blocking repository work is isolated.
- Changing API serialization/deserialization without updating tests.
- Adding config that works locally but fails in CI because env vars are undocumented.
```
