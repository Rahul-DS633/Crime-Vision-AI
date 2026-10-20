"""
CrimeVision AI - External Data Automated Test Harness
Executes multimodal forensic analysis on external files or benchmark datasets.

Usage:
  python backend/test_external_data.py --image "path/to/image.jpg"
  python backend/test_external_data.py --audio "path/to/audio.wav"
  python backend/test_external_data.py --video "path/to/video.mp4"
  python backend/test_external_data.py --all
"""

import os
import sys
import argparse

# Deep Environment Fix for Protobuf / TensorFlow
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
os.environ['USE_TF'] = 'NO'
os.environ['USE_TORCH'] = 'YES'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from services.vision_service import vision_service
from services.audio_service import audio_service
from services.video_service import video_service
from services.fusion_service import fusion_service
from services.session_store import session_store
from services.pdf_service import generate_forensic_pdf
from utils.logger import setup_logger

logger = setup_logger("test_external")

def test_image(image_path: str):
    print("\n" + "="*60)
    print(f"[IMAGE FORENSIC TEST] Analyzing: {image_path}")
    print("="*60)
    if not os.path.exists(image_path):
        print(f"[ERROR] File not found: {image_path}")
        return None

    res = vision_service.analyze_image(image_path)
    session_id = session_store.create_session(res)
    pdf_path = generate_forensic_pdf(session_id, res)

    print(f"[*] Session ID: {session_id}")
    print(f"[*] Visual Summary: {res.get('visual_summary', 'N/A')}")
    print(f"[*] Identified Objects ({res.get('objects_count', 0)} total):")
    for det in res.get('detections', [])[:5]:
        pos = det.get('position_3d', {})
        print(f"    - {det.get('label')} (conf: {det.get('confidence'):.2f}) at 3D [X:{pos.get('x')}, Y:{pos.get('y')}, Z:{pos.get('z')}]")
    print(f"[*] Forensic Scenarios:")
    for sc in res.get('scenarios', []):
        print(f"    • {sc}")
    print(f"[+] Forensic PDF Report: {pdf_path}")
    return res

def test_audio(audio_path: str):
    print("\n" + "="*60)
    print(f"[AUDIO FORENSIC TEST] Analyzing: {audio_path}")
    print("="*60)
    if not os.path.exists(audio_path):
        print(f"[ERROR] File not found: {audio_path}")
        return None

    res = audio_service.process_audio(audio_path)
    session_id = session_store.create_session(res)
    pdf_path = generate_forensic_pdf(session_id, res)

    print(f"[*] Session ID: {session_id}")
    print(f"[*] Transcription: {res.get('transcription', 'N/A')}")
    print(f"[*] Classified Crime Type: {res.get('crime_type', 'N/A')}")
    print(f"[*] AI Summary: {res.get('summary', 'N/A')}")
    print(f"[*] Chronological Events ({len(res.get('timeline', []))} events):")
    for ev in res.get('timeline', [])[:4]:
        print(f"    [{ev.get('time')}] {ev.get('event')}")
    print(f"[+] Forensic PDF Report: {pdf_path}")
    return res

def test_video(video_path: str):
    print("\n" + "="*60)
    print(f"[VIDEO FORENSIC TEST] Analyzing: {video_path}")
    print("="*60)
    if not os.path.exists(video_path):
        print(f"[ERROR] File not found: {video_path}")
        return None

    res = video_service.process_video(video_path)
    session_id = session_store.create_session(res)
    pdf_path = generate_forensic_pdf(session_id, res)

    classification = res.get('crime_classification', {})
    print(f"[*] Session ID: {session_id}")
    print(f"[*] Surveillance Alert: {classification.get('badge', 'NORMAL')}")
    print(f"[*] Reason: {classification.get('reason', 'N/A')}")
    print(f"[*] Scene Intelligence: {res.get('scene_intelligence', {})}")
    print(f"[*] Frame-by-Frame Timeline ({len(res.get('timeline', []))} keypoints):")
    for ev in res.get('timeline', [])[:4]:
        print(f"    [{ev.get('time')}] {ev.get('event')}")
    print(f"[+] Forensic PDF Report: {pdf_path}")
    return res

def test_all_external():
    ext_dir = os.path.join(current_dir, "data", "external_samples")
    if not os.path.exists(ext_dir):
        print("[*] Generating external dataset first...")
        from generate_external_dataset import (
            generate_jewelry_store_image,
            generate_distress_call_audio,
            generate_atm_assault_video
        )
        generate_jewelry_store_image()
        generate_distress_call_audio()
        generate_atm_assault_video()

    img_case = os.path.join(ext_dir, "image", "case01_jewelry_store_robbery.jpg")
    audio_case = os.path.join(ext_dir, "audio", "case01_distress_call_911.wav")
    video_case = os.path.join(ext_dir, "video", "case01_bank_atm_assault.mp4")

    print("\n" + "#"*60)
    print("# RUNNING COMPLETE EXTERNAL DATASET FORENSIC SUITE")
    print("#"*60)

    test_image(img_case)
    test_audio(audio_case)
    test_video(video_case)

    print("\n" + "="*60)
    print("[SUCCESS] All external multimodal test cases processed!")
    print("="*60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CrimeVision AI - External Data Test Harness")
    parser.add_argument("--image", type=str, help="Path to external image file")
    parser.add_argument("--audio", type=str, help="Path to external audio file")
    parser.add_argument("--video", type=str, help="Path to external video file")
    parser.add_argument("--all", action="store_true", help="Run benchmark suite on all external samples")

    args = parser.parse_args()

    if args.image:
        test_image(args.image)
    elif args.audio:
        test_audio(args.audio)
    elif args.video:
        test_video(args.video)
    elif args.all or len(sys.argv) == 1:
        test_all_external()
