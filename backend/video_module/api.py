import os
import time
from pathlib import Path
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from config import VIDEO_UPLOAD_DIR
from utils.logger import setup_logger
from services.video_service import video_service

logger = setup_logger("video_api")

video_analysis_bp = Blueprint('video_analysis', __name__, url_prefix='/api/analyze-video')

@video_analysis_bp.route('', methods=['POST'])
@video_analysis_bp.route('/', methods=['POST'])
def analyze_video():
    """
    Main endpoint for video analysis
    """
    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"status": "error", "message": "No selected video file"}), 400
            
            filename = secure_filename(file.filename)
            unique_name = f"{int(time.time())}_{filename}"
            save_path = os.path.join(VIDEO_UPLOAD_DIR, unique_name)
            file.save(save_path)
        elif request.is_json and 'video_path' in request.json:
            save_path = request.json['video_path']
        else:
            # Fallback sample surveillance video path
            sample_path = os.path.join(VIDEO_UPLOAD_DIR, "sample_surveillance_store.mp4")
            save_path = sample_path

        result = video_service.process_video(save_path)
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error in video analysis endpoint: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
