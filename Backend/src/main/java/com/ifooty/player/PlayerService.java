package com.ifooty.player;

import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Component
public class PlayerService {
    private final PlayerRepository playerRepository;

    @Autowired
    public PlayerService(PlayerRepository playerRepository) {
        this.playerRepository = playerRepository;
    }

    public List<Player> getPlayersFiltered(
             String position,
             String name,
             String nation,
             String team,
             Integer minAge,
             Integer maxAge,
             Integer minGoals,
             Integer maxGoals,
             Integer minAssists,
             Integer maxAssists,
             Integer minMatches,
             Integer maxMatches,
             Double minXG,
             Double maxXG,
             Double minXAG,
             Double maxXAG,
             Integer minStarts,
             Integer maxStarts,
             Integer minMinutes,
             Integer maxMinutes,
             Integer minNineties,
             Integer maxNineties
    ) {
        List<Player> players = playerRepository.findAll();

        //Remove this later since this will be handeled during scraping
        players.stream().filter(player -> player.getName() != "Squad Total" && player.getName() != "Opponent Total");

        if(position != null) players = players.stream().filter(player -> player.getPos() != null && position.equalsIgnoreCase(player.getPos())).collect(Collectors.toList());
        if(name != null) players = players.stream().filter(player -> player.getName() != null && player.getName().toLowerCase().startsWith(name.toLowerCase())).collect(Collectors.toList());
        if(nation != null) players = players.stream().filter(player -> player.getNation() != null && player.getNation().toLowerCase().startsWith(nation.toLowerCase())).collect(Collectors.toList());
        if(team != null) players = players.stream().filter(player -> player.getTeam() != null && player.getTeam().toLowerCase().startsWith(team.toLowerCase())).collect(Collectors.toList());
        if(minAge != null) players = players.stream().filter(player -> player.getAge() != null && player.getAge() >= minAge).collect(Collectors.toList());
        if(maxAge != null) players = players.stream().filter(player -> player.getAge() != null && player.getAge() <= maxAge).collect(Collectors.toList());
        if(minGoals != null) players = players.stream().filter(player -> player.getGls() != null && player.getGls() >= minGoals).collect(Collectors.toList());
        if(maxGoals != null) players = players.stream().filter(player -> player.getGls() != null && player.getGls() <= maxGoals).collect(Collectors.toList());
        if(minAssists != null) players = players.stream().filter(player -> player.getAst() != null && player.getAst() >= minAssists).collect(Collectors.toList());
        if(maxAssists != null) players = players.stream().filter(player -> player.getAst() != null && player.getAst() <= maxAssists).collect(Collectors.toList());
        if(minMatches != null) players = players.stream().filter(player -> player.getMp() != null && player.getMp() >= minMatches).collect(Collectors.toList());
        if(maxMatches != null) players = players.stream().filter(player -> player.getMp() != null && player.getMp() <= maxMatches).collect(Collectors.toList());
        if(minXG != null) players = players.stream().filter(player -> player.getxG() != null && player.getxG() >= minXG).collect(Collectors.toList());
        if(maxXG != null) players = players.stream().filter(player -> player.getxG() != null && player.getxG() <= maxXG).collect(Collectors.toList());
        if(minXAG != null) players = players.stream().filter(player -> player.getxAG() != null && player.getxAG() >= minXAG).collect(Collectors.toList());
        if(maxXAG != null) players = players.stream().filter(player -> player.getxAG() != null && player.getxAG() <= maxXAG).collect(Collectors.toList());
        if(minStarts != null) players = players.stream().filter(player -> player.getStarts() != null && player.getStarts() >= minStarts).collect(Collectors.toList());
        if(maxStarts != null) players = players.stream().filter(player -> player.getStarts() != null && player.getStarts() <= maxStarts).collect(Collectors.toList());
        if(minMinutes != null) players = players.stream().filter(player -> player.getMins() != null && player.getMins() >= minMinutes).collect(Collectors.toList());
        if(maxMinutes != null) players = players.stream().filter(player -> player.getMins() != null && player.getMins() <= maxMinutes).collect(Collectors.toList());
        if(minNineties != null) players = players.stream().filter(player -> player.getNineties() != null && player.getNineties() >= minNineties).collect(Collectors.toList());
        if(maxNineties != null) players = players.stream().filter(player -> player.getNineties() != null && player.getNineties() <= maxNineties).collect(Collectors.toList());

        return players;
    }

    public List<Player> getPlayers() {
        return playerRepository.findAll();
    }

    public List<Player> getPlayersFromTeam(String teamName) {
        return playerRepository.findAll().stream()
                .filter(player -> teamName.equals(player.getTeam()))
                .collect(Collectors.toList());
    }

    public List<Player> getPlayersByName(String searchText) {
        return playerRepository.findAll().stream()
                .filter(player -> player.getName().toLowerCase().contains(searchText.toLowerCase()))
                .collect(Collectors.toList());
    }

    public List<Player> getPlayersByPos(String searchText) {
        return playerRepository.findAll().stream()
                .filter(player -> player.getPos().toLowerCase().contains(searchText.toLowerCase()))
                .collect(Collectors.toList());
    }

    public List<Player> getPlayersByNation(String searchText) {
        return playerRepository.findAll().stream()
                .filter(player -> player.getNation().toLowerCase().contains(searchText.toLowerCase()))
                .collect(Collectors.toList());
    }

    public List<Player> getPlayersByTeamAndPos(String team, String pos) {
        return playerRepository.findAll().stream()
                .filter(player -> team.equals(player.getTeam()) && pos.equals(player.getPos()))
                .collect(Collectors.toList());
    }

    public Player addPlayer(Player player) {
        playerRepository.save(player);
        return player;
    }

    public Player updatePlayer(Player updatedPlayer) {
        Optional<Player> existingPlayer = playerRepository.findByName(updatedPlayer.getName());

        if(existingPlayer.isPresent()) {
            Player playerToUpdate = existingPlayer.get();
            playerToUpdate.setName(updatedPlayer.getName());
            playerToUpdate.setTeam(updatedPlayer.getTeam());
            playerToUpdate.setPos(updatedPlayer.getPos());
            playerToUpdate.setNation(updatedPlayer.getNation());

            playerRepository.save(playerToUpdate);
            return playerToUpdate;
        }
        return null;
    }

    @Transactional
    public void deletePlayer(String playerName) {
        playerRepository.deleteByName(playerName);
    }
}
