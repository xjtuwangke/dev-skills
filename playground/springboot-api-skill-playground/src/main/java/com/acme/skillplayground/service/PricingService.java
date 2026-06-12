/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.service;

import com.acme.skillplayground.mapper.CatalogMapper;
import com.acme.skillplayground.mapper.MoneyMapper;
import com.acme.skillplayground.model.catalog.CatalogItemResponse;
import com.acme.skillplayground.model.pricing.PriceQuoteRequest;
import com.acme.skillplayground.model.pricing.PriceQuoteResponse;
import java.math.BigDecimal;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class PricingService {

    private final CatalogMapper catalogMapper;
    private final MoneyMapper moneyMapper;

    public PricingService(final CatalogMapper catalogMapper, final MoneyMapper moneyMapper) {
        this.catalogMapper = catalogMapper;
        this.moneyMapper = moneyMapper;
    }

    public Mono<PriceQuoteResponse> quote(final PriceQuoteRequest request) {
        return Mono.fromSupplier(() -> {
            final CatalogItemResponse item = catalogMapper.toCatalogItem(request.sku());
            final BigDecimal subtotal = moneyMapper.subtotal(item.listPrice(), request.quantity());
            final boolean preferred = request.customerId().startsWith("ent-");
            final BigDecimal loyaltyDiscount = moneyMapper.loyaltyDiscount(subtotal, preferred);
            final BigDecimal couponDiscount = moneyMapper.couponDiscount(subtotal, request.couponCode());
            final BigDecimal discount = moneyMapper.round(loyaltyDiscount.max(couponDiscount));
            final BigDecimal taxable = moneyMapper.round(subtotal.subtract(discount));
            final BigDecimal tax = moneyMapper.tax(taxable);
            final BigDecimal total = moneyMapper.round(taxable.add(tax));
            return new PriceQuoteResponse(
                    request.sku(),
                    request.quantity(),
                    subtotal,
                    discount,
                    tax,
                    total,
                    item.currency(),
                    discount.signum() > 0 ? "DISCOUNTED" : "LIST");
        });
    }
}
