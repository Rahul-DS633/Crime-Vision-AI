import os
import time
# pyrefly: ignore [missing-import]
from flask import Blueprint, request, jsonify
# pyrefly: ignore [missing-import]
from werkzeug.utils import secure_filename
from config import IMAGE_UPLOAD_DIR, SAMPLES_DIR
from utils.logger import setup_logger
from services.vision_service import vision_service
from services.audio_service import audio_service
from services.video_service import video_service
from services.fusion_service import fusion_service
from services.session_store import session_store

logger = setup_logger("processing_bp")

processing_bp = Blueprint('processing', __name__, url_prefix='/api/process')

@processing_bp.route('/image', methods=['POST'])
def process_image():
    """
    Dedicated endpoint for single image forensic analysis
    """
    try:
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({"status": "error", "message": "No file selected"}), 400
            orig_name = secure_filename(file.filename)
            unique_name = f"{int(time.time())}_{orig_name}"
            save_path = os.path.join(IMAGE_UPLOAD_DIR, unique_name)
            file.save(save_path)
        elif request.is_json and 'image_path' in request.json:
            save_path = request.json['image_path']
        else:
            # Fallback to sample crime scene
            save_path = os.path.join(IMAGE_UPLOAD_DIR, "sample_crime_scene.jpg")

        result = vision_service.analyze_image(save_path)
        session_id = session_store.create_session(result)
        result["session_id"] = session_id
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error in image analysis: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@processing_bp.route('/complete/<case_id>', methods=['POST', 'GET'])
@processing_bp.route('/complete', methods=['POST'])
def process_complete_pipeline(case_id="default"):
    """
    Executes full multimodal 3D/Video/Audio/Image fusion pipeline
    """
    try:
        req_data = request.json if request.is_json else {}
        image_path = req_data.get("image_path")
        audio_path = req_data.get("audio_path")
        video_path = req_data.get("video_path")

        # Fallback defaults if not provided
        if not image_path:
            image_path = os.path.join(IMAGE_UPLOAD_DIR, "sample_crime_scene.jpg")
        if not audio_path:
            audio_path = os.path.join(IMAGE_UPLOAD_DIR.parent, "audio", "sample_robbery_witness.wav")
        if not video_path:
            video_path = os.path.join(IMAGE_UPLOAD_DIR.parent, "video", "sample_surveillance_store.mp4")

        # Run vision, audio, and video modules
        vision_res = vision_service.analyze_image(image_path)
        audio_res = audio_service.process_audio(audio_path)
        video_res = video_service.process_video(video_path)

        # Run multimodal fusion
        fusion_res = fusion_service.fuse_multimodal_evidence(vision_res, audio_res, video_res)

        complete_result = {
            "case_id": case_id,
            "status": "success",
            "scene_data": vision_res.get("scene_3d_data", {}),
            "vision_results": vision_res,
            "audio_results": audio_res,
            "video_results": video_res,
            "timeline_results": fusion_res.get("unified_timeline", video_res.get("timeline", [])),
            "fusion": fusion_res
        }

        session_id = session_store.create_session(complete_result)
        complete_result["session_id"] = session_id

        return jsonify(complete_result), 200

    except Exception as e:
        logger.error(f"Error in complete pipeline execution: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
