import {Stack, Card, Button, Container, Collapse, Table} from "react-bootstrap";
import "../../App.css";
import "./index.css";
import {useContext, useEffect, useState} from "react";
import {NewsContext} from "../../contexts/NewsContext";
import {TeamsContext} from "../../contexts/TeamsContext";
import {UserInfoContext} from "../../contexts/UserInfoContext";
import Loader from "../Loader/index.js";


const MyTeam = () => {

    const [loading, setLoading] = useState(true);

    const { team } = useContext(UserInfoContext);
    const { teamsForTable, getTeamsForTable } = useContext(TeamsContext);

    const { news, getNews } = useContext(NewsContext);
    const [newsCardToggleStates, setNewsCardToggleStates] = useState({})

    useEffect(() => {
        const loadTeamData = async () => {
            if(team) {
                await getTeamsForTable(team.name);
                await getNews(team.name);
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
                <Card className="card" style={{height: '40vh'}}>
                    <Card.Body>
                        <Card.Title>Fixture</Card.Title>
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