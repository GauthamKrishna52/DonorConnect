import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

print("1. Loading the synthetic donor data...")
# Load the spreadsheet we just generated
df = pd.read_csv('synthetic_donors.csv')

print("2. Preparing the data for the AI...")
# X = The "Features" (The data we give the AI)
X = df[['distance_km', 'past_donations', 'responsiveness']]

# y = The "Target" (The final score we want the AI to predict)
y = df['target_score']

# We split the data: 80% is used for the AI to "study", and 20% is kept hidden for a "test"
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("3. Training the Random Forest Engine...")
# Initialize the model (We are asking for a "forest" of 100 decision trees)
model = RandomForestRegressor(n_estimators=100, random_state=42)

# The .fit() command is where the actual learning happens!
model.fit(X_train, y_train)

print("4. Testing the AI's accuracy...")
# Let's grade the test data to see how well it learned the patterns
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy Score: {round(accuracy * 100, 2)}%")

print("5. Saving the AI Brain to a file...")
# We save the trained model into a .pkl file so we don't have to retrain it every time the server starts
joblib.dump(model, 'ranking_model.pkl')

print("Success! 'ranking_model.pkl' is ready to be used by your Flask server.")