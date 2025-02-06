package com.ifooty.fixture;

import java.util.Date;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name="pl_fixtures")
public class Fixture {

    @Id
    @Column(name="id", unique = true)
    private Integer id;
    private String home;
    private String away;
    private Date date;
    private String time;
    private String venue;
    private String prediction;

    public Fixture() {}

    public Fixture(Integer id, String home, String away, Date date, String time, String venue, String prediction) {
        this.id = id;
        this.home = home;
        this.away = away;
        this.date = date;
        this.time = time;
        this.venue = venue;
        this.prediction = prediction;
    }

    public Integer getId() {
        return id;
    }

    public String getTime() {
        return time;
    }

    public String getVenue() {
        return venue;
    }

    public Date getDate() {
        return date;
    }

    public String getAway() {
        return away;
    }

    public String getHome() {
        return home;
    }

    public String getPrediction() {
        if(this.prediction != null) 
            return this.prediction;
        else 
            return "No Prediction Available";
    }

    public void setVenue(String venue) {
        this.venue = venue;
    }

    public void setTime(String time) {
        this.time = time;
    }

    public void setAway(String away) {
        this.away = away;
    }

    public void setDate(Date date) {
        this.date = date;
    }

    public void setHome(String home) {
        this.home = home;
    }

    public void setPrediction(String prediction) {
        this.prediction = prediction;
    }
}