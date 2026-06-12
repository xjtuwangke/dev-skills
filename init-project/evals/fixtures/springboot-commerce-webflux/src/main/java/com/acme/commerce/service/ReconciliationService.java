package com.acme.commerce.service;

import com.acme.commerce.model.CommerceModels.ReconciliationJobView;
import com.acme.commerce.model.CommerceModels.ReconciliationRequest;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class ReconciliationService {
    private final Map<String, ReconciliationJobView> jobs = new ConcurrentHashMap<>();

    public Mono<ReconciliationJobView> start(ReconciliationRequest request) {
        var counts = Map.of("orders", 0, "payments", 0, "inventory", 0);
        var job = new ReconciliationJobView("rec_" + UUID.randomUUID(), request.businessDate(), "QUEUED", counts);
        jobs.put(job.jobId(), job);
        return Mono.just(job);
    }

    public Mono<ReconciliationJobView> get(String jobId) {
        return Mono.justOrEmpty(jobs.get(jobId));
    }
}

