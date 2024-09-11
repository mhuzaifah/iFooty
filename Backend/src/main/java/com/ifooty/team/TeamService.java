package com.ifooty.team;

import com.ifooty.news.News;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Component
public class TeamService {

    private final TeamRepository teamRepository;

    @Autowired
    public TeamService(TeamRepository teamRepository) {
        this.teamRepository = teamRepository;
    }

    public void updateAllNewsToTeams(List<News> newsList) {
        newsList.forEach(news -> teamRepository.findByName(news.getTeam().getName())
                .ifPresent(team -> team.addNews(news))
        );
    }

    public List<Team> getAllTeams() { return teamRepository.findAll(); }

    public List<Team> getTeamsFiltered(
             Integer minWins,
             Integer maxWins,
             Integer minDraws,
             Integer maxDraws,
             Integer minLosses,
             Integer maxLosses,
             Double minPointsPerGame,
             Double maxPointsPerGame,
             Integer minGoals,
             Integer maxGoals,
             Double minGoalsPerGame,
             Double maxGoalsPerGame
    ) {
        List<Team> teams = teamRepository.findAll();

        if(minWins != null) teams = teams.stream().filter(team -> Integer.parseInt(team.getRecord().split("-")[0]) >= minWins).collect(Collectors.toList());
        if(maxWins != null) teams = teams.stream().filter(team -> Integer.parseInt(team.getRecord().split("-")[0]) <= maxWins).collect(Collectors.toList());
        if(minDraws != null) teams = teams.stream().filter(team -> Integer.parseInt(team.getRecord().split("-")[0]) >= minDraws).collect(Collectors.toList());
        if(maxDraws != null) teams = teams.stream().filter(team -> Integer.parseInt(team.getRecord().split("-")[0]) <= maxDraws).collect(Collectors.toList());
        if(minLosses != null) teams = teams.stream().filter(team -> Integer.parseInt(team.getRecord().split("-")[0]) >= minLosses).collect(Collectors.toList());
        if(maxLosses != null) teams = teams.stream().filter(team -> Integer.parseInt(team.getRecord().split("-")[0]) <= maxLosses).collect(Collectors.toList());
        if(minPointsPerGame != null) teams = teams.stream().filter(team -> team.getPointsPerGame() >= minPointsPerGame).collect(Collectors.toList());
        if(maxPointsPerGame != null) teams = teams.stream().filter(team -> team.getPointsPerGame() <= maxPointsPerGame).collect(Collectors.toList());
        if(minGoals != null) teams = teams.stream().filter(team -> team.getGoals() >= minGoals).collect(Collectors.toList());
        if(maxGoals != null) teams = teams.stream().filter(team -> team.getGoals() <= maxGoals).collect(Collectors.toList());
        if(minGoalsPerGame != null) teams = teams.stream().filter(team -> team.getGoalsPerGame() >= minGoalsPerGame).collect(Collectors.toList());
        if(maxGoalsPerGame != null) teams = teams.stream().filter(team -> team.getGoalsPerGame() <= maxGoalsPerGame).collect(Collectors.toList());

        return teams;
    }

    public List<Team> getTeamsForTable(String teamName) {
        Optional<Team> team = teamRepository.findByName(teamName);
        if(team.isPresent()) {
            List<Team> teams = teamRepository.findAll();
            Integer teamIdx = teams.stream().collect(Collectors.toList()).indexOf(team.get());
            System.out.println(teamIdx);

            int start = Math.max(0, teamIdx-5);
            int end = Math.min(teamIdx+5, teams.size());

            if(start == 0)
                end += 5-teamIdx;
            else if(end == teams.size())
                start -= (teamIdx+5)-end;

            return teams.subList(start, end);
        }
        return null;
    }

    public List<Team> getTeamsByName(String searchText) {
        return teamRepository.findAll().stream()
                .filter(team -> team.getName().toLowerCase().contains(searchText.toLowerCase()))
                .collect(Collectors.toList());
    }

    public Team updateTeam(Team updatedTeam) {
        Optional<Team> existingTeam = teamRepository.findByName(updatedTeam.getName());

        if(existingTeam.isPresent()) {
            Team teamToUpdate = existingTeam.get();
            teamToUpdate.setName(updatedTeam.getName());
            teamToUpdate.setName(updatedTeam.getName());
            teamToUpdate.setName(updatedTeam.getName());
            teamToUpdate.setName(updatedTeam.getName());

            teamRepository.save(teamToUpdate);
            return teamToUpdate;
        }
        return null;
    }


    @Transactional
    public void deleteTeam(String playerName) {
        teamRepository.deleteByName(playerName);
    }

    public Optional<Team> getTeamByName(String teamName) {
        return teamRepository.findByName(teamName);
    }

}
