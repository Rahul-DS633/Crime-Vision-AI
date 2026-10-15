"""
Utility script to generate benchmark sample assets for CrimeVision AI:
1. sample_crime_scene.jpg (Office incident with victim, knife, tape, office furniture)
2. sample_robbery_witness.wav (Multilingual testimony audio)
3. sample_surveillance_store.mp4 (Surveillance footage with timestamps)
"""
import os
import cv2
import wave
import struct
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def generate_crime_scene_image(dest_path: str):
    width, height = 800, 600
    img = Image.new("RGB", (width, height), color=(40, 44, 52))
    draw = ImageDraw.Draw(img)

    # Room walls and floor perspective
    # Floor
    draw.polygon([(0, 280), (width, 280), (width, height), (0, height)], fill=(70, 75, 85))
    # Wall
    draw.polygon([(0, 0), (width, 0), (width, 280), (0, 280)], fill=(32, 36, 44))
    # Baseboard
    draw.rectangle([(0, 275), (width, 282)], fill=(20, 22, 26))

    # Office Furniture: Desk / Diningtable
    draw.rectangle([(500, 220), (760, 420)], fill=(90, 60, 40), outline=(120, 80, 50), width=3)
    # Chair
    draw.rectangle([(80, 210), (220, 390)], fill=(30, 40, 60), outline=(50, 70, 100), width=2)
    # Laptop on desk
    draw.rectangle([(550, 240), (660, 310)], fill=(180, 185, 190), outline=(220, 225, 230), width=2)
    draw.rectangle([(570, 250), (640, 290)], fill=(50, 90, 150))
    # Cup
    draw.ellipse([(680, 250), (710, 285)], fill=(220, 220, 220))

    # Sofa in background
    draw.rectangle([(40, 360), (240, 540)], fill=(55, 60, 70), outline=(80, 85, 95), width=2)

    # Victim lying on the floor (Human)
    # Torso
    draw.polygon([(300, 380), (460, 420), (440, 490), (280, 450)], fill=(45, 80, 140)) # Blue shirt
    # Legs (jeans)
    draw.polygon([(440, 430), (600, 450), (590, 490), (430, 480)], fill=(30, 50, 100))
    draw.polygon([(420, 470), (560, 540), (530, 560), (400, 500)], fill=(25, 45, 90))
    # Head
    draw.ellipse([(220, 380), (285, 440)], fill=(210, 165, 130))
    # Yellow Police Evidence Tape around area
    draw.line([(180, 350), (650, 370)], fill=(240, 210, 30), width=8)
    draw.line([(240, 460), (290, 480)], fill=(240, 210, 30), width=6) # Tape on floor/limbs

    # Weapon: Knife
    # Blade (metallic silver)
    draw.polygon([(480, 370), (540, 350), (535, 360)], fill=(220, 225, 235), outline=(255, 255, 255))
    # Handle
    draw.rectangle([(460, 372), (480, 382)], fill=(20, 20, 20))

    # Blood spatter / markings
    draw.ellipse([(470, 400), (510, 430)], fill=(140, 20, 20))
    draw.ellipse([(520, 390), (535, 405)], fill=(120, 15, 15))

    # Text marking / label overlay
    draw.text((20, 20), "CRIME SCENE RECONSTRUCTION - EVIDENCE FILE: SEC-OFFICE-09", fill=(200, 200, 200))

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    img.save(dest_path, quality=95)
    print(f"Generated crime scene image: {dest_path}")

