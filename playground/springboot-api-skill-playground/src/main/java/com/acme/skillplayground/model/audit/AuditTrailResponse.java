/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.model.audit;

import java.time.Instant;
import java.util.List;
import java.util.UUID;

public record AuditTrailResponse(
        UUID subjectId,
        String subjectType,
        List<String> events,
        Instant generatedAt) {
}
