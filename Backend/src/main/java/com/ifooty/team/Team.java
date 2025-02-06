package com.ifooty.team;
import java.util.ArrayList;
import java.util.List;

import com.ifooty.news.News;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

@Entity
@Table(name="pl_teams")
public class Team {

    @Id
    @Column(name="name", unique = true)
    private String name;
    private String record;
    private Double pointsPerGame;
    private String homeRecord;
    private String awayRecord;
    private Integer goals;
    private Double goalsPerGame;
    private Integer conceded;
    private Double concededPerGame;
    @OneToMany(mappedBy = "team", cascade = CascadeType.ALL, orphanRemoval = true, fetch = FetchType.EAGER)
    private List<News> news = new ArrayList<>();

    public Team() {}

    public Team(String name, String record, Double pointsPerGame, String homeRecord, String awayRecord, Integer goals, Double goalsPerGame, Integer conceded, Double concededPerGame, List<News> news) {
        this.name = name;
        this.record = record;
        this.pointsPerGame = pointsPerGame;
        this.homeRecord = homeRecord;
        this.awayRecord = awayRecord;
        this.goals = goals;
        this.goalsPerGame = goalsPerGame;
        this.conceded = conceded;
        this.concededPerGame = concededPerGame;
        this.news = news;
    }

    public Team(String name) {
        this.name = name;
    }

    public void addNews(News newsItem) { news.add(newsItem); }

    public String getName() {
        return name;
    }

    public String getRecord() {
        return record;
    }

    public Double getPointsPerGame() {
        return pointsPerGame;
    }

    public String getHomeRecord() {
        return homeRecord;
    }

    public String getAwayRecord() {
        return awayRecord;
    }

    public Integer getGoals() {
        return goals;
    }

    public Double getGoalsPerGame() {
        return goalsPerGame;
    }

    public Integer getConceded() {
        return conceded;
    }

    public Double getConcededPerGame() {
        return concededPerGame;
    }

    public List<News> getNews() {
        return news;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setRecord(String record) {
        this.record = record;
    }

    public void setPointsPerGame(Double pointsPerGame) {
        this.pointsPerGame = pointsPerGame;
    }

    public void setHomeRecord(String homeRecord) {
        this.homeRecord = homeRecord;
    }

    public void setAwayRecord(String awayRecord) {
        this.awayRecord = awayRecord;
    }

    public void setGoals(Integer goals) {
        this.goals = goals;
    }

    public void setGoalsPerGame(Double goalsPerGame) {
        this.goalsPerGame = goalsPerGame;
    }

    public void setConceded(Integer conceded) {
        this.conceded = conceded;
    }

    public void setConcededPerGame(Double concededPerGame) {
        this.concededPerGame = concededPerGame;
    }

    public void setNews(List<News> news) {
        this.news = news;
    }
}
