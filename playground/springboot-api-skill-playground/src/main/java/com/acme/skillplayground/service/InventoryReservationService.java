/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.service;

import com.acme.skillplayground.exception.ResourceConflictException;
import com.acme.skillplayground.model.inventory.InventoryReservationRequest;
import com.acme.skillplayground.model.inventory.InventoryReservationResponse;
import java.util.UUID;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class InventoryReservationService {

    public Mono<InventoryReservationResponse> reserve(final InventoryReservationRequest request) {
        return Mono.fromSupplier(() -> {
            if (request.quantity() > availableUnits(request.sku())) {
                throw new ResourceConflictException("Insufficient inventory for SKU " + request.sku());
            }
            return new InventoryReservationResponse(
                    UUID.randomUUID(),
                    request.sku(),
                    locationForSku(request.sku()),
                    request.quantity(),
                    "RESERVED");
        });
    }

    private int availableUnits(final String sku) {
        if (sku.startsWith("LOW")) {
            return 1;
        }
        return 50;
    }

    private String locationForSku(final String sku) {
        if (sku.startsWith("HZ")) {
            return "REG-HAZ-01";
        }
        return "FC-001";
    }
}
