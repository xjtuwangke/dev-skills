# Project Profile

## Identity
- Root: `/Volumes/External/work/dev-skills/playground/springboot-api-skill-playground`
- Coordinates: `com.acme.skillplayground:springboot-api-skill-playground:0.1.0-SNAPSHOT`
- Primary purpose: springboot3-webflux-service
- Template facets: baseline, maven-java, springboot3-webflux

## Structure
- Maven modules: None detected
- Maven plugins: `org.apache.maven.plugins:maven-checkstyle-plugin:3.6.0`, `org.jacoco:jacoco-maven-plugin:0.8.13`, `org.springframework.boot:spring-boot-maven-plugin`

## Source And Test Roots
- `src/main/java`
- `src/test/java`
- `src/test/resources`

## Configuration Files
- `src/main/resources/application-dev.yml`
- `src/main/resources/application-ppd.yml`
- `src/main/resources/application-prd.yml`
- `src/main/resources/application-sit.yml`
- `src/main/resources/application-uat.yml`
- `src/main/resources/application.yml`

## Spring Boot WebFlux Evidence
- Application classes: `src/main/java/com/acme/skillplayground/SkillPlaygroundApplication.java`
- Package roots: `com.acme.skillplayground`
- Profiles: `dev`, `ppd`, `prd`, `sit`, `uat`
- Environment variables referenced: `PPD_DB_HOST`, `PPD_DB_PASSWORD`, `PPD_DB_USER`, `PPD_GCP_PROJECT`, `PRD_DB_HOST`, `PRD_DB_PASSWORD`, `PRD_DB_USER`, `PRD_GCP_PROJECT`, `SIT_DB_HOST`, `SIT_DB_PASSWORD`, `SIT_DB_USER`, `SIT_GCP_PROJECT`, `UAT_DB_HOST`, `UAT_DB_PASSWORD`, `UAT_DB_USER`, `UAT_GCP_PROJECT`
- Domain areas: customer, catalog, inventory, pricing, promotion, order, payment, fulfillment, returns, support, audit
- Endpoint count: 14
- Service class count: 11
- Mapper count: 4
- Repository count: 1
- Entity count: 1
- Flyway migration count: 3
- Database table count: 37
- Flyway migrations: `src/main/resources/db/migration/V1__create_orders.sql`, `src/main/resources/db/migration/V2__retail_platform_schema.sql`, `src/main/resources/db/migration/V3__add_order_shipping_priority.sql`
- New complexity fixtures: cross-domain retail operations endpoint, manual type mappers, domain-rule errors, conflict errors, 30+ table Postgres schema, expanded JUnit 5/WebTestClient/StepVerifier tests

## Detection Evidence
```json
{
  "baseline": [
    "baseline applies to every project"
  ],
  "maven-java": [
    "pom.xml found",
    "55 Java files found",
    "Java version property: 21"
  ],
  "springboot3-webflux": [
    "Spring Boot 3 parent found",
    "spring-boot-starter-webflux dependency found",
    "Project Reactor dependency found",
    "application*.yml/yaml config found"
  ]
}
```

## Notes
- Facts in this file were generated from repository inspection and should be corrected when project-specific knowledge is available.
- Mark uncertain runtime assumptions as "Needs confirmation" instead of guessing.
