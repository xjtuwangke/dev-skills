/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.endpoint;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;

import com.acme.skillplayground.exception.ApiExceptionHandler;
import com.acme.skillplayground.exception.DomainRuleViolationException;
import com.acme.skillplayground.exception.ResourceConflictException;
import com.acme.skillplayground.model.audit.AuditTrailResponse;
import com.acme.skillplayground.model.catalog.CatalogItemResponse;
import com.acme.skillplayground.model.catalog.ProductStatus;
import com.acme.skillplayground.model.customer.CustomerProfileResponse;
import com.acme.skillplayground.model.customer.CustomerSegment;
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
import java.math.BigDecimal;
import java.time.Instant;
import java.time.LocalDate;
import java.util.List;
import java.util.UUID;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.MediaType;
import org.springframework.test.web.reactive.server.WebTestClient;
import reactor.core.publisher.Mono;

@ExtendWith(MockitoExtension.class)
class RetailOperationsEndpointTest {

    @Mock
    private CustomerProfileService customerProfileService;

    @Mock
    private CatalogQueryService catalogQueryService;

    @Mock
    private InventoryReservationService inventoryReservationService;

    @Mock
    private PricingService pricingService;

    @Mock
    private PromotionService promotionService;

    @Mock
    private PaymentAuthorizationService paymentAuthorizationService;

    @Mock
    private FulfillmentPlanningService fulfillmentPlanningService;

    @Mock
    private ReturnPolicyService returnPolicyService;

    @Mock
    private SupportTicketService supportTicketService;

    @Mock
    private AuditTrailService auditTrailService;

    private WebTestClient webTestClient;

    @BeforeEach
    void setUp() {
        final RetailOperationsEndpoint endpoint = new RetailOperationsEndpoint(
                customerProfileService,
                catalogQueryService,
                inventoryReservationService,
                pricingService,
                promotionService,
                paymentAuthorizationService,
                fulfillmentPlanningService,
                returnPolicyService,
                supportTicketService,
                auditTrailService);
        webTestClient = WebTestClient.bindToController(endpoint)
                .controllerAdvice(new ApiExceptionHandler())
                .build();
    }

    @Test
    void routesCustomerCatalogPromotionAndAuditReads() {
        final UUID orderId = UUID.randomUUID();
        when(customerProfileService.getProfile(eq("customer-1"))).thenReturn(Mono.just(new CustomerProfileResponse(
                "customer-1",
                "Customer customer-1",
                CustomerSegment.GOLD,
                "USD",
                4200,
                Instant.parse("2026-01-01T00:00:00Z"))));
        when(catalogQueryService.getItem(eq("SKU-1"))).thenReturn(Mono.just(new CatalogItemResponse(
                "SKU-1",
                "Retail item",
                "general",
                ProductStatus.ACTIVE,
                new BigDecimal("49.99"),
                "USD",
                false)));
        when(promotionService.evaluate(eq("SAVE20"), eq("customer-1"), eq("SKU-1")))
                .thenReturn(Mono.just(new PromotionDecisionResponse("SAVE20", true, new BigDecimal("20.00"), "ok")));
        when(auditTrailService.orderTrail(eq(orderId))).thenReturn(Mono.just(new AuditTrailResponse(
                orderId,
                "ORDER",
                List.of("ORDER_CREATED"),
                Instant.parse("2026-01-01T00:00:00Z"))));

        webTestClient.get().uri("/api/retail/customers/customer-1/profile")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.segment").isEqualTo("GOLD");

        webTestClient.get().uri("/api/retail/catalog/items/SKU-1")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.sku").isEqualTo("SKU-1");

        webTestClient.get().uri("/api/retail/promotions/SAVE20/eligibility?customerId=customer-1&sku=SKU-1")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.eligible").isEqualTo(true);

        webTestClient.get().uri("/api/retail/audit/orders/{orderId}", orderId)
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.subjectType").isEqualTo("ORDER");
    }

