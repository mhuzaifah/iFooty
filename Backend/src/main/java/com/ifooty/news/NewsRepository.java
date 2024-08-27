package com.fs.football_snap.news;

import com.fs.football_snap.team.Team;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface NewsRepository extends JpaRepository<News, String> {
    void deleteByTeam(Team team);
}
