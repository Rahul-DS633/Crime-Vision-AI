import os
from pathlib import Path
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
IMAGE_UPLOAD_DIR = UPLOAD_DIR / "image"
AUDIO_UPLOAD_DIR = UPLOAD_DIR / "audio"
VIDEO_UPLOAD_DIR = UPLOAD_DIR / "video"
SESSIONS_DIR = DATA_DIR / "sessions"
SAMPLES_DIR = DATA_DIR / "samples"
REPORTS_DIR = DATA_DIR / "reports"

# Ensure runtime directories exist
for path in [DATA_DIR, UPLOAD_DIR, IMAGE_UPLOAD_DIR, AUDIO_UPLOAD_DIR, VIDEO_UPLOAD_DIR, SESSIONS_DIR, SAMPLES_DIR, REPORTS_DIR]:
    path.mkdir(parents=True, exist_ok=True)

try:
    import torch
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
except Exception:
    torch = None
    DEVICE = "cpu"

API_CONFIG = {
    "host": "0.0.0.0",
    "port": int(os.getenv("PORT", 5000)),
    "debug": os.getenv("FLASK_ENV") != "production",
    "cors_origins": "*"
}

MODEL_CONFIG = {
    "rt_detr": {
        "model_name": "PekingU/rtdetr_r50vd",
        "confidence_threshold": 0.35,
        "device": DEVICE
    },
    "clip": {
        "model_name": "openai/clip-vit-base-patch32",
        "device": DEVICE
    },
    "blip2": {
        "model_name": "Salesforce/blip-image-captioning-base",
        "device": DEVICE
    },
    "whisper": {
        "model_name": "openai/whisper-base",
        "device": DEVICE
    },
    "groq_model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    "groq_fallback_model": "llama-3.1-8b-instant",
    "groq_api_key": os.getenv("GROQ_API_KEY", "")
}

PROCESSING_CONFIG = {
    "video_sample_fps": 1.0,  # 1 Hz sampling as specified in Milestone 4
    "max_video_duration_seconds": 120,
    "allowed_image_extensions": {".jpg", ".jpeg", ".png", ".webp", ".bmp"},
    "allowed_audio_extensions": {".mp3", ".wav", ".ogg", ".m4a", ".aac"},
    "allowed_video_extensions": {".mp4", ".avi", ".mov", ".mkv", ".webm"}
}
