import {createContext, useState} from 'react';
import axios from 'axios';
import {forEach} from "lodash";

export const TeamsContext = createContext();

export const TeamsProvider = ({ children }) => {

    const [filteredTeams, setFilteredTeams] = useState([]);
    const [allTeams, setAllTeams] = useState([]);
    const [teamsForTable, setTeamsForTable] = useState([]);

    const backendUrl = process.env.REACT_APP_SPRINGBOOT_URL;

    const getFilteredTeams = async (filters) => {
        try {
            axios.get(`${backendUrl}/api/teams/filtered`, {
                params: filters
            })
            .then(response => {
               setFilteredTeams(response.data);
            })
        } catch(error) {
            console.log("Error fetching teams:", error);
        }
    }

    //Right now only one league, must change when more leagues are introduced
    const getAllTeams = async () => {
        console.log(`${backendUrl}/api/teams`)
        try {
            axios.get(`${backendUrl}/api/teams`)
                .then(response => {
                    setAllTeams(response.data);
                })
        } catch(error) {
            console.log("Error fetching teams:", error);
        }
    }

    const getTeamsForTable = (teamName) => {

        try {
            axios.get(`${backendUrl}/api/teams/forTable`, {
                params: {teamName: teamName}
            })
                .then(response => {
                    const teamsData = response.data;
                    const teamsList = []

                    // Add pos value as attribute of a team during data scraping
                    forEach(teamsData, (team, i) => {
                        team = { ...teamsData[i], pos: i+1}
                        teamsList.push(team);
                    })

                    setTeamsForTable(teamsList);
                })
        } catch (error) {
            console.log("Error fetching teams:", error);
        }

    }

    return (
        <TeamsContext.Provider value={{ allTeams, getAllTeams, filteredTeams, getFilteredTeams, teamsForTable, getTeamsForTable}}>
            {children}
        </TeamsContext.Provider>
    );
}