package com.acme.commerce.database;

import java.math.BigDecimal;
import java.time.Instant;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import reactor.core.publisher.Flux;

public interface OrderRepository extends ReactiveCrudRepository<OrderRepository.OrderRow, String> {
    Flux<OrderRow> findByCustomerId(String customerId);

    @Table("orders")
    record OrderRow(@Id String id, String customerId, String status, BigDecimal totalAmount, String currency, Instant createdAt) {}
}

