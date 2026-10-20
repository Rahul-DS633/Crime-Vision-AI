"""
CrimeVision AI - External Dataset Generator
Generates realistic multimodal external test cases across images, audio, and video:
1. Images:
   - case01_jewelry_store_robbery.jpg
   - case02_bank_vault_heist.jpg
   - case03_street_confrontation.jpg
2. Audio:
   - case01_distress_call_911.wav
   - case02_gunfire_and_sirens.wav
   - case03_break_in_alarm.wav
3. Video:
   - case01_bank_atm_assault.mp4
   - case02_parking_lot_carjack.mp4
"""

import os
import math
import wave
import struct
import cv2
import numpy as np
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXTERNAL_DIR = os.path.join(BASE_DIR, "data", "external_samples")
IMG_DIR = os.path.join(EXTERNAL_DIR, "image")
AUDIO_DIR = os.path.join(EXTERNAL_DIR, "audio")
VIDEO_DIR = os.path.join(EXTERNAL_DIR, "video")

os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. External Image Test Cases
# -------------------------------------------------------------

def generate_jewelry_store_image():
    path = os.path.join(IMG_DIR, "case01_jewelry_store_robbery.jpg")
    w, h = 800, 600
    img = Image.new("RGB", (w, h), color=(25, 30, 40))
    d = ImageDraw.Draw(img)

    # Floor & walls
    d.polygon([(0, 260), (w, 260), (w, h), (0, h)], fill=(45, 50, 60))
    d.polygon([(0, 0), (w, 0), (w, 260), (0, 260)], fill=(20, 25, 35))

    # Glass display counters (shattered)
    d.rectangle([(80, 280), (320, 480)], fill=(70, 90, 110), outline=(130, 160, 200), width=3)
    d.rectangle([(480, 280), (720, 480)], fill=(70, 90, 110), outline=(130, 160, 200), width=3)

    # Broken glass shards
    for (x1, y1, x2, y2) in [(120, 310, 160, 340), (220, 290, 270, 330), (520, 330, 580, 370)]:
        d.polygon([(x1, y1), (x2, y1), (x2-15, y2), (x1+10, y2)], fill=(210, 230, 255))

    # Robber / Intruder (masked with bag)
    d.ellipse([(370, 220), (430, 280)], fill=(30, 30, 35))  # Masked head
    d.rectangle([(360, 280), (440, 440)], fill=(25, 35, 60)) # Dark jacket
    d.rectangle([(430, 330), (470, 410)], fill=(110, 80, 40)) # Loot duffle bag
    d.rectangle([(370, 440), (400, 540)], fill=(20, 25, 30)) # Left leg
    d.rectangle([(405, 440), (435, 540)], fill=(20, 25, 30)) # Right leg

    # Weapon: Handgun/pistol in hand
    d.rectangle([(340, 330), (365, 345)], fill=(15, 15, 15))
    d.rectangle([(330, 330), (345, 360)], fill=(15, 15, 15))

    # Dropped necklace / jewelry
    d.arc([(260, 490), (310, 520)], start=0, end=180, fill=(240, 215, 60), width=4)

    # Surveillance timestamp HUD
    d.text((20, 20), "EXTERNAL CCTV REC [SEC-STORE-CAM01] 20:14:52 - INCIDENT: ROBBERY", fill=(0, 255, 150))
    img.save(path, quality=95)
    print(f"[OK] Generated {path}")

