/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.pubsub;

import com.google.cloud.spring.pubsub.core.PubSubTemplate;
import java.util.concurrent.CompletableFuture;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

@Component
@ConditionalOnProperty(name = "orders.pubsub.enabled", havingValue = "true")
public class GcpPubSubGateway implements PubSubGateway {

    private final PubSubTemplate pubSubTemplate;

    public GcpPubSubGateway(final PubSubTemplate pubSubTemplate) {
        this.pubSubTemplate = pubSubTemplate;
    }

    @Override
    public CompletableFuture<String> publish(final String topic, final Object payload) {
        return pubSubTemplate.publish(topic, payload);
    }
}
