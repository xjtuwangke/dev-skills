/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.client;

import com.acme.skillplayground.client.model.CatalogAvailabilityResponse;
import com.acme.skillplayground.config.DownstreamClientProperties;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Component
public class CatalogClient {

    private final WebClient webClient;

    public CatalogClient(
            final DownstreamWebClientFactory webClientFactory,
            final DownstreamClientProperties properties) {
        this.webClient = webClientFactory.create(properties.catalog());
    }

    public Mono<CatalogAvailabilityResponse> getAvailability(final String sku) {
        return webClient.get()
                .uri("/v1/catalog/items/{sku}/availability", sku)
                .retrieve()
                .bodyToMono(CatalogAvailabilityResponse.class);
    }
}
