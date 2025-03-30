#Script thta runs all NLP tasks on comments
import sys
import os
import argparse
from tqdm import tqdm
import nltk
from sentence_transformers import SentenceTransformer, util

# Ensure the backend directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.youtube_ID_utils import extract_video_id # Import your utility

# Ensure the backend directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_comments_collection, get_db
from nlp.sentiment_model import get_ternary_sentiment
from services.transcript_service import get_video_transcript, segment_transcript


def analyze_and_update_comments(video_id: str, video_url: str):
    """
    Fetches comments and transcript for a given video ID, generates embeddings,
    links comments to transcript segments based on similarity, performs sentiment analysis,
    and updates the comment documents in the database.
    """
    comments_collection = get_comments_collection()
    db = get_db()
    transcript_collection = db.get_collection("transcripts") # Assuming you'll store transcripts here

    # --- Fetch Comments ---
    comments_cursor = comments_collection.find({"video_id": video_id, "transcript_segment": {"$exists": False}}) # Only process new comments
    comments_list = list(comments_cursor)
    if not comments_list:
        print(f"No new comments to process for video ID: {video_id}")
        return

    print(f"Processing {len(comments_list)} new comments for video ID: {video_id}...")
    comments_processed = [comment.get("text", "") for comment in comments_list if comment.get("text")]

    # --- Fetch or Generate Transcript ---
    transcript_doc = transcript_collection.find_one({"video_id": video_id})
    if not transcript_doc or not transcript_doc.get("transcript_segments"):
        print(f"Transcript not found for video ID: {video_id}. Fetching and segmenting...")
        raw_transcript = get_video_transcript(video_id, video_url)
        if raw_transcript:
            transcript_segments = segment_transcript(raw_transcript)
            # Store the transcript segments in MongoDB
            transcript_collection.update_one(
                {"video_id": video_id},
                {"$set": {"video_id": video_id, "transcript_segments": transcript_segments}},
                upsert=True
            )
        else:
            print(f"Could not fetch transcript for video ID: {video_id}. Skipping similarity analysis.")
            return
    else:
        transcript_segments = transcript_doc["transcript_segments"]

    transcript_segments_processed = [seg.strip() for seg in transcript_segments if seg.strip()]

    # --- Generate Embeddings ---
    if transcript_segments_processed and comments_processed:
        print("\nLoading embedding model...")
        embedder = SentenceTransformer('all-MiniLM-L12-v2')
        print("Generating embeddings...")
        transcript_embeddings = embedder.encode(transcript_segments_processed, convert_to_tensor=True)
        comment_embeddings = embedder.encode(comments_processed, convert_to_tensor=True)
        print("Embeddings generated.")

        # --- Link Comments to Transcript ---
        print("\nLinking comments to transcript segments...")
        similarity_results = util.semantic_search(comment_embeddings, transcript_embeddings, top_k=1)

        # --- Analyze Sentiment and Update MongoDB ---
        print("\nAnalyzing sentiment and updating MongoDB...")
        for i, comment in tqdm(enumerate(comments_list), total=len(comments_list), desc="Processing Comments"):
            if i < len(similarity_results):
                linked_segment_index = similarity_results[i][0]['corpus_id']
                similarity_score = similarity_results[i][0]['score']
                linked_segment = transcript_segments[linked_segment_index]

                text = comment.get("text")
                sentiment, sentiment_score = get_ternary_sentiment(text)

                comments_collection.update_one(
                    {"_id": comment["_id"]},
                    {"$set": {
                        "transcript_segment": linked_segment.strip(),
                        "similarity_score": round(similarity_score, 4),
                        "sentiment": sentiment,
                        "sentiment_score": sentiment_score
                    }}
                )
            else:
                print(f"Warning: Skipping update for comment {comment['_id']} due to mismatched similarity results.")
    else:
        print("Skipping embedding and linking as either transcript or comments are missing.")

    print(f"Analysis complete for video ID: {video_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetches comments and transcript, analyzes them, and stores results in MongoDB.")
    parser.add_argument("video_urls", nargs='+', help="One or two YouTube video URLs to analyze.")

    args = parser.parse_args()

    for video_url in args.video_urls:
        video_id = extract_video_id(video_url)  # Assuming this function is defined in youtube_ID_utils.py
        if video_id:
            print(f"\n--- Processing Video URL: {video_url} (ID: {video_id}) ---")
            analyze_and_update_comments(video_id, video_url)
        else:
            print(f"Could not extract video ID from URL: {video_url}")

    print("\nAnalysis process finished.")