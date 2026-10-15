"""
Video Timeline Module - Hash indexing and temporal float normalization
"""
from typing import List, Dict, Any
from utils.logger import setup_logger

logger = setup_logger("video_timeline")

def build_timeline(captions: List[Dict[str, Any]], detections: List[Dict[str, Any]], groq_client=None, config=None, duration: float = 14.0) -> Dict[str, Any]:
    """
    Builds a second-by-second forensic event timeline with exact second snapping.
    """
    # HASH INDEXING: Group by exact second
    caption_map = {}
    for c in captions:
        sec = c.get("second")
        if sec is None:
            ts = c.get("timestamp", "00:00")
            parts = ts.split(":")
            sec = int(parts[0]) * 60 + int(parts[1]) if len(parts) == 2 else 0
        caption_map[int(sec)] = c.get("caption", "")

    detection_map = {}
    for d in detections:
        sec = d.get("second")
        if sec is None:
            ts = d.get("timestamp", "00:00")
            parts = ts.split(":")
            sec = int(parts[0]) * 60 + int(parts[1]) if len(parts) == 2 else 0
        detection_map[int(sec)] = [det.get("label", "Object") for det in d.get("detections", [])]

    final_timeline = []
    total_seconds = max(int(duration), max(caption_map.keys()) if caption_map else 14)

    for s in range(total_seconds + 1):
        # NORMALIZATION: Map asynchronous AI detections to fixed temporal clock
        description = caption_map.get(s) or "No significant activity"
        final_timeline.append({
            "time": f"{s // 60:02d}:{s % 60:02d}",  # Formatted string
            "event": description,
            "seconds": s,  # Numeric float-normalized offset
            "objects_at_second": detection_map.get(s, [])
        })

    logger.info(f"Built normalized second-by-second timeline with {len(final_timeline)} time points.")
    return {"timeline": final_timeline}
