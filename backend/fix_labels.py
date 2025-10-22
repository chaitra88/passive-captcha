# backend/fix_labels.py

from pymongo import MongoClient

def fix_bot_labels():
    """Finds all documents where is_bot is 1 (Integer) and updates it to 1.0 (Double)."""
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['bot_detection_db']
        collection = db['sessions']

        print("Searching for bot documents with Integer (1) type...")

        # Filter finds documents where 'is_bot' is exactly the integer 1.
        # Update sets the 'is_bot' field to 1.0 (Double) for all documents found.
        result = collection.update_many(
            {'is_bot': 1},  # Find documents where is_bot == 1 (Integer)
            {'$set': {'is_bot': 1.0}} # Set it to 1.0 (Double)
        )

        print(f"✅ Success! Updated {result.modified_count} documents from 1 to 1.0.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == '__main__':
    fix_bot_labels()