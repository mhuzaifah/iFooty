package com.fs.football_snap.news;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fs.football_snap.team.Team;
import jakarta.persistence.*;

import java.io.Serializable;
import java.util.Date;

@Entity
@EntityListeners(NewsEntityListener.class)
@Table(name="news_data")
public class News implements Serializable {

    @Id
    @Column(name="id", unique = true)
    private String id;
    private String title;
    private String body;
    private Date date;
    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "team", nullable = false)
    @JsonIgnore // If not ignored, will create an infinite cycle Team and News list JSON object for each News entity
    private Team team;
    private String summary;

    public News() {}

    public News(String id, String title, String body, Date date) {
        this.id = id;
        this.title = title;
        this.body = body;
        this.date = date;
    }

    public News(String id, String title, String body, Date date, Team team) {
        this.id = id;
        this.title = title;
        this.body = body;
        this.date = date;
        this.team = team;
    }

    public String getId() { return id; }

    public String getTitle() {
        return title;
    }

    public String getBody() {
        return body;
    }

    public Date getDate() {
        return date;
    }

    public Team getTeam() {
        return team;
    }

    public String getSummary() { return summary; }

    public void setId(String id) {
        this.id = id;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setBody(String body) {
        this.body = body;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public void setTeam(Team team) {
        this.team = team;
    }

    public void setSummary(String summary) { this.summary = summary; }
}

