import pandas as pd
import random

print("Generating synthetic donor data...")

# We will create 200 fake donor profiles
donors = []

for _ in range(200):
    # 1. Distance from hospital (1km to 40km)
    distance_km = round(random.uniform(1.0, 40.0), 1)
    
    # 2. How many times they've donated before (0 to 15)
    past_donations = random.randint(0, 15)
    
    # 3. How fast they reply to the WhatsApp bot (0.1 = slow, 1.0 = instant)
    responsiveness = round(random.uniform(0.1, 1.0), 2)
    
    # 4. The "Target Score" (Out of 100)
    # We use a logical formula here so the AI has a real pattern to learn.
    # Closer distance is good, more donations is good, high response is good.
    score = 100 - (distance_km * 1.5) + (past_donations * 2) + (responsiveness * 15)
    
    # Keep the score between 10 and 99
    final_score = max(10, min(round(score), 99))
    
    donors.append([distance_km, past_donations, responsiveness, final_score])

# 5. Convert this list into a structured table (DataFrame)
df = pd.DataFrame(donors, columns=['distance_km', 'past_donations', 'responsiveness', 'target_score'])

# 6. Save it as a CSV file
df.to_csv('synthetic_donors.csv', index=False)

print("Success! 'synthetic_donors.csv' has been created in your folder.")