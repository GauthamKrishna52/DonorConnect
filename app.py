from flask import Flask, request, jsonify
import easyocr
import re
import os
import joblib
import pandas as pd

app = Flask(__name__)

# 1. Load the AI Models once when the server starts
print("Starting Intelligence Layer...")
print("Loading OCR Model...")
reader = easyocr.Reader(['en'])

print("Loading Random Forest Ranking Brain...")
# Load the .pkl file we just created
ranking_model = joblib.load('ranking_model.pkl')
print("Server is fully armed and operational!")

# --- ENDPOINT 1: OCR (Already working!) ---
@app.route('/intelligence/ocr', methods=['POST'])
def process_medical_note():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
        
    file = request.files['image']
    file_path = "temp_upload.jpg"
    file.save(file_path)
    
    results = reader.readtext(file_path, detail=0)
    
    if results:
        full_text = " ".join(results)
        pattern = r'(A|B|AB|O|0)[+-]'
        match = re.search(pattern, full_text, re.IGNORECASE)
        
        if match:
            blood_group = match.group(0).upper().replace('0', 'O')
        else:
            blood_group = "NOT FOUND"
            
        os.remove(file_path)
        return jsonify({
            "status": "success",
            "blood_group_detected": blood_group,
            "raw_text": full_text
        })
        
    return jsonify({"status": "failed", "message": "No text detected"}), 400

# --- ENDPOINT 2: ML RANKING (New!) ---
@app.route('/intelligence/rank', methods=['POST'])
def rank_donors():
    # 1. Get the list of donors sent by Member 2 or 3
    data = request.get_json()
    
    if not data or 'donors' not in data:
        return jsonify({"error": "Invalid data format. Please provide a list of donors."}), 400
        
    donor_list = data['donors']
    
    # 2. Convert the JSON list into a Pandas DataFrame so the AI can read it
    df = pd.DataFrame(donor_list)
    
    # Extract just the features the AI needs to make a prediction
    features = df[['distance_km', 'past_donations', 'responsiveness']]
    
    # 3. Ask the AI to predict the scores!
    predicted_scores = ranking_model.predict(features)
    
    # 4. Attach the new scores back to the original donor list
    df['priority_score'] = predicted_scores
    
    # 5. Sort the list from highest score to lowest score
    df_sorted = df.sort_values(by='priority_score', ascending=False)
    
    # Convert back to JSON and send it to the team
    sorted_donors_json = df_sorted.to_dict(orient='records')
    
    return jsonify({
        "status": "success",
        "ranked_donors": sorted_donors_json
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)