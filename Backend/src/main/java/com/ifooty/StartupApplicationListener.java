package com.ifooty;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.ifooty.news.NewsService;
import com.ifooty.team.TeamService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.event.ContextRefreshedEvent;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class StartupApplicationListener {

    @Autowired
    private NewsService newsService;

    @Autowired
    private TeamService teamService;

    @EventListener(ContextRefreshedEvent.class)
    public void onApplicationEvent() throws IOException {
        newsService.summarizeAllNews();
        teamService.updateAllNewsToTeams(newsService.getAllNews());
    }
}