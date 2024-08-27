package com.fs.football_snap.player;

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
    private Double min;
    private Double nineties;
    private Double gls;
    private Double ast;
    private Double xG;
    private Double xAG;
    private String team;

    public Player() {}

    public Player(Integer id, String player, String nation, String pos, Double age, Double mp, Integer starts, Double min, Double nineties, Double gls, Double ast, Double xG, Double xAG, String team) {
        this.id = id;
        this.name = player;
        this.nation = nation;
        this.pos = pos;
        this.age = age;
        this.mp = mp;
        this.starts = starts;
        this.min = min;
        this.nineties = nineties;
        this.gls = gls;
        this.ast = ast;
        this.xG = xG;
        this.xAG = xAG;
        this.team = team;
    }

    public Player(Integer id, String player, String nation, String pos, Double age) {
        this.id = id;
        this.name = player;
        this.nation = nation;
        this.pos = pos;
        this.age = age;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getTeam() {
        return this.team;
    }

    public String getName() {
        return this.name;
    }

    public String getPos() {
        return this.pos;
    }

    public String getNation() {
        return this.nation;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setTeam(String team) {
        this.team = team;
    }

    public void setPos(String pos) {
        this.pos = pos;
    }

    public void setNation(String nation) {
        this.nation = nation;
    }
}
