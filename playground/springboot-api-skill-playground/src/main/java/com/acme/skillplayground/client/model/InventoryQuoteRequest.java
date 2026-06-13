/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.client.model;

import java.util.UUID;

public record InventoryQuoteRequest(UUID orderId, String sku, int quantity) {
}
