import {createContext, useState} from 'react';

export const UserInfoContext = createContext();

export const UserInfoProvider = ({ children }) => {

    const [league, setLeague] = useState('');
    const [team, setTeam] = useState(
        { name:'N/A', record:'N/A', pointsPerGame:'N/A', homeRecord:'N/A', awayRecord:'N/A', goals:'N/A', goalsPerGame:'N/A' }
    );

    return (
      <UserInfoContext.Provider value={{ league, setLeague, team, setTeam }}>
          {children}
      </UserInfoContext.Provider>
    );

}