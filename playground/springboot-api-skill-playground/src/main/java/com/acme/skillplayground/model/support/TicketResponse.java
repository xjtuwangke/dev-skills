/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model.support;

import java.time.Instant;
import java.util.UUID;

public record TicketResponse(
        UUID ticketId,
        String customerId,
        String status,
        String priority,
        Instant createdAt) {
}
