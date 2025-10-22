# backend/train_model.py
from feature_engineering import engineer_features
import pandas as pd
from pymongo import MongoClient

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier
import joblib
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

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