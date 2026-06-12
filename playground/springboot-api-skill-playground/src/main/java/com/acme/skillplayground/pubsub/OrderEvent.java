/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.pubsub;

import com.acme.skillplayground.model.OrderResponse;
import com.acme.skillplayground.model.ShippingPriority;
import java.time.Instant;
import java.util.UUID;

public record OrderEvent(
        String type,
        UUID orderId,
        String customerId,
        ShippingPriority shippingPriority,
        boolean manualReviewRequired,
        Instant occurredAt) {

    public static OrderEvent created(final OrderResponse response) {
        return new OrderEvent(
                "ORDER_CREATED",
                response.id(),
                response.customerId(),
                response.shippingPriority(),
                response.manualReviewRequired(),
                Instant.now());
    }

    public static OrderEvent statusChanged(final OrderResponse response) {
        return new OrderEvent(
                "ORDER_STATUS_CHANGED",
                response.id(),
                response.customerId(),
                response.shippingPriority(),
                response.manualReviewRequired(),
                Instant.now());
    }
}
