# Clients Technical Reference

## Source Areas
- Client classes: `src/main/java/com/acme/skillplayground/client/`
- Client DTOs: `src/main/java/com/acme/skillplayground/client/model/`
- Client config: `src/main/java/com/acme/skillplayground/config/DownstreamClientProperties.java`
- Base URLs: `clients.*.base-url` in `src/main/resources/application.yml`
- Tests: `src/test/java/com/acme/skillplayground/client/DownstreamClientsTest.java`

## Common Client Rules
- All downstream HTTP calls use Spring WebFlux `WebClient`.
- Each downstream integration has a different configured host.
- `DownstreamWebClientFactory` clones the injected `WebClient.Builder` before applying a base URL.
- Request/response payloads are Java `record`s under `com.acme.skillplayground.client.model`.
- No client currently adds request headers or header validations.
- `retrieve()` uses default WebClient error behavior unless a client method adds explicit status handling later.

## Best Practices
- Keep one client class per downstream domain/host.
- Keep base URLs in `clients.*.base-url`; do not hard-code hosts in client methods.
- Model downstream request/response payloads with dedicated records under `client/model`.
- Add explicit `onStatus` mapping when downstream errors affect API behavior.
- Test host, method, path, and response mapping with a fake `ExchangeFunction`.

```java
public Mono<PaymentGatewayAuthorizationResponse> authorize(
        final PaymentGatewayAuthorizationRequest request) {
    return webClient.post()
            .uri("/v1/payment-gateway/authorizations")
            .bodyValue(request)
            .retrieve()
            .bodyToMono(PaymentGatewayAuthorizationResponse.class);
}
```

## Downstream APIs

### GET /v1/customers/{customerId}/risk
- Host config: `clients.customer-profile.base-url`
- Default host: `https://customer-profile.internal.acme.example`
- Class/method: `CustomerProfileClient#getRiskProfile`
- Request: path `customerId: String`
- Request POJO: none.
- Response POJO: `com.acme.skillplayground.client.model.CustomerRiskResponse`

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Path | `customerId` | `String`; no Bean Validation annotation |
| Header | none | No request headers declared |

- Timeout/retry/error mapping: not explicitly configured; uses default `WebClient.retrieve()` error behavior.
- Tests: `DownstreamClientsTest#callsCustomerProfileHost`.

### GET /v1/catalog/items/{sku}/availability
- Host config: `clients.catalog.base-url`
- Default host: `https://catalog.internal.acme.example`
- Class/method: `CatalogClient#getAvailability`
- Request: path `sku: String`
- Request POJO: none.
- Response POJO: `com.acme.skillplayground.client.model.CatalogAvailabilityResponse`

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Path | `sku` | `String`; no Bean Validation annotation |
| Header | none | No request headers declared |

- Timeout/retry/error mapping: not explicitly configured; uses default `WebClient.retrieve()` error behavior.
- Tests: `DownstreamClientsTest#callsCatalogHost`.

### POST /v1/inventory/reservation-quotes
- Host config: `clients.inventory.base-url`
- Default host: `https://inventory.internal.acme.example`
- Class/method: `InventoryClient#quoteReservation`
- Request: body.
- Request POJO: `com.acme.skillplayground.client.model.InventoryQuoteRequest`
- Response POJO: `com.acme.skillplayground.client.model.InventoryQuoteResponse`

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Body | `orderId` | `UUID`; no Bean Validation annotation |
| Body | `sku` | `String`; no Bean Validation annotation |
| Body | `quantity` | `int`; no Bean Validation annotation |
| Header | none | No request headers declared |

- Timeout/retry/error mapping: not explicitly configured; uses default `WebClient.retrieve()` error behavior.
- Tests: `DownstreamClientsTest#callsInventoryHost`.

### POST /v1/payment-gateway/authorizations
- Host config: `clients.payment-gateway.base-url`
- Default host: `https://payments.internal.acme.example`
- Class/method: `PaymentGatewayClient#authorize`
- Request: body.
- Request POJO: `com.acme.skillplayground.client.model.PaymentGatewayAuthorizationRequest`
- Response POJO: `com.acme.skillplayground.client.model.PaymentGatewayAuthorizationResponse`

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Body | `orderId` | `UUID`; no Bean Validation annotation |
| Body | `amount` | `BigDecimal`; no Bean Validation annotation |
| Body | `currency` | `String`; no Bean Validation annotation |
| Body | `paymentToken` | `String`; no Bean Validation annotation |
| Header | none | No request headers declared |

- Timeout/retry/error mapping: not explicitly configured; uses default `WebClient.retrieve()` error behavior.
- Tests: `DownstreamClientsTest#callsPaymentGatewayHost`.

### POST /v1/shipping/rates
- Host config: `clients.shipping.base-url`
- Default host: `https://shipping.internal.acme.example`
- Class/method: `ShippingClient#quoteRate`
- Request: body.
- Request POJO: `com.acme.skillplayground.client.model.ShippingRateRequest`
- Response POJO: `com.acme.skillplayground.client.model.ShippingRateResponse`

Validations:

| Scope | Name | Rule |
| --- | --- | --- |
| Body | `orderId` | `UUID`; no Bean Validation annotation |
| Body | `postalCode` | `String`; no Bean Validation annotation |
| Body | `sku` | `String`; no Bean Validation annotation |
| Body | `quantity` | `int`; no Bean Validation annotation |
| Header | none | No request headers declared |

- Timeout/retry/error mapping: not explicitly configured; uses default `WebClient.retrieve()` error behavior.
- Tests: `DownstreamClientsTest#callsShippingHost`.
