
# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient # <-- 1. Import MongoClient

# Initialize the Flask application
app = Flask(__name__)
CORS(app)

# --- 2. Set up MongoDB connection ---
# This connects to your local MongoDB server running by default.
client = MongoClient('mongodb://localhost:27017/')
db = client['bot_detection_db'] # This is your database name
collection = db['sessions']       # This is your collection (like a table)
# ------------------------------------

@app.route('/collect', methods=['POST'])
def collect_data():
    """
    This endpoint now receives data and saves it to MongoDB.
    """
    session_data = request.get_json()

    # --- 3. Insert the data into the collection ---
    try:
        # The insert_one function takes a Python dictionary and saves it as a document.
        collection.insert_one(session_data)
        print("✅ Session data successfully saved to MongoDB.")
        return jsonify({"status": "success", "message": "Data saved"}), 201
    except Exception as e:
        print(f"❌ Error saving to MongoDB: {e}")
        return jsonify({"status": "error", "message": "Could not save data"}), 500
    # ----------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, port=5000)