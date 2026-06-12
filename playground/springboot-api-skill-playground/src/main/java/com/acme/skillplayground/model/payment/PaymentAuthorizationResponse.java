/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model.payment;

import java.util.UUID;

public record PaymentAuthorizationResponse(
        UUID paymentId,
        boolean authorized,
        String authorizationCode,
        String reason) {
}
