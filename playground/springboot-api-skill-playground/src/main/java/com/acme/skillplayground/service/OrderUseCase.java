/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.service;

import com.acme.skillplayground.model.CreateOrderRequest;
import com.acme.skillplayground.model.OrderResponse;
import com.acme.skillplayground.model.OrderStatus;
import java.util.UUID;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

public interface OrderUseCase {

    Mono<OrderResponse> create(final CreateOrderRequest request);

    Mono<OrderResponse> findById(final UUID id);

    Flux<OrderResponse> findByCustomerId(final String customerId);

    Mono<OrderResponse> updateStatus(final UUID id, final OrderStatus status);
}
