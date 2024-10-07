from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from io import StringIO
import re
import newspaper
from datetime import datetime, timedelta
from pytz import timezone, utc
import psycopg2

def getTeamAndPlayerData():
    #Collections for storing scraped data and later converting to csv files
    pl_teams = {
        "record" : [],
        "points_per_game": [],
        "home_record": [],
        "away_record": [],
        "goals" : [],
        "goals_per_game" : []
    }
    pl_players = []
    pl_news = {
        "title" : [],
        "body" : [],
        "date" : [],
        "team" : [],
        "summary" : []
    }

    #Parsing Website to get the current PL Table
    html = requests.get('https://fbref.com/en/comps/9/Premier-League-Stats').text
    soup = BeautifulSoup(html, 'lxml')
    pl_table = soup.find_all('table', class_='stats_table')[0]

    #Parsing PL Table to get all current teams' links
    links = pl_table.find_all('a')
    links = [l.get('href') for l in links]
    links = [l for l in links if '/squads/' in l] #Only storing links related to squads
    pl_teams_urls = [f"https://fbref.com{l}" for l in links]

    #Parsing each teams link to get required information/stats related to club
    teams = [] #list to keep track of teams for pl_teams.csv file indexes and news data scraping
    for placement in range(len(pl_teams_urls)):

        team_url = pl_teams_urls[placement]
        name = team_url.split('/')[-1].replace('-Stats', '').replace('-',' ') #Getting the team name
        teams.append(name)
        print(name)

        data = requests.get(team_url).text
        soup = BeautifulSoup(data, 'lxml')

        # Parsing each teams' Player Stats
        player_stats_table = soup.find_all('table', class_='stats_table')[0]
        players_data = pd.read_html(StringIO(str(player_stats_table)))[0]
        players_data['Team'] = name
        players_data.rename(columns={'90s': 'nineties'}, inplace=True)
        players_data[('Unnamed: 3_level_0', 'Age')] = players_data[('Unnamed: 3_level_0', 'Age')].apply(lambda x: x.split('-')[0] if isinstance(x, str) else x)
        pl_players.append(players_data)
        

        # Parsing each teams' necessary Team Stats
        pTags = soup.find_all('p')
        club_stats_pTags = pTags[0:3] 
        for i in range(3):
            pTag = club_stats_pTags[i]
            text = re.sub(r'[ \n]', '', pTag.get_text())
            splitText = text.split(',')

            if i == 0:
                pl_teams["record"].append(splitText[0].split(':')[1])
                pl_teams["points_per_game"].append(splitText[1][splitText[1].find('(')+1:splitText[1].find('pergame')])
            elif i == 1:
                pl_teams["home_record"].append(splitText[0].split(':')[1])
                pl_teams["away_record"].append(splitText[1].split(':')[1])
            else:
                goalsData = splitText[0].split(':')[1].split('(')
                pl_teams["goals"].append(goalsData[0])
                pl_teams["goals_per_game"].append(goalsData[1][0:goalsData[1].find('pergame')])

        # Sleep to improve scraping perfomance/accuracy
        time.sleep(5)


    # Converting team and player data into csv files
    players_df = pd.concat(pl_players)
    players_df.columns = players_df.columns.droplevel() # removing header and making second row new header
    players_df = players_df.reset_index(drop=True) # resetting the index and dropping the old index column
    players_df = players_df.drop(players_df.columns[[10,11,12,13,14,15,17,19,20,21,22,27,30,33]], axis=1) # remove unwanted columns
    players_df = players_df.loc[:, ~players_df.columns.duplicated()] # retain only the first occurrence of each column
    players_df.rename(columns={'':'Team'}, inplace=True) # naming Team column
    players_df.to_csv('pl_players.csv')

    teams_df = pd.DataFrame(pl_teams, index=teams)
    teams_df.to_csv('pl_teams.csv')
    

# Function to import CSV into PostgreSQL
def importCSVtoPostgreSQL(csvFile, tableName, pk):
    df = pd.read_csv(csvFile)
    columns = df.columns.tolist()

    conn = psycopg2.connect(database = "ifooty", 
                            user = "postgres", 
                            host= 'localhost',
                            port = 5432)
    curr = conn.cursor()    
    
    # Loop through the rows in the DataFrame and update each row based on the primary key
    for i, row in df.iterrows():
        
        # Generate the SQL UPDATE query for each row
        setClause = ', '.join([f"{col} = %s" for col in columns[1:]]) #Pop since we don't want to include PK
        updateQuery = f"""
        UPDATE {tableName}
        SET {setClause}
        WHERE {pk} = %s
        """
        
        values = row.iloc[1:].tolist() + [row.iloc[0]] # Collect all values in list to dynamically add to query
        curr.execute(updateQuery, values) # Execute the query with the column values from the CSV

    conn.commit()
    curr.close()
    conn.close()

getTeamAndPlayerData()
importCSVtoPostgreSQL('pl_players.csv', 'player_data', 'id') 
importCSVtoPostgreSQL('pl_teams.csv', 'team_data', 'name') 