def generate_bank_vault_image():
    path = os.path.join(IMG_DIR, "case02_bank_vault_heist.jpg")
    w, h = 800, 600
    img = Image.new("RGB", (w, h), color=(35, 38, 45))
    d = ImageDraw.Draw(img)

    # Metallic vault wall
    d.rectangle([(0, 0), (w, 320)], fill=(50, 55, 65))
    d.rectangle([(0, 320), (w, h)], fill=(75, 80, 90))

    # Large Circular Safe Door (cracked open)
    d.ellipse([(450, 100), (750, 400)], fill=(100, 110, 125), outline=(180, 190, 210), width=6)
    d.ellipse([(550, 200), (650, 300)], fill=(70, 75, 85), outline=(220, 230, 240), width=4)

    # Intruder with crowbar tool
    d.ellipse([(220, 260), (280, 320)], fill=(40, 40, 40))
    d.rectangle([(210, 320), (290, 470)], fill=(40, 60, 50))
    d.rectangle([(220, 470), (250, 570)], fill=(20, 20, 25))
    d.rectangle([(255, 470), (285, 570)], fill=(20, 20, 25))

    # Tool (Crowbar / breaker)
    d.line([(290, 350), (370, 410)], fill=(200, 70, 50), width=6)

    # Cash stacks / evidence boxes on floor
    d.rectangle([(320, 490), (410, 550)], fill=(80, 140, 80), outline=(40, 100, 40), width=2)
    d.rectangle([(330, 470), (400, 500)], fill=(80, 140, 80), outline=(40, 100, 40), width=2)

    d.text((20, 20), "EXTERNAL CCTV REC [SEC-VAULT-04] 02:44:11 - INCIDENT: UNAUTHORIZED INTRUSION", fill=(255, 200, 0))
    img.save(path, quality=95)
    print(f"[OK] Generated {path}")

def generate_street_confrontation_image():
    path = os.path.join(IMG_DIR, "case03_street_confrontation.jpg")
    w, h = 800, 600
    img = Image.new("RGB", (w, h), color=(20, 22, 28))
    d = ImageDraw.Draw(img)

    # Dark street asphalt & pavement
    d.rectangle([(0, 280), (w, h)], fill=(40, 42, 48))
    d.rectangle([(0, 200), (w, 280)], fill=(70, 72, 80)) # Sidewalk
    d.line([(0, 450), (w, 450)], fill=(220, 200, 40), width=6) # Yellow street stripe

    # Dark getaway vehicle (car) parked at curb
    d.rectangle([(420, 210), (740, 380)], fill=(25, 30, 45), outline=(50, 60, 80), width=3)
    d.ellipse([(460, 350), (520, 410)], fill=(15, 15, 15)) # Tire 1
    d.ellipse([(640, 350), (700, 410)], fill=(15, 15, 15)) # Tire 2

    # Victim lying down on sidewalk
    d.polygon([(140, 290), (280, 320), (270, 360), (130, 330)], fill=(110, 40, 40)) # Maroon shirt
    d.ellipse([(90, 290), (135, 335)], fill=(200, 160, 130)) # Head
    d.polygon([(270, 330), (370, 340), (360, 375), (265, 360)], fill=(30, 40, 60)) # Jeans

    # Weapon: Dropped knife with metallic glare
    d.polygon([(260, 390), (310, 380), (305, 395)], fill=(230, 235, 245), outline=(255, 255, 255))
    d.rectangle([(245, 392), (260, 400)], fill=(30, 30, 30))

    # Police tape on scene
    d.line([(40, 250), (450, 290)], fill=(240, 220, 30), width=7)

    d.text((20, 20), "EXTERNAL TRAFFIC CAMERA [STREET-CAM-9B] 23:18:04 - INCIDENT: ASSAULT", fill=(255, 80, 80))
    img.save(path, quality=95)
    print(f"[OK] Generated {path}")


# -------------------------------------------------------------
# 2. External Audio Test Cases
# -------------------------------------------------------------

def generate_distress_call_audio():
    path = os.path.join(AUDIO_DIR, "case01_distress_call_911.wav")
    sr = 16000
    duration = 6
    n = int(sr * duration)

    with wave.open(path, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sr)

        raw = bytearray()
        for i in range(n):
            t = float(i) / sr
            # Speech formant modulation with agitated vocal cadence (approx 4Hz burst)
            burst = 0.5 + 0.5 * math.sin(2.0 * math.pi * 4.0 * t)
            carrier = (
                0.4 * math.sin(2.0 * math.pi * 320.0 * t) +
                0.3 * math.sin(2.0 * math.pi * 640.0 * t) +
                0.2 * math.sin(2.0 * math.pi * 1280.0 * t)
            )
            # Background noise / telephone filter
            noise = ((i * 1103515245 + 12345) & 0x7FFF) / 32768.0 - 0.5
            sample = (burst * carrier * 0.8) + (noise * 0.08)
            val = int(max(-1.0, min(1.0, sample)) * 24000)
            raw.extend(struct.pack('<h', val))

        wav.writeframes(raw)
    print(f"[OK] Generated {path}")

