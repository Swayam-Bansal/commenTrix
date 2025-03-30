import sys
import os
import argparse
from collections import defaultdict

# Ensure the backend directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_comments_collection, get_db

def compare_videos_analysis(video_id_a: str, video_id_b: str):
    """
    Compares the analysis results (sentiment distribution, top comments, summaries)
    between two videos.
    """
    comments_collection = get_comments_collection()
    db = get_db()
    transcript_collection = db.get_collection("transcripts")

    comparison_results = {
        "videoA": {"video_id": video_id_a},
        "videoB": {"video_id": video_id_b},
    }

    # --- Get Sentiment Distribution for Video A ---
    sentiment_counts_a = defaultdict(int)
    comments_a = list(db.comments.find({"video_id": video_id_a, "sentiment": {"$ne": None}}))
    total_comments_a = len(comments_a)
    for comment in comments_a:
        sentiment_counts_a[comment["sentiment"]] += 1

    sentiment_distribution_a = {}
    if total_comments_a > 0:
        for sentiment, count in sentiment_counts_a.items():
            sentiment_distribution_a[sentiment] = round((count / total_comments_a) * 100, 2)
    comparison_results["videoA"]["sentiment_distribution"] = sentiment_distribution_a

    # --- Get Sentiment Distribution for Video B ---
    sentiment_counts_b = defaultdict(int)
    comments_b = list(db.comments.find({"video_id": video_id_b, "sentiment": {"$ne": None}}))
    total_comments_b = len(comments_b)
    for comment in comments_b:
        sentiment_counts_b[comment["sentiment"]] += 1

    sentiment_distribution_b = {}
    if total_comments_b > 0:
        for sentiment, count in sentiment_counts_b.items():
            sentiment_distribution_b[sentiment] = round((count / total_comments_b) * 100, 2)
    comparison_results["videoB"]["sentiment_distribution"] = sentiment_distribution_b

    # --- Get Top Liked Comments (Optional for MVP, but good to include) ---
    top_comments_a = list(comments_collection.find({"video_id": video_id_a}).sort("likeCount", -1).limit(5))
    comparison_results["videoA"]["top_comments"] = [{"author": c.get("author"), "text": c.get("text"), "likes": c.get("likeCount")} for c in top_comments_a]

    top_comments_b = list(comments_collection.find({"video_id": video_id_b}).sort("likeCount", -1).limit(5))
    comparison_results["videoB"]["top_comments"] = [{"author": c.get("author"), "text": c.get("text"), "likes": c.get("likeCount")} for c in top_comments_b]

    # --- Get Summaries (We haven't implemented summarization yet, so for now, we'll leave this out) ---
    # You would query a 'summaries' collection or a field in your comment/video document here.
    comparison_results["videoA"]["summary"] = "Summary for Video A will go here."
    comparison_results["videoB"]["summary"] = "Summary for Video B will go here."

    return comparison_results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compares analysis results of two YouTube videos.")
    parser.add_argument("video_id_a", help="The video ID of the first video.")
    parser.add_argument("video_id_b", help="The video ID of the second video.")

    args = parser.parse_args()

    results = compare_videos_analysis(args.video_id_a, args.video_id_b)

    import json
    print("\n--- Comparison Results ---")
    print(json.dumps(results, indent=4))