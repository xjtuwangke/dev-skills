# Subagent Evaluation Comparison

This document compares the current playground evaluation runs for generated agent documentation, progressive references, and subagent usage.

## Summary

The tests show a clear pattern:

- For narrow analysis tasks, one agent using `AGENTS.md` and `agents/REFERENCES.md` is the most token-efficient path.
- Parallel read-only subagents cost more, but provide better independent cross-checking.
- For complex implementation tasks, the best observed pattern is one implementation worker plus one read-only explorer that produces an impact checklist.
- Subagents are not primarily a speed or token optimization. They are a risk-reduction tool for broad, ambiguous, or cross-surface work.

## Test Case 1: Impact Analysis Only

Task:

```text
Allow enterprise customers to request expedited shipping for hazardous SKUs.
```

Expected impact surface:

- Endpoint: `POST /api/retail/fulfillment/plans`
- Request model: `ShipmentPlanRequest`
- Response/model behavior: `ShipmentPlanResponse.serviceLevel`
- Service logic: `FulfillmentPlanningService`
- Type mapping: `FulfillmentMapper`, `CustomerProfileMapper`, `CatalogMapper`
- Error handling: `DomainRuleViolationException` -> 422
- Persistence: no migration unless expedited requests must be stored or audited
- Tests: `RetailDomainServicesTest`, `RetailOperationsEndpointTest`

### Scenario A: Parallel Read-Only Subagents

Method:

- Spawned endpoint, service, persistence, and test explorer agents.
- Each started with zero inherited context (`fork_context=false`).
- Each started from `AGENTS.md`, `agents/SUBAGENTS.md`, and its own `agents/subagents/*.md`.
- All agents were read-only.

Approximate cost:

- Tokens: 20.4k
- Elapsed time: 177 seconds

Effect:

- Service, persistence, and test agents identified the correct endpoint, DTO gaps, service rule, mapper impact, migration decision, and tests.
- Endpoint agent identified the correct route and API shape, but confidence was lower because it stopped too early at references instead of inspecting source.
- Parallel outputs gave useful independent cross-checks.

Weaknesses:

- About 2.7x the token cost of the reference-only run.
- More result-merging overhead.
- Specialist docs must require source inspection after reference loading.

### Scenario B: Single Agent Reference-Only

Method:

- Spawned one explorer agent.
- Explicitly forbade subagents.
- Required `AGENTS.md`, `agents/REFERENCES.md`, and focused technical/business references.

Approximate cost:

- Tokens: 7.6k
- Elapsed time: 138 seconds

Effect:

- Identified the same core endpoint, DTO, service, mapper, persistence, and test impacts.
- Produced a compact answer.
- Correctly preserved hazardous-shipping constraints as unknowns to confirm.

Weaknesses:

- No independent specialist cross-check.
- More sensitive to stale or incomplete references.

### Test Case 1 Conclusion

For narrow analysis, single-agent reference-only mode is best. Parallel subagents were more expensive without improving correctness enough to justify the cost for this specific task.

Use parallel read-only subagents when:

- The task spans many independent surfaces.
- The cost of missing one surface is high.
- The user wants review or onboarding breadth.
- The reference index may be stale and independent source inspection is useful.

## Test Case 2: Complex Implementation

Task:

```text
Add shipping priority support to order intake.
```

Business requirements:

- `POST /api/orders` accepts optional `shippingPriority` and `requestedShipDate`.
- `shippingPriority` defaults to `STANDARD`.
- Valid priorities are `STANDARD` and `EXPEDITED`.
- `EXPEDITED` orders for SKUs starting with `HAZ-` fail through `DomainRuleViolationException` and 422.
- Orders with quantity greater than 10 are accepted with `manualReviewRequired=true`.
- The orders table and `OrderEntity` store `shippingPriority`, `requestedShipDate`, and `manualReviewRequired`.
- `OrderResponse` exposes the new fields.
- `OrderEvent` exposes `shippingPriority` and `manualReviewRequired`.
- Service, endpoint, Pub/Sub, and Maven verification tests are updated.

### Scenario C: Worker Plus Read-Only Explorer

Method:

- Spawned one worker agent with zero inherited context (`fork_context=false`) to implement the full change.
- Spawned one read-only explorer with zero inherited context to independently map the expected impact surface.
- Both started from `AGENTS.md` and used `agents/REFERENCES.md` progressively.
- The main thread reviewed source and re-ran verification.

Measured goal-level cost:

- Tokens: 256,031
- Elapsed time: 595 seconds

Important note:

