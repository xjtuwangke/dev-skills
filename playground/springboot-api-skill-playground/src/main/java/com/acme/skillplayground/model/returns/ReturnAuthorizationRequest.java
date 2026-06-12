/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model.returns;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Positive;
import java.util.UUID;

public record ReturnAuthorizationRequest(
        UUID orderId,
        @NotBlank String sku,
        @Positive int quantity,
        @NotBlank String reasonCode) {
}
