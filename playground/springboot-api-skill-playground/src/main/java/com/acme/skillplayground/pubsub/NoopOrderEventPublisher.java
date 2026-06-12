/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.pubsub;

import com.acme.skillplayground.model.OrderResponse;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

@Component
@ConditionalOnProperty(name = "orders.pubsub.enabled", havingValue = "false", matchIfMissing = true)
public class NoopOrderEventPublisher implements OrderEventPublisher {

    @Override
    public Mono<Void> publishCreated(final OrderResponse response) {
        return Mono.empty();
    }

    @Override
    public Mono<Void> publishStatusChanged(final OrderResponse response) {
        return Mono.empty();
    }
}
