"""
Main Flask Application for Crime Scene Reconstruction System
CrimeVision AI - Intelligent Multimodal Forensic Analysis Platform
"""
import os
import sys

# Deep Environment Fix - Must be set BEFORE any other imports to prevent protobuf/tensorflow issues
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
os.environ['USE_TF'] = 'NO'
os.environ['USE_TORCH'] = 'YES'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Ensure backend directory is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# pyrefly: ignore [missing-import]
from flask import Flask, jsonify, request, send_from_directory

from flask_cors import CORS
from config import API_CONFIG, BASE_DIR
from routes.upload_bp import upload_bp
from routes.processing_bp import processing_bp
from routes.results_bp import results_bp
from audio_module.api import audio_analysis_bp
from video_module.api import video_analysis_bp
from routes.chat_routes import chat_bp
from utils.logger import setup_logger, app_logger
from utils.model_loader import preload_models

# Create Flask app
frontend_dir = os.path.abspath(os.path.join(current_dir, '..', 'frontend'))
app = Flask(__name__, static_folder=frontend_dir, static_url_path='')

# Registers all specialized modules as "Blueprints"
app.register_blueprint(upload_bp)
app.register_blueprint(processing_bp)
app.register_blueprint(results_bp)
app.register_blueprint(audio_analysis_bp)
app.register_blueprint(video_analysis_bp)
app.register_blueprint(chat_bp)

# Configures CORS so the frontend can talk to the backend
CORS(app, resources={r"/api/*": {"origins": "*"}})

from config import API_CONFIG, BASE_DIR, DATA_DIR, UPLOAD_DIR

@app.route('/data/<path:path>')
def serve_data(path):
    return send_from_directory(str(DATA_DIR), path)

@app.route('/uploads/<path:path>')
def serve_uploads(path):
    return send_from_directory(str(UPLOAD_DIR), path)

@app.route('/')
def index():
    return send_from_directory(frontend_dir, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(frontend_dir, path)):
        return send_from_directory(frontend_dir, path)
    if os.path.exists(os.path.join(str(DATA_DIR), path)):
        return send_from_directory(str(DATA_DIR), path)
    return send_from_directory(frontend_dir, 'index.html')

if __name__ == '__main__':
    preload_models()
    app_logger.info(f"Starting CrimeVision AI Forensic Platform on port {API_CONFIG['port']}...")
    app.run(
        host=API_CONFIG.get("host", "0.0.0.0"),
        port=API_CONFIG.get("port", 5000),
        debug=API_CONFIG.get("debug", True)
    )
