package com.ifooty.fixture;

import java.util.Comparator;
import java.util.Date;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class FixtureService {

    private final FixtureRepository fixtureRepository;

    private static final Logger logger = LoggerFactory.getLogger(FixtureService.class);

    @Autowired
    public FixtureService(FixtureRepository fixtureRepositry ) { this.fixtureRepository = fixtureRepositry; }

    public List<Fixture> getAllFixtures() { return this.fixtureRepository.findAll(); }

    public Fixture getNextFixture(String team) {

        List<Fixture> teamFixtures = this.fixtureRepository.findAll().stream()
                .filter(
                    fixture -> (fixture.getHome().equalsIgnoreCase(team) || fixture.getAway().equalsIgnoreCase(team))
                )
                .collect(
                    Collectors.toList()
                );

        
        if(!teamFixtures.isEmpty()) {
            Date currentDate = new Date();

            Optional<Fixture> nextFixture = teamFixtures.stream()
                .filter(fixture -> fixture.getDate().after(currentDate))
                .sorted(Comparator.comparing(Fixture::getDate))
                .findFirst();


            return nextFixture.isPresent() ? nextFixture.get() : null;
        }

        return null;
    }

    public void updatePrediction(Integer Id, String prediction) {

        Optional<Fixture> fixtureOptional = fixtureRepository.findById(Id);
        if(fixtureOptional.isPresent()) {
            Fixture fixture = fixtureOptional.get();
            fixture.setPrediction(prediction);
            fixtureRepository.save(fixture);
        }
    }

}