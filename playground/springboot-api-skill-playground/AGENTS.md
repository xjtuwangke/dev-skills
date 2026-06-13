# AGENTS.md

## Project
**Project:** `springboot-api-skill-playground`
**Stack:** Java 21, Spring Boot 3.4 (WebFlux), Maven, PostgreSQL, Flyway
**Business:** Order intake and retail operations API fixture for creating/querying orders, checking customer/pricing/fulfillment/payment/returns rules, publishing order events, and calling downstream services.

## STRUCTURE

```text
.
├── pom.xml                              # Maven build with Checkstyle + JaCoCo
├── config/checkstyle/                   # Checkstyle rules + license header
├── src/main/java/com/acme/skillplayground/
│   ├── SkillPlaygroundApplication.java  # Entry point
│   ├── client/                          # WebClient downstream clients + DTOs
│   ├── config/                          # Properties beans
│   ├── database/                        # JPA entities + repositories
│   ├── endpoint/                        # REST controllers (WebFlux)
│   ├── exception/                       # Custom exceptions + handler
│   ├── mapper/                          # Entity-to-DTO mapping
│   ├── model/                           # Request/response DTOs (records)
│   ├── pubsub/                          # GCP Pub/Sub abstraction
│   └── service/                         # Business logic + use-case interfaces
├── src/main/resources/
│   ├── application.yml                  # Default config
│   ├── application-{dev,sit,uat,ppd,prd}.yml  # Environment profiles
│   └── db/migration/                    # Flyway SQL
└── src/test/java/...                    # JUnit 5 + Mockito + StepVerifier
```

## Where To Look

| Task | Start Here | Notes |
| --- | --- | --- |
| Technical change, review, build, or test | `agents/technical.md` | Directory page with common Maven, Checkstyle, coding standards, and focused technical links. |
| Analyze business logic | `agents/business/` | Read only the relevant domain card before changing semantics. |
