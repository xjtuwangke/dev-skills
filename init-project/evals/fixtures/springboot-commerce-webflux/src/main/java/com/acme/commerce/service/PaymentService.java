package com.acme.commerce.service;

import com.acme.commerce.client.PaymentGatewayClient;
import com.acme.commerce.database.PaymentRepository;
import com.acme.commerce.database.PaymentRepository.PaymentRow;
import com.acme.commerce.model.CommerceModels.AuthorizePaymentRequest;
import com.acme.commerce.model.CommerceModels.PaymentAuthorizedEvent;
import com.acme.commerce.model.CommerceModels.PaymentView;
import com.acme.commerce.pubsub.CommerceEventPublisher;
import java.time.Instant;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class PaymentService {
    private final PaymentGatewayClient paymentGatewayClient;
    private final PaymentRepository paymentRepository;
    private final CommerceEventPublisher eventPublisher;

    public PaymentService(PaymentGatewayClient paymentGatewayClient, PaymentRepository paymentRepository, CommerceEventPublisher eventPublisher) {
        this.paymentGatewayClient = paymentGatewayClient;
        this.paymentRepository = paymentRepository;
        this.eventPublisher = eventPublisher;
    }

    public Mono<PaymentView> authorize(AuthorizePaymentRequest request) {
        return paymentGatewayClient.authorize(request)
            .map(view -> new PaymentRow(view.paymentId(), view.orderId(), "AUTHORIZED", view.amount(), view.providerRef()))
            .flatMap(paymentRepository::save)
            .map(this::toView)
            .flatMap(view -> eventPublisher.publishPaymentAuthorized(new PaymentAuthorizedEvent(view.paymentId(), view.orderId(), view.amount(), Instant.now())).thenReturn(view));
    }

    public Mono<PaymentView> getPayment(String paymentId) {
        return paymentRepository.findById(paymentId).map(this::toView);
    }

    public Mono<PaymentView> capture(String paymentId) {
        return paymentGatewayClient.capture(paymentId)
            .flatMap(view -> paymentRepository.findById(paymentId)
                .map(row -> new PaymentRow(row.id(), row.orderId(), "CAPTURED", row.amount(), view.providerRef()))
                .flatMap(paymentRepository::save))
            .map(this::toView);
    }

    private PaymentView toView(PaymentRow row) {
        return new PaymentView(row.id(), row.orderId(), row.status(), row.amount(), row.providerRef());
    }
}

