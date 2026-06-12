package com.acme.commerce.service;

import com.acme.commerce.client.InventoryClient;
import com.acme.commerce.database.InventoryReservationRepository;
import com.acme.commerce.database.InventoryReservationRepository.InventoryReservationRow;
import com.acme.commerce.model.CommerceModels.InventoryReservationView;
import com.acme.commerce.model.CommerceModels.InventoryReservedEvent;
import com.acme.commerce.model.CommerceModels.ReserveInventoryRequest;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class InventoryService {
    private final InventoryClient inventoryClient;
    private final InventoryReservationRepository reservationRepository;

    public InventoryService(InventoryClient inventoryClient, InventoryReservationRepository reservationRepository) {
        this.inventoryClient = inventoryClient;
        this.reservationRepository = reservationRepository;
    }

    public Mono<InventoryReservationView> reserve(ReserveInventoryRequest request) {
        return inventoryClient.reserve(request)
            .map(view -> new InventoryReservationRow(view.reservationId(), view.orderId(), view.sku(), view.quantity(), view.status()))
            .flatMap(reservationRepository::save)
            .map(this::toView);
    }

    public Mono<InventoryReservationView> getReservation(String reservationId) {
        return reservationRepository.findById(reservationId).map(this::toView);
    }

    public Mono<Void> releaseReservation(String reservationId) {
        return inventoryClient.release(reservationId)
            .then(reservationRepository.findById(reservationId))
            .map(row -> new InventoryReservationRow(row.id(), row.orderId(), row.sku(), row.quantity(), "RELEASED"))
            .flatMap(reservationRepository::save)
            .then();
    }

    public Mono<Void> markReserved(InventoryReservedEvent event) {
        var row = new InventoryReservationRow(event.reservationId(), event.orderId(), event.sku(), event.quantity(), "RESERVED");
        return reservationRepository.save(row).then();
    }

    private InventoryReservationView toView(InventoryReservationRow row) {
        return new InventoryReservationView(row.id(), row.orderId(), row.sku(), row.quantity(), row.status());
    }
}

