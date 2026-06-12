package com.acme.commerce.config;

import com.acme.commerce.model.CommerceModels.OrderView;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.redis.connection.ReactiveRedisConnectionFactory;
import org.springframework.data.redis.core.ReactiveRedisTemplate;
import org.springframework.data.redis.serializer.Jackson2JsonRedisSerializer;
import org.springframework.data.redis.serializer.RedisSerializationContext;
import org.springframework.data.redis.serializer.StringRedisSerializer;

@Configuration
public class RedisConfig {
    @Bean
    ReactiveRedisTemplate<String, OrderView> orderCacheTemplate(ReactiveRedisConnectionFactory factory) {
        var key = new StringRedisSerializer();
        var value = new Jackson2JsonRedisSerializer<>(OrderView.class);
        var context = RedisSerializationContext
            .<String, OrderView>newSerializationContext(key)
            .value(value)
            .build();
        return new ReactiveRedisTemplate<>(factory, context);
    }
}

