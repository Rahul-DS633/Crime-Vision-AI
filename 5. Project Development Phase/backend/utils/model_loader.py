import os
import torch
from config import MODEL_CONFIG, DEVICE
from utils.logger import setup_logger

logger = setup_logger("model_loader")

# Render Free Tier provides 512MB RAM. Enable lightweight mode to prevent OOM.
IS_LOW_MEMORY = os.getenv("RENDER") == "true" or os.getenv("LOW_MEMORY", "true").lower() in ("true", "1", "yes")

_models = {
    "rt_detr": None,
    "clip": None,
    "blip2": None,
    "whisper": None
}

def load_rt_detr_model():
    """
    Loads RT-DETR model and image processor.
    Uses HuggingFace AutoImageProcessor and AutoModelForObjectDetection.
    """
    if _models["rt_detr"] is not None:
        return _models["rt_detr"]

    if IS_LOW_MEMORY:
        logger.info("Cloud low-memory environment detected. Using optimized CV/YOLO fallback detector (<70MB RAM).")
        _models["rt_detr"] = {
            "processor": None,
            "model": None,
            "device": DEVICE,
            "is_fallback": True,
            "confidence_threshold": MODEL_CONFIG["rt_detr"]["confidence_threshold"]
        }
        return _models["rt_detr"]

    model_name = MODEL_CONFIG["rt_detr"]["model_name"]
    logger.info(f"Loading RT-DETR object detection model ({model_name}) on {DEVICE}...")
    try:
        from transformers import AutoImageProcessor, AutoModelForObjectDetection
        try:
            processor = AutoImageProcessor.from_pretrained(model_name, local_files_only=True)
            model = AutoModelForObjectDetection.from_pretrained(model_name, local_files_only=True).to(DEVICE)
        except Exception:
            processor = AutoImageProcessor.from_pretrained(model_name)
            model = AutoModelForObjectDetection.from_pretrained(model_name).to(DEVICE)
        model.eval()
        _models["rt_detr"] = {
            "processor": processor,
            "model": model,
            "device": DEVICE,
            "confidence_threshold": MODEL_CONFIG["rt_detr"]["confidence_threshold"]
        }
        logger.info("RT-DETR model loaded successfully.")
    except Exception as e:
        logger.warning(f"Could not load HuggingFace RT-DETR ({e}). Falling back to optimized CV/YOLO fallback detector.")
        _models["rt_detr"] = {
            "processor": None,
            "model": None,
            "device": DEVICE,
            "is_fallback": True,
            "confidence_threshold": MODEL_CONFIG["rt_detr"]["confidence_threshold"]
        }
    return _models["rt_detr"]

def load_clip_model():
    """
    Loads CLIP model for scene classification.
    """
    if _models["clip"] is not None:
        return _models["clip"]

    if IS_LOW_MEMORY:
        logger.info("Cloud low-memory environment detected. Using lightweight forensic scene classifier.")
        _models["clip"] = {
            "processor": None,
            "model": None,
            "device": DEVICE,
            "is_fallback": True
        }
        return _models["clip"]

    model_name = MODEL_CONFIG["clip"]["model_name"]
    logger.info(f"Loading CLIP model ({model_name}) on {DEVICE}...")
    try:
        from transformers import CLIPProcessor, CLIPModel
        try:
            processor = CLIPProcessor.from_pretrained(model_name, local_files_only=True)
            model = CLIPModel.from_pretrained(model_name, local_files_only=True).to(DEVICE)
        except Exception:
            processor = CLIPProcessor.from_pretrained(model_name)
            model = CLIPModel.from_pretrained(model_name).to(DEVICE)
        model.eval()
        _models["clip"] = {
            "processor": processor,
            "model": model,
            "device": DEVICE
        }
        logger.info("CLIP model loaded successfully.")
    except Exception as e:
        logger.warning(f"Could not load HuggingFace CLIP ({e}). Falling back to rule-based scene classifier.")
        _models["clip"] = {
            "processor": None,
            "model": None,
            "device": DEVICE,
            "is_fallback": True
        }
    return _models["clip"]

def load_blip2_model():
    """
    Loads BLIP / BLIP-2 model for image captioning.
    """
    if _models["blip2"] is not None:
        return _models["blip2"]

    if IS_LOW_MEMORY:
        logger.info("Cloud low-memory environment detected. Using lightweight forensic visual descriptor.")
        _models["blip2"] = {
            "processor": None,
            "model": None,
            "device": DEVICE,
            "is_fallback": True
        }
        return _models["blip2"]

    model_name = MODEL_CONFIG["blip2"]["model_name"]
    logger.info(f"Loading BLIP captioning model ({model_name}) on {DEVICE}...")
    try:
        from transformers import BlipProcessor, BlipForConditionalGeneration
        try:
            processor = BlipProcessor.from_pretrained(model_name, local_files_only=True)
            model = BlipForConditionalGeneration.from_pretrained(model_name, local_files_only=True).to(DEVICE)
        except Exception:
            processor = BlipProcessor.from_pretrained(model_name)
            model = BlipForConditionalGeneration.from_pretrained(model_name).to(DEVICE)
        model.eval()
        _models["blip2"] = {
            "processor": processor,
            "model": model,
            "device": DEVICE
        }
        logger.info("BLIP model loaded successfully.")
    except Exception as e:
        logger.warning(f"Could not load HuggingFace BLIP ({e}). Using forensic caption synthesizer.")
        _models["blip2"] = {
            "processor": None,
            "model": None,
            "device": DEVICE,
            "is_fallback": True
        }
    return _models["blip2"]

def load_whisper_model():
    """
    Loads Whisper pipeline for multilingual speech-to-text.
    """
    if _models["whisper"] is not None:
        return _models["whisper"]

    if IS_LOW_MEMORY:
        logger.info("Cloud low-memory environment detected. Using acoustic speech analyzer.")
        _models["whisper"] = None
        return _models["whisper"]

    logger.info(f"Loading Whisper pipeline on {DEVICE}...")
    try:
        from transformers import pipeline
        whisper_pipe = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-base",
            device=0 if DEVICE == "cuda" else -1,
            return_timestamps=True
        )
        _models["whisper"] = whisper_pipe
        logger.info("Whisper pipeline loaded successfully.")
    except Exception as e:
        logger.warning(f"Could not load HuggingFace Whisper pipeline ({e}). Using acoustic speech analyzer.")
        _models["whisper"] = None
    return _models["whisper"]

def preload_models():
    """
    Called on server startup to verify or prepare AI inference engines.
    """
    logger.info("Initializing CrimeVision AI model registries...")
    # Models are lazy-loaded on demand to ensure instant server start
    return True
