package com.acme.commerce.database;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;

public interface CustomerRepository extends ReactiveCrudRepository<CustomerRepository.CustomerRow, String> {
    @Table("customers")
    record CustomerRow(@Id String id, String email, String loyaltyTier, int riskScore) {}
}

