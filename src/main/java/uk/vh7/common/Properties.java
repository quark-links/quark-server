package uk.vh7.common;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
public class Properties {
    @Value("${vh7.url}")
    private String baseUrl;

    public String getBaseUrl() {
        return baseUrl;
    }
}
