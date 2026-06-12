/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.service;

import com.acme.skillplayground.mapper.CatalogMapper;
import com.acme.skillplayground.model.catalog.CatalogItemResponse;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class CatalogQueryService {

    private final CatalogMapper mapper;

    public CatalogQueryService(final CatalogMapper mapper) {
        this.mapper = mapper;
    }

    public Mono<CatalogItemResponse> getItem(final String sku) {
        return Mono.fromSupplier(() -> mapper.toCatalogItem(sku));
    }
}
