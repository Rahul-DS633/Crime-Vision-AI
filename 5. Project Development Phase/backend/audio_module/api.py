import os
import time
from pathlib import Path
# pyrefly: ignore [missing-import]
from flask import Blueprint, request, jsonify
# pyrefly: ignore [missing-import]
from werkzeug.utils import secure_filename
from config import AUDIO_UPLOAD_DIR
from utils.logger import setup_logger
from services.audio_service import audio_service

logger = setup_logger("audio_api")

audio_analysis_bp = Blueprint('audio_analysis', __name__, url_prefix='/api/analyze-audio')

@audio_analysis_bp.route('', methods=['POST'])
@audio_analysis_bp.route('/', methods=['POST'])
def analyze_audio():
    """
    Main endpoint for audio analysis
    """
    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"status": "error", "message": "No selected audio file"}), 400
            
            filename = secure_filename(file.filename)
            unique_name = f"{int(time.time())}_{filename}"
            save_path = os.path.join(AUDIO_UPLOAD_DIR, unique_name)
            file.save(save_path)
        elif request.is_json and 'audio_path' in request.json:
            target = request.json['audio_path']
            if os.path.exists(target):
                save_path = target
            else:
                alt = os.path.join(AUDIO_UPLOAD_DIR, os.path.basename(target))
                if os.path.exists(alt):
                    save_path = alt
                else:
                    save_path = os.path.join(AUDIO_UPLOAD_DIR, "case01_distress_call_911.wav")
        else:
            # Use sample audio if none uploaded directly
            sample_path = os.path.join(AUDIO_UPLOAD_DIR, "case01_distress_call_911.wav")
            if not os.path.exists(sample_path):
                sample_path = os.path.join(AUDIO_UPLOAD_DIR, "sample_robbery_witness.wav")
            save_path = sample_path

        result = audio_service.process_audio(save_path)
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error in audio analysis endpoint: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
