import googleapiclient.discovery
import json
import re
import os
from dotenv import load_dotenv

def extract_video_id(video_url):
    """
    Extracts the video ID from a YouTube video URL.

    Args:
        video_url: The YouTube video URL.

    Returns:
        The video ID, or None if the URL is invalid.
    """
    try:
        # Regular expression to extract the video ID
        video_id_match = re.search(r'(?<=v=)[^&#]+', video_url) or re.search(r'(?<=be/)[^&#]+', video_url)
        if video_id_match:
            return video_id_match.group(0)
        else:
            return None
    except Exception as e:
        print(f"Error extracting video ID: {e}")
        return None


def get_youtube_comments(api_key, video_id, max_results=100):
    """
    Retrieves comments from a YouTube video and returns them in JSON format.

    Args:
        api_key: Your YouTube Data API v3 key.
        video_id: The ID of the YouTube video.
        max_results: The maximum number of comments to retrieve.

    Returns:
        A list of dictionaries, where each dictionary represents a comment.
        Returns None if an error occurs.
    """

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=api_key
    )

    comments = []
    next_page_token = None

    try:
        while len(comments) < max_results:
            request = youtube.commentThreads().list(
                part="snippet,replies",
                videoId=video_id,
                maxResults=min(100, max_results - len(comments)), #ensure we don't exceed max_results
                pageToken=next_page_token,
            )
            response = request.execute()

            for item in response.get("items", []):
                snippet = item["snippet"]["topLevelComment"]["snippet"]
                comment_data = {
                    "text": snippet["textDisplay"],
                    "author": snippet["authorDisplayName"],
                    "publishedAt": snippet["publishedAt"],
                    "likeCount": snippet["likeCount"],
                    "replyCount": item["snippet"].get("totalReplyCount",0)
                }
                comments.append(comment_data)

                if "replies" in item:
                    for reply in item["replies"].get("comments", []):
                        reply_snippet = reply["snippet"]
                        reply_data = {
                            "text": reply_snippet["textDisplay"],
                            "author": reply_snippet["authorDisplayName"],
                            "publishedAt": reply_snippet["publishedAt"],
                            "likeCount": reply_snippet["likeCount"],
                            "isReply": True,
                        }
                        comments.append(reply_data)

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break

        return comments
    except googleapiclient.errors.HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def save_comments_to_json(comments, filename="youtube_comments.json"):
    """
    Saves the list of comments to a JSON file.

    Args:
        comments: The list of comment dictionaries.
        filename: The name of the JSON file to save to.
    """
    if comments:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(comments, f, ensure_ascii=False, indent=4)
        print(f"Comments saved to {filename}")
    else:
        print("No comments to save.")

if __name__ == "__main__":
    api_key = os.getenv("YOUTUBE_API_KEY") # get api key from .env
    if not api_key:
        print("Error: YOUTUBE_API_KEY not found in .env file.")
        exit()

    video_url = input("Enter the YouTube video URL: ")
    video_id = extract_video_id(video_url)

    if video_id:
        comments = get_youtube_comments(api_key, video_id)

        if comments:
            save_comments_to_json(comments)
        else:
            print("Failed to retrieve comments.")
    else:
        print("Invalid YouTube video URL.") # Replace with your API key
