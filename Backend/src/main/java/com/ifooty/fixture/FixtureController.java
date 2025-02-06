package com.ifooty.fixture;

import java.util.List;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@CrossOrigin
@RequestMapping(path = "api/fixtures")
public class FixtureController {

    private final FixtureService fixtureService;

    private static final Logger logger = LoggerFactory.getLogger(FixtureController.class);

    @Autowired
    public FixtureController(FixtureService fixtureService) { this.fixtureService = fixtureService; }

    @GetMapping()
    public List<Fixture> getAllFixtures() { return fixtureService.getAllFixtures(); }

    @GetMapping("/next-fixture")
    public Fixture getNextFixture(String team) {
        return fixtureService.getNextFixture(team);
    }

    @PutMapping("/{fixtureId}/setPrediction")
    public void updateFixturePrediction(@PathVariable Integer fixtureId, @RequestParam String prediction) {
        fixtureService.updatePrediction(fixtureId, prediction);
    }

}

