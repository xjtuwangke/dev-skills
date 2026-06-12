/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.mapper;

import java.time.Clock;
import java.time.LocalDate;
import org.springframework.stereotype.Component;

@Component
public class FulfillmentMapper {

    private final Clock clock;

    public FulfillmentMapper(final Clock clock) {
        this.clock = clock;
    }

    public String warehouseForPostalCode(final String postalCode) {
        if (postalCode.startsWith("9")) {
            return "SFO-01";
        }
        if (postalCode.startsWith("1")) {
            return "EWR-02";
        }
        return "DFW-01";
    }

    public String serviceLevel(final int quantity) {
        if (quantity > 20) {
            return "FREIGHT";
        }
        return "GROUND";
    }

    public LocalDate estimatedShipDate(final int quantity) {
        final int plusDays = quantity > 20 ? 3 : 1;
        return LocalDate.now(clock).plusDays(plusDays);
    }
}
