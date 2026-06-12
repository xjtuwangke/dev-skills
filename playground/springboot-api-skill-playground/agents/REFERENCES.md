# References

Use these files for progressive disclosure when subagents are unavailable or unnecessary. They contain reusable context only; they are not tool-specific agent definitions.

## Technical References
| Topic | File | Use when |
| --- | --- | --- |
| Endpoints | `agents/references/technical/endpoints.md` | Changing or reviewing HTTP routes, request/response contracts, validation, or endpoint tests. |
| Services | `agents/references/technical/services.md` | Changing service orchestration, state transitions, errors, or collaborator usage. |
| Persistence | `agents/references/technical/persistence.md` | Changing JPA entities, repositories, Flyway migrations, or Postgres profile config. |
| Pub/Sub | `agents/references/technical/pubsub.md` | Changing event publication, topic config, payloads, or Pub/Sub tests. |
| Integrations | `agents/references/technical/integrations.md` | Reviewing external systems, clients, retries, timeouts, or environment-sensitive config. |
| Testing | `agents/references/technical/testing.md` | Planning or reviewing JUnit, Mockito, Reactor, WebTestClient, Checkstyle, or JaCoCo coverage. |
| Maven | `agents/references/technical/maven.md` | Choosing build/test/checkstyle/coverage commands or interpreting Maven output. |

## Business References
| Topic | File | Use when |
| --- | --- | --- |
| Order domain | `agents/references/business/order-domain.md` | Understanding order states, customer/order identifiers, totals, and expected behavior. |
| Order API use cases | `agents/references/business/order-api-use-cases.md` | Connecting endpoints to user-facing flows and acceptance criteria. |
| Order events | `agents/references/business/order-events.md` | Understanding when events publish and what consumers may depend on. |
| Customer domain | `agents/references/business/customer-domain.md` | Understanding customer segments, loyalty, addresses, and contact preferences. |
| Pricing and promotions | `agents/references/business/pricing-promotions.md` | Understanding quote, tax, coupon, and eligibility behavior. |
| Payment, fulfillment, returns | `agents/references/business/payment-fulfillment-returns.md` | Understanding authorization, shipment planning, and return decisions. |
| Support and audit | `agents/references/business/support-audit.md` | Understanding ticket priority and audit trail expectations. |

## Loading Rule
- Start with the smallest relevant technical file.
- Add business context when behavior, naming, status transitions, event meaning, or user-facing acceptance criteria matter.
- Prefer source code over generated evidence when they disagree.
