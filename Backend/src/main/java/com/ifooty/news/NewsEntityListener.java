package com.fs.football_snap.news;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fs.football_snap.genai.GenAiService;
import jakarta.persistence.PostPersist;

import java.io.IOException;

public class NewsEntityListener {
    private final GenAiService genAiService = new GenAiService();

    public NewsEntityListener() {}

    @PostPersist
    public void generateSummary(News news) throws IOException {
        String summary = news.getSummary();
        if(summary.equalsIgnoreCase("null")) {
            String prompt = "Summarize the following news article. Focus on identifying the key points, main events, and important details. Provide a concise summary that captures the essence of the article. Here is the article body: " + news.getBody();
            summary = genAiService.callApi(prompt);
            news.setSummary(summary);
        }
    }
}


