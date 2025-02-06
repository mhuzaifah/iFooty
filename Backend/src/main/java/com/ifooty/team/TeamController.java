package com.ifooty.team;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.ifooty.news.News;

@RestController
@CrossOrigin
@RequestMapping(path = "api/teams")
public class TeamController {

    private final TeamService teamService;

    @Autowired
    public TeamController(TeamService teamService) {
        this.teamService = teamService;
    }

    @GetMapping()
    public List<Team> getAllTeams() {
        return teamService.getAllTeams();
    }

    @GetMapping("/filtered")
    public List<Team> getFilteredTeams(
            @RequestParam(required = false) Integer minWins,
            @RequestParam(required = false) Integer maxWins,
            @RequestParam(required = false) Integer minDraws,
            @RequestParam(required = false) Integer maxDraws,
            @RequestParam(required = false) Integer minLosses,
            @RequestParam(required = false) Integer maxLosses,
            @RequestParam(required = false) Double minPointsPerGame,
            @RequestParam(required = false) Double maxPointsPerGame,
            @RequestParam(required = false) Integer minGoals,
            @RequestParam(required = false) Integer maxGoals,
            @RequestParam(required = false) Double minGoalsPerGame,
            @RequestParam(required = false) Double maxGoalsPerGame,
            @RequestParam(required = false) Integer minConceded,
            @RequestParam(required = false) Integer maxConceded,
            @RequestParam(required = false) Double minConcededPerGame,
            @RequestParam(required = false) Double maxConcededPerGame
    ) {
        return teamService.getTeamsFiltered(minWins, maxWins, minDraws, maxDraws, minLosses, maxLosses, minPointsPerGame, maxPointsPerGame, minGoals, maxGoals, minGoalsPerGame, maxGoalsPerGame, minConceded, maxConceded, minConcededPerGame, maxConcededPerGame);
    }

    @GetMapping("/news")
    public List<News> getTeamNews(
            @RequestParam(required = true) String teamName
    ) {
        Optional<Team> team = teamService.getTeamByName(teamName);
        if(team.isPresent())
            return team.get().getNews();
        return null;
    }

    @GetMapping("/forTable")
    public List<Team> getTeamForTable(
        @RequestParam(required = true) String teamName
    ) {
        return teamService.getTeamsForTable(teamName);
    }

    @GetMapping("/record")
    public String getTeamRecord(
        @RequestParam(required = true) String teamName
    ) {
        Optional<Team> team = teamService.getTeamByName(teamName);
        return team.isPresent() ? team.get().getRecord() : null;
    }

    @GetMapping("/goalspergame")
    public Double getTeamGoalsPerGame(
        @RequestParam(required = true) String teamName
    ) {
        Optional<Team> team = teamService.getTeamByName(teamName);
        return team.isPresent() ? team.get().getGoalsPerGame() : null;
    }

    @GetMapping("/concededpergame")
    public Double getTeamConcededPerGame(
        @RequestParam(required = true) String teamName
    ) {
        Optional<Team> team = teamService.getTeamByName(teamName);
        return team.isPresent() ? team.get().getConcededPerGame() : null;
    }

}
