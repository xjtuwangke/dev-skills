/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.service;

import com.acme.skillplayground.model.support.CreateTicketRequest;
import com.acme.skillplayground.model.support.TicketResponse;
import java.time.Clock;
import java.time.Instant;
import java.util.UUID;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class SupportTicketService {

    private final Clock clock;

    public SupportTicketService(final Clock clock) {
        this.clock = clock;
    }

    public Mono<TicketResponse> create(final CreateTicketRequest request) {
        return Mono.fromSupplier(() -> new TicketResponse(
                UUID.randomUUID(),
                request.customerId(),
                "OPEN",
                priority(request.subject(), request.message()),
                Instant.now(clock)));
    }

    private String priority(final String subject, final String message) {
        if (subject.toLowerCase().contains("payment") || message.toLowerCase().contains("chargeback")) {
            return "HIGH";
        }
        return "NORMAL";
    }
}
