from bs4 import BeautifulSoup
import pandas as pd
import requests
import time
from io import StringIO
import re
import newspaper
from datetime import datetime, timedelta
from pytz import timezone, utc

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
html = requests.get('https://fbref.com/en/comps/9/2023-2024/2023-2024-Premier-League-Stats').text
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

    data = requests.get(team_url).text
    soup = BeautifulSoup(data, 'lxml')

    # # Parsing each teams' Player Stats
    # player_stats_table = soup.find_all('table', class_='stats_table')[0]
    # players_data = pd.read_html(StringIO(str(player_stats_table)))[0]
    # players_data["Team"] = name
    # pl_players.append(players_data)

    # # Parsing each teams' necessary Team Stats
    # pTags = soup.find_all('p')
    # club_stats_pTags = pTags[0:3] if placement < 17 else pTags[0:1] + pTags[2:4]
    # for i in range(3):
    #     pTag = club_stats_pTags[i]
    #     text = re.sub(r'[ \n]', '', pTag.get_text())
    #     splitText = text.split(',')

    #     if i == 0:
    #         pl_teams["record"].append(splitText[0].split(':')[1])
    #         pl_teams["points_per_game"].append(splitText[1][splitText[1].find('(')+1:splitText[1].find('pergame')])
    #     elif i == 1:
    #         pl_teams["home_record"].append(splitText[0].split(':')[1])
    #         pl_teams["away_record"].append(splitText[1].split(':')[1])
    #     else:
    #         goalsData = splitText[0].split(':')[1].split('(')
    #         pl_teams["goals"].append(goalsData[0])
    #         pl_teams["goals_per_game"].append(goalsData[1][0:goalsData[1].find('pergame')])

    # # Sleep to improve scraping perfomance/accuracy
    # time.sleep(5)

print(teams)
#Parsing another website to get each teams' relevant news data
for team in teams:
    team: str
    teamName = team.lower().replace(' ', '-')
    print(team, teamName)
    page = 1
    weekAgoReached = False
    print(weekAgoReached)
    while not weekAgoReached:
        print(page)
        link = f'https://www.football365.com/{teamName}/news' if page == 1 else f'https://www.football365.com/{teamName}/page/{page}'
        html = requests.get(link).text
        soup = BeautifulSoup(html, 'lxml')
        articleComponents = [article for article in soup.find_all(class_='news-card') if not article.find_parent('aside')] # only want news articles in the main section of the page

        print(len(articleComponents))
        
        #Parsing each article component/card one by one
        for articleComponent in articleComponents:

            categories = []
            categories += [tag.get_text(strip=True) for tag in articleComponent.find_all('a', class_='ps-tag')]
            categories += [tag.get_text(strip=True) for tag in articleComponent.find_all('a', class_='ps-tag-1')]

            if team not in categories: # skipping news articles not related to the team
                continue

            timeTag = articleComponent.find('time')
            if timeTag:
                postTime = datetime.strptime(re.sub(r'(\d+)(st|nd|rd|th)', r'\1', timeTag['datatime']), "%A %d %B %Y %I:%M %p")
                postTime = postTime.replace(tzinfo=utc) # localzing to UTC
                now = datetime.now(utc)
                weekAgo = now - timedelta(weeks=1)

                if not weekAgo <= postTime <= now: # only want news from current week
                    weekAgoReached = True
                    break

                pl_news['date'].append(postTime.date())

            linkTag = articleComponent.find('a', href=True)
            if linkTag:
                article = newspaper.article(linkTag['href'])
                title = article.title.replace('"', '')
                pl_news['title'].append(title)
                bodyLines = article.text.splitlines() # removing unnecassary lines from article body
                for i, line in enumerate(bodyLines):
                    if line.isupper():
                        for j in range(4): bodyLines.pop(i+j)
                        break
                pl_news['body'].append(''.join(bodyLines))

            pl_news['team'].append(team)
            pl_news['summary'].append('null')

        if page == 5: break # dont want to go more than 5 pages, just to avoid a infinte loop in the worst case
        page+=1 # if week ago article not found, we'll be continuing on to the next page


#Converting team and player data into csv files
# players_df = pd.concat(pl_players)
# players_df.columns = players_df.columns.droplevel() # removing header and making second row new header
# players_df = players_df.reset_index(drop=True) # resetting the index and dropping the old index column
# players_df = players_df.drop(players_df.columns[[10,11,12,13,14,15,17,19,20,21,22,27,30,33]], axis=1) # remove unwanted columns
# players_df = players_df.loc[:, ~players_df.columns.duplicated()] # retain only the first occurrence of each column
# players_df.rename(columns={'':'Team'}, inplace=True) # naming Team column
# players_df.to_csv('pl_players.csv')

# teams_df = pd.DataFrame(pl_teams, index=teams)
# teams_df.to_csv('pl_teams.csv')

news_df = pd.DataFrame(pl_news)
news_df.to_csv('pl_news.csv')






