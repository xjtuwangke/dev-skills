package com.acme.commerce.endpoint;

import com.acme.commerce.model.CommerceModels.InventoryReservationView;
import com.acme.commerce.model.CommerceModels.ReserveInventoryRequest;
import com.acme.commerce.service.InventoryService;
import javax.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/v1/inventory/reservations")
public class InventoryEndpoint {
    private final InventoryService inventoryService;

    public InventoryEndpoint(InventoryService inventoryService) {
        this.inventoryService = inventoryService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.ACCEPTED)
    public Mono<InventoryReservationView> reserve(@Valid @RequestBody ReserveInventoryRequest request) {
        return inventoryService.reserve(request);
    }

    @GetMapping("/{reservationId}")
    public Mono<InventoryReservationView> getReservation(@PathVariable String reservationId) {
        return inventoryService.getReservation(reservationId);
    }

    @PostMapping("/{reservationId}/release")
    @ResponseStatus(HttpStatus.ACCEPTED)
    public Mono<Void> release(@PathVariable String reservationId) {
        return inventoryService.releaseReservation(reservationId);
    }
}

