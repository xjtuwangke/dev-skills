package com.acme.commerce.endpoint;

import com.acme.commerce.model.CommerceModels.FulfillmentPlanRequest;
import com.acme.commerce.model.CommerceModels.FulfillmentPlanView;
import com.acme.commerce.service.FulfillmentService;
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
@RequestMapping("/api/v1/fulfillment/plans")
public class FulfillmentEndpoint {
    private final FulfillmentService fulfillmentService;

    public FulfillmentEndpoint(FulfillmentService fulfillmentService) {
        this.fulfillmentService = fulfillmentService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<FulfillmentPlanView> createPlan(@Valid @RequestBody FulfillmentPlanRequest request) {
        return fulfillmentService.createPlan(request);
    }

    @GetMapping("/{planId}")
    public Mono<FulfillmentPlanView> getPlan(@PathVariable String planId) {
        return fulfillmentService.getPlan(planId);
    }
}

