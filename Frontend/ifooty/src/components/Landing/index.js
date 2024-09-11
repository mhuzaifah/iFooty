import "./index.css";
import "../../App.css";
import Logo from "../../images/logo.png";
import playersHero from "../../images/playersHero.png";
import clubsHero from "../../images/clubsHero.png";
import newsHero from "../../images/newsHero.png";
import predictsHero from "../../images/predictionsHero.png";
import React, {useContext, useEffect, useState} from 'react';
import {Container, Row, Col, Button, Card, Image, FormSelect} from 'react-bootstrap';
import {TeamsContext} from "../../contexts/TeamsContext";
import {Link} from "react-router-dom";
import {UserInfoContext} from "../../contexts/UserInfoContext";

const Landing = () => {

    const { league, setLeague, team, setTeam } = useContext(UserInfoContext);
    const { allTeams, getAllTeams } = useContext(TeamsContext);
    useEffect(() => {
        if(league !== "")
            getAllTeams()
    }, [league])

    return (
        <Container fluid className="landingPageContainer">
            {/* Navbar */}
            <div className="navContainer" >
                <Container className="nav" fluid >
                    <div className="logo">
                        <Image src={Logo} alt='iFooty' style={{width:'45px', height:'45px'}}></Image>
                        <h4 style={{margin:0}}>iFooty</h4>
                    </div>
                    <Button variant="dark" className="mainButton">Sign Up</Button>
                </Container>
                <div className="divider"></div>
            </div>

            {/* Main content */}
            <Container className="sloganContainer">
                <h1 className="mb-3" style={{ fontSize: '3rem', fontWeight: 'bold' }}>Track. Support. Celebrate</h1>
                <p style={{ fontSize: '1.25rem', color: '#6c757d' }}>Everything you need to follow the beautiful game, all in one place.</p>
            </Container>

            {/* Cards */}
            <Container className="cardsContainer">
                <Row className="justify-content-center">
                    <Col md={4} className="mb-4">
                        <Card className="card sm" >
                            <Card.Body className="cardBody" >
                                <Container className='heroImgContainer' fluid>
                                    <Image src={playersHero} alt='playersHeroImg' className='heroImg' ></Image>
                                    <Image src={clubsHero} alt='clubsHeroImg' className='heroImg' ></Image>
                                </Container>
                                <h3>Teams & Players</h3>
                                <h6>Track your favourite teams and players' statistics</h6>
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col md={4} className="mb-4">
                        <Card className="card lg" >
                            <Card.Body className="cardBody" >
                                <h3>Select a Team</h3>
                                <div style={{width:'375px', display:'flex', flexDirection:'column', justifyContent:'center', alignItems:'center', gap:'10px'}} >
                                    <FormSelect value={league} onChange={(e) => setLeague(e.target.value)} >
                                        <option value="" disabled selected >Choose a League...</option>
                                        <option value="premierLeague" >Premier League</option>
                                    </FormSelect>
                                    <FormSelect
                                        value={team.name}
                                        onChange={(e) => (
                                            setTeam(allTeams.find(team => team.name === e.target.value))
                                        )}
                                    >
                                        <option value="" disabled selected >Choose a Team...</option>
                                        {
                                            allTeams.length > 0 && (
                                                allTeams.map((team, idx) => (
                                                    <option key={idx} value={team.name}>{team.name}</option>
                                                ))
                                            )
                                        }
                                    </FormSelect>
                                </div>
                                <Link to='/myteam'>
                                    <Button variant="dark" className="mainButton" >Continue</Button>
                                </Link>
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col md={4} className="mb-4">
                        <Card className="card sm" >
                            <Card.Body className="cardBody" >
                                <Container className='heroImgContainer' fluid>
                                    <Image src={newsHero} alt='newsHeroImg' className='heroImg' ></Image>
                                    <Image src={predictsHero} alt='predictsHeroImg' className='heroImg' ></Image>
                                </Container>
                                <h3>News & Predictions</h3>
                                <h6>Stay up to date with latest news efficiently and fixture predictions</h6>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>
        </Container>
    );
}

export default Landing;
