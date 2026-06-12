/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.service;

import com.acme.skillplayground.exception.DomainRuleViolationException;
import com.acme.skillplayground.mapper.FulfillmentMapper;
import com.acme.skillplayground.model.fulfillment.ShipmentPlanRequest;
import com.acme.skillplayground.model.fulfillment.ShipmentPlanResponse;
import java.util.UUID;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class FulfillmentPlanningService {

    private final FulfillmentMapper mapper;

    public FulfillmentPlanningService(final FulfillmentMapper mapper) {
        this.mapper = mapper;
    }

    public Mono<ShipmentPlanResponse> plan(final ShipmentPlanRequest request) {
        return Mono.fromSupplier(() -> {
            if (request.sku().startsWith("HZ") && !request.postalCode().startsWith("9")) {
                throw new DomainRuleViolationException("Hazardous SKUs can ship only from western region");
            }
            return new ShipmentPlanResponse(
                    UUID.randomUUID(),
                    mapper.warehouseForPostalCode(request.postalCode()),
                    "ACME-PARCEL",
                    mapper.serviceLevel(request.quantity()),
                    mapper.estimatedShipDate(request.quantity()));
        });
    }
}
