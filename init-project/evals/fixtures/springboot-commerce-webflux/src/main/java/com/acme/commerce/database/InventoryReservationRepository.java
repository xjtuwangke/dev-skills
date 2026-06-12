package com.acme.commerce.database;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;

public interface InventoryReservationRepository extends ReactiveCrudRepository<InventoryReservationRepository.InventoryReservationRow, String> {
    @Table("inventory_reservations")
    record InventoryReservationRow(@Id String id, String orderId, String sku, int quantity, String status) {}
}

