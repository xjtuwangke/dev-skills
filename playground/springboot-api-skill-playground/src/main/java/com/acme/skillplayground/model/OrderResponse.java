/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model;

import com.fasterxml.jackson.annotation.JsonFormat;
import java.time.Instant;
import java.time.LocalDate;
import java.util.UUID;

public record OrderResponse(
        UUID id,
        String customerId,
        String sku,
        int quantity,
        ShippingPriority shippingPriority,
        @JsonFormat(shape = JsonFormat.Shape.STRING)
        LocalDate requestedShipDate,
        boolean manualReviewRequired,
        OrderStatus status,
        Instant createdAt,
        Instant updatedAt) {

    public OrderResponse {
        if (shippingPriority == null) {
            shippingPriority = ShippingPriority.STANDARD;
        }
    }

    public OrderResponse(
            final UUID id,
            final String customerId,
            final String sku,
            final int quantity,
            final OrderStatus status,
            final Instant createdAt,
            final Instant updatedAt) {
        this(id, customerId, sku, quantity, ShippingPriority.STANDARD, null, false, status, createdAt, updatedAt);
    }
}
