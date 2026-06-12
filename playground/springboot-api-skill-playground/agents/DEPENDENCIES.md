# Dependencies

## Maven Project
- Maven detected: True
- Maven wrapper: False
- Coordinates: `com.acme.skillplayground:springboot-api-skill-playground:0.1.0-SNAPSHOT`
- Java version hint: 21
- Stack hints: Spring WebFlux, Hibernate/JPA, PostgreSQL, Flyway, SpringDoc OpenAPI, GCP Pub/Sub, JUnit/Spring Boot Test, Reactor Test

## Dependency Management And BOMs
- `com.google.cloud:spring-cloud-gcp-dependencies:6.5.1 (import)`

## Direct Dependencies
- `org.springframework.boot:spring-boot-starter-webflux (compile)`
- `org.springframework.boot:spring-boot-starter-data-jpa (compile)`
- `org.springframework.boot:spring-boot-starter-validation (compile)`
- `org.flywaydb:flyway-core (compile)`
- `org.flywaydb:flyway-database-postgresql (compile)`
- `org.postgresql:postgresql (runtime)`
- `org.springdoc:springdoc-openapi-starter-webflux-ui:2.8.8 (compile)`
- `com.google.cloud:spring-cloud-gcp-starter-pubsub (compile)`
- `org.springframework.boot:spring-boot-starter-test (test)`
- `io.projectreactor:reactor-test (test)`

## Direct Dependency Exclusions
- None detected

## Maven Plugins
- `org.apache.maven.plugins:maven-checkstyle-plugin:3.6.0`
- `org.jacoco:jacoco-maven-plugin:0.8.13`
- `org.springframework.boot:spring-boot-maven-plugin`

## Dependency Tree
- Command: `python3 /path/to/init-project/scripts/templates/maven-java/generate_dependency_tree.py /path/to/project --timeout 300`
- Status: Not run by the renderer. Run the command when transitive dependency analysis matters.

## Notes For Future Changes
- Prefer existing BOM or dependency management when adding versions.
- Explain new exclusions and verify the dependency tree when changing logging, HTTP, JSON/XML, database, security, or test framework dependencies.
