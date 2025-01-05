import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from ML.model.preprocess import addRecentForm, addHeadToHead 
from ML.model.predictors import PREDICTORS
from dataForPrediction import DATADF

# Encode the Home and Away teams
le = LabelEncoder()
DATADF['HomeTeamCode'] = le.fit_transform(DATADF['Home'])
DATADF['AwayTeamCode'] = le.fit_transform(DATADF['Away'])

# Preprocess input data to generate features
DATADF = addRecentForm(DATADF)
DATADF = addHeadToHead(DATADF)

# Split data by year
train = DATADF[DATADF['Year'] < 2022]  # Train on seasons before 2022
test = DATADF[DATADF['Year'] >= 2022]  # Test on the 2022 season and later

# Train the model on home goals and away goals separately
rf_home = RandomForestRegressor(n_estimators=100, random_state=1)
rf_away = RandomForestRegressor(n_estimators=100, random_state=1)
rf_home.fit(train[PREDICTORS], train['HomeGoals'])
rf_away.fit(train[PREDICTORS], train['AwayGoals'])

# Make predictions on the test set
preds_home = rf_home.predict(test[PREDICTORS])
preds_away = rf_away.predict(test[PREDICTORS])

# Evaluate the model
mse_home = mean_squared_error(test['HomeGoals'], preds_home)
mse_away = mean_squared_error(test['AwayGoals'], preds_away)

print(f'Home Goals MSE: {mse_home}')
print(f'Away Goals MSE: {mse_away}')

# Combine actual and predicted results into a DataFrame
test_results = pd.DataFrame({
    'Home': test['Home'],
    'Away': test['Away'],
    'Actual_HomeGoals': test['HomeGoals'],
    'Predicted_HomeGoals': preds_home,
    'Actual_AwayGoals': test['AwayGoals'],
    'Predicted_AwayGoals': preds_away
})

# Adding rounded predictions to the test_results DataFrame
test_results['Rounded_Predicted_HomeGoals'] = preds_home.round().astype(int)
test_results['Rounded_Predicted_AwayGoals'] = preds_away.round().astype(int)

# Calculate the number of correct predictions for both home and away goals
test_results['Correct_HomePrediction'] = (test_results['Rounded_Predicted_HomeGoals'] == test_results['Actual_HomeGoals'])
test_results['Correct_AwayPrediction'] = (test_results['Rounded_Predicted_AwayGoals'] == test_results['Actual_AwayGoals'])

# Count how many total predictions are correct for both home and away
total_correct_home = test_results['Correct_HomePrediction'].sum()
total_correct_away = test_results['Correct_AwayPrediction'].sum()

# Calculate the percentage of correct predictions
total_matches = len(test_results)
percentage_correct_home = (total_correct_home / total_matches) * 100
percentage_correct_away = (total_correct_away / total_matches) * 100

# Display the percentages
print(f"Percentage of correct home goal predictions: {percentage_correct_home:.2f}%")
print(f"Percentage of correct away goal predictions: {percentage_correct_away:.2f}%")

# If you want to calculate the percentage of games where both home and away predictions were correct:
test_results['Correct_Both'] = test_results['Correct_HomePrediction'] & test_results['Correct_AwayPrediction']
total_correct_both = test_results['Correct_Both'].sum()
percentage_correct_both = (total_correct_both / total_matches) * 100

print(f"Percentage of correct predictions for both home and away goals: {percentage_correct_both:.2f}%")

# Display the updated test_results with rounded predictions and correctness
print(test_results[['Home', 'Away', 'Actual_HomeGoals', 'Rounded_Predicted_HomeGoals', 'Correct_HomePrediction',
                    'Actual_AwayGoals', 'Rounded_Predicted_AwayGoals', 'Correct_AwayPrediction', 'Correct_Both']].head())

