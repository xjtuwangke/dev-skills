/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.service;

import com.acme.skillplayground.mapper.CustomerProfileMapper;
import com.acme.skillplayground.model.customer.CustomerProfileResponse;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class CustomerProfileService {

    private final CustomerProfileMapper mapper;

    public CustomerProfileService(final CustomerProfileMapper mapper) {
        this.mapper = mapper;
    }

    public Mono<CustomerProfileResponse> getProfile(final String customerId) {
        return Mono.fromSupplier(() -> mapper.toProfile(customerId));
    }
}
