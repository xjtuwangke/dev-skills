/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.client.model;

import java.math.BigDecimal;
import java.util.UUID;

public record PaymentGatewayAuthorizationRequest(UUID orderId, BigDecimal amount, String currency, String paymentToken) {
}
