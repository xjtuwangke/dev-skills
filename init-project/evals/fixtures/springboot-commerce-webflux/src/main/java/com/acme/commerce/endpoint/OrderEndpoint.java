package com.acme.commerce.endpoint;

import com.acme.commerce.model.CommerceModels.CancelOrderRequest;
import com.acme.commerce.model.CommerceModels.CreateOrderRequest;
import com.acme.commerce.model.CommerceModels.OrderView;
import com.acme.commerce.model.CommerceModels.UpdateStatusRequest;
import com.acme.commerce.service.OrderService;
import javax.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PatchMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@RestController
@RequestMapping("/api/v1/orders")
public class OrderEndpoint {
    private final OrderService orderService;

    public OrderEndpoint(OrderService orderService) {
        this.orderService = orderService;
    }

    @GetMapping
    public Flux<OrderView> listOrders() {
        return orderService.listOrders();
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<OrderView> createOrder(@Valid @RequestBody CreateOrderRequest request) {
        return orderService.createOrder(request);
    }

    @GetMapping("/{orderId}")
    public Mono<OrderView> getOrder(@PathVariable String orderId) {
        return orderService.getOrder(orderId);
    }

    @PatchMapping("/{orderId}/status")
    public Mono<OrderView> updateStatus(@PathVariable String orderId, @Valid @RequestBody UpdateStatusRequest request) {
        return orderService.updateStatus(orderId, request);
    }

    @PostMapping("/{orderId}/submit")
    @ResponseStatus(HttpStatus.ACCEPTED)
    public Mono<OrderView> submitOrder(@PathVariable String orderId) {
        return orderService.submitOrder(orderId);
    }

    @PostMapping("/{orderId}/cancel")
    @ResponseStatus(HttpStatus.ACCEPTED)
    public Mono<OrderView> cancelOrder(@PathVariable String orderId, @Valid @RequestBody CancelOrderRequest request) {
        return orderService.cancelOrder(orderId, request);
    }
}

