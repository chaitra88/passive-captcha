# backend/train_model.py

import pandas as pd
from pymongo import MongoClient
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
import joblib
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

def get_keystroke_features(keystrokes):
    """Calculates features from the keystrokes array."""
    if len(keystrokes) < 2:
        return 0, 0, 0 # Return 0 for count, avg, and std
    
    keystroke_count = len(keystrokes)
    timestamps = [k['t'] for k in keystrokes]
    
    # Calculate flight times (time between key presses)
    flight_times = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
    
    avg_flight_time = np.mean(flight_times)
    std_flight_time = np.std(flight_times)
    
    return keystroke_count, avg_flight_time, std_flight_time

def get_mouse_features(mouse_moves):
    """Calculates features from the mouse_moves array."""
    if len(mouse_moves) < 2:
        return 0, 0 # Return 0 for count and distance
        
    mouse_move_count = len(mouse_moves)
    
    # Calculate total distance traveled
    total_distance = 0
    for i in range(1, len(mouse_moves)):
        x1, y1 = mouse_moves[i-1]['x'], mouse_moves[i-1]['y']
        x2, y2 = mouse_moves[i]['x'], mouse_moves[i]['y']
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        total_distance += distance
        
    return mouse_move_count, total_distance


def engineer_features(data):
    """
    This is the core feature engineering function.
    It turns one raw session document into a flat row of numbers.
    """
    # 1. Keystroke Features
    ks_count, avg_flight_time, std_flight_time = get_keystroke_features(data['keystrokes'])
    
    # 2. Mouse Features
    mm_count, total_mouse_dist = get_mouse_features(data['mouse_moves'])
    
    # 3. Click Features
    click_count = len(data['clicks'])
    
    # 4. Timing Features
    duration = data['timestamps']['end'] - data['timestamps']['start']
    
    # Create a dictionary of all features
    features = {
        'ks_count': ks_count,
        'avg_flight_time': avg_flight_time,
        'std_flight_time': std_flight_time,
        'mm_count': mm_count,
        'total_mouse_dist': total_mouse_dist,
        'click_count': click_count,
        'session_duration_ms': duration
    }
    
    return features

def train_model():
    print("🚀 Starting model training process...")
    
    # --- 1. Load Data from MongoDB ---
    print("Connecting to MongoDB and loading data...")
    client = MongoClient('mongodb://localhost:27017/')
    db = client['bot_detection_db']
    collection = db['sessions']
    
    # Load all documents into a list
    all_data = list(collection.find({}))
    if not all_data:
        print("❌ No data found in MongoDB. Aborting.")
        return

    print(f"Loaded {len(all_data)} total sessions.")

    # --- 2. Feature Engineering ---
    print("Engineering features for all sessions...")
    feature_list = []
    target_list = []
    
    for session in all_data:
        features = engineer_features(session)
        feature_list.append(features)
        target_list.append(session['is_bot'])
        
    # Convert to a Pandas DataFrame
    X = pd.DataFrame(feature_list)
    y = pd.Series(target_list, name="is_bot")
    
    # Handle any potential missing values (e.g., from 0 keystrokes)
    X = X.fillna(0)

    print("✅ Feature engineering complete.")
    print("Features being used:", list(X.columns))

    # --- 3. Train/Test Split ---
    print("Splitting data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # --- 4. Train XGBoost Model ---
    print("Training XGBoost classifier...")
    model = XGBClassifier(use_label_encoder=False, eval_metric='logloss', random_state=42)
    model.fit(X_train, y_train)
    print("✅ Model training complete.")

    # --- 5. Evaluate Model Performance ---
    print("Evaluating model performance...")
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print("\n" + "="*30)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("="*30 + "\n")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=['Human (0.0)', 'Bot (1.0)']))
    print("="*30)
    
    # --- 6. Save the Model ---
    model_filename = 'bot_detector_model.pkl'
    joblib.dump(model, model_filename)
    print(f"\n✅ Model successfully saved to {model_filename}")

if __name__ == '__main__':
    train_model()