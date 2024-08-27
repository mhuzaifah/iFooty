import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Routes, Route } from 'react-router-dom';
import VerticalNavBar from "./components/NavBar";
import {Container} from "react-bootstrap";
import MyTeam from "./components/MyTeam";
import Landing from "./components/Landing";
import Teams from "./components/Teams";
import Players from "./components/Players";

function App() {
  return (
      <div className="App">
          <VerticalNavBar />
          <Container fluid>
              <Routes>
                  <Route index element={<Landing />} />
                  <Route path="/myteam" element={<MyTeam />} />
                  <Route path="/players" element={<Players />} />
                  <Route path="/teams" element={<Teams />} />
              </Routes>
          </Container>
      </div>
  );
}

export default App;
