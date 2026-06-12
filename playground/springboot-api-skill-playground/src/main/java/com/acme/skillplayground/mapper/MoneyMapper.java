/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.mapper;

import java.math.BigDecimal;
import java.math.RoundingMode;
import org.springframework.stereotype.Component;

@Component
public class MoneyMapper {

    private static final BigDecimal TAX_RATE = new BigDecimal("0.0825");

    public BigDecimal subtotal(final BigDecimal unitPrice, final int quantity) {
        return round(unitPrice.multiply(BigDecimal.valueOf(quantity)));
    }

    public BigDecimal loyaltyDiscount(final BigDecimal subtotal, final boolean preferredCustomer) {
        if (preferredCustomer) {
            return round(subtotal.multiply(new BigDecimal("0.10")));
        }
        return BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP);
    }

    public BigDecimal couponDiscount(final BigDecimal subtotal, final String couponCode) {
        if ("SAVE20".equalsIgnoreCase(couponCode)) {
            return round(subtotal.multiply(new BigDecimal("0.20")));
        }
        return BigDecimal.ZERO.setScale(2, RoundingMode.HALF_UP);
    }

    public BigDecimal tax(final BigDecimal taxableAmount) {
        return round(taxableAmount.multiply(TAX_RATE));
    }

    public BigDecimal round(final BigDecimal amount) {
        return amount.setScale(2, RoundingMode.HALF_UP);
    }
}
