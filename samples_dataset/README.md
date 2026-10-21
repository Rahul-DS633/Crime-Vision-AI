# CrimeVision AI - Forensic Sample Dataset Library

This directory contains all **14 clean external sample files** organized by media type for immediate forensic analysis, evaluation, and demonstration.

---

## Directory Structure

```
samples_dataset/
├── video/                              # 7 Surveillance CCTV Video Files
│   ├── real_cctv_surveillance_store.mp4    # Real Mall Store CCTV (65s, 9.2MB) - Retail Shoplifting
│   ├── real_intersection_surveillance.mp4 # Real City Intersection (54s, 6.0MB) - Traffic Tracking
│   ├── armed_robbery_cctv.mp4             # Commercial Register CCTV (28s, 768KB) - Armed Threat
│   ├── shoplifting_store_cctv.mp4         # Merchandise Aisle CCTV (42s, 2.3MB) - Item Concealment
│   ├── case01_bank_atm_assault.mp4        # Bank Exterior CCTV (18s, 210KB) - ATM Assault & Robbery
│   ├── case02_parking_lot_carjack.mp4     # Parking Facility CCTV (22s, 255KB) - Armed Carjacking
│   └── sample_surveillance_store.mp4      # Standard Benchmark Feed (15s, 38KB) - OpenCV Baseline
│
├── audio/                              # 5 Acoustic & Witness Audio Recordings
│   ├── case01_distress_call_911.wav       # 911 Emergency Dispatch Audio (12s, 192KB) - Acoustic Distress
│   ├── case02_gunfire_and_sirens.wav      # Gunfire Discharges & Sirens (14s, 224KB) - Ballistic Audio
│   ├── case03_break_in_alarm.wav          # Facility Intrusion Siren (10s, 160KB) - Break-in Alarm
│   ├── sample_robbery_witness.wav         # Full Witness Testimony (25s, 160KB) - Multilingual Whisper
│   └── sample_robbery_witness.mp3         # Compressed Witness Audio (25s, 82KB) - Bandwidth Test
│
└── image/                              # 2 High-Resolution Crime Scene Photos
    ├── real_street_traffic_surveillance.jpg # Urban Traffic & Pedestrian Scene (1920x1080, 487KB)
    └── sample_crime_scene.jpg               # Indoor Crime Scene Evidence Photo (1280x720, 35KB)
```

---

## How to Select & Process Samples

### Option 1: Directly in the Web Dashboard (Recommended)
1. Open the CrimeVision AI platform on Vercel:
   `https://crime-vision-ai-frontend.vercel.app`
2. Click the **"Sample Dataset Library (14 Cases)"** button on the left sidebar.
3. Browse between **Video CCTV**, **911 Audio**, and **Crime Images** tabs.
4. Click **"Load & Process Evidence"** on any case card — the system will automatically switch mode, load the media into the viewer, and trigger full AI forensic analysis.

### Option 2: Drag-and-Drop from this Folder
1. Drag any file from `samples_dataset/video/`, `samples_dataset/audio/`, or `samples_dataset/image/` directly into the web application's upload zone.
2. The platform automatically detects the file type (video/audio/image), switches to the matching mode, and processes the evidence.
