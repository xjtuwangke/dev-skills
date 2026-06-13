/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "clients")
public record DownstreamClientProperties(
        Service customerProfile,
        Service catalog,
        Service inventory,
        Service paymentGateway,
        Service shipping) {

    public record Service(String baseUrl) {
    }
}
