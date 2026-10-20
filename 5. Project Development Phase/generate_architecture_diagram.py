"""
CrimeVision AI - High-Resolution Architecture Diagram Generator
Generates a clean, modern, professional system architecture diagram image
for inclusion in the official SmartBridge documentation PDFs and repository.
"""

import os
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(BASE_DIR, "architecture_diagram.png")

def create_architecture_diagram():
    w, h = 1600, 1000
    img = Image.new("RGB", (w, h), color=(15, 23, 42)) # Deep Slate Dark (#0f172a)
    d = ImageDraw.Draw(img)

    # Header Banner
    d.rectangle([(0, 0), (w, 90)], fill=(30, 41, 59))
    d.line([(0, 90), (w, 90)], fill=(2, 132, 199), width=3) # Cyan line

    # Title
    d.text((50, 20), "CRIMEVISION AI - MULTIMODAL SYSTEM ARCHITECTURE", fill=(255, 255, 255))
    d.text((50, 52), "Intelligent Crime Scene Reconstruction, Whisper Audio, CCTV Timeline & Groq Reasoning", fill=(148, 163, 184))
    d.text((1280, 35), "DATE: 18 OCTOBER 2026", fill=(56, 189, 248))

    # Helper function for drawing rounded-style containers
    def draw_card(box, title, subtitle, bg_color, border_color, tag=""):
        x1, y1, x2, y2 = box
        d.rectangle([x1, y1, x2, y2], fill=bg_color, outline=border_color, width=2)
        # Card header bar
        d.rectangle([x1, y1, x2, y1 + 32], fill=(border_color[0]//2, border_color[1]//2, border_color[2]//2))
        d.text((x1 + 12, y1 + 8), title, fill=(255, 255, 255))
        if tag:
            d.rectangle([x2 - 80, y1 + 6, x2 - 10, y1 + 26], fill=(15, 23, 42))
            d.text((x2 - 74, y1 + 9), tag, fill=(56, 189, 248))
        if subtitle:
            # Multi-line text inside card
            lines = subtitle.split("\n")
            curr_y = y1 + 42
            for line in lines:
                d.text((x1 + 12, curr_y), line, fill=(203, 213, 225))
                curr_y += 18

    # -------------------------------------------------------------
    # LAYER 1: CLIENT PRESENTATION LAYER (Top)
    # -------------------------------------------------------------
    d.text((50, 110), "1. PRESENTATION & INTERACTIVE HUD LAYER (Browser SPA)", fill=(56, 189, 248))
    d.rectangle([(50, 135), (1550, 260)], fill=(24, 32, 47), outline=(51, 65, 85), width=2)

    draw_card((70, 150, 340, 245), "Three.js 3D Viewport", "• WebGL Spatial Canvas\n• OrbitControls & Camera\n• Evidence 3D Depth Cubes", (30, 41, 59), (14, 165, 233), "3D")
    draw_card((360, 150, 630, 245), "Evidence Upload Panel", "• Drag & Drop Zone\n• Multi-Format Validation\n• Benchmark Presets", (30, 41, 59), (99, 102, 241), "UI")
    draw_card((650, 150, 920, 245), "Acoustic & Translation HUD", "• HTML5 Audio Player\n• 36-Bar Waveform EQ\n• Whisper Speech Transcript\n• 4-Language Translation", (30, 41, 59), (168, 85, 247), "AUDIO")
    draw_card((940, 150, 1220, 245), "Surveillance & OpenCV HUD", "• OpenCV 2D Bounding Boxes\n• People / Vehicles / Weapons\n• 1.0 Hz Event Timeline Grid", (30, 41, 59), (236, 72, 153), "VIDEO")
    draw_card((1240, 150, 1530, 245), "Forensic AI Chatbot", "• Dual-Tier NLP Reasoner\n• One-Click Suggestion Chips\n• Temporal & Evidence Q&A", (30, 41, 59), (16, 185, 129), "CHAT")

    # Downward Connectors (Arrows)
    for cx in [205, 495, 785, 1080, 1385]:
        d.line([(cx, 260), (cx, 290)], fill=(56, 189, 248), width=3)
        d.polygon([(cx-5, 285), (cx+5, 285), (cx, 295)], fill=(56, 189, 248))

    # -------------------------------------------------------------
    # LAYER 2: RESTful API GATEWAY (Flask Blueprints)
    # -------------------------------------------------------------
    d.text((50, 305), "2. RESTful API GATEWAY & ROUTING LAYER (Flask Blueprints / CORS)", fill=(129, 140, 248))
    d.rectangle([(50, 330), (1550, 420)], fill=(24, 32, 47), outline=(51, 65, 85), width=2)

    draw_card((70, 345, 340, 405), "/api/process/image", "POST: multipart image / path", (30, 41, 59), (14, 165, 233))
    draw_card((360, 345, 630, 405), "/api/analyze-audio", "POST: audio/wav or /mp3", (30, 41, 59), (168, 85, 247))
    draw_card((650, 345, 920, 405), "/api/video/opencv-predict", "POST: OpenCV Video CV Engine", (30, 41, 59), (236, 72, 153))
    draw_card((940, 345, 1220, 405), "/api/process/complete", "POST: Unified multimodal fusion", (30, 41, 59), (245, 158, 11))
    draw_card((1240, 345, 1530, 405), "/api/chat & /api/reports", "POST: Grounded Chat | GET: PDF", (30, 41, 59), (16, 185, 129))

    for cx in [205, 495, 785, 1080, 1385]:
        d.line([(cx, 420), (cx, 450)], fill=(129, 140, 248), width=3)
        d.polygon([(cx-5, 445), (cx+5, 445), (cx, 455)], fill=(129, 140, 248))

    # -------------------------------------------------------------
    # LAYER 3: CORE AI FORENSIC INFERENCE SERVICES
    # -------------------------------------------------------------
    d.text((50, 465), "3. CORE AI FORENSIC INFERENCE & MULTIMODAL SERVICES", fill=(52, 211, 153))
    d.rectangle([(50, 490), (1550, 690)], fill=(24, 32, 47), outline=(51, 65, 85), width=2)

    draw_card((70, 510, 340, 670), "Vision Service", "• Model: PekingU/rtdetr_r50vd\n• Model: OpenAI CLIP ViT-B/32\n• Depth Map [X,Y,Z] Estimation\n• 2D Bounding Boxes & Confidence\n• Furniture / Weapon / Victim BBox\n• CV / Heuristic Fallback Engine", (30, 41, 59), (14, 165, 233), "VISION")
    draw_card((360, 510, 630, 670), "Audio Service", "• Model: OpenAI Whisper-Base\n• ASR Speech-to-Text Pipeline\n• Librosa Acoustic Energy\n• Forensic Crime Classification\n• Groq Multilingual Translation\n  (English, Hindi, Telugu, French)", (30, 41, 59), (168, 85, 247), "AUDIO")
    draw_card((650, 510, 920, 670), "OpenCV Video Service", "• OpenCV Computer Vision Engine\n• People & Suspect Bounding Boxes\n• Vehicle & Getaway Car Tracking\n• Weapon & Object Identification\n• 3D Spatial Trajectory Mapping\n• Carjack / ATM / Store Scoring", (30, 41, 59), (236, 72, 153), "OPENCV")
    draw_card((940, 510, 1220, 670), "Fusion Service", "• Cross-Modal Entity Resolver\n• Unified Second Timeline Clock\n• Consistency Checker (Audio vs Vid)\n• Spatial-Temporal Fact Correlator\n• Contradiction Detection\n• Master Forensic Case Record", (30, 41, 59), (245, 158, 11), "FUSION")
    draw_card((1240, 510, 1530, 670), "Dual-Tier Chat & PDF", "• Groq LLaMA-3.3-70B Cloud Model\n• Grounded Local Forensic Reasoner\n• One-Click Suggestion Chips\n• ReportLab Platypus Engine\n• XML Escape Sanitizer\n• SHA-256 Validated Court PDF", (30, 41, 59), (16, 185, 129), "CHAT/PDF")

    for cx in [205, 495, 785, 1080, 1385]:
        d.line([(cx, 690), (cx, 720)], fill=(52, 211, 153), width=3)
        d.polygon([(cx-5, 715), (cx+5, 715), (cx, 725)], fill=(52, 211, 153))

    # -------------------------------------------------------------
    # LAYER 4: DATA PERSISTENCE & VAULT STORAGE LAYER
    # -------------------------------------------------------------
    d.text((50, 735), "4. PERSISTENCE, EVIDENCE VAULT & MODEL CACHE", fill=(244, 114, 182))
    d.rectangle([(50, 760), (1550, 920)], fill=(24, 32, 47), outline=(51, 65, 85), width=2)

    draw_card((70, 780, 410, 895), "SessionStore (Dual-Tier)", "• In-Memory Fast Lookup Store\n• Disk Persistence: backend/data/sessions/\n• UUID-Keyed Forensic JSON Dossiers\n• Zero-loss on restart / reload", (30, 41, 59), (14, 165, 233), "SESSIONS")
    draw_card((440, 780, 780, 895), "Evidence Vault (/data/uploads)", "• /uploads/image/ (JPG, PNG)\n• /uploads/audio/ (WAV, MP3)\n• /uploads/video/ (MP4, AVI)\n• Read-only Evidence Custody", (30, 41, 59), (99, 102, 241), "UPLOADS")
    draw_card((810, 780, 1150, 895), "Court Reports Vault", "• backend/data/reports/\n• Courtroom-Admissible PDF Files\n• Cryptographic SHA-256 Signatures\n• Downloadable via /api/reports/<sid>", (30, 41, 59), (16, 185, 129), "REPORTS")
    draw_card((1180, 780, 1530, 895), "Local Model Hub Cache", "• ~/.cache/huggingface/hub/\n• Cached RT-DETR, CLIP, BLIP, Whisper\n• local_files_only=True instant load\n• Offline-capable architecture", (30, 41, 59), (245, 158, 11), "MODELS")

    # Bottom Footer
    d.line([(50, 950), (1550, 950)], fill=(71, 85, 105), width=1)
    d.text((50, 965), "CrimeVision AI Forensic Architecture  |  Author: Rahul Rajak (Rahul-DS633)  |  https://github.com/Rahul-DS633/Crime-Vision-AI", fill=(148, 163, 184))
    d.text((1300, 965), "SMARTBRIDGE / SKILLWALLET", fill=(56, 189, 248))

    img.save(OUTPUT_PATH, quality=95)
    print(f"[OK] Generated Architecture Diagram: {OUTPUT_PATH}")

if __name__ == "__main__":
    create_architecture_diagram()
