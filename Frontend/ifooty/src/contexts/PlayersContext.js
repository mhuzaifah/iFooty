import {createContext, useEffect, useState} from 'react';
import axios from 'axios';

export const PlayersContext = createContext();

export const PlayersProvider = ({ children }) => {
    const [players, setPlayers] = useState([]);

    const backendUrl = process.env.REACT_APP_SPRINGBOOT_URL;

    const getPlayers = async (filters) => {
        try {
            axios.get(`${backendUrl}/api/players/filtered`, {
                params: filters
            })
                .then(response => {
                    setPlayers(response.data);
                    console.log("New Players List:", response.data);
                })
        } catch(error) {
            console.log("Error fetching players:", error);
        }
    }
    
    return (
        <PlayersContext.Provider value={{ players, getPlayers }}>
            {children}
        </PlayersContext.Provider>
    );
}