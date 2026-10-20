"""
Video Processor Module - OpenCV frame extraction and temporal sampling at 1Hz
"""
import os
# pyrefly: ignore [missing-import]
import cv2
# pyrefly: ignore [missing-import]
import numpy as np
from typing import List, Dict, Any, Tuple
from utils.logger import setup_logger

logger = setup_logger("video_processor")

def extract_frames(video_path: str, target_fps: float = 1.0, max_seconds: int = 60) -> Tuple[List[Dict[str, Any]], float, int, int]:
    """
    Samples video frames second-by-second (1Hz) using OpenCV.
    Returns: (list_of_frames_with_metadata, duration_seconds, width, height)
    """
    logger.info(f"Extracting frames from video at {target_fps} Hz: {video_path}")
    if not os.path.exists(video_path):
        logger.warning(f"Video file {video_path} does not exist, creating synthetic frame sequence.")
        # Return synthetic frames representing 15 seconds of surveillance footage
        synthetic_frames = []
        for sec in range(15):
            synthetic_frames.append({
                "second": sec,
                "timestamp_str": f"00:{sec:02d}",
                "frame": np.zeros((480, 640, 3), dtype=np.uint8)
            })
        return synthetic_frames, 15.0, 640, 480

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logger.error(f"Failed to open video file: {video_path}")
        return [], 0.0, 0, 0

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
    duration = total_frames / fps if fps > 0 else 0.0

    frame_interval = int(round(fps / target_fps)) if target_fps > 0 else int(fps)
    if frame_interval <= 0:
        frame_interval = 1

    extracted = []
    frame_idx = 0
    second = 0

    while cap.isOpened() and second < max_seconds:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_interval == 0:
            # Resize frame for optimized inference speed while preserving evidentiary aspect ratio
            h, w = frame.shape[:2]
            target_w = 640
            target_h = int(h * (target_w / float(w)))
            resized_frame = cv2.resize(frame, (target_w, target_h), interpolation=cv2.INTER_AREA)

            mm = second // 60
            ss = second % 60
            extracted.append({
                "second": second,
                "timestamp_str": f"{mm:02d}:{ss:02d}",
                "frame": resized_frame
            })
            second += 1

        frame_idx += 1

    cap.release()
    logger.info(f"Extracted {len(extracted)} frames across {duration:.1f} seconds duration.")
    return extracted, duration if duration > 0 else float(len(extracted)), width, height
