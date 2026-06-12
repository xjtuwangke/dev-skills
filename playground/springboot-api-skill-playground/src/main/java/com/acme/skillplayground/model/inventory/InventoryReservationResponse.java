/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model.inventory;

import java.util.UUID;

public record InventoryReservationResponse(
        UUID reservationId,
        String sku,
        String locationCode,
        int reservedQuantity,
        String status) {
}
