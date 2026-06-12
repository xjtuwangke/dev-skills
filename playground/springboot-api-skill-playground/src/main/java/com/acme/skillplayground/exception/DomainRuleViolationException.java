/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.exception;

public class DomainRuleViolationException extends RuntimeException {

    public DomainRuleViolationException(final String message) {
        super(message);
    }
}
