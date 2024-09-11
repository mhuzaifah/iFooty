import {Button, Col, Container, Form, Modal, Row, Stack, Table} from "react-bootstrap";
import {useContext, useEffect, useRef, useState} from "react";
import "../../App.css";
import "./index.css";
import {TeamsContext} from "../../contexts/TeamsContext";
import { FaFilter } from "react-icons/fa";
import {chunk} from "lodash";
import React from "react";

const Teams = () => {

    const {filteredTeams, getFilteredTeams} = useContext(TeamsContext);

    const [filterValues, setFilterValues] = useState(
        {
            minWins:null,
            maxWins:null,
            minDraws:null,
            maxDraws:null,
            minLosses:null,
            maxLosses:null,
            minPointsPerGame:null,
            maxPointsPerGame:null,
            minGoals:null,
            maxGoals:null,
            minGoalsPerGame:null,
            maxGoalsPerGame:null,
        }
    )

    const [openFilters, setOpenFilters] = useState(false);

    const formRef = useRef(null);

    useEffect(() => {
        getFilteredTeams(filterValues);
    }, [])

    const handleFilterSubmit = (e) => {
        e.preventDefault();

        const formData = new FormData(formRef.current);
        console.log("Form Data", formData);
        const newFilterValues = {
            minWins: formData.get('minWins') || null,
            maxWins: formData.get('maxWins') || null,
            minDraws: formData.get('minDraws') || null,
            maxDraws: formData.get('maxDraws') || null,
            minLosses: formData.get('minLosses') || null,
            maxLosses: formData.get('maxLosses') || null,
            minPointsPerGame: formData.get('minPointsPerGame') || null,
            maxPointsPerGame: formData.get('maxPointsPerGame') || null,
            minGoals: formData.get('minGoals') || null,
            maxGoals: formData.get('maxGoals') || null,
            minGoalsPerGame: formData.get('minGoalsPerGame') || null,
            maxGoalsPerGame: formData.get('maxGoalsPerGame') || null,
        };
        setFilterValues(newFilterValues);
        getFilteredTeams(newFilterValues);
        handleModalToggle();
    }

    const handleModalToggle = () => {
        setOpenFilters(!openFilters);
    }

    const filters = [
        { title:'wins' },
        { title:'draws' },
        { title:'losses' },
        { title:'pointsPerGame' },
        { title:'goals' },
        { title:'goalsPerGame' }
    ]

    // Helper function to split up filter array for formatting
    const chunkArray = (array, size) => {
        return array.length > 0 ? chunk(array, size) : [];
    }

    if (filteredTeams.length === 0) {
        return <p>Loading...</p>;
    }

    return (
        <Stack direction="vertical" className="container" >
            <Modal size="xl" show={openFilters} onHide={handleModalToggle}  centered >
                <Modal.Header closeButton>
                    <Modal.Title style={{fontWeight:'bold'}} >FILTERS</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form ref={formRef} onSubmit={handleFilterSubmit} id="filterForm">
                        <Stack direction="vertical" gap={4}>
                            {chunkArray(filters, 3).map((filterGroup, groupIndex) => (
                                <Row key={groupIndex} className="filterRow">
                                    {filterGroup.map((filter) => (
                                        <Col key={filter.title} className="filter">
                                            <Form.Label style={{ fontWeight: 'bold' }}>
                                                {filter.title.charAt(0).toUpperCase() + filter.title.slice(1).replace("Per", "/")}
                                            </Form.Label>
                                            <Row>
                                                <Col className="filterInput">
                                                    <Form.Group controlId={`${filter.title}Min`}>
                                                        <Form.Control
                                                            min={0}
                                                            type="number"
                                                            placeholder="Min"
                                                            name={`min${filter.title.charAt(0).toUpperCase() + filter.title.slice(1)}`}
                                                        />
                                                    </Form.Group>
                                                </Col>
                                                <Col className="filterInput">
                                                    <Form.Group controlId={`${filter.title}Max`}>
                                                        <Form.Control
                                                            min={0}
                                                            type="number"
                                                            placeholder="Max"
                                                            name={`max${filter.title.charAt(0).toUpperCase() + filter.title.slice(1)}`}
                                                        />
                                                    </Form.Group>
                                                </Col>
                                            </Row>
                                        </Col>
                                    ))}
                                </Row>
                            ))}
                        </Stack>
                    </Form>
                </Modal.Body>
                <Modal.Footer style={{display:'flex', justifyContent:'space-evenly'}}>
                    <Button className="secondaryButton" onClick={handleModalToggle} style={{ fontWeight: 'bold' }}>
                        CLOSE
                    </Button>
                    <Button className="secondaryButton" type="submit" form="filterForm" style={{ fontWeight: 'bold' }}>
                        APPLY
                    </Button>
                </Modal.Footer>
            </Modal>
            <Container className="tableContainer" >
                <Table hover responsive={true} className="styledTable">
                    <thead>
                    <tr>
                        <th>Club</th>
                        <th>Record</th>
                        <th>Points/Game</th>
                        <th>Home Rec.</th>
                        <th>Away Rec.</th>
                        <th>Goals</th>
                        <th>Goals/Game</th>
                        <th>
                            <Button className="secondaryButton" style={{ width: '50px' }} onClick={handleModalToggle}>
                                <FaFilter />
                            </Button>
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    {filteredTeams.map(team => (
                        <tr key={team.name}>
                            <td>{team.name}</td>
                            <td>{team.record}</td>
                            <td>{team.pointsPerGame}</td>
                            <td>{team.homeRecord}</td>
                            <td>{team.awayRecord}</td>
                            <td>{team.goals}</td>
                            <td>{team.goalsPerGame}</td>
                            <td style={{ width: '1px', whiteSpace: 'nowrap' }}></td>
                        </tr>
                    ))}
                    </tbody>
                </Table>
            </Container>
        </Stack>
    );
}

export default Teams;