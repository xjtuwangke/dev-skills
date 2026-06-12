/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.service;

import com.acme.skillplayground.database.entity.OrderEntity;
import com.acme.skillplayground.database.repository.OrderRepository;
import com.acme.skillplayground.exception.DomainRuleViolationException;
import com.acme.skillplayground.exception.OrderNotFoundException;
import com.acme.skillplayground.model.CreateOrderRequest;
import com.acme.skillplayground.model.OrderResponse;
import com.acme.skillplayground.model.OrderStatus;
import com.acme.skillplayground.model.ShippingPriority;
import com.acme.skillplayground.pubsub.OrderEventPublisher;
import java.util.List;
import java.util.UUID;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

@Service
public class OrderService implements OrderUseCase {

    private final OrderRepository orderRepository;
    private final OrderEventPublisher eventPublisher;

    public OrderService(final OrderRepository orderRepository, final OrderEventPublisher eventPublisher) {
        this.orderRepository = orderRepository;
        this.eventPublisher = eventPublisher;
    }

    @Override
    public Mono<OrderResponse> create(final CreateOrderRequest request) {
        return Mono.fromCallable(() -> {
            validateCreateRequest(request);
            return orderRepository.save(OrderEntity.create(request, requiresManualReview(request)));
        })
                .subscribeOn(Schedulers.boundedElastic())
                .map(this::toResponse)
                .flatMap((final OrderResponse response) -> eventPublisher.publishCreated(response).thenReturn(response));
    }

    @Override
    public Mono<OrderResponse> findById(final UUID id) {
        return Mono.fromCallable(() -> orderRepository.findById(id).orElseThrow(() -> new OrderNotFoundException(id)))
                .subscribeOn(Schedulers.boundedElastic())
                .map(this::toResponse);
    }

    @Override
    public Flux<OrderResponse> findByCustomerId(final String customerId) {
        return Mono.fromCallable(() -> orderRepository.findByCustomerId(customerId))
                .subscribeOn(Schedulers.boundedElastic())
                .flatMapMany((final List<OrderEntity> orders) -> Flux.fromIterable(orders).map(this::toResponse));
    }

    @Override
    public Mono<OrderResponse> updateStatus(final UUID id, final OrderStatus status) {
        return Mono.fromCallable(() -> {
            final OrderEntity entity = orderRepository.findById(id).orElseThrow(() -> new OrderNotFoundException(id));
            entity.setStatus(status);
            return orderRepository.save(entity);
        })
                .subscribeOn(Schedulers.boundedElastic())
                .map(this::toResponse)
                .flatMap((final OrderResponse response) -> eventPublisher.publishStatusChanged(response)
                        .thenReturn(response));
    }

    private OrderResponse toResponse(final OrderEntity entity) {
        return new OrderResponse(
                entity.getId(),
                entity.getCustomerId(),
                entity.getSku(),
                entity.getQuantity(),
                entity.getShippingPriority(),
                entity.getRequestedShipDate(),
                entity.isManualReviewRequired(),
                entity.getStatus(),
                entity.getCreatedAt(),
                entity.getUpdatedAt());
    }

    private void validateCreateRequest(final CreateOrderRequest request) {
        if (request.resolvedShippingPriority() == ShippingPriority.EXPEDITED && request.sku().startsWith("HAZ-")) {
            throw new DomainRuleViolationException("Expedited shipping is not available for hazardous SKUs");
        }
    }

    private boolean requiresManualReview(final CreateOrderRequest request) {
        return request.quantity() > 10;
    }
}
