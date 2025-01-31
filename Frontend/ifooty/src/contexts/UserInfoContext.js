import {createContext, useEffect, useState} from 'react';

export const UserInfoContext = createContext();

export const UserInfoProvider = ({ children }) => {

    const [league, setLeague] = useState('');
    const [team, setTeam] = useState(() => {
            const storedTeam = localStorage.getItem('team');
            return storedTeam ? JSON.parse(storedTeam) : { name:'N/A', record:'N/A', pointsPerGame:'N/A', homeRecord:'N/A', awayRecord:'N/A', goals:'N/A', goalsPerGame:'N/A' };
    });

    useEffect(() => {
        if(team) {
            localStorage.setItem("team", JSON.stringify(team));
        }
        else {
            localStorage.removeItem("team");
        }
    }, [team])

    return (
      <UserInfoContext.Provider value={{ league, setLeague, team, setTeam }}>
          {children}
      </UserInfoContext.Provider>
    );

}