package com.acme.commerce.pubsub;

import com.acme.commerce.config.CommerceProperties;
import com.acme.commerce.model.CommerceModels.OrderCancelledEvent;
import com.acme.commerce.model.CommerceModels.OrderCreatedEvent;
import com.acme.commerce.model.CommerceModels.PaymentAuthorizedEvent;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.cloud.spring.pubsub.core.PubSubTemplate;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

@Component
public class CommerceEventPublisher {
    private final PubSubTemplate pubSubTemplate;
    private final CommerceProperties properties;
    private final ObjectMapper objectMapper;

    public CommerceEventPublisher(PubSubTemplate pubSubTemplate, CommerceProperties properties, ObjectMapper objectMapper) {
        this.pubSubTemplate = pubSubTemplate;
        this.properties = properties;
        this.objectMapper = objectMapper;
    }

    public Mono<Void> publishOrderCreated(OrderCreatedEvent event) {
        return publish(properties.getPubsub().getOrderCreatedTopic(), event);
    }

    public Mono<Void> publishOrderCancelled(OrderCancelledEvent event) {
        return publish(properties.getPubsub().getOrderCancelledTopic(), event);
    }

    public Mono<Void> publishPaymentAuthorized(PaymentAuthorizedEvent event) {
        return publish(properties.getPubsub().getPaymentAuthorizedTopic(), event);
    }

    private Mono<Void> publish(String topic, Object event) {
        return Mono.fromFuture(pubSubTemplate.publish(topic, toJson(event))).then();
    }

    private String toJson(Object event) {
        try {
            return objectMapper.writeValueAsString(event);
        } catch (JsonProcessingException ex) {
            throw new IllegalArgumentException("Unable to serialize domain event", ex);
        }
    }
}