This cost is not comparable to Test Case 1 directly. Test Case 1 was analysis-only. Test Case 2 included code implementation, tests, Maven verification, manual review, documentation repair, and final audit.

Effect:

- Worker completed the cross-surface feature.
- Explorer accurately identified the endpoint, request/response models, entity, migration, service rule, event payload, and tests before implementation.
- Main thread independently verified the code and command results.

Verification:

```bash
mvn -Dtest=OrderServiceTest,OrderEndpointTest,GcpPubSubOrderEventPublisherTest,NoopOrderEventPublisherTest test
mvn clean verify
```

Result:

- Targeted tests passed: 16 tests.
- Full verification passed: 26 tests.
- Checkstyle: 0 violations.
- JaCoCo: coverage gate met.

Files changed by the implementation:

- `src/main/java/com/acme/skillplayground/model/ShippingPriority.java`
- `src/main/java/com/acme/skillplayground/model/CreateOrderRequest.java`
- `src/main/java/com/acme/skillplayground/model/OrderResponse.java`
- `src/main/java/com/acme/skillplayground/database/entity/OrderEntity.java`
- `src/main/java/com/acme/skillplayground/service/OrderService.java`
- `src/main/java/com/acme/skillplayground/pubsub/OrderEvent.java`
- `src/main/resources/db/migration/V3__add_order_shipping_priority.sql`
- `src/test/java/com/acme/skillplayground/service/OrderServiceTest.java`
- `src/test/java/com/acme/skillplayground/endpoint/OrderEndpointTest.java`
- `src/test/java/com/acme/skillplayground/pubsub/GcpPubSubOrderEventPublisherTest.java`

Observed strengths:

- Zero-context worker was able to complete a realistic DB/API/service/event/test change using the generated docs.
- The read-only explorer gave a high-quality acceptance checklist for main-thread review.
- The reference structure helped both agents find the right surfaces without loading every document.

Observed weaknesses:

- Business references were stale before repair. They mentioned `PENDING`, `CONFIRMED`, and `amount`, while source used `CREATED`, `ACCEPTED`, `FULFILLED`, `CANCELLED`, SKU, and quantity.
- `requestedShipDate` semantics were underspecified. The implementation treated it as nullable echo-only data.
- The Maven Runner role existed in docs, but the generic worker executed Maven directly. Tool-native wrapper behavior still needs a separate eval.

### Test Case 2 Conclusion

For complex implementation, the strongest observed pattern is:

```text
1 worker agent for implementation
1 read-only explorer for impact mapping
main agent for integration, source review, and final verification
```

This pattern is more expensive than single-agent implementation, but it reduces missed-surface risk. The explorer is especially useful because it creates an independent checklist before final review.

## Comparative Table

| Test case | Scenario | Agent pattern | Approx tokens | Approx time | Result quality | Best use |
| --- | --- | --- | ---: | ---: | --- | --- |
| Impact analysis | Parallel subagents | 4 read-only specialists | 20.4k | 177s | Broad, independent, more duplication | Wide or risky analysis |
| Impact analysis | Reference-only | 1 explorer, no subagents | 7.6k | 138s | Compact and correct for narrow scope | Focused analysis |
| Implementation | Worker + explorer | 1 worker + 1 read-only explorer | 256k goal total | 595s | Successful implementation plus independent checklist | Cross-surface code changes |

## Practical Guidance

Use no subagent when:

- The task is narrow.
- One reference file and a few source files are enough.
- The user is asking for impact analysis, not implementation.
- Token cost matters more than independent review.

Use parallel read-only subagents when:

- The task is broad or ambiguous.
- Multiple surfaces can be inspected independently.
- The user wants review confidence.
- Missing one surface would be costly.

Use worker plus read-only explorer when:

- The task requires real code changes across API, persistence, business logic, events, and tests.
- One agent can own implementation.
- Another agent can independently produce a review checklist.
- The main thread can integrate, verify, and update references afterward.

Avoid many parallel implementation workers unless:

- Write scopes are clearly disjoint.
- Merge conflicts are unlikely.
- The task can be decomposed cleanly by module or feature boundary.

## Skill Improvements Confirmed By The Tests

These evals support the following `init-project` skill rules:

- Keep `AGENTS.md` thin.
- Keep reusable project facts under `agents/references/technical/` and `agents/references/business/`.
- Keep `agents/subagents/*.md` focused on role behavior, not project facts.
- Require source inspection after loading references before giving high confidence.
- Default to reference-only mode for narrow work.
- Use subagents for broad, risky, ambiguous, or cross-surface work.
- After code-changing work, update affected references so future zero-context agents are not guided by stale business context.

