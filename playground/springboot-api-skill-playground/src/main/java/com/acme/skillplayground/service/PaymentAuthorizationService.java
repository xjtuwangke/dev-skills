/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.service;

import com.acme.skillplayground.exception.DomainRuleViolationException;
import com.acme.skillplayground.model.payment.PaymentAuthorizationRequest;
import com.acme.skillplayground.model.payment.PaymentAuthorizationResponse;
import java.math.BigDecimal;
import java.util.UUID;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class PaymentAuthorizationService {

    private static final BigDecimal MANUAL_REVIEW_LIMIT = new BigDecimal("5000.00");

    public Mono<PaymentAuthorizationResponse> authorize(final PaymentAuthorizationRequest request) {
        return Mono.fromSupplier(() -> {
            if (!"USD".equals(request.currency())) {
                throw new DomainRuleViolationException("Unsupported payment currency " + request.currency());
            }
            if (request.amount().compareTo(MANUAL_REVIEW_LIMIT) > 0) {
                return new PaymentAuthorizationResponse(UUID.randomUUID(), false, null, "manual review required");
            }
            return new PaymentAuthorizationResponse(
                    UUID.randomUUID(),
                    true,
                    "AUTH-" + request.paymentToken().substring(0, 4).toUpperCase(),
                    "approved");
        });
    }
}
