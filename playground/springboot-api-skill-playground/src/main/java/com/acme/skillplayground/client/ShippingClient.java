/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.client;

import com.acme.skillplayground.client.model.ShippingRateRequest;
import com.acme.skillplayground.client.model.ShippingRateResponse;
import com.acme.skillplayground.config.DownstreamClientProperties;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Component
public class ShippingClient {

    private final WebClient webClient;

    public ShippingClient(
            final DownstreamWebClientFactory webClientFactory,
            final DownstreamClientProperties properties) {
        this.webClient = webClientFactory.create(properties.shipping());
    }

    public Mono<ShippingRateResponse> quoteRate(final ShippingRateRequest request) {
        return webClient.post()
                .uri("/v1/shipping/rates")
                .bodyValue(request)
                .retrieve()
                .bodyToMono(ShippingRateResponse.class);
    }
}
