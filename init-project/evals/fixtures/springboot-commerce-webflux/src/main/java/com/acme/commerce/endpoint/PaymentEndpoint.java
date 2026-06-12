package com.acme.commerce.endpoint;

import com.acme.commerce.model.CommerceModels.AuthorizePaymentRequest;
import com.acme.commerce.model.CommerceModels.PaymentView;
import com.acme.commerce.service.PaymentService;
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
@RequestMapping("/api/v1/payments")
public class PaymentEndpoint {
    private final PaymentService paymentService;

    public PaymentEndpoint(PaymentService paymentService) {
        this.paymentService = paymentService;
    }

    @PostMapping("/authorize")
    @ResponseStatus(HttpStatus.ACCEPTED)
    public Mono<PaymentView> authorize(@Valid @RequestBody AuthorizePaymentRequest request) {
        return paymentService.authorize(request);
    }

    @GetMapping("/{paymentId}")
    public Mono<PaymentView> getPayment(@PathVariable String paymentId) {
        return paymentService.getPayment(paymentId);
    }

    @PostMapping("/{paymentId}/capture")
    @ResponseStatus(HttpStatus.ACCEPTED)
    public Mono<PaymentView> capture(@PathVariable String paymentId) {
        return paymentService.capture(paymentId);
    }
}

