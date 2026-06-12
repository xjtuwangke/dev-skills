# Spring Boot API Skill Playground

This is a realistic backend fixture for testing the `init-project` skill. It is intentionally small enough to read quickly, but it includes the same signals agents commonly need to discover in production services:

- Maven + Spring Boot 3.4 WebFlux.
- Hibernate/JPA with PostgreSQL and Flyway migrations.
- SpringDoc OpenAPI annotations.
- Google Cloud Pub/Sub publisher wiring.
- `dev`, `sit`, `uat`, `ppd`, and `prd` profile files.
- JUnit 5, Mockito, Reactor Test, JaCoCo, and Checkstyle.

The service uses WebFlux endpoints while wrapping blocking Hibernate repository calls in Reactor `boundedElastic`. That combination is deliberate so agent docs can capture the architectural risk instead of assuming all WebFlux persistence is reactive.

## Commands

```bash
mvn test
mvn checkstyle:check
mvn jacoco:report
mvn clean verify
```

The local `dev` profile uses PostgreSQL connection placeholders. Unit tests mock repositories and Pub/Sub, so they do not require a running database or GCP credentials.
