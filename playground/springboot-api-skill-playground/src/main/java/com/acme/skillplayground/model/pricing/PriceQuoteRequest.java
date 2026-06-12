/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model.pricing;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;

public record PriceQuoteRequest(
        @NotBlank String customerId,
        @NotBlank String sku,
        @Positive int quantity,
        String couponCode) {
}
