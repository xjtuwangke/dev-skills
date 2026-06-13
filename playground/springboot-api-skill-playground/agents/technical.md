# Technical

## Use This Page
- Start here for code changes, code review, builds, tests, Checkstyle, and local run commands.
- Then open the smallest focused card needed for the touched surface.
- For behavior semantics, also read the relevant `agents/business/*.md` card.

## Focused Cards

| Task | Read Next |
| --- | --- |
| Change endpoints or DTO contracts | `agents/technical/endpoints.md` |
| Change service behavior | `agents/technical/services.md` |
| Change persistence or migrations | `agents/technical/persistence.md` |
| Change Pub/Sub behavior | `agents/technical/pubsub.md` |
| Change downstream WebClient calls | `agents/technical/clients.md` |
| Review external runtime seams | `agents/technical/integrations.md` |
| Choose targeted tests | `agents/technical/testing.md` |

## Common Maven Commands
- Unit tests: `mvn -B -ntp test`
- Endpoint tests: `mvn -B -ntp -Dtest=OrderEndpointTest,RetailOperationsEndpointTest test`
- Service/domain tests: `mvn -B -ntp -Dtest=OrderServiceTest,RetailDomainServicesTest test`
- Pub/Sub tests: `mvn -B -ntp -Dtest=GcpPubSubOrderEventPublisherTest,NoopOrderEventPublisherTest test`
- Checkstyle: `mvn -B -ntp checkstyle:check`
- Coverage report: `mvn -B -ntp test jacoco:report`
- Full gate: `mvn -B -ntp clean verify`
- Run locally: `mvn -B -ntp spring-boot:run`
- Run with dev profile: `mvn -B -ntp spring-boot:run -Dspring-boot.run.profiles=dev`

## Checkstyle
- Config: `config/checkstyle/checkstyle.xml`
- Run directly with `mvn -B -ntp checkstyle:check`.
- Checkstyle also runs at `validate` and enforces Apache license headers, imports, and `final` style rules.
- Inspect `target/checkstyle-result.xml` when failures need detail.
- `.mvn/maven.config` already enables `--no-transfer-progress`.

## Maven Log Discipline
Do not stream full Maven logs into the agent context. Use this pattern for noisy commands:

```bash
mkdir -p target/agent-maven-logs
mvn -B -ntp clean verify > target/agent-maven-logs/clean-verify.log 2>&1
grep -E "Tests run:|BUILD SUCCESS|BUILD FAILURE|Total time|ERROR|FAILURE" target/agent-maven-logs/clean-verify.log | tail -40
```

If a command fails, inspect focused reports before opening the full log:

- `target/surefire-reports/*.txt`
- `target/checkstyle-result.xml`
- `target/site/jacoco/jacoco.xml`
- `tail -80 target/agent-maven-logs/clean-verify.log`

## Best Practices
- Use constructor injection with `final` fields.
- Prefer records for request/response payloads.
- Keep transport, business, persistence, and downstream client concerns in separate packages.
- Run targeted tests first, then `mvn -B -ntp verify` for broad confidence.

```java
@Service
public class PricingService {

    private final CatalogMapper catalogMapper;
    private final MoneyMapper moneyMapper;

    public PricingService(final CatalogMapper catalogMapper, final MoneyMapper moneyMapper) {
        this.catalogMapper = catalogMapper;
        this.moneyMapper = moneyMapper;
    }

    public Mono<PriceQuoteResponse> quote(final PriceQuoteRequest request) {
        return Mono.fromSupplier(() -> {
            final CatalogItemResponse item = catalogMapper.toCatalogItem(request.sku());
            final BigDecimal subtotal = moneyMapper.subtotal(item.listPrice(), request.quantity());
            return new PriceQuoteResponse(request.sku(), request.quantity(), subtotal, BigDecimal.ZERO,
                    BigDecimal.ZERO, subtotal, item.currency(), "LIST");
        });
    }
}
```

## Coding Standards
- Follow the nearest package style before adding abstractions.
- Keep Apache license headers on Java source files.
- Do not use wildcard imports.
- Add `final` to method parameters and local variables when Checkstyle requires it.
- Use constructor injection with `final` fields; do not add field `@Autowired`.
- DTOs and API payload models should usually be Java `record`s under `model/`.
- Put business rules in services and keep endpoints thin.
- Keep outbound HTTP/WebClient calls under `client/`; do not put downstream calls in endpoints.
- Register exception-to-problem-detail behavior in `ApiExceptionHandler`.
- Keep `spring.jpa.open-in-view: false`.
- Do not hard-code Pub/Sub topic names; use `OrderProperties`.
- Do not remove `subscribeOn(Schedulers.boundedElastic())` around blocking JPA repository calls.
- Do not add blocking I/O directly to request-handling reactive chains.
- Endpoint tests use `WebTestClient.bindToController()`.
- Service tests use JUnit 5, Mockito, and Reactor `StepVerifier` where reactive behavior matters.
- Prefer focused unit/slice tests; add full Spring context tests only when wiring or runtime config is the behavior under test.
- Do not commit generated output under `target/` or local Maven logs.
