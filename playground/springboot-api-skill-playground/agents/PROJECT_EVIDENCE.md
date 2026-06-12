# Project Evidence

This file is a generated evidence snapshot for future agents. Prefer the human-oriented files first, then use this file when you need the raw signals behind a claim.

## Current Manual Refresh
- Java source files: 56
- Test source files: 6
- Endpoint classes: `OrderEndpoint`, `RetailOperationsEndpoint`
- Endpoint routes: 14
- Service classes: 11
- Mapper classes: 4
- Flyway migrations: 3
- Database tables: 37
- Domain areas: customer, catalog, inventory, pricing, promotion, order, payment, fulfillment, returns, support, audit
- Current human-maintained navigation files: `agents/BACKEND_SURFACES.md`, `agents/CALL_CHAINS.md`, `agents/REFERENCES.md`

The generated JSON below is retained as raw historical evidence for the initial fixture shape. Prefer the current manual refresh and human-maintained navigation files when they disagree.

## Detection
```json
{
  "root": "/Volumes/External/work/dev-skills/playground/springboot-api-skill-playground",
  "matched_templates": [
    "baseline",
    "maven-java",
    "springboot3-webflux"
  ],
  "primary_purpose": "springboot3-webflux-service",
  "confidence": {
    "baseline": "high",
    "maven-java": "high",
    "springboot3-webflux": "high",
    "karate-at": "none"
  },
  "scores": {
    "baseline": 10,
    "maven-java": 7,
    "springboot3-webflux": 9,
    "karate-at": 0
  },
  "signals": {
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
    ],
    "karate-at": []
  },
  "template_reference_paths": {
    "baseline": "references/templates/baseline/index.md",
    "maven-java": "references/templates/maven-java/index.md",
    "springboot3-webflux": "references/templates/springboot3-webflux/index.md"
  },
  "pom": {
    "exists": true,
    "parent": {
      "groupId": "org.springframework.boot",
      "artifactId": "spring-boot-starter-parent",
      "version": "3.4.6"
    },
    "modules": [],
    "properties": {
      "java.version": "21"
    },
    "dependency_count": 12,
    "parse_error": null
  },
  "file_counts": {
    "java": 55,
    "feature": 0,
    "application_config": 6,
    "karate_config": 0,
    "maven_wrapper": 0
  }
}
```

