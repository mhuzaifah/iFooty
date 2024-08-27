import {Stack, Card} from "react-bootstrap";

const MyTeam = () => {
    return (
        <Stack direction='horizontal' style={{maxHeight:'100vh', width:'100%', padding:'1%'}} gap={2}>
            <Stack direction='vertical' style={{width:'65%'}} gap={2} >
                <Card style={{ height:'75vh' }}>
                    <Card.Body>
                        <Card.Title>News</Card.Title>
                    </Card.Body>
                </Card>
                <Card style={{ height:'25vh' }}>
                    <Card.Body>
                        <Card.Title>Stats</Card.Title>
                    </Card.Body>
                </Card>
            </Stack>
            <Stack direction='vertical' style={{width:'35%'}} gap={2} >
                <Card style={{ height:'40vh' }}>
                    <Card.Body>
                        <Card.Title>Fixture</Card.Title>
                    </Card.Body>
                </Card>
                <Card style={{ height:'60vh' }}>
                    <Card.Body>
                        <Card.Title>Table</Card.Title>
                    </Card.Body>
                </Card>
            </Stack>
        </Stack>
    );
}

export default MyTeam;