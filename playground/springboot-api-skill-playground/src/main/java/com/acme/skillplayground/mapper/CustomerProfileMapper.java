/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.mapper;

import com.acme.skillplayground.model.customer.CustomerProfileResponse;
import com.acme.skillplayground.model.customer.CustomerSegment;
import java.time.Instant;
import org.springframework.stereotype.Component;

@Component
public class CustomerProfileMapper {

    public CustomerProfileResponse toProfile(final String customerId) {
        final CustomerSegment segment = customerId.startsWith("ent-")
                ? CustomerSegment.ENTERPRISE
                : CustomerSegment.GOLD;
        final int loyaltyPoints = segment == CustomerSegment.ENTERPRISE ? 25000 : 4200;
        return new CustomerProfileResponse(
                customerId,
                "Customer " + customerId,
                segment,
                "USD",
                loyaltyPoints,
                Instant.parse("2026-01-01T00:00:00Z"));
    }
}
