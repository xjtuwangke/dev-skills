/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.service;

import com.acme.skillplayground.model.returns.ReturnAuthorizationRequest;
import com.acme.skillplayground.model.returns.ReturnAuthorizationResponse;
import java.util.UUID;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class ReturnPolicyService {

    public Mono<ReturnAuthorizationResponse> authorize(final ReturnAuthorizationRequest request) {
        return Mono.fromSupplier(() -> {
            if ("FRAUD".equalsIgnoreCase(request.reasonCode())) {
                return new ReturnAuthorizationResponse(UUID.randomUUID(), false, "REVIEW", "manual fraud review");
            }
            if (request.sku().startsWith("HZ")) {
                return new ReturnAuthorizationResponse(UUID.randomUUID(), true, "SPECIAL_HANDLING", "hazmat return");
            }
            return new ReturnAuthorizationResponse(UUID.randomUUID(), true, "RESTOCK", "standard return");
        });
    }
}
