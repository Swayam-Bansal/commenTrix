# backend/routes/analysis_routes.py
from flask import Blueprint, request, jsonify
from scripts.compare_videos import compare_videos_analysis

analysis_bp = Blueprint('analysis', __name__, url_prefix='/analysis')

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

# You can add other analysis-related routes here, e.g., for triggering individual video analysis