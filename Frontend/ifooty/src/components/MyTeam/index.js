import {Stack, Card, Button, Container, Collapse, Table} from "react-bootstrap";
import "../../App.css";
import "./index.css";
import {useContext, useEffect, useState} from "react";
import {NewsContext} from "../../contexts/NewsContext";
import {TeamsContext} from "../../contexts/TeamsContext";
import {UserInfoContext} from "../../contexts/UserInfoContext";
import Loader from "../Loader/index.js";
import { FixtureContext } from "../../contexts/FixturesContext.js";
import { get } from "lodash";


const MyTeam = () => {

    const [loading, setLoading] = useState(true);

    const { team } = useContext(UserInfoContext);
    const { teamsForTable, getTeamsForTable, getTeamStat } = useContext(TeamsContext);

    const { news, getNews } = useContext(NewsContext);
    const [newsCardToggleStates, setNewsCardToggleStates] = useState({});

    const { nextFixture, getNextFixture, getFixturePrediction, setFixturePrediction } = useContext(FixtureContext);

    const getFixtureData = async () => {
        const fixture = await getNextFixture(team.name);
        if(fixture && fixture.prediction === "No Prediction Available") {
            try {
                const [
                    homeRec,
                    awayRec,
                    homeGPG,
                    awayGPG,
                    homeCPG,
                    awayCPG
                ] = await Promise.all([
                    getTeamStat(fixture.home, 'record'),
                    getTeamStat(fixture.away, 'record'),
                    getTeamStat(fixture.home, 'goalspergame'),
                    getTeamStat(fixture.away, 'goalspergame'),
                    getTeamStat(fixture.home, 'concededpergame'),
                    getTeamStat(fixture.away, 'concededpergame')
                ]);
        
                const data = {
                    "Home": fixture.home,
                    "Away": fixture.away,
                    "HomeRec": homeRec,
                    "AwayRec": awayRec,
                    "HomeGoalsPerGame": homeGPG,
                    "AwayGoalsPerGame": awayGPG,
                    "HomeConcededPerGame": homeCPG,
                    "AwayConcededPerGame": awayCPG,
                    "Year": 2025
                };
                
                try {
                    const prediction = await getFixturePrediction(data);
                    setFixturePrediction(fixture.id, prediction.predictedHome+"-"+prediction.predictedAway);
                    nextFixture.prediction = prediction.predictedHome+"-"+prediction.predictedAway;
                } catch (predictionError) {
                    console.error("Error getting prediction:", predictionError);
                    throw predictionError;
                }
            } catch (error) {
                console.error("Error getting prediction:", error);
            }
            
        }
    }

    useEffect(() => {
        const loadTeamData = async () => {
            if(team) {
                await getTeamsForTable(team.name);
                await getNews(team.name);
                await getFixtureData();
                setLoading(false);
            }
        };

        loadTeamData();
    }, [team]);


    const toggleNewsCard = (id) => {
        setNewsCardToggleStates( (prevState) => (
            {
                ...prevState,
                [id]: !prevState[id]
            }
        ))
    }

    if(loading)
        return ( <Loader /> )

    return (
        <Stack direction='horizontal' style={{maxHeight:'100%', width:'100%', margin:'1.5%'}} gap={4}>
            <Stack direction='vertical' style={{width:'65%'}} gap={4} >
                <Container className="card infoContainer"  style={{height:'75vh'}}>
                    <Stack direction="vertical" style={{overflow:'auto'}} gap={5} >
                        {
                            news
                            ?
                                news.length !== 0
                                ?
                                news.map((newsItem) => (
                                    <div className="newsCardContainer" key={newsItem.id} >
                                        <Stack direction="horizontal" className={`newsCardHeader ${newsCardToggleStates[newsItem.id] ? 'active' : ''}`}>
                                            <Container fluid style={{fontWeight:'bold'}} >{newsItem.title}</Container>
                                            <Button onClick={() => toggleNewsCard(newsItem.id)} className="dropDownButton">^</Button>
                                        </Stack>
                                        <Collapse in={newsCardToggleStates[newsItem.id] || false}>
                                            <div>
                                                <Container fluid className="newsCardBody" >
                                                    {newsItem.summary}
                                                </Container>
                                            </div>
                                        </Collapse>
                                    </div>
                                ))
                                :
                                <h2>Currently no news for your team!</h2>
                            :
                            <Loader />
                        }
                    </Stack>
                </Container>
                <Container className="card infoContainer" style={{height:'25vh'}}>
                    {
                        team
                            ?
                            (
                                <Table >
                                    <thead>
                                    <tr>
                                        <th>Club</th>
                                        <th>Record</th>
                                        <th>Points/Game</th>
                                        <th>Home Rec.</th>
                                        <th>Away Rec.</th>
                                        <th>Goals</th>
                                        <th>Goals/Game</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr key={team.name}>
                                        <td>{team.name}</td>
                                        <td>{team.record}</td>
                                        <td>{team.pointsPerGame}</td>
                                        <td>{team.homeRecord}</td>
                                        <td>{team.awayRecord}</td>
                                        <td>{team.goals}</td>
                                        <td>{team.goalsPerGame}</td>
                                    </tr>
                                    </tbody>
                                </Table>
                            )
                            :
                            <Loader />
                    }
                </Container>
            </Stack>
            <Stack direction='vertical' style={{width: '35%'}} gap={4}>
            <Card
            className="card"
            style={{
                height: '40vh',
                backgroundColor: 'whitesmoke',
                border: 'none',
                borderRadius: '10px',
                padding: '20px',
            }}
            >
            <Card.Body>
                <Card.Title
                style={{
                    fontSize: '1.5rem',
                    fontWeight: 'bold',
                    color: 'black',
                    marginBottom: '10px',
                }}
                >
                Next Fixture Prediction
                </Card.Title>
                <hr style={{ width: '100%', borderTop: '1px solid #ccc', marginBottom: '20px' }} />

                {nextFixture ? (
                <div
                    style={{
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                    alignItems: 'center',
                    height: '80%',
                    width: '100%',
                    gap: '30px',
                    }}
                >
                    <Stack direction="horizontal" gap={5}>
                    <Card.Text style={{ fontSize: '1rem', fontWeight: '600', color: 'black' }}>
                        {nextFixture.date.toLocaleDateString()}
                    </Card.Text>
                    <Card.Text style={{ fontSize: '1rem', fontWeight: '600', color: 'black' }}>
                        {nextFixture.time}
                    </Card.Text>
                    <Card.Text style={{ fontSize: '1rem', fontWeight: '600', color: 'black' }}>
                        {nextFixture.venue}
                    </Card.Text>
                    </Stack>

                    <Stack direction="horizontal" gap={3} style={{ justifyContent: 'center', alignItems: 'center' }}>
                    {/* Home Team Logo */}
                    <img
                        src="placeholder-home.png"
                        alt="Home Team Logo"
                        style={{ width: '50px', height: '50px', objectFit: 'contain' }}
                    />

                    <Card.Text style={{ fontSize: '1rem', fontWeight: '600', color: 'black', margin: 0 }}>
                        {nextFixture.home}
                    </Card.Text>

                    <Card.Text style={{ fontSize: '1rem', fontWeight: '500', color: 'black', margin: 0 }}>
                        {nextFixture.prediction}
                    </Card.Text>

                    <Card.Text style={{ fontSize: '1rem', fontWeight: '600', color: 'black', margin: 0 }}>
                        {nextFixture.away}
                    </Card.Text>

                    {/* Away Team Logo */}
                    <img
                        src="placeholder-away.png"
                        alt="Away Team Logo"
                        style={{ width: '50px', height: '50px', objectFit: 'contain' }}
                    />
                    </Stack>
                </div>
                ) : (
                <Loader />
                )}
            </Card.Body>
            </Card>
                <Container className="card newsCardContainer" style={{ height:'60vh' }}>
                    {
                        teamsForTable.length !== 0
                        ?
                        (
                            <Table hover responsive={true}>
                                <thead>
                                <tr>
                                    <th></th>
                                    <th>Club</th>
                                    <th>Record</th>
                                    <th>Points/Game</th>
                                </tr>
                                </thead>
                                <tbody>
                                {(teamsForTable.map( team => (
                                    <tr key={team.pos} className='teamRow'>
                                        <td>{team.pos}</td>
                                        <td>{team.name}</td>
                                        <td>{team.record}</td>
                                        <td>{team.pointsPerGame}</td>
                                    </tr>
                                )))}
                                </tbody>
                            </Table>
                        )
                        :
                        <Loader />
                    }

                </Container>
            </Stack>
        </Stack>
    );
}

export default MyTeam;