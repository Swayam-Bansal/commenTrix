# backend/routes/comments_routes.py
from flask import Blueprint, request, jsonify
from scripts.fetch_comments import save_comments_to_mongo
from services.youtube_service import get_youtube_comments
from utils.youtube_ID_utils import extract_video_id
from db.connection import get_comments_collection

comments_bp = Blueprint('comments', __name__, url_prefix='/comments')

@comments_bp.route('/fetch', methods=['POST'])
def fetch_comments():
    urls = request.json.get('urls')
    if not urls or not isinstance(urls, list) or not 1 <= len(urls) <= 2:
        return jsonify({"error": "Please provide a list of one or two YouTube video URLs in the request body."}), 400

    fetched_counts = {}
    for url in urls:
        video_id = extract_video_id(url)
        if video_id:
            comments = get_youtube_comments(video_id)
            count = save_comments_to_mongo(comments)
            fetched_counts[video_id] = count
        else:
            fetched_counts[url] = "Could not extract video ID."

    return jsonify({"message": "Fetching and storing process initiated.", "details": fetched_counts}), 200

@comments_bp.route('/<video_id>', methods=['GET'])
def get_comments(video_id):
    collection = get_comments_collection()
    comments = list(collection.find({"video_id": video_id}, {'_id': 0})) # Exclude _id from response
    return jsonify(comments)