def generate_witness_audio(dest_path: str, duration_sec: int = 5):
    """
    Generates a synthetic speech-frequency audio wave file.
    """
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    sample_rate = 16000
    n_samples = int(sample_rate * duration_sec)

    with wave.open(dest_path, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)

        # Generate harmonic speech-formant modulated audio
        data = bytearray()
        for i in range(n_samples):
            t = float(i) / sample_rate
            # Syllabic envelope modulation (approx 3Hz voice cadences)
            envelope = 0.5 + 0.5 * math.sin(2.0 * math.pi * 3.0 * t)
            # Formant carrier frequencies
            sample_val = envelope * (
                0.5 * math.sin(2.0 * math.pi * 220.0 * t) +
                0.3 * math.sin(2.0 * math.pi * 440.0 * t) +
                0.2 * math.sin(2.0 * math.pi * 880.0 * t)
            )
            val = int(sample_val * 16000)
            data.extend(struct.pack('<h', max(-32767, min(32767, val))))

        wav.writeframes(data)
    print(f"Generated witness testimony audio: {dest_path}")

def generate_surveillance_video(dest_path: str, duration_sec: int = 15):
    """
    Generates synthetic 15-second surveillance video with 1Hz timestamp stamps matching benchmark.
    """
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    width, height = 640, 480
    fps = 10
    total_frames = duration_sec * fps
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(dest_path, fourcc, fps, (width, height))

    for f_idx in range(total_frames):
        sec = f_idx // fps
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Background: Store interior with refrigerators
        # Floor (tiles)
        frame[180:, :] = (55, 60, 65)
        # Wall
        frame[:180, :] = (35, 38, 42)

        # Refrigerator units (Left and Right aisles)
        cv2.rectangle(frame, (30, 80), (180, 440), (120, 130, 140), -1)
        cv2.rectangle(frame, (40, 100), (170, 240), (190, 210, 225), -1)
        cv2.rectangle(frame, (40, 260), (170, 420), (190, 210, 225), -1)

        cv2.rectangle(frame, (480, 80), (620, 440), (120, 130, 140), -1)
        cv2.rectangle(frame, (490, 100), (610, 240), (190, 210, 225), -1)
        cv2.rectangle(frame, (490, 260), (610, 420), (190, 210, 225), -1)

        # Moving person 1 (walking across aisle)
        p1_x = int(220 + (sec * 12) % 180)
        p1_y = 300
        # Head
        cv2.circle(frame, (p1_x, p1_y - 80), 20, (180, 150, 120), -1)
        # Torso
        cv2.rectangle(frame, (p1_x - 18, p1_y - 60), (p1_x + 18, p1_y + 20), (40, 90, 160), -1)
        # Handbag
        cv2.rectangle(frame, (p1_x + 18, p1_y - 10), (p1_x + 36, p1_y + 15), (30, 30, 30), -1)
        # Legs
        cv2.rectangle(frame, (p1_x - 15, p1_y + 20), (p1_x + 15, p1_y + 90), (30, 40, 50), -1)

        # Person 2 (shopper browsing shelves)
        p2_x = 420
        p2_y = 280
        cv2.circle(frame, (p2_x, p2_y - 75), 18, (190, 160, 130), -1)
        cv2.rectangle(frame, (p2_x - 15, p2_y - 55), (p2_x + 15, p2_y + 15), (140, 60, 60), -1)
        # Backpack
        cv2.rectangle(frame, (p2_x - 30, p2_y - 45), (p2_x - 15, p2_y), (40, 40, 40), -1)

        # Surveillance CCTV HUD overlay
        cv2.putText(frame, f"CAM-04 MALL STORE AISLE 2", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"TIME: 00:{sec:02d} / 00:{duration_sec:02d}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, "REC [LIVE]", (520, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        out.write(frame)

    out.release()
    print(f"Generated surveillance video: {dest_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(base_dir, "data", "uploads", "image", "sample_crime_scene.jpg")
    audio_path = os.path.join(base_dir, "data", "uploads", "audio", "sample_robbery_witness.wav")
    video_path = os.path.join(base_dir, "data", "uploads", "video", "sample_surveillance_store.mp4")

    generate_crime_scene_image(img_path)
    generate_witness_audio(audio_path)
    generate_surveillance_video(video_path)
