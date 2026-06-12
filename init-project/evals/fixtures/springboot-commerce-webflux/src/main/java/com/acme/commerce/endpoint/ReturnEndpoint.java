package com.acme.commerce.endpoint;

import com.acme.commerce.model.CommerceModels.CreateReturnRequest;
import com.acme.commerce.model.CommerceModels.ReturnView;
import com.acme.commerce.service.ReturnService;
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
@RequestMapping("/api/v1/returns")
public class ReturnEndpoint {
    private final ReturnService returnService;

    public ReturnEndpoint(ReturnService returnService) {
        this.returnService = returnService;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Mono<ReturnView> createReturn(@Valid @RequestBody CreateReturnRequest request) {
        return returnService.createReturn(request);
    }

    @GetMapping("/{returnId}")
    public Mono<ReturnView> getReturn(@PathVariable String returnId) {
        return returnService.getReturn(returnId);
    }
}

