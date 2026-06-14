---
name: design-arch
description: Create, review, or refine architecture decision records (ADRs) and architectural trade-off analysis. Use this skill whenever the user needs to choose between technologies or architecture options, document why an architectural decision was made, evaluate a design proposal, compare alternatives such as Kafka vs SQS or REST vs GraphQL, or record consequences, risks, and follow-up actions for an architecture decision.
---

# Design Arch

Create architecture decision records and evaluate architectural choices. This
skill focuses on decisions: which option to choose, why that option fits the
constraints, what trade-offs it accepts, and what future work follows.

Keep this file as the router. Load only the reference needed for the request.

## Route The Request

| Scenario | User intent | Read next |
| --- | --- | --- |
| Create ADR | Choose among architecture options or document a decision | `references/adr.md` |
| Review proposal | Evaluate an existing design or ADR draft | `references/review.md` |
| Compare options | Analyze trade-offs without a full ADR | `references/tradeoffs.md` |
| Find context | User mentions prior docs, tickets, or connected knowledge sources | `references/connectors.md` plus the relevant scenario reference |

If the user asks for full system behavior, API design, data modeling, sequence
diagrams, workflow/state design, implementation plan, or rollout details, use
`design-tech` instead or pair this skill with it. Use `design-arch` for the
decision record that captures a key choice inside that larger technical design.

## Core Principles

- Start from constraints: timeline, scale, cost, existing stack, team
  experience, compliance, migration risk, and operational ownership.
- Compare meaningful alternatives. If the user provides only one option, infer
  reasonable alternatives and label assumptions clearly.
- Make trade-offs explicit. Avoid presenting a choice as free of downside.
- Separate the decision from implementation detail. Capture follow-up actions,
  but do not turn the ADR into a full project plan.
- Surface uncertainty and conflicts. Mark missing information as open questions
  instead of inventing certainty.

## Default Output

Produce an ADR unless the user asks for another format.

Use concise prose, decision tables where useful, and action items that can be
converted into implementation tasks.
