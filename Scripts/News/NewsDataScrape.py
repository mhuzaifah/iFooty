from bs4 import BeautifulSoup
import pandas as pd
import requests
import re
import newspaper
from datetime import datetime, timedelta
from pytz import utc

# Gets news articles published during the past 24 hours for each team in the premier league
# Logic is that this script runs every day, and when the new week starts, an automated query at the database level would remove all news so that each team has a fresh new news section
def getNews():
    pl_news = {
            "title" : [],
            "body" : [],
            "date" : [],
            "team" : [],
            "summary" : []
        }

    # Parsing Website to get the current PL Table for team names (could use DB or already stored pl_teams csv, but this website deals with teams name differently)
    html = requests.get('https://www.football365.com/premier-league/table').text
    
    # Not dynamically checking the teams and hardcoding it instead for now, change later
    teams = ['liverpool', 'manchester-city', 'chelsea', 'arsenal', 'nottingham-forest', 'brighton', 'fulham', 'newcastle-united', 'aston-villa', 'tottenham-hotspur', 'brentford', 'bournemouth', 'manchester-united', 'west-ham-united', 'leicester-city', 'everton', 'ipswich-town', 'crystal-palace', 'wolves', 'southampton']
    
    # Capture the script start time as a fixed reference
    scriptStart = datetime.now(utc)
    dayAgo = scriptStart - timedelta(hours=24)

    #Parsing another website to get each teams' relevant news data
    for teamURLName in teams:
        teamURLName: str
        teamName = " ".join([x.capitalize() for x in teamURLName.split('-')])
        # print(teamURLName, teamName)
        page = 1
        dayLimitReached = False
        while not dayLimitReached:
            # print(page)
            link = f'https://www.football365.com/{teamURLName}/news' if page == 1 else f'https://www.football365.com/{teamURLName}/page/{page}'
            html = requests.get(link).text
            soup = BeautifulSoup(html, 'lxml')
            articleComponents = [article for article in soup.find_all(class_='news-card') if not article.find_parent('aside')] # only want news articles in the main section of the page
            
            #Parsing each article component/card one by one
            for articleComponent in articleComponents:
                                
                categories = []
                categories += [tag.get_text(strip=True) for tag in articleComponent.find_all('a', class_='ps-tag')]
                categories += [tag.get_text(strip=True) for tag in articleComponent.find_all('a', class_='ps-tag-1')]

                if teamName not in categories: # skipping news articles not related to the team
                    continue

                timeTag = articleComponent.find('time')
                if timeTag:
                    postTime = datetime.strptime(re.sub(r'(\d+)(st|nd|rd|th)', r'\1', timeTag['datatime']), "%A %d %B %Y %I:%M %p")
                    postTime = postTime.replace(tzinfo=utc) # localzing to UTC

                    if not dayAgo <= postTime <= scriptStart: # only want news from current week
                        dayLimitReached = True
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

                pl_news['team'].append(teamName)
                pl_news['summary'].append('null')

            if page == 5: break # break for any weird cases causing search to reach 5+ pages
            page+=1 # if day limit not reached, we'll be continuing on to the next page
            
    news_df = pd.DataFrame(pl_news)
    news_df.index.name = 'id'
    news_df.to_csv('pl_news.csv')
    
    return news_df
        
    