/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model.pricing;

import java.math.BigDecimal;

public record PriceQuoteResponse(
        String sku,
        int quantity,
        BigDecimal subtotal,
        BigDecimal discount,
        BigDecimal tax,
        BigDecimal total,
        String currency,
        String priceRule) {
}
