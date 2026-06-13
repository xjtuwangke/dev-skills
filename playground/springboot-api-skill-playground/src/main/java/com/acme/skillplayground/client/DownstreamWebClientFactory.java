/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.client;

import com.acme.skillplayground.config.DownstreamClientProperties;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;

@Component
public class DownstreamWebClientFactory {

    private final WebClient.Builder webClientBuilder;

    public DownstreamWebClientFactory(final WebClient.Builder webClientBuilder) {
        this.webClientBuilder = webClientBuilder;
    }

    public WebClient create(final DownstreamClientProperties.Service service) {
        return webClientBuilder.clone()
                .baseUrl(service.baseUrl())
                .build();
    }
}
