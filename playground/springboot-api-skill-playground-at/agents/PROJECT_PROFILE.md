# Project Profile

## Identity
- Root: `playground/springboot-api-skill-playground-at`
- Coordinates: `com.acme.skillplayground:springboot-api-skill-playground-at:0.1.0-SNAPSHOT`
- Primary purpose: acceptance tests for the demo Spring Boot API service
- Service under test: `../springboot-api-skill-playground`
- Template facets: `baseline`, `maven-java`, `karate-at`

## Structure
- Maven POM: `pom.xml`
- Java runner: `src/test/java/com/acme/skillplayground/at/DemoServiceAtRunner.java`
- Karate config: `src/test/resources/karate-config.js`
- Feature root: `src/test/resources/features/`
- Payload fixtures: `src/test/resources/payloads/`

## Suite Coverage
- Orders: `features/orders/order-lifecycle.feature`
- Retail operations: `features/retail/retail-operations.feature`
- Problem-detail error mapping: `features/errors/error-mapping.feature`

## Environment Model
- Default `demo.baseUrl`: `http://localhost:8080`
- Hosted AT execution is disabled unless `-Dat.enabled=true` is passed.
- `karate.env` can select a named environment, but the base URL still comes from `-Ddemo.baseUrl`.
- Reports are generated under `target/karate-reports/`.

## Notes
- The demo service currently uses PostgreSQL/Flyway configuration at startup. Hosted AT runs need a running service with a suitable database/profile.
- Facts in this file were inferred from the AT project files and the adjacent demo service endpoint/DTO sources.
