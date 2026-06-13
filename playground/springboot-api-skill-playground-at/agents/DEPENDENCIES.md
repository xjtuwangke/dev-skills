# Dependencies

## Maven Project
- Coordinates: `com.acme.skillplayground:springboot-api-skill-playground-at:0.1.0-SNAPSHOT`
- Java release: 17
- Maven wrapper: absent; use `mvn`

## Direct Dependencies
- `io.karatelabs:karate-junit5:${karate.version}` with test scope.
- `org.junit.jupiter:junit-jupiter-api:${junit.jupiter.version}` with test scope.
- `org.junit.jupiter:junit-jupiter-engine:${junit.jupiter.version}` with test scope.

## Plugins
- `maven-compiler-plugin` compiles with release 17.
- `maven-surefire-plugin` includes `**/*Runner.java` and passes `at.enabled`, `demo.baseUrl`, and `karate.tags` to the test JVM.

## Dependency Guidance
- Prefer keeping this project dependency-light; Karate should own HTTP test execution.
- Do not add a dependency on the demo service artifact unless the AT suite intentionally stops being black-box.
- If upgrading Karate, run compile-only Maven first, then hosted smoke tests against a running service.
