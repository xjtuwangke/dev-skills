# Evaluation Notes

This file records playground observations about the agent-documentation layout. It is not a product requirement.

## Scenario
Analysis task:

```text
Allow enterprise customers to request expedited shipping for hazardous SKUs.
```

Expected impact surface:
- Existing endpoint: `POST /api/retail/fulfillment/plans`
- Request model: `ShipmentPlanRequest`
- Response/model behavior: `ShipmentPlanResponse.serviceLevel`
- Service logic: `FulfillmentPlanningService`
- Type mapping: `FulfillmentMapper`, `CustomerProfileMapper`, `CatalogMapper`
- Error handling: `DomainRuleViolationException` -> 422
- Persistence: likely no migration unless expedited requests must be stored/audited
- Tests: `RetailDomainServicesTest`, `RetailOperationsEndpointTest`

## Run 1: Parallel Subagents
Method:
- Spawned endpoint, service, persistence, and test explorer agents with `fork_context=false`.
- Each agent started from `AGENTS.md`, `agents/SUBAGENTS.md`, and its own `agents/subagents/*.md`.
- Agents were read-only and did not edit files.

Rough cost from goal-level counters:
- Start tokens: 262,673
- End tokens before reference-only run: 283,074
- Approximate delta: 20.4k tokens
- Approximate elapsed goal time delta: 177 seconds

Correctness:
- Service, persistence, and test agents identified the correct endpoint, DTO gaps, service rule, mapper impact, migration decision, and tests.
- Endpoint agent identified the correct route and API shape but had lower confidence because it stopped at references and did not inspect DTO/source files.

Observed strengths:
- Parallel agents produced independent cross-checks and caught complementary details.
- Persistence agent correctly distinguished implemented JPA surfaces from schema-only V2 tables.
- Test agent produced useful focused Maven commands.

Observed weaknesses:
- More total token use than the reference-only run for this narrow task.
- Specialist docs must explicitly require source inspection after references; otherwise a specialist can stop too early.
- Cross-domain tasks may need a coordinator summary to deduplicate repeated unknowns.

## Run 2: Reference-Only
Method:
- Spawned one explorer with `fork_context=false`.
- Explicitly forbade subagents.
- Required use of `AGENTS.md`, `agents/REFERENCES.md`, and focused technical/business references.

Rough cost from goal-level counters:
- Start tokens: 283,074
- End tokens: 290,638
- Approximate delta: 7.6k tokens
- Approximate elapsed goal time delta: 138 seconds

Correctness:
- Identified the same core endpoint, DTO, service, mapper, persistence, and test impacts.
- Produced a more compact answer for this single focused change request.
- Correctly preserved the western-region hazardous shipping rule as an unknown/constraint.

Observed strengths:
- Best token efficiency for a single, well-scoped cross-domain analysis.
- `agents/REFERENCES.md` gave enough progressive disclosure to locate relevant source quickly.

Observed weaknesses:
- No independent specialist cross-checks.
- Easier for one agent to miss a surface if the reference index is stale.

## Architecture Takeaways
- Keep `AGENTS.md` thin.
- Keep reusable context in `agents/references/technical` and `agents/references/business`.
- Keep `agents/subagents/*.md` as role/permission/workflow prompts, not as the main source of project facts.
- Use subagents when the task is broad, ambiguous, or needs parallel specialist review.
- Use reference-only mode for narrow analysis where one agent can follow the reference index cheaply.

## Follow-Up Improvements
- Add a coordinator output template that explicitly merges endpoint/service/persistence/test findings.
- Add source-inspection requirements to every specialist role.
- Consider splitting `technical/services.md` into `services-core.md` and `services-retail-operations.md` if service count grows further.
- Consider adding `agents/references/business/fulfillment-rules.md` if fulfillment behavior becomes richer.
- Consider adding JPA entities/repositories for selected V2 tables when the fixture needs deeper persistence realism.

## Scenario 2
Implementation task:

```text
Add shipping priority support to order intake.
```

Expected impact surface:
- Existing endpoint: `POST /api/orders`
- Request model: `CreateOrderRequest`
- Response model: `OrderResponse`
- Persistence: `orders` table, `OrderEntity`, new Flyway migration
- Business logic: `OrderService#create`
- Error handling: `DomainRuleViolationException` -> 422
- Pub/Sub contract: `OrderEvent`
- Tests: `OrderServiceTest`, `OrderEndpointTest`, `GcpPubSubOrderEventPublisherTest`, `NoopOrderEventPublisherTest`

Business requirements:
- `shippingPriority` is optional and defaults to `STANDARD`.
- Valid priorities are `STANDARD` and `EXPEDITED`.
- `requestedShipDate` is optional and is echoed in the API response.
- `EXPEDITED` orders for SKUs starting with `HAZ-` fail with 422.
- Quantity greater than 10 is accepted with `manualReviewRequired=true`.
- Order events include `shippingPriority` and `manualReviewRequired`.

## Run 3: Zero-Context Worker Plus Read-Only Explorer
Method:
- Spawned one worker agent with `fork_context=false` to implement the full change.
- Spawned one explorer agent with `fork_context=false` to independently map the expected impact surface.
- Both were instructed to start from `AGENTS.md`, use `agents/REFERENCES.md` progressively, and avoid web search or new analyzers.

Correctness:
- Explorer accurately identified the endpoint, request/response models, entity, migration, service rule, event payload, and tests before implementation.
- Worker implemented the full cross-surface change and reported the docs loaded first.
- Main thread independently inspected source and re-ran verification.

Verification:
- Targeted command passed: `mvn -Dtest=OrderServiceTest,OrderEndpointTest,GcpPubSubOrderEventPublisherTest,NoopOrderEventPublisherTest test`
- Full command passed: `mvn clean verify`
- Full gate result: 26 tests, Checkstyle clean, JaCoCo coverage check met.

Observed strengths:
- Zero-context worker was able to make a realistic DB/API/service/event/test change using the generated docs.
- The reference index gave both agents enough navigation to find the relevant surfaces quickly.
- The read-only explorer provided a useful independent checklist before final review.

Observed weaknesses:
- Business references were stale: they mentioned `PENDING`/`CONFIRMED` and `amount`, while source used `CREATED`/`ACCEPTED`/`FULFILLED`/`CANCELLED`, SKU, and quantity.
- `requestedShipDate` semantics were underspecified; worker treated it as nullable echo-only data.
- The Maven Runner role existed in docs, but the worker executed Maven directly because the eval used a generic worker rather than tool-native project subagent wrappers.

Follow-up improvements from this run:
- Keep business references explicit about confirmed source evidence versus product policy.
- After code-changing evals, update affected references so future zero-context agents are not guided by stale business language.
- For tool-native subagent evals, test the wrapper path separately from generic worker delegation.
