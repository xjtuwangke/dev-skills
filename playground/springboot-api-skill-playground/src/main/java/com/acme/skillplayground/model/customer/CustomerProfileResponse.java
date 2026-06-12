/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model.customer;

import java.time.Instant;

public record CustomerProfileResponse(
        String customerId,
        String displayName,
        CustomerSegment segment,
        String defaultCurrency,
        int loyaltyPoints,
        Instant lastActivityAt) {
}
