# Technical Design Document

Use this reference for end-to-end technical design.

## Inputs To Gather

Ask only for missing information that would change the design materially.

- Problem statement and desired outcome.
- Users, clients, or systems affected.
- Functional requirements.
- Non-functional requirements: scale, latency, availability, security,
  compliance, cost, and observability.
- Existing system context.
- Constraints: timeline, team ownership, existing stack, compatibility,
  migration limits, and release process.

## Output Format

```markdown
# Technical Design: [Title]

## Summary
[One-paragraph overview of the proposed change.]

## Problem
[What problem this solves and why it matters.]

## Goals
- [Goal]

## Non-Goals
- [Explicitly out of scope]

## Current State
[Relevant existing architecture, behavior, data, APIs, and pain points.]

## Proposed Design
[High-level approach and main components.]

## System Architecture
[Components, service boundaries, storage, queues, integrations.]

## Behavior And Flows
[Request flow, sequence diagram, state transitions, workflow, failure paths.]

## API And Data Model
[Endpoints, events, schemas, database changes, compatibility notes.]

## Implementation Plan
1. [Step]

## Migration And Compatibility
[Data migration, backfill, dual writes, versioning, backwards compatibility.]

## Testing Strategy
[Unit, integration, contract, migration, load, and end-to-end tests.]

## Observability
[Logs, metrics, traces, dashboards, alerts.]

## Rollout And Rollback
[Feature flags, phased rollout, validation, rollback steps.]

## Risks And Mitigations
| Risk | Mitigation |
| --- | --- |

## Open Questions
- [Question]
```

## Quality Bar

A good technical design lets reviewers understand:

- What will change.
- Why this approach fits the constraints.
- How the design behaves in normal and failure cases.
- How it will be implemented, tested, released, and rolled back.
- What remains uncertain.
