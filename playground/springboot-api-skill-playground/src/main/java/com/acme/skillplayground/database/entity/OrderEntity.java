/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.database.entity;

import com.acme.skillplayground.model.CreateOrderRequest;
import com.acme.skillplayground.model.OrderStatus;
import com.acme.skillplayground.model.ShippingPriority;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.PrePersist;
import jakarta.persistence.PreUpdate;
import jakarta.persistence.Table;
import java.time.Instant;
import java.time.LocalDate;
import java.util.UUID;

@Entity
@Table(name = "orders")
public class OrderEntity {

    @Id
    @Column(nullable = false)
    private UUID id;

    @Column(nullable = false, length = 64)
    private String customerId;

    @Column(nullable = false, length = 64)
    private String sku;

    @Column(nullable = false)
    private int quantity;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 32)
    private ShippingPriority shippingPriority;

    private LocalDate requestedShipDate;

    @Column(nullable = false)
    private boolean manualReviewRequired;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 32)
    private OrderStatus status;

    @Column(nullable = false)
    private Instant createdAt;

    @Column(nullable = false)
    private Instant updatedAt;

    public static OrderEntity create(final CreateOrderRequest request) {
        return create(request, request.quantity() > 10);
    }

    public static OrderEntity create(final CreateOrderRequest request, final boolean manualReviewRequired) {
        final Instant now = Instant.now();
        final OrderEntity entity = new OrderEntity();
        entity.setId(UUID.randomUUID());
        entity.setCustomerId(request.customerId());
        entity.setSku(request.sku());
        entity.setQuantity(request.quantity());
        entity.setShippingPriority(request.resolvedShippingPriority());
        entity.setRequestedShipDate(request.requestedShipDate());
        entity.setManualReviewRequired(manualReviewRequired);
        entity.setStatus(OrderStatus.CREATED);
        entity.setCreatedAt(now);
        entity.setUpdatedAt(now);
        return entity;
    }

    @PrePersist
    public void prePersist() {
        final Instant now = Instant.now();
        if (id == null) {
            id = UUID.randomUUID();
        }
        if (status == null) {
            status = OrderStatus.CREATED;
        }
        if (shippingPriority == null) {
            shippingPriority = ShippingPriority.STANDARD;
        }
        if (createdAt == null) {
            createdAt = now;
        }
        updatedAt = now;
    }

    @PreUpdate
    public void preUpdate() {
        updatedAt = Instant.now();
    }

    public UUID getId() {
        return id;
    }

    public void setId(final UUID id) {
        this.id = id;
    }

    public String getCustomerId() {
        return customerId;
    }

    public void setCustomerId(final String customerId) {
        this.customerId = customerId;
    }

    public String getSku() {
        return sku;
    }

    public void setSku(final String sku) {
        this.sku = sku;
    }

    public int getQuantity() {
        return quantity;
    }

    public void setQuantity(final int quantity) {
        this.quantity = quantity;
    }

    public ShippingPriority getShippingPriority() {
        return shippingPriority;
    }

    public void setShippingPriority(final ShippingPriority shippingPriority) {
        this.shippingPriority = shippingPriority;
    }

    public LocalDate getRequestedShipDate() {
        return requestedShipDate;
    }

    public void setRequestedShipDate(final LocalDate requestedShipDate) {
        this.requestedShipDate = requestedShipDate;
    }

    public boolean isManualReviewRequired() {
        return manualReviewRequired;
    }

    public void setManualReviewRequired(final boolean manualReviewRequired) {
        this.manualReviewRequired = manualReviewRequired;
    }

    public OrderStatus getStatus() {
        return status;
    }

    public void setStatus(final OrderStatus status) {
        this.status = status;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(final Instant createdAt) {
        this.createdAt = createdAt;
    }

    public Instant getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(final Instant updatedAt) {
        this.updatedAt = updatedAt;
    }
}
