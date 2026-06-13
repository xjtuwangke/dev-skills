/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.client;

import com.acme.skillplayground.client.model.PaymentGatewayAuthorizationRequest;
import com.acme.skillplayground.client.model.PaymentGatewayAuthorizationResponse;
import com.acme.skillplayground.config.DownstreamClientProperties;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Component
public class PaymentGatewayClient {

    private final WebClient webClient;

    public PaymentGatewayClient(
            final DownstreamWebClientFactory webClientFactory,
            final DownstreamClientProperties properties) {
        this.webClient = webClientFactory.create(properties.paymentGateway());
    }

    public Mono<PaymentGatewayAuthorizationResponse> authorize(
            final PaymentGatewayAuthorizationRequest request) {
        return webClient.post()
                .uri("/v1/payment-gateway/authorizations")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(PaymentGatewayAuthorizationResponse.class);
    }
}
