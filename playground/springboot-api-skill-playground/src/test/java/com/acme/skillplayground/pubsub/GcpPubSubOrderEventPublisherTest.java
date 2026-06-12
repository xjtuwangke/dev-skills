/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.pubsub;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.acme.skillplayground.config.OrderProperties;
import com.acme.skillplayground.model.OrderResponse;
import com.acme.skillplayground.model.OrderStatus;
import com.acme.skillplayground.model.ShippingPriority;
import java.time.Instant;
import java.util.UUID;
import java.util.concurrent.CompletableFuture;
import org.junit.jupiter.api.Test;
import org.mockito.ArgumentCaptor;
import reactor.test.StepVerifier;

class GcpPubSubOrderEventPublisherTest {

    @Test
    void publishesCreatedEventToConfiguredTopic() {
        final PubSubGateway pubSubGateway = mock(PubSubGateway.class);
        final OrderProperties properties = new OrderProperties(
                new OrderProperties.PubSub(true, "orders.created.dev", "orders.status-changed.dev"));
        final GcpPubSubOrderEventPublisher publisher = new GcpPubSubOrderEventPublisher(pubSubGateway, properties);
        final OrderResponse response = response(OrderStatus.CREATED);
        when(pubSubGateway.publish(eq("orders.created.dev"), any(OrderEvent.class)))
                .thenReturn(CompletableFuture.completedFuture("message-id"));

        StepVerifier.create(publisher.publishCreated(response))
                .verifyComplete();

        final ArgumentCaptor<OrderEvent> eventCaptor = ArgumentCaptor.forClass(OrderEvent.class);
        verify(pubSubGateway).publish(eq("orders.created.dev"), eventCaptor.capture());
        assertThat(eventCaptor.getValue().shippingPriority()).isEqualTo(ShippingPriority.EXPEDITED);
        assertThat(eventCaptor.getValue().manualReviewRequired()).isTrue();
    }

    @Test
    void publishesStatusChangedEventToConfiguredTopic() {
        final PubSubGateway pubSubGateway = mock(PubSubGateway.class);
        final OrderProperties properties = new OrderProperties(
                new OrderProperties.PubSub(true, "orders.created.dev", "orders.status-changed.dev"));
        final GcpPubSubOrderEventPublisher publisher = new GcpPubSubOrderEventPublisher(pubSubGateway, properties);
        final OrderResponse response = response(OrderStatus.ACCEPTED);
        when(pubSubGateway.publish(eq("orders.status-changed.dev"), any(OrderEvent.class)))
                .thenReturn(CompletableFuture.completedFuture("message-id"));

        StepVerifier.create(publisher.publishStatusChanged(response))
                .verifyComplete();

        verify(pubSubGateway).publish(eq("orders.status-changed.dev"), any(OrderEvent.class));
    }

    private OrderResponse response(final OrderStatus status) {
        final Instant now = Instant.parse("2026-01-01T00:00:00Z");
        return new OrderResponse(
                UUID.randomUUID(),
                "customer-1",
                "sku-1",
                11,
                ShippingPriority.EXPEDITED,
                null,
                true,
                status,
                now,
                now);
    }
}
