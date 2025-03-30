#Script thta runs all NLP tasks on comments
import sys
import os
from tqdm import tqdm  # For progress bar

# Ensure the backend directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_comments_collection
from nlp.sentiment_model import get_ternary_sentiment

def analyze_and_update_sentiment(video_id: str):
    """
    Fetches comments for a given video ID from MongoDB, analyzes their sentiment,
    and updates the comment documents in the database.
    """
    comments_collection = get_comments_collection()
    comments_to_analyze = comments_collection.find({"video_id": video_id, "sentiment": None})
    total_comments = comments_to_analyze.count()

    if total_comments == 0:
        print(f"No new comments to analyze for video ID: {video_id}")
        return

    print(f"Analyzing sentiment for {total_comments} comments for video ID: {video_id}...")

    for comment in tqdm(comments_to_analyze, total=total_comments, desc="Analyzing Comments"):
        text = comment.get("text")
        if text:
            sentiment, score = get_ternary_sentiment(text)
            comments_collection.update_one(
                {"_id": comment["_id"]},
                {"$set": {"sentiment": sentiment, "sentiment_score": score}}
            )

    print(f"Sentiment analysis complete for video ID: {video_id}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Analyze sentiment of YouTube comments stored in MongoDB.")
    parser.add_argument("video_ids", nargs='+', help="One or more video IDs to analyze.")

    args = parser.parse_args()

    for video_id in args.video_ids:
        print(f"\n--- Analyzing Video ID: {video_id} ---")
        analyze_and_update_sentiment(video_id)

    print("\nSentiment analysis process finished.")