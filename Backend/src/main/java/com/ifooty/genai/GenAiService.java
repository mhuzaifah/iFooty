package com.ifooty.genai;

import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.io.IOException;
import java.util.concurrent.TimeUnit;

@Service
public class GenAiService {

    @Autowired
    private RestTemplate restTemplate;

    @Value("${gemini.api.key}")
    private String geminiApiKey;
    private final String API_URL_TEMPLATE = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=%s";
    private static final int REQUEST_LIMIT = 15; // GEMINI 1.5 Flash model request / min limit
    private int requestCount = 0; // Amount of requests made
    private long startTime = System.currentTimeMillis(); // To track the start time

    public String callApi(String prompt) throws IOException {

        checkRateLimit(); // Check if we can make the API call

        requestCount++;

        String apiUrl = String.format(API_URL_TEMPLATE, geminiApiKey);
        HttpHeaders headers = new HttpHeaders();
        headers.set("Content-Type", "application/json");

        ObjectMapper objectMapper = new ObjectMapper();
        ObjectNode contentNode = objectMapper.createObjectNode();
        ObjectNode partsNode = objectMapper.createObjectNode();
        partsNode.put("text", prompt);
        contentNode.set("parts", objectMapper.createArrayNode().add(partsNode));
        ObjectNode requestBodyNode = objectMapper.createObjectNode();
        requestBodyNode.set("contents", objectMapper.createArrayNode().add(contentNode));

        String requestBody;
        try {
            requestBody = objectMapper.writeValueAsString(requestBodyNode);
        } catch (Exception e) {
            throw new RuntimeException("Failed to construct JSON request body", e);
        }

        HttpEntity<String> request = new HttpEntity<>(requestBody, headers);
        ResponseEntity<String> response = restTemplate.exchange(apiUrl, HttpMethod.POST, request, String.class);

        ObjectMapper mapper = new ObjectMapper();
        JsonNode node = mapper.readTree(response.getBody());

        return node
                .path("candidates")
                .get(0)
                .path("content")
                .path("parts")
                .get(0)
                .path("text")
                .asText();

    }

    private void checkRateLimit() {
        if(requestCount >= REQUEST_LIMIT) {
            long elapsedTime = (System.currentTimeMillis() - startTime) / 1000; //Convert from mins to seconds

            if(elapsedTime < 60) {
                long timeToSleep = 60 - elapsedTime;
                System.out.println("Rate limit reached. Sleeping for " + timeToSleep + " seconds.");

                try {
                    TimeUnit.SECONDS.sleep(timeToSleep);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    throw new RuntimeException();
                }
            }

            // Reset counter variables
            requestCount = 0;
            startTime = System.currentTimeMillis();
        }
    }

}
