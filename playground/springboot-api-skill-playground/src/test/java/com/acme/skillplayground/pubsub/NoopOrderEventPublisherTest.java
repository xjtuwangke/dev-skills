/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.pubsub;

import com.acme.skillplayground.model.OrderResponse;
import com.acme.skillplayground.model.OrderStatus;
import java.time.Instant;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import reactor.test.StepVerifier;

class NoopOrderEventPublisherTest {

    @Test
    void completesWithoutPublishing() {
        final NoopOrderEventPublisher publisher = new NoopOrderEventPublisher();
        final Instant now = Instant.parse("2026-01-01T00:00:00Z");
        final OrderResponse response = new OrderResponse(
                UUID.randomUUID(), "customer-1", "sku-1", 2, OrderStatus.CREATED, now, now);

        StepVerifier.create(publisher.publishCreated(response))
                .verifyComplete();
    }
}
