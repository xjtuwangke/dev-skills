# Code Style

## General
- Follow the nearest existing package/module style.
- Prefer existing helpers and test utilities over new abstractions.
- Keep naming, assertions, logging, and error handling consistent with nearby code.
- Avoid broad formatting-only churn unless the project formatter requires it.

## Checkstyle
- Maven Checkstyle plugin detected: True.
- Config files: `config/checkstyle/checkstyle.xml`.
- Rule hints: locals that can be final should be final (`config/checkstyle/checkstyle.xml`), method parameters should be final (`config/checkstyle/checkstyle.xml`), source files require a license/copyright header (`config/checkstyle/checkstyle.xml`), wildcard imports are banned (`config/checkstyle/checkstyle.xml`).
- Run: `mvn checkstyle:check`.

## Spring Boot WebFlux
- Preserve reactive composition with `Mono` and `Flux`.
- Avoid blocking calls in request handling paths. If the project uses Hibernate/JPA, keep blocking repository work isolated and documented.
- Follow existing controller/router/handler, DTO, validation, and exception mapping style.
