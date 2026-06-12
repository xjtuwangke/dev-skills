package com.acme.commerce.database;

import java.math.BigDecimal;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;

public interface PaymentRepository extends ReactiveCrudRepository<PaymentRepository.PaymentRow, String> {
    @Table("payments")
    record PaymentRow(@Id String id, String orderId, String status, BigDecimal amount, String providerRef) {}
}

