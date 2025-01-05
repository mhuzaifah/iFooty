import pandas as pd
import numpy as np

# Using Rolling Window technique to compute a team's recent form relative to historically against each other and current season  
def addRecentForm(df, currentStats, window=1):
    # For training, make window 5-10
    
    # Apply rolling averages within each year for both home and away teams
    df['HomeGoalsRolling'] = df.groupby(['Home', 'Year'])['HomeGoals'].rolling(window).mean().reset_index(level=[0, 1], drop=True)
    df['AwayGoalsRolling'] = df.groupby(['Away', 'Year'])['AwayGoals'].rolling(window).mean().reset_index(level=[0, 1], drop=True)
    df['HomeConcededRolling'] = df.groupby(['Home', 'Year'])['AwayGoals'].rolling(window).mean().reset_index(level=[0, 1], drop=True)
    df['AwayConcededRolling'] = df.groupby(['Away', 'Year'])['HomeGoals'].rolling(window).mean().reset_index(level=[0, 1], drop=True)
    df['HomeWinsRolling'] = df.groupby(['Home', 'Year'])['HomeWins'].rolling(window).mean().reset_index(level=[0, 1], drop=True)
    df['AwayWinsRolling'] = df.groupby(['Away', 'Year'])['AwayWins'].rolling(window).mean().reset_index(level=[0, 1], drop=True)
    df['HomeDrawsRolling'] = df.groupby(['Home', 'Year'])['HomeLosses'].rolling(window).mean().reset_index(level=[0, 1], drop=True)
    df['AwayDrawsRolling'] = df.groupby(['Away', 'Year'])['AwayLosses'].rolling(window).mean().reset_index(level=[0, 1], drop=True)
    df['HomeLossesRolling'] = df.groupby(['Home', 'Year'])['HomeLosses'].rolling(window).mean().reset_index(level=[0, 1], drop=True)
    df['AwayLossesRolling'] = df.groupby(['Away', 'Year'])['AwayLosses'].rolling(window).mean().reset_index(level=[0, 1], drop=True)
    
    # Adjust rolling averages using current season stats (REMOVE FOR MODEL TRAINING)
    df['HomeGoalsRolling'] = df['HomeGoalsRolling'] * 0.8 + currentStats['HomeGoals'] * 0.2
    df['AwayGoalsRolling'] = df['AwayGoalsRolling'] * 0.8 + currentStats['AwayGoals'] * 0.2
    df['HomeConcededRolling'] = df['HomeConcededRolling'] * 0.8 + currentStats['HomeConceded'] * 0.2
    df['AwayConcededRolling'] = df['AwayConcededRolling'] * 0.8 + currentStats['AwayConceded'] * 0.2
    df['HomeWinsRolling'] = df['HomeWinsRolling'] * 0.8 + currentStats['HomeWins'] * 0.2
    df['AwayWinsRolling'] = df['AwayWinsRolling'] * 0.8 + currentStats['AwayWins'] * 0.2
    df['HomeDrawsRolling'] = df['HomeDrawsRolling'] * 0.8 + currentStats['HomeDraws'] * 0.2
    df['AwayDrawsRolling'] = df['AwayDrawsRolling'] * 0.8 + currentStats['AwayDraws'] * 0.2
    df['HomeLossesRolling'] = df['HomeLossesRolling'] * 0.8 + currentStats['HomeLosses'] * 0.2
    df['AwayLossesRolling'] = df['AwayLossesRolling'] * 0.8 + currentStats['AwayLosses'] * 0.2
    
    # Fill NaNs with 0 after adjustment
    df.dropna()

    return df

# Incorporating home/away advantage/disadvantage for each mathcup (Used on whole dataset instead of one filtered on the fixture)
def addHomeAway(df):
    
    # Calculate team's average goals scored and conceded at home
    homeStats = df.groupby('Home').agg({
        'HomeGoals': 'mean', 
        'AwayGoals': 'mean'
    }).rename(columns={
        'HomeGoals': 'AvgHomeGoalsScored',  # Average goals scored by home team
        'AwayGoals': 'AvgHomeGoalsConceded' # Average goals conceded by home team
    })

    # Calculate team's average goals scored and conceded away
    awayStats = df.groupby('Away').agg({
        'AwayGoals': 'mean', 
        'HomeGoals': 'mean'
    }).rename(columns={
        'AwayGoals': 'AvgAwayGoalsScored',  # Average goals scored by away team
        'HomeGoals': 'AvgAwayGoalsConceded' # Average goals conceded by away team
    })
    
    # Merge these stats back into the original dataframe for each home and away team
    df = df.merge(homeStats, left_on='Home', right_index=True, how='left', suffixes=('', '_HomeStats'))
    df = df.merge(awayStats, left_on='Away', right_index=True, how='left', suffixes=('', '_AwayStats'))

    # Calculate home advantage and away disadvantage as differences in performance
    df['HomeAdvantage'] = df['AvgHomeGoalsScored'] - df['AvgAwayGoalsConceded']
    df['AwayDisadvantage'] = df['AvgAwayGoalsConceded'] - df['AvgHomeGoalsScored']

    return df


# Incorporating the head-to-head history the specific fixture
def addHeadToHead(df):
    
    headToHeadStats = []

    # Loop through each match and calculate head-to-head statistics based on past data only
    for _, row in df.iterrows():
        
        pastMatches = df[df['Year'] < row['Year']]  # Only consider matches that occurred before the current match's year

        if pastMatches.empty:
            headToHeadStats.append({
                'AvgHomeGoalsHeadToHead': np.nan,
                'AvgAwayGoalsHeadToHead': np.nan,
                'HomeWinsHeadToHead': np.nan,
                'AwayWinsHeadToHead': np.nan
            })
        else:
            avgHomeGoals = pastMatches['HomeGoals'].mean()
            avgAwayGoals = pastMatches['AwayGoals'].mean()
            homeWins = pastMatches['HomeWins'].sum()
            awayWins = pastMatches['AwayWins'].sum()

            headToHeadStats.append({
                'AvgHomeGoalsHeadToHead': avgHomeGoals,
                'AvgAwayGoalsHeadToHead': avgAwayGoals,
                'HomeWinsHeadToHead': homeWins,
                'AwayWinsHeadToHead': awayWins
            })

    headToHeadStatsDf = pd.DataFrame(headToHeadStats)

    # # Merge the head-to-head stats DataFrame back with the original DataFrame 
    # for column in headToHeadStats.columns:
    #     df[column] = headToHeadStats[column]
        
    # Merge the head-to-head stats DataFrame back with the original DataFrame
    df = pd.concat([df.reset_index(drop=True), headToHeadStatsDf.reset_index(drop=True)], axis=1)

    return df
