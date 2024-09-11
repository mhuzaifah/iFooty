import {Button, Col, Container, Form, Modal, Row, Stack, Table} from "react-bootstrap";
import React, {useContext, useEffect, useRef, useState} from "react";
import {PlayersContext} from "../../contexts/PlayersContext";
import {FaFilter} from "react-icons/fa";
import "./index.css";
import { chunk } from 'lodash';


const Players = () => {

    const {players, getPlayers} = useContext(PlayersContext);

    const [openFilters, setOpenFilters] = useState(false);

    const formRef = useRef(null);

    const initFilterValues = {
        position:null,
        name:null,
        nation:null,
        team:null,
        minAge:null,
        maxAge:null,
        minGoals:null,
        maxGoals:null,
        minAssists:null,
        maxAssists:null,
        minMatches:null,
        maxMatches:null,
        minXG:null,
        maxXG:null,
        minXAG:null,
        maxXAG:null,
        minStarts:null,
        maxStarts:null,
        minMinutes:null,
        maxMinutes:null,
        minNineties:null,
        maxNineties:null
    }

    const [filterValues, setFilterValues] = useState(initFilterValues)

    const filters = [
        { title:'position', type:"select",
            options: [
                { title:"Any", value:null },
                { title:"Forward", value:"FW" },
                { title:"Midfielder", value:"MF" },
                { title:"Defender", value:"DF" },
                { title:"Goalkeeper", value:"Gk" },
            ]
        },
        { title:'age', type:"number" },
        { title:'goals', type:"number" },
        { title:'assists', type:"number" },
        { title:'matches', type:"number" },
        { title:'xG', type:"number" },
        { title:'xAG', type:"number" },
        { title:'starts', type:"number" },
        { title:'minutes', type:"number" },
        { title:'nineties', type:"number" },
        { title:'name', type:"text", placeholder:"" },
        { title:'nation', type:"text", placeholder:"" },
        { title:'team', type:"text", placeholder:"" }
    ]

    useEffect(() => {
        getPlayers(filterValues);
    }, [])

    const handleFilterSubmit = (e) => {
        e.preventDefault();

        const formData = new FormData(formRef.current);
        const newFilterValues = {
            position: (formData.get('position') && formData.get('position') !== 'Any') ? formData.get('position') : null,
            name: (formData.get('name') && formData.get('name').replace(" ", "") !== "") ? formData.get('name') : null,
            nation: (formData.get('nation') && formData.get('nation').replace(" ", "") !== "") ? formData.get('nation') : null,
            team: (formData.get('team') && formData.get('team').replace(" ", "") !== "") ? formData.get('team') : null,
            minAge: formData.get('minAge') || null,
            maxAge: formData.get('maxAge') || null,
            minGoals: formData.get('minGoals') || null,
            maxGoals: formData.get('maxGoals') || null,
            minAssists: formData.get('minAssists') || null,
            maxAssists: formData.get('maxAssists') || null,
            minMatches: formData.get('minMatches') || null,
            maxMatches: formData.get('maxMatches') || null,
            minXG: formData.get('minXG') || null,
            maxXG: formData.get('maxXG') || null,
            minXAG: formData.get('minXAG') || null,
            maxXAG: formData.get('maxXAG') || null,
            minStarts: formData.get('minStarts') || null,
            maxStarts: formData.get('maxStarts') || null,
            minMinutes: formData.get('minMinutes') || null,
            maxMinutes: formData.get('maxMinutes') || null,
            minNineties: formData.get('minNineties') || null,
            maxNineties: formData.get('maxNineties') || null
        };
        console.log("New Filters:", newFilterValues);
        setFilterValues(newFilterValues);
        getPlayers(newFilterValues);
        handleModalToggle();
    }

    const handleModalToggle = () => {
        setOpenFilters(!openFilters);
    }

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFilterValues((prevValues) => (
            {
                ...prevValues,
                [name]: value,
            }
        ));
    }

    const handleFiltersReset = async () => {
        setFilterValues(initFilterValues);
        handleModalToggle();
        getPlayers(initFilterValues);
    }

    const chunkArray = (array, size) => {
        return array.length > 0 ? chunk(array, size) : [];
    }

    if (players.length === 0) {
        return <p>Loading...</p>;
    }

    return (
        <Stack direction="vertical" className="container">
            <Modal size="xl" show={openFilters} onHide={handleModalToggle} centered >
                <Modal.Header closeButton>
                    <Modal.Title style={{fontWeight:'bold'}} >FILTERS</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form ref={formRef} onSubmit={handleFilterSubmit} id="filterForm" >
                        <Stack direction="vertical" gap={4}>
                            {chunkArray(filters, 5).map((filterGroup, groupIndex) => (
                                <Row key={groupIndex} className="filterRow" >
                                    {filterGroup.map((filter) => (
                                        <Col key={filter.title} className="filter" >
                                            <Form.Label style={{ fontWeight: 'bold' }}>
                                                {filter.title.charAt(0).toUpperCase() + filter.title.slice(1)}
                                            </Form.Label>
                                            <Row>
                                                { filter.type === "number" && (
                                                    <div>
                                                        <Col className="filterInput">
                                                            <Form.Group controlId={`${filter.title}Min`}>
                                                                <Form.Control
                                                                    min={0}
                                                                    type="number"
                                                                    placeholder="Min"
                                                                    name={`min${filter.title.charAt(0).toUpperCase() + filter.title.slice(1)}`}
                                                                    value={filterValues[`min${filter.title.charAt(0).toUpperCase() + filter.title.slice(1)}`]}
                                                                    onChange={handleInputChange}
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
                                                                    value={filterValues[`max${filter.title.charAt(0).toUpperCase() + filter.title.slice(1)}`]}
                                                                    onChange={handleInputChange}
                                                                />
                                                            </Form.Group>
                                                        </Col>
                                                    </div>
                                                )}
                                                { filter.type === "text" && (
                                                    <Col className="filterInput">
                                                        <Form.Control
                                                            type="text"
                                                            placeholder={filter.placeholder}
                                                            name={filter.title}
                                                            value={filterValues[filter.title]}
                                                            onChange={handleInputChange}
                                                    />
                                                    </Col>
                                                )}
                                                { filter.type === "select" && (
                                                    <Col className="filterInput">
                                                        <Form.Control as="select" name={filter.title} value={filterValues[filter.title]} onChange={handleInputChange} >
                                                            { filter.options.map((option, idx) => (
                                                                <option key={idx} value={option.value} >
                                                                    {option.title}
                                                                </option>
                                                            ))}
                                                        </Form.Control>
                                                    </Col>
                                                )}
                                            </Row>
                                        </Col>
                                    ))}
                                </Row>
                            ))}
                        </Stack>
                    </Form>
                </Modal.Body>
                <Modal.Footer style={{display:'flex', justifyContent:'center'}}>
                    <Button className="secondaryButton" onClick={handleFiltersReset} style={{ fontWeight: 'bold' }}>
                        RESET
                    </Button>
                    <Button className="secondaryButton" type="submit" form="filterForm" style={{ fontWeight: 'bold' }}>
                        APPLY
                    </Button>
                </Modal.Footer>
            </Modal>
            <Container className="tableContainer">
                <Table hover responsive={true} className="styledTable">
                    <thead>
                    <tr>
                        <th>Name</th>
                        <th>Nation</th>
                        <th>Position</th>
                        <th>Age</th>
                        <th>Team</th>
                        <th>Goals</th>
                        <th>Assists</th>
                        <th>Matches</th>
                        <th>xG</th>
                        <th>xAG</th>
                        <th>Starts</th>
                        <th>Minutes</th>
                        <th>90s</th>
                        <th>
                            <Button className="secondaryButton" style={{width: '50px'}} onClick={handleModalToggle}>
                                <FaFilter/>
                            </Button>
                        </th>
                    </tr>
                    </thead>
                    <tbody>
                    {players.map(player => (
                        <tr key={player.id}>
                            <td>{player.name}</td>
                            <td>{player.nation}</td>
                            <td>{player.pos}</td>
                            <td>{player.age}</td>
                            <td>{player.team}</td>
                            <td>{player.gls}</td>
                            <td>{player.ast}</td>
                            <td>{player.mp}</td>
                            <td>{player.xG}</td>
                            <td>{player.xAG}</td>
                            <td>{player.starts}</td>
                            <td>{player.mins}</td>
                            <td>{player.nineties}</td>
                            <td style={{width: '1px', whiteSpace: 'nowrap'}}></td>
                        </tr>
                    ))}
                    </tbody>
                </Table>
            </Container>
        </Stack>
    );
}

export default Players;