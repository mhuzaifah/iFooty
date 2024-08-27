package com.fs.football_snap.team;

import com.fs.football_snap.news.News;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

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

    public List<Team> getTeams() { return teamRepository.findAll(); }

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
