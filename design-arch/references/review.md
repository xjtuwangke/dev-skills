# Architecture Review

Use this reference to review an existing architecture proposal or ADR draft.

## Review Checklist

Check for:

- Clear problem statement and decision scope.
- Explicit constraints and non-functional requirements.
- Real alternatives, not just a preferred option.
- Trade-off analysis tied to the constraints.
- Security, privacy, compliance, and operational impact.
- Migration and compatibility concerns.
- Failure modes and rollback implications.
- Ownership, action items, and open questions.

## Output Format

```markdown
## Architecture Review

### Summary
[One paragraph on whether the decision is ready, risky, or incomplete.]

### Blocking Issues
| Issue | Why it matters | Suggested fix |
| --- | --- | --- |

### Non-Blocking Suggestions
| Issue | Why it matters | Suggested fix |
| --- | --- | --- |

### Missing Context
- [Question or missing evidence]

### Decision Readiness
Ready / Ready with changes / Not ready
```

Use "Blocking Issues" only for gaps that could lead to the wrong decision or a
material production, security, cost, or migration problem.
