🧠 Donor Connect - Intelligence Layer API (Module 4)Owner: Gautham Krishna (Group 13)System: B.Tech Mini-Project - Two-Track ProtocolThis module acts as the "brain" of the Donor Connect system. It provides offline AI capabilities to parse handwritten medical notes (OCR) and mathematically rank potential donors using a Machine Learning algorithm (Random Forest).🚀 How to Run This Server LocallyFor Aryanandha, Dhanooja, or Franceena to test their modules against this AI, they need to run this server on their own machines.Install Requirements:Make sure you have Python installed, then run:pip install flask easyocr pandas scikit-learn joblib

Start the Server:Navigate into the intelligence folder and run:python app.py

Note: The first time it runs, EasyOCR will download its detection models. It will run on http://127.0.0.1:5000.📡 API Endpoints (The Contract)1. Extract Blood Group from Image (OCR)Reads a handwritten medical note and extracts the emergency blood group using Regex pattern matching.URL: /intelligence/ocrMethod: POSTBody Type: form-dataRequest Format:| Key | Type | Value || :--- | :--- | :--- || image | File | [Attach .jpg or .png] |Success Response (200 OK):{
    "status": "success",
    "blood_group_detected": "O+",
    "raw_text": "URGENT... Blood Group: 0+ ... Hospital"
}

2. Smart Donor Ranking (Machine Learning)Takes an unsorted list of donors matching the required blood/organ type and returns them sorted by priority score (0-100). The model weighs distance, past donation history, and responsiveness.URL: /intelligence/rankMethod: POSTBody Type: raw (JSON)Request Format:{
    "donors": [
        {
            "donor_id": "D001",
            "name": "Alice",
            "distance_km": 35.0,
            "past_donations": 1,
            "responsiveness": 0.2
        },
        {
            "donor_id": "D002",
            "name": "Bob",
            "distance_km": 2.5,
            "past_donations": 10,
            "responsiveness": 0.9
        }
    ]
}

Success Response (200 OK):{
    "status": "success",
    "ranked_donors": [
        {
            "donor_id": "D002",
            "name": "Bob",
            "distance_km": 2.5,
            "past_donations": 10,
            "responsiveness": 0.9,
            "priority_score": 99.0
        },
        {
            "donor_id": "D001",
            "name": "Alice",
            "distance_km": 35.0,
            "past_donations": 1,
            "responsiveness": 0.2,
            "priority_score": 60.52
        }
    ]
}

🛠️ Internal Files Structureapp.py: The main Flask server and API routes.ranking_model.pkl: The trained Random Forest brain (Do not delete).generate_data.py: Script to generate synthetic testing data.train_model.py: Script used to train the Random Forest on the CSV data.synthetic_donors.csv: The mock dataset representing MongoDB queries.