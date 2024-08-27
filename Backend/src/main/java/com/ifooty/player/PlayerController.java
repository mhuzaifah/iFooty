package com.fs.football_snap.player;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping(path = "api/players")
public class PlayerController {
    private final PlayerService playerService;

    @Autowired
    public PlayerController(PlayerService playerService) {
        this.playerService = playerService;
    }

    @GetMapping
    public List<Player> getPlayers(
            @RequestParam(required = false) String name,
            @RequestParam(required = false) String team,
            @RequestParam(required = false) String pos,
            @RequestParam(required = false) String nation
    ) {
        if(team != null && pos != null) {
            return playerService.getPlayersByTeamAndPos(team, pos);
        }
        else if(team != null) {
            return playerService.getPlayersFromTeam(team);
        }
        else if(name != null) {
            return playerService.getPlayersByName(name);
        }
        else if(pos != null) {
            return playerService.getPlayersByPos(pos);
        }
        else if(nation != null) {
            return playerService.getPlayersByPos(nation);
        }
        else {
            return playerService.getPlayers(); // Get all players since no params were provided
        }
    }

    @PostMapping
    public ResponseEntity<Player> addPlayer(@RequestBody Player player) {
        Player createdPlayer = playerService.addPlayer(player);
        return new ResponseEntity<>(createdPlayer, HttpStatus.CREATED);
    }

    @PutMapping
    public ResponseEntity<Player> updatePlayer(@RequestBody Player player) {
        Player resultPlayer = playerService.updatePlayer(player);

        if(resultPlayer != null) {
            return new ResponseEntity<>(resultPlayer, HttpStatus.OK);
        }
        else {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }

    @DeleteMapping("/{playerName}")
    public ResponseEntity<String> deletePlayer(@PathVariable String playerName) {
        playerService.deletePlayer(playerName);
        return new ResponseEntity<>("Player deleted successfully", HttpStatus.OK);
    }
}
