# Trade-off Analysis

Use this reference when the user wants option comparison without a full ADR.

## Comparison Dimensions

Choose dimensions that matter for the decision:

- Complexity.
- Cost.
- Scalability.
- Reliability.
- Latency.
- Security and compliance.
- Operability.
- Vendor lock-in.
- Migration effort.
- Team familiarity.
- Time to market.
- Long-term maintainability.

## Output Format

```markdown
## Recommendation
[Recommended option and short rationale.]

## Comparison
| Dimension | Option A | Option B | Notes |
| --- | --- | --- | --- |

## Best Fit By Scenario
- Choose [A] when [...]
- Choose [B] when [...]

## Risks
- [Risk and mitigation]

## Revisit When
- [Condition that could change the decision]
```

If the user's constraints are underspecified, state assumptions before the
recommendation.
