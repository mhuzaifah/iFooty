package com.ifooty.player;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name="player_data")
public class Player {

    @Id
    @Column(name = "id", unique = true)
    private Integer id;
    private String name;
    private String nation;
    private String pos;
    private Double age;
    private Double mp;
    private Integer starts;
    private Double mins;
    private Double nineties;
    private Double gls;
    private Double ast;
    private Double xG;
    private Double xAG;
    private String team;

    public Player() {}

    public Player(Integer id, String player, String nation, String pos, Double age, Double mp, Integer starts, Double mins, Double nineties, Double gls, Double ast, Double xG, Double xAG, String team) {
        this.id = id;
        this.name = player;
        this.nation = nation;
        this.pos = pos;
        this.age = age;
        this.mp = mp;
        this.starts = starts;
        this.mins = mins;
        this.nineties = nineties;
        this.gls = gls;
        this.ast = ast;
        this.xG = xG;
        this.xAG = xAG;
        this.team = team;
    }

    public String getNation() {
        return nation;
    }

    public Integer getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public Double getAge() {
        return age;
    }

    public String getPos() {
        return pos;
    }

    public Double getMp() {
        return mp;
    }

    public Integer getStarts() {
        return starts;
    }

    public Double getMins() {
        return mins;
    }

    public Double getNineties() {
        return nineties;
    }

    public Double getGls() {
        return gls;
    }

    public Double getAst() {
        return ast;
    }

    public Double getxG() {
        return xG;
    }

    public Double getxAG() {
        return xAG;
    }

    public String getTeam() {
        return team;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setNation(String nation) {
        this.nation = nation;
    }

    public void setPos(String pos) {
        this.pos = pos;
    }

    public void setAge(Double age) {
        this.age = age;
    }

    public void setMp(Double mp) {
        this.mp = mp;
    }

    public void setStarts(Integer starts) {
        this.starts = starts;
    }

    public void setMins(Double mins) {
        this.mins = mins;
    }

    public void setNineties(Double nineties) {
        this.nineties = nineties;
    }

    public void setGls(Double gls) {
        this.gls = gls;
    }

    public void setAst(Double ast) {
        this.ast = ast;
    }

    public void setxAG(Double xAG) {
        this.xAG = xAG;
    }

    public void setxG(Double xG) {
        this.xG = xG;
    }

    public void setTeam(String team) {
        this.team = team;
    }
}
