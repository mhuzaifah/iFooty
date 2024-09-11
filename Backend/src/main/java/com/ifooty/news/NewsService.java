package com.ifooty.news;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.ifooty.genai.GenAiService;
import com.ifooty.team.Team;
import jakarta.persistence.PostPersist;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;

@Component
public class NewsService {
    private final NewsRepository newsRepository;
    private final GenAiService genAiService;

    @Autowired
    public NewsService(NewsRepository newsRepository, GenAiService genAiService) {
        this.newsRepository = newsRepository;
        this.genAiService = genAiService;
    }

    public List<News> getAllNews() {
        return newsRepository.findAll();
    }

    public void summarizeAllNews() throws IOException {
        List<News> newsList = newsRepository.findAll().stream().filter(news -> news.getSummary().equalsIgnoreCase("null")).toList();

        newsList.forEach(news -> {
            String prompt = "Summarize the following news article. Focus on identifying the key points, main events, and important details. Provide a concise summary that captures the essence of the article. Here is the article body: " + news.getBody();
            try {
                news.setSummary(genAiService.callApi(prompt));
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            newsRepository.save(news);
        });
    }

    List<News> getNewsByTeam(String teamName) {
        return newsRepository.findAll().stream()
                .filter(news -> news.getTeam().getName().equalsIgnoreCase(teamName))
                .collect(Collectors.toList());
    }

    List<News> getNewsByDate(Date date) {
        return newsRepository.findAll().stream()
                .filter(news -> news.getDate().equals(date))
                .collect(Collectors.toList());
    }

    @Transactional
    public void deleteTeamNews(Team team) { newsRepository.deleteByTeam(team); }
}
