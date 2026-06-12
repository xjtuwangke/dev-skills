package com.acme.commerce.service;

import com.acme.commerce.model.CommerceModels.DomainEventView;
import java.time.Instant;
import java.util.Map;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;

@Service
public class EventQueryService {
    public Flux<DomainEventView> listOrderEvents(String orderId) {
        return Flux.just(
            new DomainEventView("evt_1", orderId, "ORDER_CREATED", Instant.now(), Map.of("source", "demo")),
            new DomainEventView("evt_2", orderId, "PAYMENT_AUTHORIZED", Instant.now(), Map.of("source", "demo"))
        );
    }
}

