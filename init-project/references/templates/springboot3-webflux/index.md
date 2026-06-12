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

It emits JSON for application classes, controllers/handlers, WebClient usage, Reactor sources, configuration/property classes, WebFlux tests, package roots, and application config files. Use this output to refine `PROJECT_PROFILE.md`, `ARCHITECTURE_NOTES.md`, `BUILD_AND_TEST.md`, and `TEMPLATE_NOTES.md`.

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

## BUILD_AND_TEST.md Content

Add service commands when supported by the repo:

```bash
./mvnw spring-boot:run
./mvnw test
./mvnw -Dtest=SomeWebFluxTest test
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
- Changing API serialization/deserialization without updating tests.
- Adding config that works locally but fails in CI because env vars are undocumented.
```
