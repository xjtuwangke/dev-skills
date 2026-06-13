/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.client.model;

public record PaymentGatewayAuthorizationResponse(boolean authorized, String authorizationCode, String reason) {
}
