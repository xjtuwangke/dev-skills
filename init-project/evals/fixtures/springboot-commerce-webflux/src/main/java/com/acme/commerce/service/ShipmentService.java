package com.acme.commerce.service;

import com.acme.commerce.client.ShippingClient;
import com.acme.commerce.model.CommerceModels.CreateShipmentRequest;
import com.acme.commerce.model.CommerceModels.ShipmentUpdatedEvent;
import com.acme.commerce.model.CommerceModels.ShipmentView;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;

@Service
public class ShipmentService {
    private final ShippingClient shippingClient;
    private final Map<String, ShipmentView> shipments = new ConcurrentHashMap<>();

    public ShipmentService(ShippingClient shippingClient) {
        this.shippingClient = shippingClient;
    }

    public Mono<ShipmentView> createShipment(CreateShipmentRequest request) {
        return shippingClient.createShipment(request)
            .doOnNext(view -> shipments.put(view.shipmentId(), view));
    }

    public Mono<ShipmentView> getShipment(String shipmentId) {
        var cached = shipments.get(shipmentId);
        if (cached != null) {
            return Mono.just(cached);
        }
        return shippingClient.getShipment(shipmentId).doOnNext(view -> shipments.put(view.shipmentId(), view));
    }

    public Mono<Void> recordShipmentUpdate(ShipmentUpdatedEvent event) {
        var view = new ShipmentView(event.shipmentId(), event.orderId(), "unknown", "unknown", event.status());
        shipments.put(event.shipmentId(), view);
        return Mono.empty();
    }
}