def generate_gunfire_and_sirens_audio():
    path = os.path.join(AUDIO_DIR, "case02_gunfire_and_sirens.wav")
    sr = 16000
    duration = 7
    n = int(sr * duration)

    with wave.open(path, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sr)

        raw = bytearray()
        for i in range(n):
            t = float(i) / sr
            sample = 0.0

            # Gunshots at t=1.0s, 1.8s, 2.4s (rapid explosive decaying blast)
            for shot_t in [1.0, 1.8, 2.4]:
                if 0 <= (t - shot_t) < 0.35:
                    dt = t - shot_t
                    decay = math.exp(-dt * 18.0)
                    sample += decay * math.sin(2.0 * math.pi * 90.0 * dt) * 1.5

            # Police siren sweeps in starting at t=3.0s (wailing 600Hz -> 1100Hz)
            if t > 3.0:
                siren_freq = 800.0 + 300.0 * math.sin(2.0 * math.pi * 0.6 * (t - 3.0))
                siren_gain = min(1.0, (t - 3.0) * 0.5)
                sample += siren_gain * 0.35 * math.sin(2.0 * math.pi * siren_freq * t)

            val = int(max(-1.0, min(1.0, sample)) * 28000)
            raw.extend(struct.pack('<h', val))

        wav.writeframes(raw)
    print(f"[OK] Generated {path}")

def generate_break_in_alarm_audio():
    path = os.path.join(AUDIO_DIR, "case03_break_in_alarm.wav")
    sr = 16000
    duration = 5
    n = int(sr * duration)

    with wave.open(path, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sr)

        raw = bytearray()
        for i in range(n):
            t = float(i) / sr
            # Rapid high-pitch intrusion alarm pulsed at 5Hz
            pulse = 1.0 if (int(t * 5.0) % 2 == 0) else 0.1
            alarm = 0.4 * math.sin(2.0 * math.pi * 1850.0 * t) + 0.2 * math.sin(2.0 * math.pi * 3700.0 * t)
            sample = pulse * alarm
            val = int(max(-1.0, min(1.0, sample)) * 22000)
            raw.extend(struct.pack('<h', val))

        wav.writeframes(raw)
    print(f"[OK] Generated {path}")


# -------------------------------------------------------------
# 3. External Video Test Cases
# -------------------------------------------------------------

