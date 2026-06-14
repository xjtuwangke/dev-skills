# System Design

Use this reference for system structure, service boundaries, APIs, storage, and
scale/reliability design.

## Framework

### 1. Requirements

Capture:

- Functional requirements.
- Non-functional requirements: scale, latency, availability, durability,
  consistency, cost, security, privacy, and observability.
- Constraints: timeline, team size, existing stack, ownership, and migration
  boundaries.

### 2. High-Level Design

Describe:

- Main components and responsibilities.
- Service boundaries.
- Data flow.
- Synchronous and asynchronous paths.
- External dependencies.

### 3. Interfaces And Data

Define:

- API contracts: REST, GraphQL, gRPC, events, or batch interfaces.
- Request and response shapes.
- Data model and storage choices.
- Schema evolution and backwards compatibility.

### 4. Scale And Reliability

Cover:

- Load estimates and bottlenecks.
- Caching strategy.
- Queue/event design.
- Error handling and retry logic.
- Idempotency and deduplication.
- Failover and redundancy.
- Monitoring and alerting.

### 5. Trade-offs

Explain the trade-offs behind major choices. If the choice deserves a durable
decision record, recommend writing a `design-arch` ADR.

## Output Shape

Use sections from `references/tech-design.md` when the user needs a complete
document. For focused system design, include:

```markdown
## Requirements
## Assumptions
## High-Level Design
## Component Responsibilities
## Data Flow
## API / Event Contracts
## Data Model
## Scale And Reliability
## Trade-offs
## Open Questions
```
