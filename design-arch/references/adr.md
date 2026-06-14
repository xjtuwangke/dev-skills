# ADR Creation

Use this reference to create an Architecture Decision Record.

## Inputs To Gather

Capture these before writing the decision. Ask only for missing details that
would materially change the recommendation.

- Decision to make.
- Options under consideration.
- Business or product goals.
- Functional requirements.
- Non-functional requirements: scale, latency, availability, cost, security,
  compliance, maintainability, and observability.
- Constraints: timeline, team skills, existing platform, vendor commitments,
  migration boundaries, and operational ownership.
- Deciders and stakeholders when known.

## ADR Format

```markdown
# ADR-[number]: [Decision title]

**Status:** Proposed | Accepted | Deprecated | Superseded
**Date:** YYYY-MM-DD
**Deciders:** [People or team]

## Context
[Situation, goals, constraints, and forces at play.]

## Decision
[The chosen option and the concise reason it fits best.]

## Options Considered

### Option A: [Name]
| Dimension | Assessment |
| --- | --- |
| Complexity | Low / Medium / High |
| Cost | [Assessment] |
| Scalability | [Assessment] |
| Reliability | [Assessment] |
| Security / compliance | [Assessment] |
| Team familiarity | [Assessment] |
| Time to deliver | [Assessment] |

**Pros**
- [Benefit]

**Cons**
- [Cost or risk]

### Option B: [Name]
[Use the same structure.]

## Trade-off Analysis
[Explain why the chosen option wins under the stated constraints. Note where
another option would be better under different constraints.]

## Consequences
- [What becomes easier]
- [What becomes harder]
- [Operational or migration impact]
- [What should be revisited later]

## Risks And Mitigations
| Risk | Mitigation |
| --- | --- |
| [Risk] | [Mitigation] |

## Action Items
1. [ ] [Implementation or follow-up step]

## Open Questions
- [Question that needs follow-up]
```

## Quality Bar

An ADR is good when a future reader can understand:

- Why the decision was needed.
- Which options were seriously considered.
- Why the chosen option won.
- What costs and risks the team accepted.
- When the decision should be revisited.

Avoid restating generic pros and cons without tying them to the user's
constraints.
