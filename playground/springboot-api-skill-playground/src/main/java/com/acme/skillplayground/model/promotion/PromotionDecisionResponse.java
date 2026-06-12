/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model.promotion;

import java.math.BigDecimal;

public record PromotionDecisionResponse(
        String couponCode,
        boolean eligible,
        BigDecimal discountAmount,
        String reason) {
}
