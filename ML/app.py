from flask import Flask, request, jsonify
import joblib
import numpy as np
from model.preprocess import addRecentForm, addHeadToHead 
from model.predictors import PREDICTORS
from dataForPrediction import DATADF, parseForMatchup
import os 
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# CORS(app)

# Get relative path to model folder
modelPath = os.path.join(os.path.dirname(__file__), 'model')

# Load model and encoder
model = joblib.load(os.path.join(modelPath, 'fixturePredictionModel.pkl'))
rfHome = model['rf_home']
rfAway = model['rf_away']
le = joblib.load(os.path.join(modelPath, 'labelEncoder.pkl'))

@app.route('/')
def home():
    return "Welcome to the PL Prediction Model!"

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the request body (JSON)
    data = request.json
    homeTeam = data['Home']
    awayTeam = data['Away']
    homeRec = data['HomeRec']  
    awayRec = data['AwayRec']  
    homeGoalsPerGame = data['HomeGoalsPerGame']
    awayGoalsPerGame = data['AwayGoalsPerGame']
    homeConcededPerGame = data['HomeConcededPerGame']
    awayConcededPerGame = data['AwayConcededPerGame']
    year = data['Year']
        
    currentData = {
        'Home' : homeTeam,
        'Away' : awayTeam,
        'HomeRec' : homeRec,
        'AwayRec' : awayRec,
        'HomeGoals' : homeGoalsPerGame,
        'AwayGoals' : awayGoalsPerGame,
        'HomeConceded' : homeConcededPerGame,
        'AwayConceded' : awayConcededPerGame,
        'Year' : year 
    }
    # Parsing Home and Away team records to extract each teams' wins, draws, and losses
    homeWins, homeDraws, homeLosses = map(int, currentData['HomeRec'].replace('–', '-').split('-'))
    awayWins, awayDraws, awayLosses = map(int, currentData['AwayRec'].replace('–', '-').split('-'))
    currentData["HomeWins"] = homeWins
    currentData["HomeDraws"] = homeDraws
    currentData["HomeLosses"] = homeLosses
    currentData["AwayWins"] = awayWins
    currentData["AwayDraws"] = awayDraws
    currentData["AwayLosses"] = awayLosses
    # Remove unnecessary keys
    currentData.pop('HomeRec', None)
    currentData.pop('AwayRec', None)
    
    # Filter the match data on the 2 teams playing
    df = parseForMatchup(DATADF, homeTeam, awayTeam)
    
    # Encode the Home and Away teams (using saved encodings from training)
    df['HomeTeamCode'] = le.transform(df['Home'])
    df['AwayTeamCode'] = le.transform(df['Away'])

    # Preprocess input data to generate features
    df = addRecentForm(df, currentData)
    df = addHeadToHead(df)
    
    # Make predictions
    homeScores = rfHome.predict(df[PREDICTORS])
    awayScores = rfAway.predict(df[PREDICTORS])

    # Adjusting predictions with current 'form' of each team
    currentWeight = 0.4
    historicalWeight = 0.6
    homeScorePred = round(currentWeight * currentData["HomeGoals"] + historicalWeight * np.mean(homeScores))
    awayScorePred = round(currentWeight * currentData["AwayGoals"] + historicalWeight * np.mean(awayScores))

    response = {
        'predictedHome': homeScorePred,
        'predictedAway': awayScorePred
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
