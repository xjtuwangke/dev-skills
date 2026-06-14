# Mermaid Sequence Diagrams

Use sequence diagrams when order over time matters: API calls, login flows, checkout flows, event publication, retries, callbacks, and method-level interactions.

## Basic Shape

```mermaid
sequenceDiagram
    actor User
    participant Web as Web App
    participant API as API Service
    participant DB as Database

    User->>Web: Submit login form
    Web->>API: POST /login
    API->>DB: Find user by email
    DB-->>API: User record
    API-->>Web: 200 OK + session
    Web-->>User: Show dashboard
```

Use `actor` for users or external people, and `participant` for systems, services, classes, or stores.

## Message Types

```mermaid
sequenceDiagram
    Client->>Server: Synchronous request
    Server-->>Client: Response
    Client-)Queue: Asynchronous publish
    Queue--)Worker: Deliver event
```

Prefer:

- `->>` for request/call.
- `-->>` for response/return.
- `-)` for asynchronous send.
- `--)` for asynchronous callback or event delivery.

## Control Blocks

Use control blocks to show meaningful alternatives, not every trivial branch.

```mermaid
sequenceDiagram
    User->>API: POST /orders
    API->>Payment: Authorize payment
    alt Payment approved
        Payment-->>API: Authorization id
        API->>DB: Create order
        API-->>User: 201 Created
    else Payment declined
        Payment-->>API: Decline reason
        API-->>User: 402 Payment Required
    end
```

Useful blocks:

- `alt` / `else` / `end` for alternatives.
- `opt` for optional behavior.
- `loop` for retry, polling, or batch processing.
- `par` for parallel work.

## Notes

Use notes to capture assumptions or non-obvious constraints.

```mermaid
sequenceDiagram
    participant API
    participant Cache
    API->>Cache: GET session
    Note right of Cache: TTL is 15 minutes
```

## Pitfalls

- Do not turn a sequence diagram into an architecture inventory. Only include participants that exchange messages in this flow.
- Avoid long method names and payload dumps. Use concise intent labels.
- If the same service appears in many unrelated flows, create separate diagrams per scenario.

