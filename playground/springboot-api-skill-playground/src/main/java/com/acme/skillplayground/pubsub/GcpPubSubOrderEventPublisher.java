/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.pubsub;

import com.acme.skillplayground.config.OrderProperties;
import com.acme.skillplayground.model.OrderResponse;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

@Component
@ConditionalOnProperty(name = "orders.pubsub.enabled", havingValue = "true")
public class GcpPubSubOrderEventPublisher implements OrderEventPublisher {

    private final PubSubGateway pubSubGateway;
    private final OrderProperties properties;

    public GcpPubSubOrderEventPublisher(final PubSubGateway pubSubGateway, final OrderProperties properties) {
        this.pubSubGateway = pubSubGateway;
        this.properties = properties;
    }

    @Override
    public Mono<Void> publishCreated(final OrderResponse response) {
        return publish(properties.pubsub().createdTopic(), OrderEvent.created(response));
    }

    @Override
    public Mono<Void> publishStatusChanged(final OrderResponse response) {
        return publish(properties.pubsub().statusChangedTopic(), OrderEvent.statusChanged(response));
    }

    private Mono<Void> publish(final String topic, final OrderEvent event) {
        return Mono.fromFuture(pubSubGateway.publish(topic, event)).then();
    }
}
