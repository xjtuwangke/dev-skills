# Subagent Scenario Report

This report records the playground simulation for agent-friendly project documentation, subagent planning, no-subagent fallback behavior, and Maven verification.

## Scope

Goal:

```text
Simulate multiple requirement scenarios, document the requirements, simulate subagent execution behavior, run UT and API/AT verification, and compare different subagent planning schemes.
```

Constraints:

- No new inspector tools were introduced.
- No Python pattern-matching fallback was used.
- Agents used repository files, `AGENTS.md`, progressive references, source inspection, and Maven commands.
- Subagent role files stay separate from reference docs so tools without subagent support can still use progressive disclosure.

## Existing Evidence

| Run | Scenario | Pattern | Measured cost | Result |
| --- | --- | --- | --- | --- |
| Run 1 | Narrow impact analysis | 4 read-only specialists | About 20.4k tokens, 177s | Correct broad surface map, more duplicate merging |
| Run 2 | Narrow impact analysis | single reference-only explorer | About 7.6k tokens, 138s | Same core findings, cheaper |
| Run 3 | Shipping-priority implementation | worker plus read-only explorer | 256,031 goal tokens, 595s | Implementation passed targeted tests and full verify |
| Run 4 | Shipping-priority implementation replay | no subagent, reference-only main thread | 165s, token count not captured | Implementation passed targeted tests and full verify |
| Run 5 | Multi-scenario planning | 3 read-only planning specialists plus main-thread verification | Included in current goal accounting | Produced scenario matrix, planning topology, and verification plan |

Run 4 is the direct answer to the scenario 2 no-subagent request. It was successful, but it was an optimistic replay because the main thread already had prior feature context and the references had been repaired after Run 3.

## Requirement Scenario Matrix

| ID | Requirement | Main surfaces | Best default pattern | Verification |
| --- | --- | --- | --- | --- |
| S1 | Determine whether `GET /api/orders/customers/{customerId}` guarantees response ordering, and identify what changes if newest-first ordering becomes required. | `OrderEndpoint`, `OrderService`, `OrderRepository`, endpoint/service tests | No-subagent reference-only | Analysis only; if implemented: `mvn -Dtest=OrderEndpointTest,OrderServiceTest test` |
| S2 | When an order is cancelled, require a nonblank `cancellationReason`, persist it, and echo it in order responses. | PATCH API, DTO validation, service rule, entity, Flyway migration, endpoint/service tests | Worker plus read-only explorer | `mvn -Dtest=OrderEndpointTest,OrderServiceTest test`, then `mvn clean verify` |
| S3 | Add `sku`, current `status`, and `schemaVersion` to all order events without changing publish timing. | `OrderEvent`, Pub/Sub publisher, service trigger timing, publisher tests, event reference docs | Read-only specialists first, then one implementation owner | `mvn -Dtest=GcpPubSubOrderEventPublisherTest,NoopOrderEventPublisherTest,OrderServiceTest test` |
| S4 | Enable Pub/Sub only for `sit`, `uat`, `ppd`, and `prd`; keep `dev` and default local profiles no-op; make non-dev topic names env-configurable. | profile YAML, conditional Pub/Sub beans, properties binding, integration docs | Read-only specialists plus Maven runner | `mvn -Dtest=GcpPubSubOrderEventPublisherTest,NoopOrderEventPublisherTest test`, `mvn -DskipTests package` |
| S5 | Add regression coverage proving `updateStatus` on a missing order returns existing not-found behavior and does not publish an event. | service test, endpoint error test, existing service behavior | No-subagent reference-only | `mvn -Dtest=OrderServiceTest,OrderEndpointTest test` |
| S6 | Support tickets mentioning `refund` should be high priority, same as payment and chargeback; update business reference docs. | `SupportTicketService`, `RetailDomainServicesTest`, optional endpoint examples, `business/support-audit.md` | Worker plus explorer for code+docs, no-subagent if only docs/tests | `mvn -Dtest=RetailDomainServicesTest,RetailOperationsEndpointTest test` |

## Planning Scheme Comparison

| Scheme | Best use | Strengths | Weaknesses | Recommendation |
| --- | --- | --- | --- | --- |
| No-subagent reference-only | Narrow analysis, small tests, low-risk single-owner implementation | Lowest coordination cost; progressive references work in Codex, OpenCode, and Copilot Chat | No independent checklist; more sensitive to stale references | Default for focused tasks |
| Parallel read-only specialists | Broad analysis, onboarding, review, ambiguous cross-surface requirements | Independent endpoint/service/persistence/Pub/Sub/test perspectives; good missed-surface reduction | More tokens; result merging; specialists must inspect source after references | Use before risky or unclear changes |
| Worker plus read-only explorer | Cross-surface implementation that touches API, service, DB, events, and tests | One writer avoids merge churn; explorer gives acceptance checklist | Higher total tokens than single-agent; main thread still must verify | Best safety pattern for complex code changes |
| Domain-sliced multi-worker | Truly disjoint implementation slices | Can reduce wall-clock time when file ownership is separate | High merge risk in shared endpoint, service, model, migration, and test files | Avoid by default in this playground |
| Coordinator plus Maven runner | Verification-heavy tasks | Keeps build output focused; Maven runner does not edit files | Does not solve analysis or implementation by itself | Use for build/test execution after changes |

