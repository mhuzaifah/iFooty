import { createContext, useState } from "react";
import axios from "axios";

export const FixtureContext = createContext();

export const FixtureProvider = ({ children }) => {

    const backendUrl = process.env.REACT_APP_SPRINGBOOT_URL;
    const mlModelUrl = process.env.REACT_APP_PREDICTOR_URL;

    const [nextFixture, setNextFixture] = useState(null);

    const getNextFixture = async (team) => {
        try {
            const response = await axios.get(`${backendUrl}/api/fixtures/next-fixture`, {
                params: { team: team },
            });
            const fixtureData = response.data;
            fixtureData.date = new Date(fixtureData.date); 
            setNextFixture(fixtureData);
            return fixtureData;
        }
        catch(error) {
            console.log(`Error fetching next fixture for ${team}:`, error);
        }
    };

    const getFixturePrediction = async (data) => {
        console.log(`Accessing ${mlModelUrl}/predict`);
        try {
            const response = await axios.post(`${mlModelUrl}/predict`, data, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });            
            console.log(response.data);
            return response.data;
        }
        catch(error) {
            console.log(`Error fetching next fixture prediction for ${data}:`, error);
            throw error;
        }
    };

    const setFixturePrediction = async (fixtureId, prediction) => {
        try {
            await axios.put(`${backendUrl}/api/fixtures/${fixtureId}/setPrediction`, null, {
                params : {prediction : prediction}
            })
            console.log(`Successfully set prediction for fixture ${fixtureId}`);
        } catch(error) {
            console.log(`Error setting prediction for fixture ${fixtureId}:`, error);
            throw error;
        }
    } 

    return (
        <FixtureContext.Provider value={{nextFixture, getNextFixture, getFixturePrediction, setFixturePrediction}} >
            {children}
        </FixtureContext.Provider>
    );

}
