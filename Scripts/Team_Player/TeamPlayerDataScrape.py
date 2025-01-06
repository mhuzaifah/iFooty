from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from io import StringIO
import re

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

    #Parsing Website to get the current PL Table
    html = requests.get('https://fbref.com/en/comps/9/Premier-League-Stats').text
    soup = BeautifulSoup(html, 'lxml')
    pl_table = soup.find_all('table', class_='stats_table')[0]

    #Parsing PL Table to get all current teams' links
    links = pl_table.find_all('a')
    links = [l.get('href') for l in links]
    links = [l for l in links if '/squads/' in l] #Only storing links related to squads
    plTeamUrls = [f"https://fbref.com{l}" for l in links]

    #Parsing each teams link to get required information/stats related to club
    teams = [] #list to keep track of teams for pl_teams.csv file indexes and news data scraping
    teamDict = {'Brighton and Hove Albion' : 'Brighton', 'Wolverhampton Wanderers' : 'Wolves'} # names of teams that are different in pl teams table (cause primary key errors)
    for placement in range(len(plTeamUrls)):

        teamUrl = plTeamUrls[placement]
        teamURLName = teamUrl.split('/')[-1].replace('-Stats', '').replace('-',' ') # Getting the team url name
        teamName = teamDict.get(teamURLName) if teamURLName in teamDict else teamURLName # Choose the correct team name relative to pl teams table in database
        teams.append(teamName) # Append the team name to teams

        data = requests.get(teamUrl).text
        soup = BeautifulSoup(data, 'lxml')

        # Parsing each teams' Player Stats
        player_stats_table = soup.find_all('table', class_='stats_table')[0]
        players_data = pd.read_html(StringIO(str(player_stats_table)))[0]
        players_data['team'] = teamName
        players_data.rename(columns={'90s': 'nineties'}, inplace=True) #renaming 90s column 
        players_data.rename(columns={'Nation': 'nation'}, inplace=True) #renaming Nation column 
        players_data.rename(columns={'Age': 'age'}, inplace=True) #renaming Age column 
        players_data.rename(columns={ 'Player' : 'name' }, inplace=True) #renaming Player column 
        players_data.rename(columns={ 'Min' : 'mins' }, inplace=True) #renaming Min column 
        players_data.rename(columns={ 'MP' : 'mp' }, inplace=True) #renaming MP column 
        players_data.rename(columns={ 'Starts' : 'starts' }, inplace=True) #renaming Start column 
        players_data.rename(columns={ 'xG' : 'xg' }, inplace=True) #renaming xG column 
        players_data.rename(columns={ 'xAG' : 'xag' }, inplace=True) #renaming xAG column 
        players_data.rename(columns={ 'Pos' : 'pos' }, inplace=True) #renaming Pos column 
        players_data.rename(columns={ 'Gls' : 'gls' }, inplace=True) #renaming Gls column 
        players_data.rename(columns={ 'Ast' : 'ast' }, inplace=True) #renaming Ast column 
        players_data[('Unnamed: 3_level_0', 'age')] = players_data[('Unnamed: 3_level_0', 'age')].apply(lambda x: x.split('-')[0] if isinstance(x, str) else x) #adjusting the age information
        players_data[('Unnamed: 1_level_0', 'nation')] = players_data[('Unnamed: 1_level_0', 'nation')].apply(lambda x: x.split(' ')[1] if isinstance(x, str) else x) #adjusting the nation information 
        players_data = players_data.drop(players_data.tail(2).index) #removing last 2 rows (irrelavant information)
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
    players_df.rename(columns={'':'team'}, inplace=True) # naming Team column
    players_df.index.name = 'id' # naming index column
    players_df.to_csv('pl_players.csv', index=False)

    teams_df = pd.DataFrame(pl_teams, index=teams)
    teams_df.index.name = 'name' # naming index column
    teams_df.to_csv('pl_teams.csv')
    
    return players_df, teams_df
    


        
    







