/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.service;

import static org.assertj.core.api.Assertions.assertThat;

import com.acme.skillplayground.exception.DomainRuleViolationException;
import com.acme.skillplayground.exception.ResourceConflictException;
import com.acme.skillplayground.mapper.CatalogMapper;
import com.acme.skillplayground.mapper.CustomerProfileMapper;
import com.acme.skillplayground.mapper.FulfillmentMapper;
import com.acme.skillplayground.mapper.MoneyMapper;
import com.acme.skillplayground.model.fulfillment.ShipmentPlanRequest;
import com.acme.skillplayground.model.inventory.InventoryReservationRequest;
import com.acme.skillplayground.model.payment.PaymentAuthorizationRequest;
import com.acme.skillplayground.model.pricing.PriceQuoteRequest;
import com.acme.skillplayground.model.returns.ReturnAuthorizationRequest;
import com.acme.skillplayground.model.support.CreateTicketRequest;
import java.math.BigDecimal;
import java.time.Clock;
import java.time.Instant;
import java.time.ZoneOffset;
import java.util.UUID;
import org.junit.jupiter.api.Test;
import reactor.test.StepVerifier;

class RetailDomainServicesTest {

    private static final Clock CLOCK = Clock.fixed(Instant.parse("2026-02-03T04:05:06Z"), ZoneOffset.UTC);

    @Test
    void customerAndCatalogServicesMapDomainTypes() {
        final CustomerProfileService customerService = new CustomerProfileService(new CustomerProfileMapper());
        final CatalogQueryService catalogService = new CatalogQueryService(new CatalogMapper());

        StepVerifier.create(customerService.getProfile("ent-42"))
                .assertNext((final var profile) -> {
                    assertThat(profile.customerId()).isEqualTo("ent-42");
                    assertThat(profile.segment().name()).isEqualTo("ENTERPRISE");
                    assertThat(profile.loyaltyPoints()).isEqualTo(25000);
                })
                .verifyComplete();

        StepVerifier.create(catalogService.getItem("HZ-100"))
                .assertNext((final var item) -> {
                    assertThat(item.hazardous()).isTrue();
                    assertThat(item.status().name()).isEqualTo("ACTIVE");
                    assertThat(item.listPrice()).isEqualByComparingTo("129.99");
                })
                .verifyComplete();
    }

    @Test
    void inventoryReservationRejectsUnavailableStock() {
        final InventoryReservationService service = new InventoryReservationService();
        final InventoryReservationRequest request = new InventoryReservationRequest(UUID.randomUUID(), "LOW-1", 2);

        StepVerifier.create(service.reserve(request))
                .expectError(ResourceConflictException.class)
                .verify();
    }

    @Test
    void pricingChoosesLargestDiscountAndAppliesTax() {
        final PricingService service = new PricingService(new CatalogMapper(), new MoneyMapper());
        final PriceQuoteRequest request = new PriceQuoteRequest("customer-1", "SKU-1", 2, "SAVE20");

        StepVerifier.create(service.quote(request))
                .assertNext((final var quote) -> {
                    assertThat(quote.subtotal()).isEqualByComparingTo("99.98");
                    assertThat(quote.discount()).isEqualByComparingTo("20.00");
                    assertThat(quote.total()).isEqualByComparingTo("86.58");
                    assertThat(quote.priceRule()).isEqualTo("DISCOUNTED");
                })
                .verifyComplete();
    }

    @Test
    void promotionHandlesCouponAndEnterpriseFallback() {
        final PromotionService service = new PromotionService();

        StepVerifier.create(service.evaluate("SAVE20", "customer-1", "SKU-1"))
                .expectNextMatches((final var decision) -> decision.eligible()
                        && decision.discountAmount().compareTo(new BigDecimal("20.00")) == 0)
                .verifyComplete();

        StepVerifier.create(service.evaluate("NONE", "ent-1", "OLD-1"))
                .expectNextMatches((final var decision) -> decision.eligible()
                        && "enterprise".equals(decision.reason()))
                .verifyComplete();
    }

    @Test
    void paymentRejectsUnsupportedCurrencyAndFlagsManualReview() {
        final PaymentAuthorizationService service = new PaymentAuthorizationService();
        final PaymentAuthorizationRequest unsupported = new PaymentAuthorizationRequest(
                UUID.randomUUID(),
                new BigDecimal("10.00"),
                "EUR",
                "tok_test");
        final PaymentAuthorizationRequest largePayment = new PaymentAuthorizationRequest(
                UUID.randomUUID(),
                new BigDecimal("6000.00"),
                "USD",
                "tok_test");

        StepVerifier.create(service.authorize(unsupported))
                .expectError(DomainRuleViolationException.class)
                .verify();

        StepVerifier.create(service.authorize(largePayment))
                .expectNextMatches((final var response) -> !response.authorized()
                        && "manual review required".equals(response.reason()))
                .verifyComplete();
    }

    @Test
    void fulfillmentRejectsHazardousShipmentsOutsideAllowedRegion() {
        final FulfillmentPlanningService service = new FulfillmentPlanningService(new FulfillmentMapper(CLOCK));
        final ShipmentPlanRequest allowed = new ShipmentPlanRequest(UUID.randomUUID(), "94105", "HZ-1", 3);
        final ShipmentPlanRequest blocked = new ShipmentPlanRequest(UUID.randomUUID(), "10001", "HZ-1", 3);

        StepVerifier.create(service.plan(allowed))
                .assertNext((final var plan) -> {
                    assertThat(plan.warehouseCode()).isEqualTo("SFO-01");
                    assertThat(plan.estimatedShipDate().toString()).isEqualTo("2026-02-04");
                })
                .verifyComplete();

        StepVerifier.create(service.plan(blocked))
                .expectError(DomainRuleViolationException.class)
                .verify();
    }

    @Test
    void returnsSupportAndAuditServicesApplyBusinessRules() {
        final ReturnPolicyService returnService = new ReturnPolicyService();
        final SupportTicketService supportService = new SupportTicketService(CLOCK);
        final AuditTrailService auditTrailService = new AuditTrailService(CLOCK);
        final UUID orderId = UUID.randomUUID();

        StepVerifier.create(returnService.authorize(new ReturnAuthorizationRequest(orderId, "HZ-1", 1, "DAMAGED")))
                .expectNextMatches((final var response) -> response.approved()
                        && "SPECIAL_HANDLING".equals(response.disposition()))
                .verifyComplete();

        StepVerifier.create(supportService.create(new CreateTicketRequest(
                        "customer-1",
                        orderId.toString(),
                        "Payment issue",
                        "Possible chargeback")))
                .expectNextMatches((final var ticket) -> "HIGH".equals(ticket.priority())
                        && Instant.parse("2026-02-03T04:05:06Z").equals(ticket.createdAt()))
                .verifyComplete();

        StepVerifier.create(auditTrailService.orderTrail(orderId))
                .expectNextMatches((final var trail) -> trail.events().contains("SHIPMENT_PLANNED")
                        && Instant.parse("2026-02-03T04:05:06Z").equals(trail.generatedAt()))
                .verifyComplete();
    }
}
