package com.ifooty.player;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@CrossOrigin
@RequestMapping(path = "api/players")
public class PlayerController {
    private final PlayerService playerService;

    @Autowired
    public PlayerController(PlayerService playerService) {
        this.playerService = playerService;
    }

    @GetMapping("/filtered")
    public List<Player> getPlayers(
            @RequestParam(required = false) String position,
            @RequestParam(required = false) String name,
            @RequestParam(required = false) String nation,
            @RequestParam(required = false) String team,
            @RequestParam(required = false) Integer minAge,
            @RequestParam(required = false) Integer maxAge,
            @RequestParam(required = false) Integer minGoals,
            @RequestParam(required = false) Integer maxGoals,
            @RequestParam(required = false) Integer minAssists,
            @RequestParam(required = false) Integer maxAssists,
            @RequestParam(required = false) Integer minMatches,
            @RequestParam(required = false) Integer maxMatches,
            @RequestParam(required = false) Double minXG,
            @RequestParam(required = false) Double maxXG,
            @RequestParam(required = false) Double minXAG,
            @RequestParam(required = false) Double maxXAG,
            @RequestParam(required = false) Integer minStarts,
            @RequestParam(required = false) Integer maxStarts,
            @RequestParam(required = false) Integer minMinutes,
            @RequestParam(required = false) Integer maxMinutes,
            @RequestParam(required = false) Integer minNineties,
            @RequestParam(required = false) Integer maxNineties
    ) {
        return playerService.getPlayersFiltered(position, name, nation, team, minAge, maxAge, minGoals, maxGoals, minAssists, maxAssists, minMatches, maxMatches, minXG, maxXG, minXAG, maxXAG, minStarts, maxStarts, minMinutes, maxMinutes, minNineties, maxNineties);
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
