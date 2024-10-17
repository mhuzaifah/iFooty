from bs4 import BeautifulSoup
import requests
import pandas as pd
from io import StringIO
import time

REQUESTS_LIMIT = 18 # Must track number of requests to not go over limit (Max: 18 requests / Min)
TIME_WINDOW = 60 # Seconds (1 min)
request_times = []

def make_request(url):
    global request_times
    
    # Clean up request_times by removing any requests older than the current time window
    request_times = [t for t in request_times if time.time() - t < TIME_WINDOW]
    
    # If we've hit the request limit, wait until a request slot becomes available
    if len(request_times) >= REQUESTS_LIMIT:
        # Calculate the time to wait until we can make another request
        wait_time = TIME_WINDOW - (time.time() - request_times[0])
        if wait_time > 0:
            print(f"Rate limit hit! Sleeping for {wait_time:.2f} seconds...")
            time.sleep(wait_time)

    # After waiting (if necessary), send the request
    response = requests.get(url)
    
    # Record the time of the request
    request_times.append(time.time())

    return response


# Want: Home Team, Away Team, Score, Home Team Record, Away Team Record
fixtures = {
    "Home" : [],
    "Away" : [],
    "Score" : [],
    "HomeRec" : [],
    "AwayRec" : [],
}

mainPageReq = make_request("https://fbref.com/en/comps/9/2020-2021/schedule/2020-2021-Premier-League-Scores-and-Fixtures")
html = mainPageReq.text
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
for i, row in enumerate(fixturesTableRows):
    
    print(i)
    cols = row.find_all('td')
    
    # Skip rows that are completely empty or contain only empty cells
    if all(col.text.strip() == '' for col in cols):
        continue  # Skip this row if all columns are empty
    
    for i, col in enumerate(cols):
        if i in reqCols:
            label = reqCols[i]
            print(label)
            if label != "Match Report":
                fixtures[label].append(col.text)
            else:
                aElem = col.find('a')
                if aElem:
                    link = "https://fbref.com"+aElem['href']
                    matchReportPageReq = make_request(link)
                    fixtureHtml = matchReportPageReq.text
                    fixtureSoup = BeautifulSoup(fixtureHtml, 'lxml')
                    scoreBox = fixtureSoup.find('div', class_="scorebox")
                    
                    if scoreBox:
                        scoreBox = scoreBox.find_all(recursive=False)
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
                    else:
                        fixtures["Score"] = 'null'
                        fixtures["HomeRec"] = 'null'
                        fixtures["AwayRec"] = 'null'
                        
                    time.sleep(5)
                        
                                        
fixturesDF = pd.DataFrame(fixtures)
fixturesDF.to_csv('pl_fixtures_20-21.csv')