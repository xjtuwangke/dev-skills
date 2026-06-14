# Mermaid Architecture And C4 Diagrams

Use architecture and C4 diagrams for system structure, service boundaries, external dependencies, container/component views, and technical design documents.

## Choose A View

| View | Use when | Mermaid type |
| --- | --- | --- |
| System context | Show users, external systems, and the system under discussion | `C4Context` |
| Container | Show deployable apps, services, databases, queues, and clients | `C4Container` |
| Component | Show internals of one container or service | `C4Component` |
| Infrastructure or cloud layout | Show resources and network-ish connections | `architecture-beta` or `flowchart` |
| Simple box diagram | Need broad compatibility and predictable rendering | `flowchart LR` with subgraphs |

When in doubt, start with a C4 context or container view, then add a sequence diagram for the most important runtime flow.

## C4 Context

```mermaid
C4Context
    title System Context - Order Platform

    Person(customer, "Customer", "Places and tracks orders")
    System(orderPlatform, "Order Platform", "Handles order capture and fulfillment")
    System_Ext(payment, "Payment Provider", "Authorizes card payments")
    System_Ext(email, "Email Service", "Sends order notifications")

    Rel(customer, orderPlatform, "Uses")
    Rel(orderPlatform, payment, "Authorizes payments via", "HTTPS")
    Rel(orderPlatform, email, "Sends notifications via", "API")
```

## C4 Container

```mermaid
C4Container
    title Container View - Order Platform

    Person(customer, "Customer", "Places orders")
    System_Boundary(platform, "Order Platform") {
        Container(web, "Web App", "React", "Customer-facing checkout UI")
        Container(api, "Order API", "Spring Boot", "Order commands and queries")
        Container(worker, "Fulfillment Worker", "Java", "Processes order events")
        ContainerDb(db, "Orders DB", "PostgreSQL", "Stores orders and payments")
        ContainerQueue(queue, "Order Events", "Kafka", "Publishes order lifecycle events")
    }
    System_Ext(payment, "Payment Provider", "Payment authorization")

    Rel(customer, web, "Uses")
    Rel(web, api, "Calls", "HTTPS/JSON")
    Rel(api, db, "Reads/writes")
    Rel(api, payment, "Authorizes", "HTTPS")
    Rel(api, queue, "Publishes")
    Rel(worker, queue, "Consumes")
    Rel(worker, db, "Updates fulfillment state")
```

## Simple Box Diagram With Flowchart

Use this when the target renderer does not support C4 Mermaid diagrams.

```mermaid
flowchart LR
    User[Customer]

    subgraph Platform[Order Platform]
        Web[Web App]
        API[Order API]
        DB[(Orders DB)]
        Queue[(Order Events)]
        Worker[Fulfillment Worker]
    end

    Payment[Payment Provider]

    User --> Web
    Web --> API
    API --> DB
    API --> Payment
    API --> Queue
    Queue --> Worker
    Worker --> DB
```

## Architecture-Beta

Mermaid `architecture-beta` can produce architecture-looking layouts, but support may vary by renderer version. Prefer C4 or flowchart when GitHub compatibility matters.

```mermaid
architecture-beta
    group platform(cloud)[Order Platform]
    service web(internet)[Web App] in platform
    service api(server)[Order API] in platform
    service db(database)[Orders DB] in platform
    service payment(cloud)[Payment Provider]

    web:R --> L:api
    api:B --> T:db
    api:R --> L:payment
```

## Design Guidance

- Name boundaries after ownership or deployable systems.
- Label protocols and technologies only when they help reviewers make decisions.
- Keep context views free of implementation details.
- Keep component views scoped to one container or service.
- Use prose for non-visual details such as SLOs, scaling rules, data retention, and security controls.

## Pitfalls

- Do not mix context, container, and component detail in one view.
- Do not include every dependency if it distracts from the design decision.
- Check whether the target Markdown renderer supports C4 or `architecture-beta`; fall back to flowchart when compatibility matters.

