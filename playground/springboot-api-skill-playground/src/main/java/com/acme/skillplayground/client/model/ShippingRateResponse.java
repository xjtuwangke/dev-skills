/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.client.model;

import java.math.BigDecimal;

public record ShippingRateResponse(String carrier, String serviceLevel, BigDecimal amount, String currency) {
}
