package com.acme.commerce.model;

import java.math.BigDecimal;
import java.time.Instant;
import java.util.List;
import java.util.Map;

public final class CommerceModels {
    private CommerceModels() {}

    public record CreateOrderRequest(String customerId, List<OrderLine> lines, String currency) {}
    public record OrderLine(String sku, int quantity, BigDecimal unitPrice) {}
    public record OrderView(String orderId, String customerId, String status, BigDecimal totalAmount, String currency) {}
    public record UpdateStatusRequest(String status, String reason) {}
    public record CancelOrderRequest(String reason, boolean releaseInventory) {}
    public record CustomerView(String customerId, String email, String loyaltyTier, int riskScore) {}
    public record ReserveInventoryRequest(String orderId, String sku, int quantity) {}
    public record InventoryReservationView(String reservationId, String orderId, String sku, int quantity, String status) {}
    public record AuthorizePaymentRequest(String orderId, BigDecimal amount, String currency, String token) {}
    public record PaymentView(String paymentId, String orderId, String status, BigDecimal amount, String providerRef) {}
    public record FulfillmentPlanRequest(String orderId, String warehouseCode, String deliveryPromise) {}
    public record FulfillmentPlanView(String planId, String orderId, String warehouseCode, String status) {}
    public record CreateShipmentRequest(String orderId, String carrier, String addressId) {}
    public record ShipmentView(String shipmentId, String orderId, String carrier, String trackingNumber, String status) {}
    public record CreateReturnRequest(String orderId, List<String> skus, String reason) {}
    public record ReturnView(String returnId, String orderId, String status, String reason) {}
    public record ReconciliationRequest(String businessDate, List<String> domains) {}
    public record ReconciliationJobView(String jobId, String businessDate, String status, Map<String, Integer> counts) {}
    public record DomainEventView(String eventId, String aggregateId, String type, Instant occurredAt, Map<String, Object> payload) {}
    public record OrderCreatedEvent(String orderId, String customerId, BigDecimal totalAmount, Instant occurredAt) {}
    public record OrderCancelledEvent(String orderId, String reason, Instant occurredAt) {}
    public record PaymentAuthorizedEvent(String paymentId, String orderId, BigDecimal amount, Instant occurredAt) {}
    public record InventoryReservedEvent(String reservationId, String orderId, String sku, int quantity, Instant occurredAt) {}
    public record ShipmentUpdatedEvent(String shipmentId, String orderId, String status, Instant occurredAt) {}
}

