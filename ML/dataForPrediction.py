import pandas as pd
import os
from model.preprocess import addHomeAway

# Load the dataset
csvPath = os.path.join(os.path.dirname(__file__), "Data", "pl_fixtures.csv")
DATADF = pd.read_csv(csvPath)

# Parsing Score to extract Home and Away team's goals
DATADF[['HomeGoals', 'AwayGoals']] = DATADF['Score'].str.replace('–', '-').str.split('-', expand=True).astype(int)

# Parsing Home and Away team records to extract each's wins, draws, and losses
DATADF[['HomeWins', 'HomeDraws', 'HomeLosses']] = DATADF['HomeRec'].str.replace('–', '-').str.split('-', expand=True).astype(int)
DATADF[['AwayWins', 'AwayDraws', 'AwayLosses']] = DATADF['AwayRec'].str.replace('–', '-').str.split('-', expand=True).astype(int)

# Drop unnecessary columns (won't need the original Score, HomeRec, and AwayRec)
DATADF.drop(columns=['Score', 'HomeRec', 'AwayRec'], inplace=True)

# Apply Preprocessing method Home/Away advantage/disadvantage stats to each fixture, to aid model prediction
DATADF = addHomeAway(DATADF)

def parseForMatchup(df, homeTeam, awayTeam):
    parsedDf = df[
                ((df['Home'] == homeTeam) & (df['Away'] == awayTeam)) | 
                ((df['Away'] == homeTeam) & (df['Home'] == awayTeam))
                ].copy()
    
    return parsedDf
