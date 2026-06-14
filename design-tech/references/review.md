# Technical Design Review

Use this reference to review a technical design draft.

## Review Checklist

Check:

- Problem, goals, and non-goals are clear.
- Current state and proposed state are separated.
- Requirements include scale, reliability, security, privacy, and operational
  constraints where relevant.
- Component responsibilities and service boundaries are clear.
- APIs, events, and data models are specific enough to implement.
- Sequence/call flows and state/workflow changes are documented.
- Failure paths, retries, idempotency, and consistency are addressed.
- Migration and backwards compatibility are covered.
- Testing strategy maps to the highest risks.
- Observability, rollout, and rollback are concrete.
- Open questions are explicit.

## Output Format

```markdown
## Technical Design Review

### Summary
[Ready, risky, or incomplete.]

### Blocking Issues
| Issue | Why it matters | Suggested fix |
| --- | --- | --- |

### Suggestions
| Issue | Why it matters | Suggested fix |
| --- | --- | --- |

### Missing Decisions
- [Decision]

### Recommended Next Step
[What should happen before implementation.]
```

Use blocking issues only for gaps that could cause wrong implementation,
production risk, security/privacy issues, incompatible migrations, or review
failure.
