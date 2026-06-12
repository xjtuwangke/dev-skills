/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model.fulfillment;

import java.time.LocalDate;
import java.util.UUID;

public record ShipmentPlanResponse(
        UUID shipmentId,
        String warehouseCode,
        String carrier,
        String serviceLevel,
        LocalDate estimatedShipDate) {
}
