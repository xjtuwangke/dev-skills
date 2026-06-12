/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model.returns;

import java.util.UUID;

public record ReturnAuthorizationResponse(
        UUID returnId,
        boolean approved,
        String disposition,
        String reason) {
}
