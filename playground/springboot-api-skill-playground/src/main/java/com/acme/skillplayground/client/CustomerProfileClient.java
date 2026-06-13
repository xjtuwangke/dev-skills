/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.client;

import com.acme.skillplayground.client.model.CustomerRiskResponse;
import com.acme.skillplayground.config.DownstreamClientProperties;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Component
public class CustomerProfileClient {

    private final WebClient webClient;

    public CustomerProfileClient(
            final DownstreamWebClientFactory webClientFactory,
            final DownstreamClientProperties properties) {
        this.webClient = webClientFactory.create(properties.customerProfile());
    }

    public Mono<CustomerRiskResponse> getRiskProfile(final String customerId) {
        return webClient.get()
                .uri("/v1/customers/{customerId}/risk", customerId)
                .retrieve()
                .bodyToMono(CustomerRiskResponse.class);
    }
}
