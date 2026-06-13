# Project Evidence

## Detection Evidence
- Root `pom.xml` exists.
- Java runner exists under `src/test/java`.
- Karate dependency: `io.karatelabs:karate-junit5`.
- Karate config: `src/test/resources/karate-config.js`.
- Feature files exist under `src/test/resources/features/`.
- Payload fixtures exist under `src/test/resources/payloads/`.

## Service Evidence
- Demo service root: `../springboot-api-skill-playground`
- Application entrypoint: `src/main/java/com/acme/skillplayground/SkillPlaygroundApplication.java`
- Default service port: `src/main/resources/application.yml` declares `server.port: 8080`.
- Order endpoints: `src/main/java/com/acme/skillplayground/endpoint/OrderEndpoint.java`
- Retail operation endpoints: `src/main/java/com/acme/skillplayground/endpoint/RetailOperationsEndpoint.java`
- Request/response DTOs: `src/main/java/com/acme/skillplayground/model/`

## AT Surface Evidence
- `order-lifecycle.feature` exercises create, get, list-by-customer, and status update for `/api/orders`.
- `retail-operations.feature` exercises customer, catalog, promotion, audit, inventory, pricing, payment, fulfillment, returns, and support endpoints under `/api/retail`.
- `error-mapping.feature` exercises domain-rule and resource-conflict problem details.

## Command Evidence
- Compile-only command: `mvn -B -ntp -DskipTests test`
- Hosted AT command: `mvn -B -ntp test -Dat.enabled=true -Ddemo.baseUrl=http://localhost:8080`
- Tag-filtered hosted AT command: `mvn -B -ntp test -Dat.enabled=true -Dkarate.tags=@smoke`
