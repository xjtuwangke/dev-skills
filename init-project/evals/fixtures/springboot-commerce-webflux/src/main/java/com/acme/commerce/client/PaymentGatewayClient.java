package com.acme.commerce.client;

import com.acme.commerce.model.CommerceModels.AuthorizePaymentRequest;
import com.acme.commerce.model.CommerceModels.PaymentView;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;

@Component
public class PaymentGatewayClient {
    private final WebClient webClient;

    public PaymentGatewayClient(@Qualifier("paymentWebClient") WebClient webClient) {
        this.webClient = webClient;
    }

    public Mono<PaymentView> authorize(AuthorizePaymentRequest request) {
        return webClient.post()
            .uri("/internal/payments/authorizations")
            .bodyValue(request)
            .retrieve()
            .bodyToMono(PaymentView.class);
    }

    public Mono<PaymentView> capture(String paymentId) {
        return webClient.post()
            .uri("/internal/payments/{paymentId}/capture", paymentId)
            .retrieve()
            .bodyToMono(PaymentView.class);
    }
}

