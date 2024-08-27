package com.fs.football_snap.team;

import com.fs.football_snap.news.News;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping(path = "api/teams")
public class TeamController {

    private final TeamService teamService;

    @Autowired
    public TeamController(TeamService teamService) {
        this.teamService = teamService;
    }

    @GetMapping
    public List<Team> getTeams(
            @RequestParam(required = false) String name
    ) {
        if(name != null) {
            return teamService.getTeamsByName(name);
        }
        else {
            return teamService.getTeams(); // Get all teams since no params were provided
        }
    }

    @GetMapping("/{teamName}/news")
    public List<News> getTeamNews(
            @PathVariable String teamName
    ) {
        Optional<Team> team = teamService.getTeamByName(teamName);
        if(team.isPresent()) {
            return team.get().getNews();
        }
        return null;
    }

}
