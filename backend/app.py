# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import joblib
import pandas as pd
from feature_engineering import engineer_features # <-- 1. Import our function

app = Flask(__name__)
CORS(app)

# --- Database Connection (for /collect) ---
client = MongoClient('mongodb://localhost:27017/')
db = client['bot_detection_db']
collection = db['sessions']

# --- 2. Load the Model at Startup ---
try:
    model = joblib.load('bot_detector_model.pkl')
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("❌ Model file 'bot_detector_model.pkl' not found. /predict will not work.")
    model = None

# --- 3. Create the /predict Endpoint ---
@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"status": "error", "message": "Model not loaded"}), 500

    session_data = request.get_json()

    # 1. Engineer features from the incoming data
    # We must use the *exact same* function as in training
    features_dict = engineer_features(session_data)
    
    # 2. Convert features to a DataFrame (models expect this)
    # The [0] is because we are predicting a single sample
    features_df = pd.DataFrame([features_dict])

    # 3. Handle any potential missing values (just in case)
    features_df = features_df.fillna(0)
    
    # 4. Make a prediction
    # .predict_proba gives [prob_human, prob_bot]
    prediction_proba = model.predict_proba(features_df)
    human_probability = prediction_proba[0][0] # Probability of class 0 (Human)

    print(f"Prediction: Human Prob = {human_probability:.4f}")

    # 5. Make a decision
    decision = 'allow' if human_probability > 0.5 else 'block' # 0.5 is our threshold

    # 6. Send the decision back to the frontend
    return jsonify({
        'status': 'success',
        'decision': decision,
        'human_probability': float(human_probability)
    })


# --- This is our old endpoint for data collection ---
@app.route('/collect', methods=['POST'])
def collect_data():
    session_data = request.get_json()
    try:
        collection.insert_one(session_data)
        return jsonify({"status": "success", "message": "Data saved"}), 201
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")
        return jsonify({"status": "error", "message": "Could not save data"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)