package com.acme.commerce.config;

import java.time.Duration;
import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "commerce")
public class CommerceProperties {
    private String gcpProjectId;
    private final Clients clients = new Clients();
    private final Pubsub pubsub = new Pubsub();

    public String getGcpProjectId() {
        return gcpProjectId;
    }

    public void setGcpProjectId(String gcpProjectId) {
        this.gcpProjectId = gcpProjectId;
    }

    public Clients getClients() {
        return clients;
    }

    public Pubsub getPubsub() {
        return pubsub;
    }

    public static class Clients {
        private final Downstream inventory = new Downstream();
        private final Downstream payment = new Downstream();
        private final Downstream shipping = new Downstream();

        public Downstream getInventory() {
            return inventory;
        }

        public Downstream getPayment() {
            return payment;
        }

        public Downstream getShipping() {
            return shipping;
        }
    }

    public static class Downstream {
        private String baseUrl;
        private Duration timeout = Duration.ofSeconds(2);

        public String getBaseUrl() {
            return baseUrl;
        }

        public void setBaseUrl(String baseUrl) {
            this.baseUrl = baseUrl;
        }

        public Duration getTimeout() {
            return timeout;
        }

        public void setTimeout(Duration timeout) {
            this.timeout = timeout;
        }
    }

    public static class Pubsub {
        private String orderCreatedTopic;
        private String orderCancelledTopic;
        private String paymentAuthorizedTopic;
        private String inventoryReservedSubscription;
        private String shipmentUpdatedSubscription;

        public String getOrderCreatedTopic() {
            return orderCreatedTopic;
        }

        public void setOrderCreatedTopic(String orderCreatedTopic) {
            this.orderCreatedTopic = orderCreatedTopic;
        }

        public String getOrderCancelledTopic() {
            return orderCancelledTopic;
        }

        public void setOrderCancelledTopic(String orderCancelledTopic) {
            this.orderCancelledTopic = orderCancelledTopic;
        }

        public String getPaymentAuthorizedTopic() {
            return paymentAuthorizedTopic;
        }

        public void setPaymentAuthorizedTopic(String paymentAuthorizedTopic) {
            this.paymentAuthorizedTopic = paymentAuthorizedTopic;
        }

        public String getInventoryReservedSubscription() {
            return inventoryReservedSubscription;
        }

        public void setInventoryReservedSubscription(String inventoryReservedSubscription) {
            this.inventoryReservedSubscription = inventoryReservedSubscription;
        }

        public String getShipmentUpdatedSubscription() {
            return shipmentUpdatedSubscription;
        }

        public void setShipmentUpdatedSubscription(String shipmentUpdatedSubscription) {
            this.shipmentUpdatedSubscription = shipmentUpdatedSubscription;
        }
    }
}