## Maven Inspection
```json
{
  "root": "/Volumes/External/work/dev-skills/playground/springboot-api-skill-playground",
  "is_maven_project": true,
  "maven_wrapper": {
    "present": false,
    "files": []
  },
  "pom_tree": {
    "path": "/Volumes/External/work/dev-skills/playground/springboot-api-skill-playground/pom.xml",
    "relative_path": "pom.xml",
    "modelVersion": "4.0.0",
    "coordinates": {
      "groupId": "com.acme.skillplayground",
      "artifactId": "springboot-api-skill-playground",
      "version": "0.1.0-SNAPSHOT",
      "packaging": "jar"
    },
    "name": "springboot-api-skill-playground",
    "description": "Spring Boot backend fixture for init-project skill evaluation",
    "parent": {
      "groupId": "org.springframework.boot",
      "artifactId": "spring-boot-starter-parent",
      "version": "3.4.6",
      "relativePath": null
    },
    "properties": {
      "java.version": "21",
      "spring-cloud-gcp.version": "6.5.1",
      "springdoc.version": "2.8.8",
      "checkstyle.version": "10.21.4",
      "jacoco.version": "0.8.13",
      "maven-checkstyle-plugin.version": "3.6.0"
    },
    "java_version_hint": "21",
    "modules": [],
    "dependencies": [
      {
        "groupId": "org.springframework.boot",
        "artifactId": "spring-boot-starter-webflux",
        "version": null,
        "type": null,
        "classifier": null,
        "scope": null,
        "optional": null,
        "exclusions": []
      },
      {
        "groupId": "org.springframework.boot",
        "artifactId": "spring-boot-starter-data-jpa",
        "version": null,
        "type": null,
        "classifier": null,
        "scope": null,
        "optional": null,
        "exclusions": []
      },
      {
        "groupId": "org.springframework.boot",
        "artifactId": "spring-boot-starter-validation",
        "version": null,
        "type": null,
        "classifier": null,
        "scope": null,
        "optional": null,
        "exclusions": []
      },
      {
        "groupId": "org.flywaydb",
        "artifactId": "flyway-core",
        "version": null,
        "type": null,
        "classifier": null,
        "scope": null,
        "optional": null,
        "exclusions": []
      },
      {
        "groupId": "org.flywaydb",
        "artifactId": "flyway-database-postgresql",
        "version": null,
        "type": null,
        "classifier": null,
        "scope": null,
        "optional": null,
        "exclusions": []
      },
      {
        "groupId": "org.postgresql",
        "artifactId": "postgresql",
        "version": null,
        "type": null,
        "classifier": null,
        "scope": "runtime",
        "optional": null,
        "exclusions": []
      },
      {
        "groupId": "org.springdoc",
        "artifactId": "springdoc-openapi-starter-webflux-ui",
        "version": "${springdoc.version}",
        "type": null,
        "classifier": null,
        "scope": null,
        "optional": null,
        "exclusions": []
      },
      {
        "groupId": "com.google.cloud",
        "artifactId": "spring-cloud-gcp-starter-pubsub",
        "version": null,
        "type": null,
        "classifier": null,
        "scope": null,
        "optional": null,
        "exclusions": []
      },
      {
        "groupId": "org.springframework.boot",
        "artifactId": "spring-boot-starter-test",
        "version": null,
        "type": null,
        "classifier": null,
        "scope": "test",
        "optional": null,
        "exclusions": []
      },
      {
        "groupId": "io.projectreactor",
        "artifactId": "reactor-test",
        "version": null,
        "type": null,
        "classifier": null,
        "scope": "test",
        "optional": null,
        "exclusions": []
      }
    ],
    "dependencyManagement": [
      {
        "groupId": "com.google.cloud",
        "artifactId": "spring-cloud-gcp-dependencies",
        "version": "${spring-cloud-gcp.version}",
        "type": "pom",
        "classifier": null,
        "scope": "import",
        "optional": null,
        "exclusions": []
      }
    ],
    "plugins": {
      "plugins": [
        {
          "groupId": "org.springframework.boot",
          "artifactId": "spring-boot-maven-plugin",
          "version": null,
          "executions": []
        },
        {
          "groupId": "org.apache.maven.plugins",
          "artifactId": "maven-checkstyle-plugin",
          "version": "${maven-checkstyle-plugin.version}",
          "executions": [
            {
              "id": "checkstyle",
              "phase": "validate",
              "goals": [
                "check"
              ]
            }
          ]
        },
        {
          "groupId": "org.jacoco",
          "artifactId": "jacoco-maven-plugin",
          "version": "${jacoco.version}",
          "executions": [
            {
              "id": "prepare-agent",
              "phase": null,
              "goals": [
                "prepare-agent"
              ]
            },
            {
              "id": "report",
              "phase": "test",
              "goals": [
                "report"
              ]
            },
            {
              "id": "coverage-check",
              "phase": "verify",
              "goals": [
                "check"
              ]
            }
          ]
        }
      ],
      "pluginManagement": []
    },
    "profiles": [],
    "module_details": []
  }
}
```

