# backend/scripts/fetch_comments.py
import argparse
import sys
import os

# Ensure the backend directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_comments_collection
from services.youtube_service import get_youtube_comments
from utils.youtube_ID_utils import extract_video_id



def save_comments_to_mongo(comments: list):
    """Saves a list of comments to the MongoDB collection."""
    if not comments:
        print("No comments to save.")
        return 0

    collection = get_comments_collection()
    video_id = comments[0]['video_id'] # Get video_id from the first comment

    # --- Strategy: Replace or Update? ---
    # Option A: Delete existing comments for this video_id first, then insert new ones.
    # Ensures fresh data but loses any previous analysis on comments that might be deleted in a partial fetch.
    # print(f"Deleting existing comments for video_id: {video_id}...")
    # delete_result = collection.delete_many({"video_id": video_id})
    # print(f"Deleted {delete_result.deleted_count} old comments.")

    # Option B: Update/Insert (Upsert) based on comment_id. More robust but complex.
    # For simplicity in MVP, let's use Option A or just insert without checking (simpler but duplicates possible if run twice).
    # Let's try a simple insert for now, assuming we fetch fresh each time or handle duplicates later.
    # A better approach for production would be upserting based on comment_id.

    # For simplicity now: Insert all fetched comments.
    # Consider adding checks or deletion logic if running this repeatedly is expected.
    try:
         # Check if comments already exist for this video_id
        existing_count = collection.count_documents({"video_id": video_id})
        if existing_count > 0:
            print(f"Warning: Comments for video_id {video_id} already exist ({existing_count}). Consider deleting them first if you want a fresh fetch.")
            # Decide how to handle this: skip, delete, or merge. For MVP, let's just print a warning.
            # return 0 # uncomment to skip insertion if comments exist

        print(f"Inserting {len(comments)} comments for video_id: {video_id}...")
        insert_result = collection.insert_many(comments)
        print(f"Successfully inserted {len(insert_result.inserted_ids)} comments.")
        return len(insert_result.inserted_ids)
    except Exception as e:
        print(f"Error saving comments to MongoDB: {e}")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch YouTube comments for one or two videos and store them in MongoDB.")
    parser.add_argument("urls", nargs='+', help="One or two YouTube video URLs or video IDs.")
    parser.add_argument("--max", type=int, default=1000, help="Maximum number of comments to fetch per video.")
    # Add argument to clear existing comments
    parser.add_argument("--clear", action='store_true', help="Delete existing comments for the video ID(s) before fetching.")


    args = parser.parse_args()

    if len(args.urls) > 2:
        print("Error: Please provide a maximum of two URLs.")
        sys.exit(1)

    video_ids = []
    for url in args.urls:
        video_id = extract_video_id(url)
        if not video_id:
            print(f"Error: Could not extract video ID from URL: {url}")
        else:
            video_ids.append(video_id)

    if not video_ids:
        print("No valid video IDs found. Exiting.")
        sys.exit(1)

    collection = get_comments_collection() # Get collection once

    for video_id in video_ids:
        print(f"\n--- Processing Video ID: {video_id} ---")

        # Clear existing comments if requested
        if args.clear:
            print(f"Clearing existing comments for video_id: {video_id}...")
            delete_result = collection.delete_many({"video_id": video_id})
            print(f"Deleted {delete_result.deleted_count} comments.")

        comments_data = get_youtube_comments(video_id, max_total_results=args.max)
        if comments_data:
            save_comments_to_mongo(comments_data)
        else:
            print(f"No comments fetched or an error occurred for video ID: {video_id}")

    print("\nScript finished.")