package com.acme.commerce.service;

import com.acme.commerce.model.CommerceModels.FulfillmentPlanRequest;
import com.acme.commerce.model.CommerceModels.FulfillmentPlanView;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class FulfillmentService {
    private final Map<String, FulfillmentPlanView> plans = new ConcurrentHashMap<>();

    public Mono<FulfillmentPlanView> createPlan(FulfillmentPlanRequest request) {
        var plan = new FulfillmentPlanView("plan_" + UUID.randomUUID(), request.orderId(), request.warehouseCode(), "READY_TO_PICK");
        plans.put(plan.planId(), plan);
        return Mono.just(plan);
    }

    public Mono<FulfillmentPlanView> getPlan(String planId) {
        return Mono.justOrEmpty(plans.get(planId));
    }
}