## Spring Boot WebFlux Inspection
```json
{
  "root": "/Volumes/External/work/dev-skills/playground/springboot-api-skill-playground",
  "application_classes": [
    "src/main/java/com/acme/skillplayground/SkillPlaygroundApplication.java"
  ],
  "controllers_or_handlers": [
    "src/main/java/com/acme/skillplayground/endpoint/OrderEndpoint.java",
    "src/main/java/com/acme/skillplayground/exception/ApiExceptionHandler.java"
  ],
  "web_clients": [],
  "reactive_sources": [
    "src/main/java/com/acme/skillplayground/endpoint/OrderEndpoint.java",
    "src/main/java/com/acme/skillplayground/pubsub/GcpPubSubOrderEventPublisher.java",
    "src/main/java/com/acme/skillplayground/pubsub/NoopOrderEventPublisher.java",
    "src/main/java/com/acme/skillplayground/pubsub/OrderEventPublisher.java",
    "src/main/java/com/acme/skillplayground/service/OrderService.java",
    "src/main/java/com/acme/skillplayground/service/OrderUseCase.java",
    "src/test/java/com/acme/skillplayground/endpoint/OrderEndpointTest.java",
    "src/test/java/com/acme/skillplayground/service/OrderServiceTest.java"
  ],
  "configuration_properties": [
    "src/main/java/com/acme/skillplayground/SkillPlaygroundApplication.java",
    "src/main/java/com/acme/skillplayground/config/OrderProperties.java"
  ],
  "package_roots": [
    "com.acme.skillplayground"
  ],
  "application_configs": [
    "src/main/resources/application-dev.yml",
    "src/main/resources/application-ppd.yml",
    "src/main/resources/application-prd.yml",
    "src/main/resources/application-sit.yml",
    "src/main/resources/application-uat.yml",
    "src/main/resources/application.yml"
  ],
  "profiles": [
    "dev",
    "ppd",
    "prd",
    "sit",
    "uat"
  ],
  "environment_variables": [
    "PPD_DB_HOST",
    "PPD_DB_PASSWORD",
    "PPD_DB_USER",
    "PPD_GCP_PROJECT",
    "PRD_DB_HOST",
    "PRD_DB_PASSWORD",
    "PRD_DB_USER",
    "PRD_GCP_PROJECT",
    "SIT_DB_HOST",
    "SIT_DB_PASSWORD",
    "SIT_DB_USER",
    "SIT_GCP_PROJECT",
    "UAT_DB_HOST",
    "UAT_DB_PASSWORD",
    "UAT_DB_USER",
    "UAT_GCP_PROJECT"
  ],
  "pubsub_topic_hints": [
    {
      "source": "src/main/resources/application-dev.yml",
      "line": "created-topic: orders.created.dev"
    },
    {
      "source": "src/main/resources/application-dev.yml",
      "line": "status-changed-topic: orders.status-changed.dev"
    },
    {
      "source": "src/main/resources/application-ppd.yml",
      "line": "created-topic: orders.created.ppd"
    },
    {
      "source": "src/main/resources/application-ppd.yml",
      "line": "status-changed-topic: orders.status-changed.ppd"
    },
    {
      "source": "src/main/resources/application-prd.yml",
      "line": "created-topic: orders.created.prd"
    },
    {
      "source": "src/main/resources/application-prd.yml",
      "line": "status-changed-topic: orders.status-changed.prd"
    },
    {
      "source": "src/main/resources/application-sit.yml",
      "line": "created-topic: orders.created.sit"
    },
    {
      "source": "src/main/resources/application-sit.yml",
      "line": "status-changed-topic: orders.status-changed.sit"
    },
    {
      "source": "src/main/resources/application-uat.yml",
      "line": "created-topic: orders.created.uat"
    },
    {
      "source": "src/main/resources/application-uat.yml",
      "line": "status-changed-topic: orders.status-changed.uat"
    },
    {
      "source": "src/main/resources/application.yml",
      "line": "created-topic: orders.created.dev"
    },
    {
      "source": "src/main/resources/application.yml",
      "line": "status-changed-topic: orders.status-changed.dev"
    }
  ],
  "endpoints": [
    {
      "method": "POST",
      "path": "/api/orders",
      "handler": "OrderEndpoint#create",
      "request": "CreateOrderRequest",
      "response": "Mono<ResponseEntity<OrderResponse>>",
      "path_variables": [],
      "source": "src/main/java/com/acme/skillplayground/endpoint/OrderEndpoint.java"
    },
    {
      "method": "GET",
      "path": "/api/orders/{id}",
      "handler": "OrderEndpoint#getById",
      "request": "None detected",
      "response": "Mono<OrderResponse>",
      "path_variables": [
        "id"
      ],
      "source": "src/main/java/com/acme/skillplayground/endpoint/OrderEndpoint.java"
    },
    {
      "method": "GET",
      "path": "/api/orders/customers/{customerId}",
      "handler": "OrderEndpoint#listByCustomer",
      "request": "None detected",
      "response": "Mono<List<OrderResponse>>",
      "path_variables": [
        "customerId"
      ],
      "source": "src/main/java/com/acme/skillplayground/endpoint/OrderEndpoint.java"
    },
    {
      "method": "PATCH",
      "path": "/api/orders/{id}/status",
      "handler": "OrderEndpoint#updateStatus",
      "request": "UpdateOrderStatusRequest",
      "response": "Mono<OrderResponse>",
      "path_variables": [
        "id"
      ],
      "source": "src/main/java/com/acme/skillplayground/endpoint/OrderEndpoint.java"
    }
  ],
  "services": [
    {
      "class": "OrderService",
      "source": "src/main/java/com/acme/skillplayground/service/OrderService.java",
      "methods": [
        "create",
        "findByCustomerId",
        "findById",
        "updateStatus"
      ],
      "collaborators": [
        "OrderEventPublisher",
        "OrderRepository"
      ]
    }
  ],
  "repositories": [
    {
      "repository": "OrderRepository",
      "entity": "OrderEntity",
      "id_type": "UUID",
      "source": "src/main/java/com/acme/skillplayground/database/repository/OrderRepository.java"
    }
  ],
  "entities": [
    {
      "entity": "OrderEntity",
      "table": "orders",
      "source": "src/main/java/com/acme/skillplayground/database/entity/OrderEntity.java"
    }
  ],
  "migrations": [
    "src/main/resources/db/migration/V1__create_orders.sql"
  ],
  "pubsub": [
    {
      "class": "GcpPubSubGateway",
      "source": "src/main/java/com/acme/skillplayground/pubsub/GcpPubSubGateway.java",
      "signals": "PubSubTemplate, publisher interface/gateway, conditional pubsub bean"
    },
    {
      "class": "GcpPubSubOrderEventPublisher",
      "source": "src/main/java/com/acme/skillplayground/pubsub/GcpPubSubOrderEventPublisher.java",
      "signals": "publisher interface/gateway, conditional pubsub bean"
    },
    {
      "class": "NoopOrderEventPublisher",
      "source": "src/main/java/com/acme/skillplayground/pubsub/NoopOrderEventPublisher.java",
      "signals": "publisher interface/gateway, conditional pubsub bean"
    },
    {
      "class": "OrderEvent",
      "source": "src/main/java/com/acme/skillplayground/pubsub/OrderEvent.java",
      "signals": "package path"
    },
    {
      "class": "OrderEventPublisher",
      "source": "src/main/java/com/acme/skillplayground/pubsub/OrderEventPublisher.java",
      "signals": "publisher interface/gateway"
    },
    {
      "class": "PubSubGateway",
      "source": "src/main/java/com/acme/skillplayground/pubsub/PubSubGateway.java",
      "signals": "publisher interface/gateway"
    }
  ],
  "webflux_tests": [
    "src/test/java/com/acme/skillplayground/endpoint/OrderEndpointTest.java",
    "src/test/java/com/acme/skillplayground/pubsub/GcpPubSubOrderEventPublisherTest.java",
    "src/test/java/com/acme/skillplayground/pubsub/NoopOrderEventPublisherTest.java",
    "src/test/java/com/acme/skillplayground/service/OrderServiceTest.java"
  ],
  "tests": [
    {
      "class": "OrderEndpointTest",
      "source": "src/test/java/com/acme/skillplayground/endpoint/OrderEndpointTest.java",
      "signals": "Mockito, WebTestClient"
    },
    {
      "class": "GcpPubSubOrderEventPublisherTest",
      "source": "src/test/java/com/acme/skillplayground/pubsub/GcpPubSubOrderEventPublisherTest.java",
      "signals": "Mockito, StepVerifier"
    },
    {
      "class": "NoopOrderEventPublisherTest",
      "source": "src/test/java/com/acme/skillplayground/pubsub/NoopOrderEventPublisherTest.java",
      "signals": "StepVerifier"
    },
    {
      "class": "OrderServiceTest",
      "source": "src/test/java/com/acme/skillplayground/service/OrderServiceTest.java",
      "signals": "Mockito, StepVerifier"
    }
  ]
}
```

## Karate Inspection
```json
{}
```
