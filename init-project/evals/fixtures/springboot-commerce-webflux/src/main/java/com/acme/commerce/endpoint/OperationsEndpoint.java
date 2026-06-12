package com.acme.commerce.endpoint;

import com.acme.commerce.model.CommerceModels.ReconciliationJobView;
import com.acme.commerce.model.CommerceModels.ReconciliationRequest;
import com.acme.commerce.service.ReconciliationService;
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
@RequestMapping("/api/v1/operations/reconciliation/jobs")
public class OperationsEndpoint {
    private final ReconciliationService reconciliationService;

    public OperationsEndpoint(ReconciliationService reconciliationService) {
        this.reconciliationService = reconciliationService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.ACCEPTED)
    public Mono<ReconciliationJobView> start(@Valid @RequestBody ReconciliationRequest request) {
        return reconciliationService.start(request);
    }

    @GetMapping("/{jobId}")
    public Mono<ReconciliationJobView> get(@PathVariable String jobId) {
        return reconciliationService.get(jobId);
    }
}

