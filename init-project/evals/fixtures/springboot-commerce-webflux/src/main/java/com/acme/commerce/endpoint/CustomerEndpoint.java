package com.acme.commerce.endpoint;

import com.acme.commerce.model.CommerceModels.CustomerView;
import com.acme.commerce.model.CommerceModels.OrderView;
import com.acme.commerce.service.CustomerService;
import com.acme.commerce.service.OrderService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/v1/customers")
public class CustomerEndpoint {
    private final CustomerService customerService;
    private final OrderService orderService;

    public CustomerEndpoint(CustomerService customerService, OrderService orderService) {
        this.customerService = customerService;
        this.orderService = orderService;
    }

    @GetMapping("/{customerId}")
    public Mono<CustomerView> getCustomer(@PathVariable String customerId) {
        return customerService.getCustomer(customerId);
    }

    @GetMapping("/{customerId}/orders")
    public Flux<OrderView> listCustomerOrders(@PathVariable String customerId) {
        return orderService.listCustomerOrders(customerId);
    }
}

