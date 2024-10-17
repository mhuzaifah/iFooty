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
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../.env')

def getNews():
    pl_news = {
            "title" : [],
            "body" : [],
            "date" : [],
            "team" : [],
            "summary" : []
        }

    teams_df = pd.read_csv('pl_teams.csv', index_col=0) #getting all the teams from corresonding csv file

    #Parsing another website to get each teams' relevant news data
    for team in teams_df.index:
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
            
    news_df = pd.DataFrame(pl_news)
    news_df.index.name = 'id'
    
    return news_df
    # news_df.to_csv('pl_news.csv')
            
def importCSVtoPostgreSQL(df, tableName):
    
    columns = df.columns.tolist()

    # Conneting to database 
    db_password = os.getenv('DB_PASSWORD')
    print(db_password)
    conn = psycopg2.connect(database = "ifooty", 
                            user = "postgres", 
                            host= 'localhost',
                            password = "Huzi@1975",
                            port = 5432)
    curr = conn.cursor()   
    
    # Delete old news data
    deleteQuery = f"DELETE FROM {tableName}" 
    curr.execute(deleteQuery)
    conn.commit()
    
    # Create template to insert new data from the CSV
    insertColumns = ', '.join(columns)  #comma-separated column names
    insertValues = ', '.join(['%s'] * len(columns))  #placeholder for values
    insertQuery = f"INSERT INTO {tableName} ({insertColumns}) VALUES ({insertValues})"
    
    # Loop through the rows in the DataFrame and update each row based on the primary key
    for _, row in df.iterrows():
        values = row.tolist() #get values of row
        curr.execute(insertQuery, values) #execute the query with the column values from the CSV
    conn.commit()
    
    curr.close()
    conn.close()
    
newsDf = getNews()
importCSVtoPostgreSQL(newsDf, 'news_data')