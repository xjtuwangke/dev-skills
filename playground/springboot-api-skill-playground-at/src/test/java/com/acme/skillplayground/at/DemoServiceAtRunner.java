package com.acme.skillplayground.at;

import com.intuit.karate.junit5.Karate;
import org.junit.jupiter.api.condition.EnabledIfSystemProperty;

@EnabledIfSystemProperty(named = "at.enabled", matches = "true")
class DemoServiceAtRunner {

    @Karate.Test
    Karate runAcceptanceTests() {
        final String configuredTags = System.getProperty("karate.tags", "~@wip");
        final String[] tags = configuredTags.split("\\s*,\\s*");
        return Karate.run("classpath:features").tags(tags);
    }
}
