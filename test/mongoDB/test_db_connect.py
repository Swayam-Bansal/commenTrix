# test_db_connection.py
import sys
import os

# Add the project root (commenTrix/) to sys.path
# Add the project root to the path no matter where you're running from
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))  # adjust if needed
sys.path.append(project_root)

from backend.db.connection import db, comments_col
from bson.objectid import ObjectId

def test_mongo_connection():
    # 1. Print existing databases
    print("Available databases:")
    print(db.client.list_database_names(), "\n")
    
    # 2. Print existing collections in our database
    print("Collections in 'commenTrixDB':")
    print(db.list_collection_names(), "\n")

    # 3. Test insert a dummy doc
    test_doc = {
        "test_field": "Hello, MongoDB!",
        "status": "testing_connection"
    }
    insert_result = db["test_collection"].insert_one(test_doc)
    print(f"Inserted doc with _id: {insert_result.inserted_id}")

    # 4. Find and print the document you just inserted
    retrieved_doc = db["test_collection"].find_one({"_id": ObjectId(insert_result.inserted_id)})
    print("Retrieved doc from 'test_collection':")
    print(retrieved_doc, "\n")

    # 5. Clean up the test doc (optional)
    db["test_collection"].delete_one({"_id": ObjectId(insert_result.inserted_id)})
    print("Test document removed from 'test_collection'.")

if __name__ == "__main__":
    test_mongo_connection()
