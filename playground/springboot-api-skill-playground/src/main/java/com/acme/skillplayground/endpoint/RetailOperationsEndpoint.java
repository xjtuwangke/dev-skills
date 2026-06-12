/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.endpoint;

import com.acme.skillplayground.model.audit.AuditTrailResponse;
import com.acme.skillplayground.model.catalog.CatalogItemResponse;
import com.acme.skillplayground.model.customer.CustomerProfileResponse;
import com.acme.skillplayground.model.fulfillment.ShipmentPlanRequest;
import com.acme.skillplayground.model.fulfillment.ShipmentPlanResponse;
import com.acme.skillplayground.model.inventory.InventoryReservationRequest;
import com.acme.skillplayground.model.inventory.InventoryReservationResponse;
import com.acme.skillplayground.model.payment.PaymentAuthorizationRequest;
import com.acme.skillplayground.model.payment.PaymentAuthorizationResponse;
import com.acme.skillplayground.model.pricing.PriceQuoteRequest;
import com.acme.skillplayground.model.pricing.PriceQuoteResponse;
import com.acme.skillplayground.model.promotion.PromotionDecisionResponse;
import com.acme.skillplayground.model.returns.ReturnAuthorizationRequest;
import com.acme.skillplayground.model.returns.ReturnAuthorizationResponse;
import com.acme.skillplayground.model.support.CreateTicketRequest;
import com.acme.skillplayground.model.support.TicketResponse;
import com.acme.skillplayground.service.AuditTrailService;
import com.acme.skillplayground.service.CatalogQueryService;
import com.acme.skillplayground.service.CustomerProfileService;
import com.acme.skillplayground.service.FulfillmentPlanningService;
import com.acme.skillplayground.service.InventoryReservationService;
import com.acme.skillplayground.service.PaymentAuthorizationService;
import com.acme.skillplayground.service.PricingService;
import com.acme.skillplayground.service.PromotionService;
import com.acme.skillplayground.service.ReturnPolicyService;
import com.acme.skillplayground.service.SupportTicketService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import jakarta.validation.Valid;
import java.util.UUID;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/retail")
@Tag(name = "Retail operations")
public class RetailOperationsEndpoint {

    private final CustomerProfileService customerProfileService;
    private final CatalogQueryService catalogQueryService;
    private final InventoryReservationService inventoryReservationService;
    private final PricingService pricingService;
    private final PromotionService promotionService;
    private final PaymentAuthorizationService paymentAuthorizationService;
    private final FulfillmentPlanningService fulfillmentPlanningService;
    private final ReturnPolicyService returnPolicyService;
    private final SupportTicketService supportTicketService;
    private final AuditTrailService auditTrailService;

    public RetailOperationsEndpoint(
            final CustomerProfileService customerProfileService,
            final CatalogQueryService catalogQueryService,
            final InventoryReservationService inventoryReservationService,
            final PricingService pricingService,
            final PromotionService promotionService,
            final PaymentAuthorizationService paymentAuthorizationService,
            final FulfillmentPlanningService fulfillmentPlanningService,
            final ReturnPolicyService returnPolicyService,
            final SupportTicketService supportTicketService,
            final AuditTrailService auditTrailService) {
        this.customerProfileService = customerProfileService;
        this.catalogQueryService = catalogQueryService;
        this.inventoryReservationService = inventoryReservationService;
        this.pricingService = pricingService;
        this.promotionService = promotionService;
        this.paymentAuthorizationService = paymentAuthorizationService;
        this.fulfillmentPlanningService = fulfillmentPlanningService;
        this.returnPolicyService = returnPolicyService;
        this.supportTicketService = supportTicketService;
        this.auditTrailService = auditTrailService;
    }

    @GetMapping("/customers/{customerId}/profile")
    @Operation(summary = "Get a customer profile")
    public Mono<CustomerProfileResponse> getCustomerProfile(@PathVariable final String customerId) {
        return customerProfileService.getProfile(customerId);
    }

    @GetMapping("/catalog/items/{sku}")
    @Operation(summary = "Get a catalog item")
    public Mono<CatalogItemResponse> getCatalogItem(@PathVariable final String sku) {
        return catalogQueryService.getItem(sku);
    }

    @PostMapping("/inventory/reservations")
    @Operation(summary = "Reserve inventory")
    public Mono<InventoryReservationResponse> reserveInventory(
            @Valid @RequestBody final InventoryReservationRequest request) {
        return inventoryReservationService.reserve(request);
    }

    @PostMapping("/pricing/quotes")
    @Operation(summary = "Create a price quote")
    public Mono<PriceQuoteResponse> quotePrice(@Valid @RequestBody final PriceQuoteRequest request) {
        return pricingService.quote(request);
    }

    @GetMapping("/promotions/{couponCode}/eligibility")
    @Operation(summary = "Evaluate promotion eligibility")
    public Mono<PromotionDecisionResponse> evaluatePromotion(
            @PathVariable final String couponCode,
            @RequestParam final String customerId,
            @RequestParam final String sku) {
        return promotionService.evaluate(couponCode, customerId, sku);
    }

    @PostMapping("/payments/authorizations")
    @Operation(summary = "Authorize a payment")
    public Mono<PaymentAuthorizationResponse> authorizePayment(
            @Valid @RequestBody final PaymentAuthorizationRequest request) {
        return paymentAuthorizationService.authorize(request);
    }

    @PostMapping("/fulfillment/plans")
    @Operation(summary = "Plan a shipment")
    public Mono<ShipmentPlanResponse> planShipment(@Valid @RequestBody final ShipmentPlanRequest request) {
        return fulfillmentPlanningService.plan(request);
    }

    @PostMapping("/returns/authorizations")
    @Operation(summary = "Authorize a return")
    public Mono<ReturnAuthorizationResponse> authorizeReturn(
            @Valid @RequestBody final ReturnAuthorizationRequest request) {
        return returnPolicyService.authorize(request);
    }

    @PostMapping("/support/tickets")
    @Operation(summary = "Create a support ticket")
    public Mono<TicketResponse> createTicket(@Valid @RequestBody final CreateTicketRequest request) {
        return supportTicketService.create(request);
    }

    @GetMapping("/audit/orders/{orderId}")
    @Operation(summary = "Get order audit trail")
    public Mono<AuditTrailResponse> getOrderAuditTrail(@PathVariable final UUID orderId) {
        return auditTrailService.orderTrail(orderId);
    }
}
