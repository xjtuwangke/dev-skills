/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.client;

import static org.assertj.core.api.Assertions.assertThat;

import com.acme.skillplayground.client.model.CatalogAvailabilityResponse;
import com.acme.skillplayground.client.model.CustomerRiskResponse;
import com.acme.skillplayground.client.model.InventoryQuoteRequest;
import com.acme.skillplayground.client.model.InventoryQuoteResponse;
import com.acme.skillplayground.client.model.PaymentGatewayAuthorizationRequest;
import com.acme.skillplayground.client.model.PaymentGatewayAuthorizationResponse;
import com.acme.skillplayground.client.model.ShippingRateRequest;
import com.acme.skillplayground.client.model.ShippingRateResponse;
import com.acme.skillplayground.config.DownstreamClientProperties;
import java.math.BigDecimal;
import java.net.URI;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.client.ClientRequest;
import org.springframework.web.reactive.function.client.ClientResponse;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

class DownstreamClientsTest {

    private DownstreamClientProperties properties;
    private DownstreamWebClientFactory webClientFactory;
    private List<ClientRequest> requests;

    @BeforeEach
    void setUp() {
        requests = new ArrayList<>();
        final WebClient.Builder webClientBuilder = WebClient.builder()
                .exchangeFunction((final ClientRequest request) -> {
                    requests.add(request);
                    return responseFor(request.url());
                });
        webClientFactory = new DownstreamWebClientFactory(webClientBuilder);
        properties = new DownstreamClientProperties(
                new DownstreamClientProperties.Service("https://customer-profile.test.example"),
                new DownstreamClientProperties.Service("https://catalog.test.example"),
                new DownstreamClientProperties.Service("https://inventory.test.example"),
                new DownstreamClientProperties.Service("https://payments.test.example"),
                new DownstreamClientProperties.Service("https://shipping.test.example"));
    }

    @Test
    void callsCustomerProfileHost() {
        final CustomerProfileClient client = new CustomerProfileClient(webClientFactory, properties);

        StepVerifier.create(client.getRiskProfile("customer-1"))
                .expectNext(new CustomerRiskResponse("customer-1", "LOW", 12))
                .verifyComplete();

        assertRequest(HttpMethod.GET, "customer-profile.test.example", "/v1/customers/customer-1/risk");
    }

    @Test
    void callsCatalogHost() {
        final CatalogClient client = new CatalogClient(webClientFactory, properties);

        StepVerifier.create(client.getAvailability("SKU-1"))
                .expectNext(new CatalogAvailabilityResponse("SKU-1", true, 42))
                .verifyComplete();

        assertRequest(HttpMethod.GET, "catalog.test.example", "/v1/catalog/items/SKU-1/availability");
    }

    @Test
    void callsInventoryHost() {
        final InventoryClient client = new InventoryClient(webClientFactory, properties);
        final UUID orderId = UUID.randomUUID();
        final InventoryQuoteRequest request = new InventoryQuoteRequest(orderId, "SKU-1", 2);

        StepVerifier.create(client.quoteReservation(request))
                .expectNext(new InventoryQuoteResponse("SKU-1", 42, "FC-001"))
                .verifyComplete();

        assertRequest(HttpMethod.POST, "inventory.test.example", "/v1/inventory/reservation-quotes");
    }

    @Test
    void callsPaymentGatewayHost() {
        final PaymentGatewayClient client = new PaymentGatewayClient(webClientFactory, properties);
        final UUID orderId = UUID.randomUUID();
        final PaymentGatewayAuthorizationRequest request = new PaymentGatewayAuthorizationRequest(
                orderId, new BigDecimal("86.58"), "USD", "tok_123");

        StepVerifier.create(client.authorize(request))
                .expectNext(new PaymentGatewayAuthorizationResponse(true, "AUTH-123", "approved"))
                .verifyComplete();

        assertRequest(HttpMethod.POST, "payments.test.example", "/v1/payment-gateway/authorizations");
    }

    @Test
    void callsShippingHost() {
        final ShippingClient client = new ShippingClient(webClientFactory, properties);
        final UUID orderId = UUID.randomUUID();
        final ShippingRateRequest request = new ShippingRateRequest(orderId, "75001", "SKU-1", 2);

        StepVerifier.create(client.quoteRate(request))
                .expectNext(new ShippingRateResponse("ACME-PARCEL", "GROUND", new BigDecimal("12.50"), "USD"))
                .verifyComplete();

        assertRequest(HttpMethod.POST, "shipping.test.example", "/v1/shipping/rates");
    }

    private Mono<ClientResponse> responseFor(final URI uri) {
        final String body = switch (uri.getHost()) {
            case "customer-profile.test.example" -> """
                    {"customerId":"customer-1","riskBand":"LOW","score":12}
                    """;
            case "catalog.test.example" -> """
                    {"sku":"SKU-1","available":true,"availableQuantity":42}
                    """;
            case "inventory.test.example" -> """
                    {"sku":"SKU-1","availableQuantity":42,"locationCode":"FC-001"}
                    """;
            case "payments.test.example" -> """
                    {"authorized":true,"authorizationCode":"AUTH-123","reason":"approved"}
                    """;
            case "shipping.test.example" -> """
                    {"carrier":"ACME-PARCEL","serviceLevel":"GROUND","amount":12.50,"currency":"USD"}
                    """;
            default -> "{}";
        };
        return Mono.just(ClientResponse.create(HttpStatus.OK)
                .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
                .body(body)
                .build());
    }

    private void assertRequest(final HttpMethod method, final String host, final String path) {
        final ClientRequest request = requests.get(requests.size() - 1);
        assertThat(request.method()).isEqualTo(method);
        assertThat(request.url().getHost()).isEqualTo(host);
        assertThat(request.url().getPath()).isEqualTo(path);
    }
}
