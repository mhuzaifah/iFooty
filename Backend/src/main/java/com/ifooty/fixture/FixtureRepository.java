package com.ifooty.fixture;

import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;

public interface FixtureRepository extends JpaRepository<Fixture, String> {
    Optional<Fixture> findById(Integer Id);
}