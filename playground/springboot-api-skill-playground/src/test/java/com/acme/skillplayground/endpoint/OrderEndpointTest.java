/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.endpoint;

import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.acme.skillplayground.exception.ApiExceptionHandler;
import com.acme.skillplayground.exception.DomainRuleViolationException;
import com.acme.skillplayground.exception.OrderNotFoundException;
import com.acme.skillplayground.model.CreateOrderRequest;
import com.acme.skillplayground.model.OrderResponse;
import com.acme.skillplayground.model.OrderStatus;
import com.acme.skillplayground.model.ShippingPriority;
import com.acme.skillplayground.model.UpdateOrderStatusRequest;
import com.acme.skillplayground.service.OrderUseCase;
import java.time.Instant;
import java.time.LocalDate;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.MediaType;
import org.springframework.test.web.reactive.server.WebTestClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

class OrderEndpointTest {

    private OrderUseCase orderUseCase;
    private WebTestClient webTestClient;

    @BeforeEach
    void setUp() {
        orderUseCase = mock(OrderUseCase.class);
        webTestClient = WebTestClient.bindToController(new OrderEndpoint(orderUseCase))
                .controllerAdvice(new ApiExceptionHandler())
                .build();
    }

    @Test
    void createReturnsCreatedOrder() {
        final LocalDate requestedShipDate = LocalDate.parse("2026-01-05");
        final CreateOrderRequest request = new CreateOrderRequest(
                "customer-1", "sku-1", 2, ShippingPriority.EXPEDITED, requestedShipDate);
        final OrderResponse response = response(OrderStatus.CREATED, ShippingPriority.EXPEDITED, requestedShipDate,
                false);
        when(orderUseCase.create(eq(request))).thenReturn(Mono.just(response));

        webTestClient.post()
                .uri("/api/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue("{\"customerId\":\"customer-1\",\"sku\":\"sku-1\",\"quantity\":2,"
                        + "\"shippingPriority\":\"EXPEDITED\",\"requestedShipDate\":\"2026-01-05\"}")
                .exchange()
                .expectStatus().isCreated()
                .expectHeader().valueEquals("Location", "/api/orders/" + response.id())
                .expectBody()
                .jsonPath("$.id").isEqualTo(response.id().toString())
                .jsonPath("$.shippingPriority").isEqualTo("EXPEDITED")
                .jsonPath("$.requestedShipDate").isEqualTo("2026-01-05")
                .jsonPath("$.manualReviewRequired").isEqualTo(false)
                .jsonPath("$.status").isEqualTo("CREATED");
    }

    @Test
    void createMapsDomainRuleViolation() {
        final CreateOrderRequest request = new CreateOrderRequest(
                "customer-1", "HAZ-1", 2, ShippingPriority.EXPEDITED, null);
        when(orderUseCase.create(eq(request))).thenReturn(Mono.error(
                new DomainRuleViolationException("Expedited shipping is not available for hazardous SKUs")));

        webTestClient.post()
                .uri("/api/orders")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue("{\"customerId\":\"customer-1\",\"sku\":\"HAZ-1\",\"quantity\":2,"
                        + "\"shippingPriority\":\"EXPEDITED\"}")
                .exchange()
                .expectStatus().isEqualTo(422)
                .expectBody()
                .jsonPath("$.title").isEqualTo("Domain rule violation");
    }

    @Test
    void getByIdReturnsOrder() {
        final OrderResponse response = response(OrderStatus.ACCEPTED);
        when(orderUseCase.findById(eq(response.id()))).thenReturn(Mono.just(response));

        webTestClient.get()
                .uri("/api/orders/{id}", response.id())
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.id").isEqualTo(response.id().toString())
                .jsonPath("$.status").isEqualTo("ACCEPTED");
    }

    @Test
    void getByIdMapsNotFound() {
        final UUID id = UUID.randomUUID();
        when(orderUseCase.findById(eq(id))).thenReturn(Mono.error(new OrderNotFoundException(id)));

        webTestClient.get()
                .uri("/api/orders/{id}", id)
                .exchange()
                .expectStatus().isNotFound()
                .expectBody()
                .jsonPath("$.title").isEqualTo("Order not found");
    }

    @Test
    void listByCustomerReturnsOrders() {
        final OrderResponse response = response(OrderStatus.FULFILLED);
        when(orderUseCase.findByCustomerId(eq("customer-1"))).thenReturn(Flux.just(response));

        webTestClient.get()
                .uri("/api/orders/customers/{customerId}", "customer-1")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$[0].id").isEqualTo(response.id().toString());
    }

    @Test
    void updateStatusReturnsUpdatedOrder() {
        final OrderResponse response = response(OrderStatus.CANCELLED);
        final UpdateOrderStatusRequest request = new UpdateOrderStatusRequest(OrderStatus.CANCELLED);
        when(orderUseCase.updateStatus(eq(response.id()), eq(OrderStatus.CANCELLED))).thenReturn(Mono.just(response));

        webTestClient.patch()
                .uri("/api/orders/{id}/status", response.id())
                .bodyValue(request)
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.status").isEqualTo("CANCELLED");
    }

    private OrderResponse response(final OrderStatus status) {
        return response(status, ShippingPriority.STANDARD, null, false);
    }

    private OrderResponse response(
            final OrderStatus status,
            final ShippingPriority shippingPriority,
            final LocalDate requestedShipDate,
            final boolean manualReviewRequired) {
        final UUID id = UUID.randomUUID();
        final Instant now = Instant.parse("2026-01-01T00:00:00Z");
        return new OrderResponse(
                id,
                "customer-1",
                "sku-1",
                2,
                shippingPriority,
                requestedShipDate,
                manualReviewRequired,
                status,
                now,
                now);
    }
}
