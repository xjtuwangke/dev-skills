/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.endpoint;

import com.acme.skillplayground.model.CreateOrderRequest;
import com.acme.skillplayground.model.OrderResponse;
import com.acme.skillplayground.model.UpdateOrderStatusRequest;
import com.acme.skillplayground.service.OrderUseCase;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import java.net.URI;
import java.util.List;
import java.util.UUID;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/orders")
@Validated
@Tag(name = "Orders")
public class OrderEndpoint {

    private final OrderUseCase orderUseCase;

    public OrderEndpoint(final OrderUseCase orderUseCase) {
        this.orderUseCase = orderUseCase;
    }

    @PostMapping
    @Operation(summary = "Create an order")
    public Mono<ResponseEntity<OrderResponse>> create(@Valid @RequestBody final CreateOrderRequest request) {
        return orderUseCase.create(request)
                .map((final OrderResponse response) -> ResponseEntity.created(location(response)).body(response));
    }

    @GetMapping("/{id}")
    @Operation(summary = "Get an order by id")
    public Mono<OrderResponse> getById(@PathVariable final UUID id) {
        return orderUseCase.findById(id);
    }

    @GetMapping("/customers/{customerId}")
    @Operation(summary = "List orders by customer id")
    public Mono<List<OrderResponse>> listByCustomer(@PathVariable final String customerId) {
        return orderUseCase.findByCustomerId(customerId).collectList();
    }

    @PatchMapping("/{id}/status")
    @Operation(summary = "Update order status")
    public Mono<OrderResponse> updateStatus(
            @PathVariable final UUID id,
            @Valid @RequestBody final UpdateOrderStatusRequest request) {
        return orderUseCase.updateStatus(id, request.status());
    }

    private URI location(final OrderResponse response) {
        return URI.create("/api/orders/" + response.id());
    }
}