## Scenario 2 No-Subagent Result

Scenario 2 implemented shipping-priority support for order intake:

- `POST /api/orders` accepts optional `shippingPriority` and `requestedShipDate`.
- `shippingPriority` defaults to `STANDARD`.
- Valid priorities are `STANDARD` and `EXPEDITED`.
- `EXPEDITED` orders for `HAZ-` SKUs return the existing 422 domain-rule path.
- Quantity greater than 10 is accepted and sets `manualReviewRequired=true`.
- The entity, Flyway migration, response model, event payload, and focused tests were updated.

No-subagent replay method:

- Created a temporary copy of the project.
- Removed the shipping-priority implementation to recreate the pre-change state.
- Loaded `AGENTS.md`, `agents/REFERENCES.md`, focused technical references, focused business references, and then source files.
- Implemented the feature without spawning subagents.
- Ran targeted tests and full Maven verification.

Replay result:

- Baseline temp-copy targeted tests passed with 13 tests.
- Replay targeted tests passed with 16 tests.
- Replay full `mvn clean verify` passed with 26 tests.
- Checkstyle had 0 violations.
- JaCoCo coverage gate was met.
- Elapsed replay time from first doc read through full verification: 165 seconds.

Interpretation:

- No-subagent mode can complete this class of implementation when references are current and the agent already has enough project context.
- It is cheaper in coordination and wall-clock time in this replay.
- It is less robust than worker-plus-explorer when references are stale or the change has hidden surfaces such as Pub/Sub and migrations.

## Current Verification

The current playground project was verified after the scenario simulations.

| Level | Command | Result |
| --- | --- | --- |
| UT group | `mvn -Dtest=OrderServiceTest,RetailDomainServicesTest,GcpPubSubOrderEventPublisherTest,NoopOrderEventPublisherTest test` | Passed, 17 tests |
| API/AT-style group | `mvn -Dtest=OrderEndpointTest,RetailOperationsEndpointTest test` | Passed, 9 tests |
| Full gate | `mvn clean verify` | Passed, 26 tests, Checkstyle clean, JaCoCo gate met |

The endpoint tests are controller-level API contract tests using `WebTestClient` and mocked services. They are useful AT-style checks for request/response behavior, but they are not full deployed-environment acceptance tests with a real database, Pub/Sub emulator, or random-port Spring context.

## Decision Rules

1. Start with no-subagent reference-only mode when the request is narrow and the relevant files fit in one mental pass.
2. Use parallel read-only specialists when the request spans several surfaces or when a missed surface would be expensive.
3. For complex implementation, prefer one writer plus one read-only explorer. The writer owns edits; the explorer owns the impact checklist.
4. Use Maven runner only for build/test commands and concise output summaries.
5. Avoid many implementation workers unless the write sets are truly disjoint.
6. After code-changing work, update affected `agents/references/technical` and `agents/references/business` docs so future agents are not guided by stale context.

## Maven Output Protocol

Maven output should be low-context in both subagent and no-subagent modes:

- Prefer `-B -ntp` for agent-run Maven commands.
- Redirect full stdout/stderr to `target/agent-maven-logs/`.
- Return only pass/fail, test counts, first actionable failures, Checkstyle/Jacoco failures, generated report paths, and the next useful command.
- Inspect `target/surefire-reports/*.txt`, `target/checkstyle-result.xml`, and `target/site/jacoco/jacoco.xml` before reading full logs.
- Use `tail -80 target/agent-maven-logs/<name>.log` only when the concise summary is not enough.

## Skill Implications

The playground supports these `init-project` skill improvements:

- Generate a thin root `AGENTS.md`.
- Generate `agents/REFERENCES.md` as the progressive-disclosure index.
- Split reusable evidence into `agents/references/technical` and `agents/references/business`.
- Keep `agents/subagents/*.md` as role protocols, not project fact dumps.
- Generate wrappers for Codex, OpenCode, and Copilot Chat that point back to neutral role files.
- Include a Maven runner role for verification, separate from code-editing roles.
- Include no-subagent Maven log discipline in `AGENTS.md`, `BUILD_AND_TEST.md`, and `technical/maven.md`.
- Tell specialists to inspect source files after references before claiming high confidence.
- Preserve no-subagent fallback paths for tools that do not support custom subagents.

## Remaining Gaps

- Run 4 did not capture a fresh-thread token count.
- The current API/AT checks are controller-level tests, not deployed-environment AT.
- There is no real Postgres/Flyway integration test or Pub/Sub emulator test in the playground yet.
- Domain-sliced multi-worker implementation has not been executed because the current playground has many shared files where merge risk would dominate.
