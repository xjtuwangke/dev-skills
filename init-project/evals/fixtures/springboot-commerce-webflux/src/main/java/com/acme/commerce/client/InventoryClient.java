package com.acme.commerce.client;

import com.acme.commerce.model.CommerceModels.InventoryReservationView;
import com.acme.commerce.model.CommerceModels.ReserveInventoryRequest;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Component
public class InventoryClient {
    private final WebClient webClient;

    public InventoryClient(@Qualifier("inventoryWebClient") WebClient webClient) {
        this.webClient = webClient;
    }

    public Mono<InventoryReservationView> reserve(ReserveInventoryRequest request) {
        return webClient.post()
            .uri("/internal/inventory/reservations")
            .bodyValue(request)
            .retrieve()
            .bodyToMono(InventoryReservationView.class);
    }

    public Mono<Void> release(String reservationId) {
        return webClient.post()
            .uri("/internal/inventory/reservations/{reservationId}/release", reservationId)
            .retrieve()
            .bodyToMono(Void.class);
    }
}

