"""
Video Service - Orchestration of OpenCV, RT-DETR frame detection, and temporal event timeline
"""
import os
import time
from typing import Dict, Any, List
from config import VIDEO_UPLOAD_DIR
from utils.logger import setup_logger
from video_module.opencv_detector import opencv_video_analyzer
from services.session_store import session_store

logger = setup_logger("video_service")

class VideoService:
    def __init__(self):
        pass

    def process_video(self, video_path: str) -> Dict[str, Any]:
        """
        Processes video footage at 1Hz using OpenCV, generates predictions for
        objects, people, vehicles, 2D boxes, 3D spatial trajectories, and timeline.
        """
        logger.info(f"Initiating full OpenCV video forensic analysis for {video_path}")
        result = opencv_video_analyzer.analyze_video(video_path, target_fps=1.0)

        # Save session context for chat and retrieval
        session_id = session_store.create_session(result)
        result["session_id"] = session_id
        return result

video_service = VideoService()
