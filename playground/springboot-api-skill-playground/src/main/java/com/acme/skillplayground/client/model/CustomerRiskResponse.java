/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.client.model;

public record CustomerRiskResponse(String customerId, String riskBand, int score) {
}
