# backend/db/connection.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv() 

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("MONGO_DB_NAME", "youtube_analysis") # Default name if not in .env

if not MONGO_URI:
    raise ValueError("MONGO_URI not found in environment variables. Did you create a .env file?")

try:
    client = MongoClient(MONGO_URI)
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster') 
    print("MongoDB connection successful.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    client = None # Set client to None if connection fails

def get_db():
    """Returns the database instance."""
    if client:
        return client[DB_NAME]
    else:
        # Optionally, try to reconnect or raise an error
        print("Attempting to reconnect to MongoDB...")
        try:
            new_client = MongoClient(MONGO_URI)
            new_client.admin.command('ismaster')
            print("Reconnection successful.")
            # Update the global client variable if needed, though this pattern isn't ideal for web servers
            # For Flask, it's better to manage the client within the app context if possible
            return new_client[DB_NAME] 
        except Exception as recon_e:
             print(f"Reconnection failed: {recon_e}")
             raise ConnectionError("Could not connect to MongoDB")


def get_comments_collection():
    """Returns the 'comments' collection."""
    db = get_db()
    return db.comments

# You can add more functions here to get other collections if needed
# e.g., get_summaries_collection()

# Simple test when running the script directly
if __name__ == "__main__":
    try:
        db = get_db()
        print(f"Successfully connected to database: {DB_NAME}")
        collections = db.list_collection_names()
        print(f"Collections in the database: {collections}")
        comments_coll = get_comments_collection()
        print(f"Got comments collection: {comments_coll.name}")
        
        # Example: Insert a test document (optional)
        test_doc_id = comments_coll.insert_one({"test": "connection"}).inserted_id
        print(f"Inserted test document with ID: {test_doc_id}")
        comments_coll.delete_one({"_id": test_doc_id}) # Clean up test doc
        print("Cleaned up test document.")

    except ConnectionError as ce:
        print(f"Main execution failed: {ce}")
    except Exception as e:
        print(f"An error occurred during testing: {e}")