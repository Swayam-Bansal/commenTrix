from flask import Blueprint, request, jsonify
from scripts.compare_videos import compare_videos_analysis
from scripts.analyze_comments import analyze_and_update_comments # Import the analysis function

from db.connection import get_comments_collection
from db.connection import get_db

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')

@analysis_bp.route('/run', methods=['POST'])
def run_analysis():
    data = request.get_json()
    if not data or 'video_ids' not in data or not isinstance(data['video_ids'], list):
        return jsonify({"error": "Please provide a list of 'video_ids' in the request body."}), 400

    video_ids = data['video_ids']
    url = request.args.get('url') # Assuming URL is passed as a query param

    for video_id in video_ids:
        if video_id and url:
            print(f"Initiating analysis for video ID: {video_id}")
            analyze_and_update_comments(video_id, url)
        else:
            print("Skipping analysis for invalid video ID or URL.")

    return jsonify({"message": "Analysis initiated for the provided video IDs."}, 200)


@analysis_bp.route('/single/<video_id>', methods=['GET'])
def get_single_video_analysis(video_id):
    comments_collection = get_comments_collection()
    db = get_db()
    transcript_collection = db.get_collection("transcripts")

    results = {"video_id": video_id}

    # Sentiment Distribution
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    comments = comments_collection.find({"video_id": video_id, "sentiment": {"$ne": None}})
    total_comments = comments_collection.count_documents({"video_id": video_id, "sentiment": {"$ne": None}}) # Use count_documents here
    for comment in comments:
        sentiment_counts[comment["sentiment"]] += 1

    sentiment_distribution = {}
    if total_comments > 0:
        for sentiment, count in sentiment_counts.items():
            sentiment_distribution[sentiment] = round((count / total_comments) * 100, 2)
    results["sentiment_distribution"] = sentiment_distribution

    # Top Comments
    top_comments = list(comments_collection.find({"video_id": video_id}).sort("likeCount", -1).limit(5))
    results["top_comments"] = [{"author": c.get("author"), "text": c.get("text"), "likes": c.get("likeCount")} for c in top_comments]

    # Summary
    transcript = transcript_collection.find_one({"video_id": video_id})
    results["summary"] = transcript.get("comment_summary", "No summary available.") if transcript else "No transcript found."

    return jsonify(results)


@analysis_bp.route('/compare', methods=['GET'])
def compare_videos():
    video_id_a = request.args.get('videoA')
    video_id_b = request.args.get('videoB')

    if not video_id_a or not video_id_b:
        return jsonify({"error": "Please provide both 'videoA' and 'videoB' as query parameters."}), 400

    try:
        comparison_results = compare_videos_analysis(video_id_a, video_id_b)
        return jsonify(comparison_results)
    except Exception as e:
        return jsonify({"error": f"An error occurred during comparison: {e}"}), 500