package com.acme.commerce.client;

import com.acme.commerce.model.CommerceModels.CreateShipmentRequest;
import com.acme.commerce.model.CommerceModels.ShipmentView;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Component
public class ShippingClient {
    private final WebClient webClient;

    public ShippingClient(@Qualifier("shippingWebClient") WebClient webClient) {
        this.webClient = webClient;
    }

    public Mono<ShipmentView> createShipment(CreateShipmentRequest request) {
        return webClient.post()
            .uri("/internal/shipments")
            .bodyValue(request)
            .retrieve()
            .bodyToMono(ShipmentView.class);
    }

    public Mono<ShipmentView> getShipment(String shipmentId) {
        return webClient.get()
            .uri("/internal/shipments/{shipmentId}", shipmentId)
            .retrieve()
            .bodyToMono(ShipmentView.class);
    }
}