def generate_atm_assault_video():
    path = os.path.join(VIDEO_DIR, "case01_bank_atm_assault.mp4")
    w, h = 640, 480
    fps = 10
    duration = 10
    total_frames = fps * duration

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(path, fourcc, fps, (w, h))

    for f in range(total_frames):
        sec = f // fps
        frame = np.zeros((h, w, 3), dtype=np.uint8)

        # ATM vestibule (glass walls, floor)
        frame[160:, :] = (45, 48, 55) # Floor
        frame[:160, :] = (25, 28, 35) # Dark glass wall

        # ATM machine unit (bright blue/grey screen)
        cv2.rectangle(frame, (80, 100), (220, 420), (100, 110, 120), -1)
        cv2.rectangle(frame, (100, 130), (200, 210), (20, 140, 220), -1) # ATM screen
        cv2.rectangle(frame, (110, 240), (190, 280), (40, 40, 40), -1)  # Keypad

        # Victim at ATM (Seconds 0-4)
        vic_x = 260
        vic_y = 300
        cv2.circle(frame, (vic_x, vic_y - 80), 20, (190, 160, 130), -1)
        cv2.rectangle(frame, (vic_x - 18, vic_y - 60), (vic_x + 18, vic_y + 30), (50, 120, 80), -1)
        cv2.rectangle(frame, (vic_x - 15, vic_y + 30), (vic_x + 15, vic_y + 110), (30, 40, 50), -1)

        # Aggressor approaching from right (enters at sec >= 2)
        if sec >= 2:
            agg_x = int(600 - (sec - 2) * 55)
            agg_x = max(310, agg_x)
            agg_y = 300
            # Hooded aggressor
            cv2.circle(frame, (agg_x, agg_y - 82), 22, (20, 20, 20), -1) # Black hood
            cv2.circle(frame, (agg_x - 4, agg_y - 80), 14, (180, 140, 110), -1) # Face
            cv2.rectangle(frame, (agg_x - 20, agg_y - 60), (agg_x + 20, agg_y + 30), (25, 30, 40), -1)
            cv2.rectangle(frame, (agg_x - 16, agg_y + 30), (agg_x + 16, agg_y + 110), (20, 20, 20), -1)
            # Weapon drawn
            if sec >= 4:
                cv2.rectangle(frame, (agg_x - 35, agg_y - 20), (agg_x - 18, agg_y - 10), (10, 10, 10), -1)

        # CCTV timestamp HUD
        cv2.putText(frame, f"CAM-ATM-02 [NIGHT VISION]", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 120), 2)
        cv2.putText(frame, f"2026-10-20 01:23:{sec:02d}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 120), 2)
        cv2.putText(frame, "INCIDENT ALERT: CLOSE PROXIMITY BREACH", (20, h - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        out.write(frame)

    out.release()
    print(f"[OK] Generated {path}")

def generate_carjack_video():
    path = os.path.join(VIDEO_DIR, "case02_parking_lot_carjack.mp4")
    w, h = 640, 480
    fps = 10
    duration = 10
    total_frames = fps * duration

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(path, fourcc, fps, (w, h))

    for f in range(total_frames):
        sec = f // fps
        frame = np.zeros((h, w, 3), dtype=np.uint8)

        # Parking lot asphalt & lines
        frame[140:, :] = (40, 44, 50)
        frame[:140, :] = (20, 22, 26)
        cv2.line(frame, (100, 140), (40, h), (200, 200, 200), 3) # Parking stall
        cv2.line(frame, (350, 140), (290, h), (200, 200, 200), 3)
        cv2.line(frame, (600, 140), (540, h), (200, 200, 200), 3)

        # Parked Car
        car_x = 140
        car_y = 240
        cv2.rectangle(frame, (car_x, car_y), (car_x + 150, car_y + 110), (70, 30, 30), -1)
        cv2.circle(frame, (car_x + 30, car_y + 110), 18, (15, 15, 15), -1)
        cv2.circle(frame, (car_x + 120, car_y + 110), 18, (15, 15, 15), -1)

        # Suspect running towards vehicle (Seconds 0-8)
        p_x = int(550 - sec * 35)
        p_y = 290
        cv2.circle(frame, (p_x, p_y - 65), 16, (190, 150, 120), -1)
        cv2.rectangle(frame, (p_x - 14, p_y - 50), (p_x + 14, p_y + 20), (35, 45, 80), -1)
        cv2.rectangle(frame, (p_x - 12, p_y + 20), (p_x + 12, p_y + 80), (25, 25, 30), -1)

        # CCTV timestamp HUD
        cv2.putText(frame, f"CAM-PARKING-NORTH [REC]", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"TIMESTAMP: 2026-10-20 22:50:{sec:02d}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        out.write(frame)

    out.release()
    print(f"[OK] Generated {path}")

if __name__ == "__main__":
    print("Generating comprehensive external test cases for CrimeVision AI...")
    generate_jewelry_store_image()
    generate_bank_vault_image()
    generate_street_confrontation_image()

    generate_distress_call_audio()
    generate_gunfire_and_sirens_audio()
    generate_break_in_alarm_audio()

    generate_atm_assault_video()
    generate_carjack_video()
    print("All external test cases generated successfully in data/external_samples/")
