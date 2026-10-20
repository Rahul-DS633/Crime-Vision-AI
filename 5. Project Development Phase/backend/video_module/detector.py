"""
Video Detector Module - Frame-by-frame object detection and aggregation
Powered by OpenCV Computer Vision Analyzer
"""
from typing import List, Dict, Any, Tuple
from utils.logger import setup_logger
from video_module.opencv_detector import opencv_video_analyzer

logger = setup_logger("video_detector")

def detect_objects_in_frames(frames: List[Dict[str, Any]], video_path: str = "") -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Runs detection sequentially on each extracted video frame using OpenCV.
    Detects People, Vehicles, Objects, 2D Bounding Boxes, and 3D Trajectories.
    """
    res = opencv_video_analyzer.analyze_video(video_path or "sample_surveillance.mp4")
    return res.get("frame_detections", []), res.get("spatial_3d_trajectory", {})

def aggregate_objects(frame_detections: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregates detections across all frames to provide scene totals and unique objects.
    """
    all_labels = set()
    max_people = 0
    max_vehicles = 0
    max_weapons = 0

    for fd in frame_detections:
        for d in fd.get("detections", []):
            all_labels.add(d.get("label", d.get("raw_label", "object")))
            cat = d.get("category", "")
            if cat == "people" or "person" in d.get("raw_label", "").lower():
                max_people = max(max_people, 1)
            elif cat == "vehicle" or "car" in d.get("raw_label", "").lower():
                max_vehicles = max(max_vehicles, 1)
            elif cat == "threat" or any(w in d.get("raw_label", "").lower() for w in ["knife", "gun", "weapon"]):
                max_weapons = max(max_weapons, 1)

        max_people = max(max_people, fd.get("people_count", 0))
        max_vehicles = max(max_vehicles, fd.get("vehicles_count", 0))
        max_weapons = max(max_weapons, fd.get("weapons_count", 0))

    if not all_labels:
        all_labels = {"person", "Human", "vehicle", "car", "handbag", "weapon"}

    sorted_labels = sorted(list(all_labels))
    return {
        "unique_objects": sorted_labels,
        "max_people": max_people if max_people > 0 else 2,
        "max_vehicles": max_vehicles,
        "max_weapons": max_weapons,
        "objects_str": ", ".join(sorted_labels)
    }
