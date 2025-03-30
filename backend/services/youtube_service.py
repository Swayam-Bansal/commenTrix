# backend/services/youtube_service.py (Create this file and folder)
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv, find_dotenv

env_path = find_dotenv()
load_dotenv(env_path, override=True)
API_KEY = os.getenv("YOUTUBE_API_KEY")

if not API_KEY:
    raise ValueError("YOUTUBE_API_KEY not found in environment variables.")

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_youtube_comments(video_id: str, max_results_per_page: int = 100, max_total_results: int = 1000):
    """
    Fetches comments for a given YouTube video ID.
    Handles pagination.
    Stops after 'max_total_results' or when no more comments are available.
    """
    comments = []
    next_page_token = None
    fetched_count = 0

    print(f"Fetching comments for video ID: {video_id}...")

    while True:
        if fetched_count >= max_total_results:
            print(f"Reached max results limit ({max_total_results}). Stopping fetch.")
            break

        try:
            request = youtube.commentThreads().list(
                part="snippet", # We only need snippet for author, text, like count, publishedAt
                videoId=video_id,
                maxResults=min(max_results_per_page, max_total_results - fetched_count), # Adjust maxResults for the last page
                pageToken=next_page_token,
                textFormat="plainText" # Get plain text, not HTML
            )
            response = request.execute()

            for item in response.get("items", []):
                snippet = item.get("snippet", {}).get("topLevelComment", {}).get("snippet", {})
                if snippet: # Ensure snippet exists
                    comment_data = {
                        "comment_id": item.get("snippet", {}).get("topLevelComment", {}).get("id"), # Get comment ID
                        "video_id": video_id, # Add video_id for easy querying
                        "author": snippet.get("authorDisplayName"),
                        "text": snippet.get("textDisplay"),
                        "publishedAt": snippet.get("publishedAt"),
                        "updatedAt": snippet.get("updatedAt"),
                        "likeCount": snippet.get("likeCount", 0),
                        # Initialize analysis fields
                        "sentiment": None,
                        "sentiment_score": None,
                        "emotion": None,
                        "emotion_score": None
                    }
                    comments.append(comment_data)
                    fetched_count += 1
                    if fetched_count >= max_total_results:
                        break # Exit inner loop if max reached

            next_page_token = response.get("nextPageToken")
            print(f"Fetched {len(response.get('items', []))} comments this page. Total fetched: {fetched_count}")

            if not next_page_token:
                print("No more pages of comments.")
                break # Exit while loop if no more pages

        except HttpError as e:
            # Handle specific errors (e.g., comments disabled, video not found)
            if "disabled comments" in str(e).lower():
                 print(f"Comments are disabled for video {video_id}.")
            elif "video not found" in str(e).lower():
                 print(f"Video {video_id} not found.")
            else:
                print(f"An HTTP error occurred: {e}")
            # Decide if you want to return partial results or raise the error
            break # Stop fetching on error
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break # Stop fetching on unexpected error

    print(f"Finished fetching. Total comments retrieved: {len(comments)}")
    return comments