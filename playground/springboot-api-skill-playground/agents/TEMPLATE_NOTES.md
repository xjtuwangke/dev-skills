# Template Notes

## baseline
- Keep instructions short, concrete, scoped, and project-specific.
- Verify changes with the smallest useful command and document skipped checks.
- Do not expose secrets or commit generated build output/local state.

## maven-java
- Prefer `./mvnw` when present; otherwise use `mvn`.
- Inspect root and module POMs before changing dependencies or build plugins.
- Use `agents/DEPENDENCIES.md` for dependency management, exclusions, and tree findings.

## springboot3-webflux
- Preserve non-blocking reactive flows.
- If the service combines WebFlux with Hibernate/JPA, treat repository calls as blocking work and verify how the project isolates them.
- Use existing `WebTestClient`, `StepVerifier`, Spring test, and configuration patterns.
- Spring Boot 3 implies Java 17+ and Jakarta namespaces unless the project proves otherwise.
