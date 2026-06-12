package com.acme.commerce.service;

import com.acme.commerce.database.CustomerRepository;
import com.acme.commerce.database.CustomerRepository.CustomerRow;
import com.acme.commerce.model.CommerceModels.CustomerView;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class CustomerService {
    private final CustomerRepository customerRepository;

    public CustomerService(CustomerRepository customerRepository) {
        this.customerRepository = customerRepository;
    }

    public Mono<CustomerView> getCustomer(String customerId) {
        return customerRepository.findById(customerId).map(this::toView);
    }

    private CustomerView toView(CustomerRow row) {
        return new CustomerView(row.id(), row.email(), row.loyaltyTier(), row.riskScore());
    }
}

