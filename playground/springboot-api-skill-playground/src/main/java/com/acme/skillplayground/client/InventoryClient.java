/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.client;

import com.acme.skillplayground.client.model.InventoryQuoteRequest;
import com.acme.skillplayground.client.model.InventoryQuoteResponse;
import com.acme.skillplayground.config.DownstreamClientProperties;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Component
public class InventoryClient {

    private final WebClient webClient;

    public InventoryClient(
            final DownstreamWebClientFactory webClientFactory,
            final DownstreamClientProperties properties) {
        this.webClient = webClientFactory.create(properties.inventory());
    }

    public Mono<InventoryQuoteResponse> quoteReservation(final InventoryQuoteRequest request) {
        return webClient.post()
                .uri("/v1/inventory/reservation-quotes")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(InventoryQuoteResponse.class);
    }
}