    @Test
    void routesWriteOperations() {
        final UUID orderId = UUID.randomUUID();
        when(inventoryReservationService.reserve(any(InventoryReservationRequest.class)))
                .thenReturn(Mono.just(new InventoryReservationResponse(UUID.randomUUID(), "SKU-1", "FC-001", 2,
                        "RESERVED")));
        when(pricingService.quote(any(PriceQuoteRequest.class))).thenReturn(Mono.just(new PriceQuoteResponse(
                "SKU-1",
                2,
                new BigDecimal("99.98"),
                new BigDecimal("20.00"),
                new BigDecimal("6.60"),
                new BigDecimal("86.58"),
                "USD",
                "DISCOUNTED")));
        when(paymentAuthorizationService.authorize(any(PaymentAuthorizationRequest.class)))
                .thenReturn(Mono.just(new PaymentAuthorizationResponse(UUID.randomUUID(), true, "AUTH-TOK1",
                        "approved")));
        when(fulfillmentPlanningService.plan(any(ShipmentPlanRequest.class))).thenReturn(Mono.just(
                new ShipmentPlanResponse(UUID.randomUUID(), "DFW-01", "ACME-PARCEL", "GROUND",
                        LocalDate.parse("2026-02-04"))));
        when(returnPolicyService.authorize(any(ReturnAuthorizationRequest.class))).thenReturn(Mono.just(
                new ReturnAuthorizationResponse(UUID.randomUUID(), true, "RESTOCK", "standard return")));
        when(supportTicketService.create(any(CreateTicketRequest.class))).thenReturn(Mono.just(
                new TicketResponse(UUID.randomUUID(), "customer-1", "OPEN", "NORMAL",
                        Instant.parse("2026-01-01T00:00:00Z"))));

        webTestClient.post().uri("/api/retail/inventory/reservations")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue("{\"orderId\":\"" + orderId + "\",\"sku\":\"SKU-1\",\"quantity\":2}")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.status").isEqualTo("RESERVED");

        webTestClient.post().uri("/api/retail/pricing/quotes")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue("{\"customerId\":\"customer-1\",\"sku\":\"SKU-1\",\"quantity\":2,\"couponCode\":\"SAVE20\"}")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.priceRule").isEqualTo("DISCOUNTED");

        webTestClient.post().uri("/api/retail/payments/authorizations")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue("{\"orderId\":\"" + orderId
                        + "\",\"amount\":86.58,\"currency\":\"USD\",\"paymentToken\":\"tok1_abc\"}")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.authorized").isEqualTo(true);

        webTestClient.post().uri("/api/retail/fulfillment/plans")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue("{\"orderId\":\"" + orderId + "\",\"postalCode\":\"75001\",\"sku\":\"SKU-1\","
                        + "\"quantity\":2}")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.warehouseCode").isEqualTo("DFW-01");

        webTestClient.post().uri("/api/retail/returns/authorizations")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue("{\"orderId\":\"" + orderId + "\",\"sku\":\"SKU-1\",\"quantity\":1,"
                        + "\"reasonCode\":\"DAMAGED\"}")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.approved").isEqualTo(true);

        webTestClient.post().uri("/api/retail/support/tickets")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue("{\"customerId\":\"customer-1\",\"orderId\":\"" + orderId
                        + "\",\"subject\":\"Where is order\",\"message\":\"Please help\"}")
                .exchange()
                .expectStatus().isOk()
                .expectBody()
                .jsonPath("$.status").isEqualTo("OPEN");
    }

    @Test
    void mapsDomainErrorsToProblemDetails() {
        when(inventoryReservationService.reserve(any(InventoryReservationRequest.class)))
                .thenReturn(Mono.error(new ResourceConflictException("Insufficient inventory")));
        when(paymentAuthorizationService.authorize(any(PaymentAuthorizationRequest.class)))
                .thenReturn(Mono.error(new DomainRuleViolationException("Unsupported payment currency EUR")));

        webTestClient.post().uri("/api/retail/inventory/reservations")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue("{\"orderId\":\"" + UUID.randomUUID() + "\",\"sku\":\"LOW-1\",\"quantity\":2}")
                .exchange()
                .expectStatus().isEqualTo(409)
                .expectBody()
                .jsonPath("$.title").isEqualTo("Resource conflict");

        webTestClient.post().uri("/api/retail/payments/authorizations")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue("{\"orderId\":\"" + UUID.randomUUID()
                        + "\",\"amount\":10.00,\"currency\":\"EUR\",\"paymentToken\":\"tok1_abc\"}")
                .exchange()
                .expectStatus().isEqualTo(422)
                .expectBody()
                .jsonPath("$.title").isEqualTo("Domain rule violation");
    }
}
