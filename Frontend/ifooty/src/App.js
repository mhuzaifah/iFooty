import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Routes, Route, useLocation } from 'react-router-dom';
import VerticalNavBar from "./components/NavBar";
import {Container} from "react-bootstrap";
import MyTeam from "./components/MyTeam";
import Landing from "./components/Landing";
import Teams from "./components/Teams";
import Players from "./components/Players";
import {PlayersProvider} from "./contexts/PlayersContext";
import {TeamsProvider} from "./contexts/TeamsContext";
import {NewsProvider} from "./contexts/NewsContext";
import {UserInfoProvider} from "./contexts/UserInfoContext";

function App() {

    const location = useLocation();

    return (
      <div className={`App ${location.pathname === '/' ? 'designBackground' : 'simpleBackground'}`}>
          {location.pathname !== '/' && <VerticalNavBar />}
          <Container className="mainContentContainer">
              <UserInfoProvider>
              <PlayersProvider>
              <TeamsProvider>
              <NewsProvider>
                  <Routes>
                      <Route index element={<Landing />} />
                      <Route path="/myteam" element={<MyTeam />} />
                      <Route path="/players" element={<Players />} />
                      <Route path="/teams" element={<Teams />} />
                  </Routes>
              </NewsProvider>
              </TeamsProvider>
              </PlayersProvider>
              </UserInfoProvider>
          </Container>
      </div>
    );
}

export default App;
