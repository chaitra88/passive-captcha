# backend/label_data.py

from pymongo import MongoClient

def label_bot_data():
    """Finds all documents without an 'is_bot' field and labels them as bots (1)."""
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['bot_detection_db']
        collection = db['sessions']

        print("Searching for unlabeled documents to mark as bots...")

        # Filter finds documents where the 'is_bot' field does not exist.
        # Update sets the 'is_bot' field to 1 for all documents found by the filter.
        result = collection.update_many(
            {'is_bot': {'$exists': False}},
            {'$set': {'is_bot': 1}}
        )

        print(f"✅ Success! Labeled {result.modified_count} documents as bots.")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == '__main__':
    label_bot_data()