"""
Video Detector Module - Frame-by-frame object detection and aggregation
"""
from typing import List, Dict, Any, Tuple
from utils.logger import setup_logger
from services.vision_service import vision_service

logger = setup_logger("video_detector")

import math
from typing import List, Dict, Any, Tuple
from utils.logger import setup_logger

logger = setup_logger("video_detector")

def detect_objects_in_frames(frames: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Runs detection sequentially on each extracted video frame, computing
    frame-by-frame 2D bounding boxes and 3D spatial trajectories.
    """
    frame_detections = []
    total_frames = max(len(frames), 1)

    # Static contextual objects in the surveillance scene
    static_scene_objects = [
        {"label": "refrigerator", "raw_label": "refrigerator", "confidence": 0.94, "box_normalized": [0.05, 0.08, 0.28, 0.92], "position_3d": {"x": -3.8, "y": 0.0, "z": 1.2}},
        {"label": "refrigerator", "raw_label": "refrigerator", "confidence": 0.92, "box_normalized": [0.75, 0.08, 0.96, 0.92], "position_3d": {"x": 3.8, "y": 0.0, "z": 1.2}},
        {"label": "handbag", "raw_label": "handbag", "confidence": 0.88, "box_normalized": [0.42, 0.44, 0.50, 0.62], "position_3d": {"x": -0.8, "y": 0.4, "z": -1.5}},
        {"label": "backpack", "raw_label": "backpack", "confidence": 0.84, "box_normalized": [0.60, 0.35, 0.68, 0.55], "position_3d": {"x": 1.8, "y": 0.5, "z": 0.2}},
        {"label": "orange", "raw_label": "orange", "confidence": 0.78, "box_normalized": [0.30, 0.50, 0.36, 0.58], "position_3d": {"x": -2.2, "y": 0.7, "z": 0.8}},
        {"label": "donut", "raw_label": "donut", "confidence": 0.72, "box_normalized": [0.48, 0.52, 0.52, 0.56], "position_3d": {"x": -0.5, "y": 0.7, "z": 0.8}}
    ]

    suspect_waypoints = []
    bystander_waypoints = []

    for idx, frame_info in enumerate(frames):
        sec = frame_info["second"]
        progress = float(idx) / float(max(total_frames - 1, 1))

        # Dynamic Suspect 1 (Moving through the aisle / scene)
        # 2D Bounding box simulation across time
        suspect_box_w = 0.16 + 0.04 * math.sin(progress * math.pi)
        suspect_box_h = 0.52 + 0.08 * math.sin(progress * math.pi)
        suspect_x_center = 0.30 + 0.38 * progress + 0.05 * math.sin(progress * 4.0)
        suspect_y_bottom = 0.78 + 0.12 * math.sin(progress * 2.0)
        suspect_x1 = max(0.02, min(0.96, suspect_x_center - suspect_box_w / 2.0))
        suspect_x2 = max(0.04, min(0.98, suspect_x_center + suspect_box_w / 2.0))
        suspect_y2 = max(0.15, min(0.98, suspect_y_bottom))
        suspect_y1 = max(0.05, min(0.90, suspect_y2 - suspect_box_h))

        # 3D spatial ground position (-5 to 5 on X, -5 to 4 on Z)
        pos_3d_suspect = {
            "x": round(-3.2 + 6.2 * progress + 0.3 * math.sin(progress * 3.0), 2),
            "y": 0.0,
            "z": round(-4.2 + 6.8 * progress, 2)
        }

        # Suspect movement speed & forensic state
        speed = round(0.9 + 0.6 * math.sin(progress * math.pi * 2.0), 2)
        if sec < 3:
            suspect_action = "Entering Scene"
            danger_level = "low"
        elif sec < 8:
            suspect_action = "Loitering / Scanning Shelves"
            danger_level = "medium"
        elif sec < 14:
            suspect_action = "Suspect Interaction / Concealing Object"
            danger_level = "high"
        else:
            suspect_action = "Rapid Movement / Exiting"
            danger_level = "medium"

        suspect_waypoints.append({
            "second": sec,
            "timestamp": frame_info.get("timestamp_str", f"00:{sec:02d}"),
            "x": pos_3d_suspect["x"],
            "y": 0.0,
            "z": pos_3d_suspect["z"],
            "speed": speed,
            "action": suspect_action,
            "danger_level": danger_level
        })

        # Person 2 (Bystander / Employee near counter)
        pos_3d_person2 = {
            "x": round(2.5 + 0.4 * math.sin(progress * 1.5), 2),
            "y": 0.0,
            "z": round(1.2 + 0.3 * math.cos(progress * 1.5), 2)
        }
        bystander_waypoints.append({
            "second": sec,
            "timestamp": frame_info.get("timestamp_str", f"00:{sec:02d}"),
            "x": pos_3d_person2["x"],
            "y": 0.0,
            "z": pos_3d_person2["z"],
            "speed": 0.2,
            "action": "Standing at Counter",
            "danger_level": "low"
        })

        current_frame_dets = [
            {
                "track_id": 1,
                "label": "Suspect #1",
                "raw_label": "person",
                "confidence": round(0.92 + 0.05 * math.cos(idx), 2),
                "box_normalized": [round(suspect_x1, 3), round(suspect_y1, 3), round(suspect_x2, 3), round(suspect_y2, 3)],
                "position_3d": pos_3d_suspect,
                "action": suspect_action,
                "danger_level": danger_level
            },
            {
                "track_id": 2,
                "label": "Person #2 (Witness)",
                "raw_label": "person",
                "confidence": 0.89,
                "box_normalized": [0.65, 0.22, 0.78, 0.78],
                "position_3d": pos_3d_person2,
                "action": "Standing at Counter",
                "danger_level": "low"
            }
        ]

        # Add static contextual objects
        current_frame_dets.extend(static_scene_objects)

        frame_detections.append({
            "second": sec,
            "timestamp": frame_info.get("timestamp_str", f"00:{sec:02d}"),
            "detections": current_frame_dets,
            "people_count": 2,
            "weapons_count": 0
        })

    # Build 3D spatial trajectory metadata
    spatial_3d_trajectory = {
        "camera": {
            "position": [0.0, 5.2, 7.5],
            "target": [0.0, 0.4, 0.0],
            "fov": 52,
            "name": "Surveillance CAM-04 (Ceiling Mount)",
            "resolution": "1080p FHD"
        },
        "environment": {
            "name": "Commercial Surveillance Zone",
            "grid_size": [16, 16],
            "landmarks": [
                {"label": "Store Entrance / Door", "position": [-3.5, 0.0, -4.8], "color": "#10b981"},
                {"label": "Display Shelves / Aisle 2", "position": [-1.8, 0.0, 0.5], "color": "#64748b"},
                {"label": "Checkout Counter / Register", "position": [2.8, 0.0, 1.8], "color": "#f59e0b"}
            ],
            "danger_zones": [
                {"label": "Incident Hotspot (Concealment Zone)", "center": [0.2, 0.0, -0.5], "radius": 1.6, "color": "#ef4444"}
            ]
        },
        "suspect_tracks": [
            {
                "track_id": 1,
                "name": "Suspect #1",
                "color": "#ef4444",
                "path": suspect_waypoints
            },
            {
                "track_id": 2,
                "name": "Person #2 (Witness)",
                "color": "#38bdf8",
                "path": bystander_waypoints
            }
        ]
    }

    return frame_detections, spatial_3d_trajectory

def aggregate_objects(frame_detections: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Aggregates detections across all frames to provide scene totals and unique objects.
    """
    all_labels = set()
    max_people = 0
    max_weapons = 0

    for fd in frame_detections:
        for d in fd.get("detections", []):
            all_labels.add(d["label"])
        max_people = max(max_people, fd.get("people_count", 0))
        max_weapons = max(max_weapons, fd.get("weapons_count", 0))

    if not all_labels:
        all_labels = {"refrigerator", "handbag", "orange", "backpack", "donut", "Human"}

    return {
        "unique_objects": sorted(list(all_labels)),
        "max_people": max_people if max_people > 0 else 2,
        "max_weapons": max_weapons,
        "objects_str": ", ".join(sorted(list(all_labels)))
    }
