# Spring Boot API Skill Playground AT

Karate acceptance tests for the demo service in `../springboot-api-skill-playground`.

The project is intentionally a separate Maven/Java 17 test repository so it can model a black-box AT suite: it talks to a running service through HTTP and does not depend on demo service source classes.

## Commands

Compile without calling the service:

```bash
mvn -B -ntp -DskipTests test
```

Run all enabled acceptance tests against a local service:

```bash
mvn -B -ntp test -Dat.enabled=true -Ddemo.baseUrl=http://localhost:8080
```

Run only smoke scenarios:

```bash
mvn -B -ntp test -Dat.enabled=true -Ddemo.baseUrl=http://localhost:8080 -Dkarate.tags=@smoke
```

Run against a named Karate environment:

```bash
mvn -B -ntp test -Dat.enabled=true -Dkarate.env=sit -Ddemo.baseUrl=https://sit.example.test
```

Reports are written under `target/karate-reports/`.

## Service Prerequisites

The target service must be started separately. The demo service defaults to port `8080` and currently uses PostgreSQL/Flyway configuration, so start it with a profile and database suitable for the environment under test before running hosted AT scenarios.
