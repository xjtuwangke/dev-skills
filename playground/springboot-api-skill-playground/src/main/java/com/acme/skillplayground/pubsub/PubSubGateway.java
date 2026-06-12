/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.pubsub;

import java.util.concurrent.CompletableFuture;

public interface PubSubGateway {

    CompletableFuture<String> publish(final String topic, final Object payload);
}
