import {createContext, useEffect, useState} from 'react';
import axios from 'axios';

export const NewsContext = createContext();

export const NewsProvider = ({ children }) => {

    const [news, setNews] = useState([]);

    const getNews = async (teamName) => {
        try {
            axios.get('http://localhost:8080/api/teams/news', {
                params: {teamName: teamName}
            })
                .then(response => {
                    setNews(response.data);
                })
        } catch(error) {
            console.log("Error fetching news:", error);
        }
    }

    return (
        <NewsContext.Provider value={{ news, getNews }}>
            {children}
        </NewsContext.Provider>
    );
}