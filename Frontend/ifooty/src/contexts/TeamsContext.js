import {createContext, useState} from 'react';
import axios from 'axios';
import {forEach} from "lodash";
import teams from "../components/Teams";

export const TeamsContext = createContext();

export const TeamsProvider = ({ children }) => {

    const [filteredTeams, setFilteredTeams] = useState([]);
    const [allTeams, setAllTeams] = useState([]);
    const [teamsForTable, setTeamsForTable] = useState([]);

    const getFilteredTeams = async (filters) => {
        try {
            axios.get('http://localhost:8080/api/teams/filtered', {
                params: filters
            })
            .then(response => {
               setFilteredTeams(response.data);
            })
        } catch(error) {
            console.log("Error fetching teams:", error);
        }
    }

    //Right now only one league, must change when more leagures are introduced
    const getAllTeams = async () => {
        try {
            axios.get('http://localhost:8080/api/teams')
                .then(response => {
                    setAllTeams(response.data);
                })
        } catch(error) {
            console.log("Error fetching teams:", error);
        }
    }

    const getTeamsForTable = (teamName) => {

        try {
            axios.get('http://localhost:8080/api/teams/forTable', {
                params: {teamName: teamName}
            })
                .then(response => {
                    const teamsData = response.data;
                    console.log("Team Data", teamsData)
                    const teamsList = []

                    // Add pos value as attribute of a team during data scraping
                    forEach(teamsData, (team, i) => {
                        team = { ...teamsData[i], pos: i+1}
                        teamsList.push(team);
                    })

                    console.log("Teams", teamsList);
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