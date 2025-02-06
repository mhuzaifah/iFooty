from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

REQUESTS_LIMIT = 18 # Must track number of requests to not go over limit (Max: 18 requests / Min)
TIME_WINDOW = 60 # Seconds (1 min)
request_times = []

# Custom make request method to sleep the scraper if the request limit / min has been reached
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
# fixturesData = {
#     "Home" : [],
#     "Away" : [],
#     "Score" : [],
#     "HomeRec" : [],
#     "AwayRec" : [],
# }
fixturesData = {
    "Home" : [],
    "Away" : [],
    "Date" : [],
    "Time" : [],
    "Venue" : []
}

seasonLink = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures" # Choose the link to pl season fixtures to scrape
mainPageReq = make_request(seasonLink) 
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
    # if colLabel in fixturesData or colLabel == "Match Report":
    if colLabel in fixturesData:
        reqCols[i-1] = colLabel # i-1 since in the rows with the data, the first col (Wk) is the 'tr', so there are n-1 cols  
fixturesTableRows.pop(0) #Don't need header column 

teamDict = { 'Manchester Utd' : 'Manchester United', 'Nott\'ham Forest' : 'Nottingham Forest', 'Tottenham' : 'Tottenham Hotspur',  'West Ham' : 'West Ham United', 'Newcastle Utd' : 'Newcastle United' }

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
            data = col.text.strip()
            if data in teamDict: data = teamDict.get(data) #Adjusting certain team names that are shortened in this table to match with the team names in my current Teams table in DB
            
            # LOGIC FOR JUST EXTRACT GENERAL FIXTURE INFO (Teams, Data, Time, Venue, etc.), NO SCORES 
            fixturesData[label].append(data) # Stripped since Time value has empty space

            # LOGIC FOR PAST FIXTURES TO EXTRACT SCORES
            # if label != "Match Report":
            #   fixturesData[label].append(col.text)
            # else:
            #     aElem = col.find('a')
            #     if aElem:
            #         link = "https://fbref.com"+aElem['href']
            #         matchReportPageReq = make_request(link)
            #         fixtureHtml = matchReportPageReq.text
            #         fixtureSoup = BeautifulSoup(fixtureHtml, 'lxml')
            #         scoreBox = fixtureSoup.find('div', class_="scorebox")
                    
            #         if scoreBox:
            #             scoreBox = scoreBox.find_all(recursive=False)
            #             homeTeamRecList = scoreBox[0].find_all(recursive=False)[2].text.split('-')
            #             awayTeamRecList = scoreBox[1].find_all(recursive=False)[2].text.split('-')
                        
            #             #Adjusting both team's record to before the game was played
            #             score = fixturesData["Score"][-1]
            #             homeScore, awayScore = int(score[0]), int(score[2])
            #             if homeScore > awayScore:
            #                 homeTeamRecList[0] = str(int(homeTeamRecList[0])-1)
            #                 awayTeamRecList[2] = str(int(awayTeamRecList[2])-1)
            #             elif awayScore > homeScore:
            #                 awayTeamRecList[0] = str(int(awayTeamRecList[0])-1)
            #                 homeTeamRecList[2] = str(int(homeTeamRecList[2])-1)
            #             else:
            #                 awayTeamRecList[1] = str(int(awayTeamRecList[1])-1)
            #                 homeTeamRecList[1] = str(int(homeTeamRecList[1])-1)
                        
            #             fixturesData["HomeRec"].append('-'.join(homeTeamRecList))
            #             fixturesData["AwayRec"].append('-'.join(awayTeamRecList))
            #         else:
            #             fixturesData["Score"] = 'null'
            #             fixturesData["HomeRec"] = 'null'
            #             fixturesData["AwayRec"] = 'null'
                        
            #         time.sleep(5)
                        
                                        
fixturesDF = pd.DataFrame(fixturesData)
fixturesDF.to_csv('pl_fixtures_24-25.csv', index_label='id') #Rename csv file to the corresponding season data was scraped for