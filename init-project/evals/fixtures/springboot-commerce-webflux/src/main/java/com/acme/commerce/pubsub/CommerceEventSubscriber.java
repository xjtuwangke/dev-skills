package com.acme.commerce.pubsub;

import com.acme.commerce.model.CommerceModels.InventoryReservedEvent;
import com.acme.commerce.model.CommerceModels.ShipmentUpdatedEvent;
import com.acme.commerce.service.InventoryService;
import com.acme.commerce.service.ShipmentService;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.google.cloud.spring.pubsub.support.BasicAcknowledgeablePubsubMessage;
import com.google.cloud.spring.pubsub.support.GcpPubSubHeaders;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.messaging.handler.annotation.Header;
import org.springframework.stereotype.Component;

@Component
public class CommerceEventSubscriber {
    private final InventoryService inventoryService;
    private final ShipmentService shipmentService;
    private final ObjectMapper objectMapper;

    public CommerceEventSubscriber(InventoryService inventoryService, ShipmentService shipmentService, ObjectMapper objectMapper) {
        this.inventoryService = inventoryService;
        this.shipmentService = shipmentService;
        this.objectMapper = objectMapper;
    }

    @ServiceActivator(inputChannel = "inventoryReservedInputChannel")
    public void handleInventoryReserved(String payload, @Header(GcpPubSubHeaders.ORIGINAL_MESSAGE) BasicAcknowledgeablePubsubMessage message) throws Exception {
        var event = objectMapper.readValue(payload, InventoryReservedEvent.class);
        inventoryService.markReserved(event).doOnSuccess(unused -> message.ack()).subscribe();
    }

    @ServiceActivator(inputChannel = "shipmentUpdatedInputChannel")
    public void handleShipmentUpdated(String payload, @Header(GcpPubSubHeaders.ORIGINAL_MESSAGE) BasicAcknowledgeablePubsubMessage message) throws Exception {
        var event = objectMapper.readValue(payload, ShipmentUpdatedEvent.class);
        shipmentService.recordShipmentUpdate(event).doOnSuccess(unused -> message.ack()).subscribe();
    }
}

