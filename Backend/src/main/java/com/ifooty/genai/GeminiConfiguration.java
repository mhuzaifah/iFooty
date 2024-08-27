package com.fs.football_snap.genai;

import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class GeminiConfiguration {

    @Bean
    public RestTemplate restTemplate(RestTemplateBuilder builder) { return builder.build(); }
}
