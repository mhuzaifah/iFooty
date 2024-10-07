from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO
import time

REQUESTS_LIMIT = 20 # Must track number of requests to not go over limit (Max: 20 requests / Min)
TIME_WINDOW = 60 # Seconds (1 min)
request_times = []
def make_request(url):
    global request_times
    
    # Check if we have already made 20 requests in the past minute
    if len(request_times) >= REQUESTS_LIMIT:
        # Calculate the time since the oldest request in the past minute
        elapsed_time = time.time() - request_times[0]
        
        # If it's less than 60 seconds, wait for the remaining time
        if elapsed_time < TIME_WINDOW:
            sleep_time = TIME_WINDOW - elapsed_time
            print(f"Rate limit hit! Sleeping for {sleep_time:.2f} seconds...")
            time.sleep(sleep_time)

    # Send the request after ensuring we are within the limit
    response = requests.get(url)

    # Update the request timestamps list (remove old ones)
    request_times = [t for t in request_times if time.time() - t < TIME_WINDOW]
    request_times.append(time.time())

    return response


seasons = ["2023-2024", "2022-2023", "2021-2022", "2020-2021"] # Later get fixtures for all these years

# Only getting fixture data for 2023-2024 right now

# Want: Home Team, Away Team, Score, Home Team Record, Away Team Record
fixtures = {
    "Home" : [],
    "Away" : [],
    "Score" : [],
    "HomeRec" : [],
    "AwayRec" : [],
}

mainPageReq = make_request("https://fbref.com/en/comps/9/2023-2024/schedule/2023-2024-Premier-League-Scores-and-Fixtures")
html = mainPageReq.text
print(html)
soup = BeautifulSoup(html, 'lxml')
fixturesTableHtml = soup.find_all('table', class_='stats_table')[0]
fixturesTableRows = fixturesTableHtml.find_all('tr')

#Find index of the relevant columns
header = fixturesTableRows[0]
headerCols = header.find_all('th')
reqCols = {}

for i, col in enumerate(headerCols):
    colLabel = col.get('aria-label')
    if colLabel in fixtures or colLabel == "Match Report":
        reqCols[i-1] = colLabel # i-1 since in the rows with the data, the first col (Wk) is the 'tr', so there are n-1 cols  
fixturesTableRows.pop(0) #Don't need header column 

#Iterate over all fixtures in table
for row in fixturesTableRows:
    cols = row.find_all('td')
    for i, col in enumerate(cols):
        if i in reqCols:
            label = reqCols[i]
            if label != "Match Report":
                fixtures[label].append(col.text)
            else:
                aElem = col.find('a')
                if aElem:
                    link = "https://fbref.com"+aElem['href']
                    matchReportPageReq = make_request(link)
                    fixtureHtml = matchReportPageReq.text
                    fixtureSoup = BeautifulSoup(fixtureHtml, 'lxml')
                    scoreBox = fixtureSoup.find('div', class_="scorebox").find_all(recursive=False)
                    homeTeamRecList = scoreBox[0].find_all(recursive=False)[2].text.split('-')
                    awayTeamRecList = scoreBox[1].find_all(recursive=False)[2].text.split('-')
                    
                    #Adjusting both team's record to before the game was played
                    score = fixtures["Score"][-1]
                    homeScore, awayScore = int(score[0]), int(score[2])
                    if homeScore > awayScore:
                        homeTeamRecList[0] = str(int(homeTeamRecList[0])-1)
                        awayTeamRecList[2] = str(int(awayTeamRecList[2])-1)
                    elif awayScore > homeScore:
                        awayTeamRecList[0] = str(int(awayTeamRecList[0])-1)
                        homeTeamRecList[2] = str(int(homeTeamRecList[2])-1)
                    else:
                        awayTeamRecList[1] = str(int(awayTeamRecList[1])-1)
                        homeTeamRecList[1] = str(int(homeTeamRecList[1])-1)
                    
                    fixtures["HomeRec"].append('-'.join(homeTeamRecList))
                    fixtures["AwayRec"].append('-'.join(awayTeamRecList))
                                        
fixturesDF = pd.DataFrame(fixtures)
fixturesDF.to_csv('pl_fixtures.csv')