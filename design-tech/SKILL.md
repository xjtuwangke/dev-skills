---
name: design-tech
description: Create, review, or refine technical design documents for systems, services, features, APIs, workflows, and implementation plans. Use this skill whenever the user asks for a tech design, system design, service design, API design, data model, sequence diagram, call flow, state machine, workflow, migration plan, rollout plan, or technical proposal that explains how a change or system should be built and verified.
---

# Design Tech

Create technical design documents that explain how a system, service, feature,
or change should work and how it should be implemented safely. This skill covers
system structure, behavior, data, APIs, workflows, operational concerns,
implementation plan, testing, and rollout.

Keep this file as the router. Load only the references needed for the request.

## Route The Request

| Scenario | User intent | Read next |
| --- | --- | --- |
| Full tech design | Design a feature, service, migration, or system end-to-end | `references/tech-design.md` |
| System structure | Components, service boundaries, API/data/storage choices | `references/system-design.md` |
| Behavior and flow | Sequence diagrams, call flows, workflows, state transitions | `references/flows.md` |
| Implementation planning | Code changes, migration, rollout, rollback, task breakdown | `references/implementation.md` |
| Review | Evaluate a draft tech design or system proposal | `references/review.md` |

If the user is asking to choose between architecture options and record why,
use `design-arch` for the ADR. If the user asks for diagrams only, pair this
skill with a diagram-focused skill when available.

## Core Principles

- Start with the problem, goals, non-goals, and constraints.
- Separate current state from proposed state.
- Make assumptions explicit and mark open questions.
- Include behavior, not only boxes. Call flows, state transitions, and failure
  paths are often the most useful part of a technical design.
- Tie implementation, testing, rollout, and observability back to the design
  risks.
- Prefer concrete interfaces, data shapes, and migration steps over abstract
  prose.

## Default Output

Produce a structured technical design document. Include diagrams as Mermaid,
ASCII, or described diagrams when helpful and supported by the output medium.
