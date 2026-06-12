/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model;

import com.fasterxml.jackson.annotation.JsonFormat;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import java.time.LocalDate;

public record CreateOrderRequest(
        @NotBlank String customerId,
        @NotBlank String sku,
        @Positive int quantity,
        ShippingPriority shippingPriority,
        @JsonFormat(shape = JsonFormat.Shape.STRING)
        LocalDate requestedShipDate) {

    public CreateOrderRequest(final String customerId, final String sku, final int quantity) {
        this(customerId, sku, quantity, null, null);
    }

    public ShippingPriority resolvedShippingPriority() {
        if (shippingPriority == null) {
            return ShippingPriority.STANDARD;
        }
        return shippingPriority;
    }
}
