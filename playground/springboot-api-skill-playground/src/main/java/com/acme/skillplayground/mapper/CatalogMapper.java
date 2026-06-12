/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.mapper;

import com.acme.skillplayground.exception.DomainRuleViolationException;
import com.acme.skillplayground.model.catalog.CatalogItemResponse;
import com.acme.skillplayground.model.catalog.ProductStatus;
import java.math.BigDecimal;
import org.springframework.stereotype.Component;

@Component
public class CatalogMapper {

    public CatalogItemResponse toCatalogItem(final String sku) {
        if (sku.startsWith("OLD")) {
            return new CatalogItemResponse(
                    sku,
                    "Legacy item " + sku,
                    "clearance",
                    ProductStatus.DISCONTINUED,
                    new BigDecimal("19.99"),
                    "USD",
                    false);
        }
        if (sku.startsWith("HZ")) {
            return new CatalogItemResponse(
                    sku,
                    "Hazardous kit " + sku,
                    "regulated",
                    ProductStatus.ACTIVE,
                    new BigDecimal("129.99"),
                    "USD",
                    true);
        }
        if (sku.isBlank()) {
            throw new DomainRuleViolationException("SKU must not be blank");
        }
        return new CatalogItemResponse(
                sku,
                "Retail item " + sku,
                "general",
                ProductStatus.ACTIVE,
                new BigDecimal("49.99"),
                "USD",
                false);
    }
}
