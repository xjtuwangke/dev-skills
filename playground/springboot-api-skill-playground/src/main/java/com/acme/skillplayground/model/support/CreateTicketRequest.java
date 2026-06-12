/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model.support;

import jakarta.validation.constraints.NotBlank;

public record CreateTicketRequest(
        @NotBlank String customerId,
        @NotBlank String orderId,
        @NotBlank String subject,
        @NotBlank String message) {
}
