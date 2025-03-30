from flask import Blueprint, request, jsonify
from scripts.compare_videos import compare_videos_analysis
from scripts.analyze_comments import analyze_and_update_comments # Import the analysis function

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')

@analysis_bp.route('/run', methods=['POST'])
def run_analysis():
    data = request.get_json()
    if not data or 'video_ids' not in data or not isinstance(data['video_ids'], list):
        return jsonify({"error": "Please provide a list of 'video_ids' in the request body."}), 400

    video_ids = data['video_ids']
    for video_id in video_ids:
        # We need the video URL to fetch the transcript if it doesn't exist.
        # You might need to adjust how you pass the URL here.
        # For now, let's assume the frontend will also pass the URLs.
        # A better approach might be to store the URL when fetching comments.
        # For this example, we'll expect URLs in the request.
        video_url = request.args.get('url') # Or expect it in the JSON body

        if video_id:
            print(f"Initiating analysis for video ID: {video_id}")
            analyze_and_update_comments(video_id, video_url) # Call the analysis function
        else:
            print("Skipping analysis for invalid video ID.")

    return jsonify({"message": "Analysis initiated for the provided video IDs."}), 200

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