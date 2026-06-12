/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.exception;

public class ResourceConflictException extends RuntimeException {

    public ResourceConflictException(final String message) {
        super(message);
    }
}
