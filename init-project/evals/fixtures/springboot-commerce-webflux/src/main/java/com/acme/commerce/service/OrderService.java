package com.acme.commerce.service;

import com.acme.commerce.database.OrderRepository;
import com.acme.commerce.database.OrderRepository.OrderRow;
import com.acme.commerce.model.CommerceModels.CancelOrderRequest;
import com.acme.commerce.model.CommerceModels.CreateOrderRequest;
import com.acme.commerce.model.CommerceModels.OrderCancelledEvent;
import com.acme.commerce.model.CommerceModels.OrderCreatedEvent;
import com.acme.commerce.model.CommerceModels.OrderLine;
import com.acme.commerce.model.CommerceModels.OrderView;
import com.acme.commerce.model.CommerceModels.UpdateStatusRequest;
import com.acme.commerce.pubsub.CommerceEventPublisher;
import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;
import org.springframework.data.redis.core.ReactiveRedisTemplate;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
public class OrderService {
    private final OrderRepository orderRepository;
    private final ReactiveRedisTemplate<String, OrderView> orderCache;
    private final CommerceEventPublisher eventPublisher;

    public OrderService(OrderRepository orderRepository, ReactiveRedisTemplate<String, OrderView> orderCache, CommerceEventPublisher eventPublisher) {
        this.orderRepository = orderRepository;
        this.orderCache = orderCache;
        this.eventPublisher = eventPublisher;
    }

    public Flux<OrderView> listOrders() {
        return orderRepository.findAll().map(this::toView);
    }

    public Flux<OrderView> listCustomerOrders(String customerId) {
        return orderRepository.findByCustomerId(customerId).map(this::toView);
    }

    public Mono<OrderView> getOrder(String orderId) {
        return orderCache.opsForValue().get(cacheKey(orderId))
            .switchIfEmpty(orderRepository.findById(orderId).map(this::toView)
                .flatMap(view -> orderCache.opsForValue().set(cacheKey(orderId), view).thenReturn(view)));
    }

    public Mono<OrderView> createOrder(CreateOrderRequest request) {
        var orderId = "ord_" + UUID.randomUUID();
        var total = request.lines().stream().map(this::lineTotal).reduce(BigDecimal.ZERO, BigDecimal::add);
        var row = new OrderRow(orderId, request.customerId(), "DRAFT", total, request.currency(), Instant.now());
        return orderRepository.save(row).map(this::toView);
    }

    public Mono<OrderView> submitOrder(String orderId) {
        return updateStatus(orderId, new UpdateStatusRequest("SUBMITTED", "customer checkout"))
            .flatMap(view -> eventPublisher.publishOrderCreated(new OrderCreatedEvent(view.orderId(), view.customerId(), view.totalAmount(), Instant.now())).thenReturn(view));
    }

    public Mono<OrderView> updateStatus(String orderId, UpdateStatusRequest request) {
        return orderRepository.findById(orderId)
            .map(row -> new OrderRow(row.id(), row.customerId(), request.status(), row.totalAmount(), row.currency(), row.createdAt()))
            .flatMap(orderRepository::save)
            .map(this::toView)
            .flatMap(view -> orderCache.opsForValue().delete(cacheKey(orderId)).thenReturn(view));
    }

    public Mono<OrderView> cancelOrder(String orderId, CancelOrderRequest request) {
        return updateStatus(orderId, new UpdateStatusRequest("CANCELLED", request.reason()))
            .flatMap(view -> eventPublisher.publishOrderCancelled(new OrderCancelledEvent(orderId, request.reason(), Instant.now())).thenReturn(view));
    }

    private BigDecimal lineTotal(OrderLine line) {
        return line.unitPrice().multiply(BigDecimal.valueOf(line.quantity()));
    }

    private OrderView toView(OrderRow row) {
        return new OrderView(row.id(), row.customerId(), row.status(), row.totalAmount(), row.currency());
    }

    private String cacheKey(String orderId) {
        return "orders:" + orderId;
    }
}

