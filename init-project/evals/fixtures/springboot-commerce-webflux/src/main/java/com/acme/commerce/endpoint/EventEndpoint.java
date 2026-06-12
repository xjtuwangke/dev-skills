package com.acme.commerce.endpoint;

import com.acme.commerce.model.CommerceModels.DomainEventView;
import com.acme.commerce.service.EventQueryService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;

@RestController
@RequestMapping("/api/v1/events")
public class EventEndpoint {
    private final EventQueryService eventQueryService;

    public EventEndpoint(EventQueryService eventQueryService) {
        this.eventQueryService = eventQueryService;
    }

    @GetMapping("/orders/{orderId}")
    public Flux<DomainEventView> listOrderEvents(@PathVariable String orderId) {
        return eventQueryService.listOrderEvents(orderId);
    }
}

