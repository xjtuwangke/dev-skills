/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.service;

import com.acme.skillplayground.model.promotion.PromotionDecisionResponse;
import java.math.BigDecimal;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class PromotionService {

    public Mono<PromotionDecisionResponse> evaluate(
            final String couponCode,
            final String customerId,
            final String sku) {
        return Mono.fromSupplier(() -> {
            if ("SAVE20".equalsIgnoreCase(couponCode) && !sku.startsWith("OLD")) {
                return new PromotionDecisionResponse(couponCode, true, new BigDecimal("20.00"), "eligible");
            }
            if (customerId.startsWith("ent-")) {
                return new PromotionDecisionResponse(couponCode, true, new BigDecimal("10.00"), "enterprise");
            }
            return new PromotionDecisionResponse(couponCode, false, BigDecimal.ZERO, "not eligible");
        });
    }
}
