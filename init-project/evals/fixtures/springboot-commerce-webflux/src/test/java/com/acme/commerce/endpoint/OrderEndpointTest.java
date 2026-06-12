package com.acme.commerce.endpoint;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.test.web.reactive.server.WebTestClient;

@WebFluxTest(OrderEndpoint.class)
class OrderEndpointTest {
    @Test
    void documentsExpectedTestStyle() {
        WebTestClient.bindToController(new Object()).build();
    }
}

