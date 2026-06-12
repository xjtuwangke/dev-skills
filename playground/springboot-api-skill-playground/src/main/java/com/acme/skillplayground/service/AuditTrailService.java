/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.service;

import com.acme.skillplayground.model.audit.AuditTrailResponse;
import java.time.Clock;
import java.time.Instant;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class AuditTrailService {

    private final Clock clock;

    public AuditTrailService(final Clock clock) {
        this.clock = clock;
    }

    public Mono<AuditTrailResponse> orderTrail(final UUID orderId) {
        return Mono.fromSupplier(() -> new AuditTrailResponse(
                orderId,
                "ORDER",
                List.of("ORDER_CREATED", "PAYMENT_AUTHORIZED", "SHIPMENT_PLANNED"),
                Instant.now(clock)));
    }
}
