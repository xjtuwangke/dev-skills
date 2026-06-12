package com.acme.commerce.service;

import com.acme.commerce.model.CommerceModels.CreateReturnRequest;
import com.acme.commerce.model.CommerceModels.ReturnView;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class ReturnService {
    private final Map<String, ReturnView> returns = new ConcurrentHashMap<>();

    public Mono<ReturnView> createReturn(CreateReturnRequest request) {
        var view = new ReturnView("ret_" + UUID.randomUUID(), request.orderId(), "REQUESTED", request.reason());
        returns.put(view.returnId(), view);
        return Mono.just(view);
    }

    public Mono<ReturnView> getReturn(String returnId) {
        return Mono.justOrEmpty(returns.get(returnId));
    }
}

