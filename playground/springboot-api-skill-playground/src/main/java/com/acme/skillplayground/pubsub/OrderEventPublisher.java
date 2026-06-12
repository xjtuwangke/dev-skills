/*
 * Copyright 2026 Acme Corp.
 *
 * Licensed under the Apache License, Version 2.0.
 */
package com.acme.skillplayground.pubsub;

import com.acme.skillplayground.model.OrderResponse;
import reactor.core.publisher.Mono;

public interface OrderEventPublisher {

    Mono<Void> publishCreated(final OrderResponse response);

    Mono<Void> publishStatusChanged(final OrderResponse response);
}
