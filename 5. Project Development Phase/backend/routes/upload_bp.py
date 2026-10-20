import os
import time
# pyrefly: ignore [missing-import]
from flask import Blueprint, request, jsonify
# pyrefly: ignore [missing-import]
from werkzeug.utils import secure_filename
from config import UPLOAD_DIR, IMAGE_UPLOAD_DIR, AUDIO_UPLOAD_DIR, VIDEO_UPLOAD_DIR, PROCESSING_CONFIG
from utils.logger import setup_logger

logger = setup_logger("upload_routes")

upload_bp = Blueprint('upload', __name__, url_prefix='/api/upload')

@upload_bp.route('', methods=['POST'])
@upload_bp.route('/', methods=['POST'])
@upload_bp.route('/batch', methods=['POST'])
def upload_batch():
    """
    Universal File Uploader for images, audio, and video
    """
    try:
        uploaded_files = []
        files = request.files.getlist('files') or request.files.getlist('file')

        if not files:
            return jsonify({"status": "error", "message": "No files provided in request"}), 400

        for file in files:
            if file and file.filename:
                orig_name = secure_filename(file.filename)
                ext = os.path.splitext(orig_name)[1].lower()
                unique_name = f"{int(time.time())}_{orig_name}"

                # Route to correct media directory
                if ext in PROCESSING_CONFIG["allowed_image_extensions"]:
                    dest_dir = IMAGE_UPLOAD_DIR
                    media_type = "image"
                elif ext in PROCESSING_CONFIG["allowed_audio_extensions"]:
                    dest_dir = AUDIO_UPLOAD_DIR
                    media_type = "audio"
                elif ext in PROCESSING_CONFIG["allowed_video_extensions"]:
                    dest_dir = VIDEO_UPLOAD_DIR
                    media_type = "video"
                else:
                    dest_dir = UPLOAD_DIR
                    media_type = "generic"

                save_path = os.path.join(dest_dir, unique_name)
                file.save(save_path)
                
                uploaded_files.append({
                    "original_name": orig_name,
                    "saved_name": unique_name,
                    "file_path": save_path,
                    "media_type": media_type,
                    "file_size": os.path.getsize(save_path)
                })

        logger.info(f"Successfully uploaded {len(uploaded_files)} file(s).")
        return jsonify({
            "status": "success",
            "message": f"Successfully uploaded {len(uploaded_files)} file(s)",
            "files": uploaded_files
        }), 200

    except Exception as e:
        logger.error(f"Error in batch upload: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
