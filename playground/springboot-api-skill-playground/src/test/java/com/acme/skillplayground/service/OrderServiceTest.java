/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.service;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.acme.skillplayground.database.entity.OrderEntity;
import com.acme.skillplayground.database.repository.OrderRepository;
import com.acme.skillplayground.exception.DomainRuleViolationException;
import com.acme.skillplayground.exception.OrderNotFoundException;
import com.acme.skillplayground.model.CreateOrderRequest;
import com.acme.skillplayground.model.OrderResponse;
import com.acme.skillplayground.model.OrderStatus;
import com.acme.skillplayground.model.ShippingPriority;
import com.acme.skillplayground.pubsub.OrderEventPublisher;
import java.time.Instant;
import java.time.LocalDate;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.mockito.invocation.InvocationOnMock;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @Mock
    private OrderEventPublisher eventPublisher;

    private OrderService orderService;

    @BeforeEach
    void setUp() {
        orderService = new OrderService(orderRepository, eventPublisher);
    }

    @Test
    void createPersistsOrderAndPublishesEvent() {
        final LocalDate requestedShipDate = LocalDate.parse("2026-01-05");
        final CreateOrderRequest request = new CreateOrderRequest(
                "customer-1", "sku-1", 2, ShippingPriority.EXPEDITED, requestedShipDate);
        when(orderRepository.save(any(OrderEntity.class)))
                .thenAnswer((final InvocationOnMock invocation) -> invocation.getArgument(0));
        when(eventPublisher.publishCreated(any(OrderResponse.class))).thenReturn(Mono.empty());

        StepVerifier.create(orderService.create(request))
                .assertNext((final OrderResponse response) -> {
                    assertThat(response.customerId()).isEqualTo("customer-1");
                    assertThat(response.sku()).isEqualTo("sku-1");
                    assertThat(response.quantity()).isEqualTo(2);
                    assertThat(response.shippingPriority()).isEqualTo(ShippingPriority.EXPEDITED);
                    assertThat(response.requestedShipDate()).isEqualTo(requestedShipDate);
                    assertThat(response.manualReviewRequired()).isFalse();
                    assertThat(response.status()).isEqualTo(OrderStatus.CREATED);
                    assertThat(response.id()).isNotNull();
                })
                .verifyComplete();

        verify(orderRepository).save(any(OrderEntity.class));
        verify(eventPublisher).publishCreated(any(OrderResponse.class));
    }

    @Test
    void createDefaultsShippingPriorityAndFlagsManualReview() {
        final CreateOrderRequest request = new CreateOrderRequest("customer-1", "sku-1", 11);
        when(orderRepository.save(any(OrderEntity.class)))
                .thenAnswer((final InvocationOnMock invocation) -> invocation.getArgument(0));
        when(eventPublisher.publishCreated(any(OrderResponse.class))).thenReturn(Mono.empty());

        StepVerifier.create(orderService.create(request))
                .assertNext((final OrderResponse response) -> {
                    assertThat(response.shippingPriority()).isEqualTo(ShippingPriority.STANDARD);
                    assertThat(response.manualReviewRequired()).isTrue();
                })
                .verifyComplete();
    }

    @Test
    void createRejectsExpeditedHazardousSku() {
        final CreateOrderRequest request = new CreateOrderRequest(
                "customer-1", "HAZ-1", 2, ShippingPriority.EXPEDITED, null);

        StepVerifier.create(orderService.create(request))
                .expectError(DomainRuleViolationException.class)
                .verify();

        verify(orderRepository, never()).save(any(OrderEntity.class));
        verify(eventPublisher, never()).publishCreated(any(OrderResponse.class));
    }

    @Test
    void findByIdReturnsExistingOrder() {
        final OrderEntity entity = entity(OrderStatus.ACCEPTED);
        when(orderRepository.findById(eq(entity.getId()))).thenReturn(Optional.of(entity));

        StepVerifier.create(orderService.findById(entity.getId()))
                .expectNextMatches((final OrderResponse response) -> response.status() == OrderStatus.ACCEPTED)
                .verifyComplete();
    }

    @Test
    void findByIdFailsWhenMissing() {
        final UUID id = UUID.randomUUID();
        when(orderRepository.findById(eq(id))).thenReturn(Optional.empty());

        StepVerifier.create(orderService.findById(id))
                .expectError(OrderNotFoundException.class)
                .verify();
    }

    @Test
    void findByCustomerReturnsRepositoryResults() {
        final OrderEntity entity = entity(OrderStatus.FULFILLED);
        when(orderRepository.findByCustomerId(eq("customer-1"))).thenReturn(List.of(entity));

        StepVerifier.create(orderService.findByCustomerId("customer-1"))
                .expectNextMatches((final OrderResponse response) -> response.id().equals(entity.getId()))
                .verifyComplete();
    }

    @Test
    void updateStatusPersistsAndPublishesStatusEvent() {
        final OrderEntity entity = entity(OrderStatus.CREATED);
        when(orderRepository.findById(eq(entity.getId()))).thenReturn(Optional.of(entity));
        when(orderRepository.save(any(OrderEntity.class)))
                .thenAnswer((final InvocationOnMock invocation) -> invocation.getArgument(0));
        when(eventPublisher.publishStatusChanged(any(OrderResponse.class))).thenReturn(Mono.empty());

        StepVerifier.create(orderService.updateStatus(entity.getId(), OrderStatus.CANCELLED))
                .expectNextMatches((final OrderResponse response) -> response.status() == OrderStatus.CANCELLED)
                .verifyComplete();

        verify(orderRepository).save(any(OrderEntity.class));
        verify(eventPublisher).publishStatusChanged(any(OrderResponse.class));
    }

    private OrderEntity entity(final OrderStatus status) {
        final Instant now = Instant.parse("2026-01-01T00:00:00Z");
        final OrderEntity entity = new OrderEntity();
        entity.setId(UUID.randomUUID());
        entity.setCustomerId("customer-1");
        entity.setSku("sku-1");
        entity.setQuantity(2);
        entity.setShippingPriority(ShippingPriority.STANDARD);
        entity.setManualReviewRequired(false);
        entity.setStatus(status);
        entity.setCreatedAt(now);
        entity.setUpdatedAt(now);
        return entity;
    }
}
