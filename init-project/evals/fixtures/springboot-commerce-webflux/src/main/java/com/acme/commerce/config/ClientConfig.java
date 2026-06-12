package com.acme.commerce.config;

import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
@EnableConfigurationProperties(CommerceProperties.class)
public class ClientConfig {
    @Bean
    WebClient inventoryWebClient(WebClient.Builder builder, CommerceProperties properties) {
        return builder.baseUrl(properties.getClients().getInventory().getBaseUrl()).build();
    }

    @Bean
    WebClient paymentWebClient(WebClient.Builder builder, CommerceProperties properties) {
        return builder.baseUrl(properties.getClients().getPayment().getBaseUrl()).build();
    }

    @Bean
    WebClient shippingWebClient(WebClient.Builder builder, CommerceProperties properties) {
        return builder.baseUrl(properties.getClients().getShipping().getBaseUrl()).build();
    }
}

