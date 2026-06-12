/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model.catalog;

import java.math.BigDecimal;

public record CatalogItemResponse(
        String sku,
        String name,
        String category,
        ProductStatus status,
        BigDecimal listPrice,
        String currency,
        boolean hazardous) {
}
