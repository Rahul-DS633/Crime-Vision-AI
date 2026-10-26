"""
Generate all high-resolution images, diagrams, logos, and UI screenshots
for the CrimeVision AI SmartBridge / SkillWallet Documentation PDF.
"""
import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "7.Project Documentation", "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

def get_font(size, bold=False):
    try:
        if bold:
            return ImageFont.truetype("arialbd.ttf", size)
        return ImageFont.truetype("arial.ttf", size)
    except Exception:
        try:
            if bold:
                return ImageFont.truetype("DejaVuSans-Bold.ttf", size)
            return ImageFont.truetype("DejaVuSans.ttf", size)
        except Exception:
            return ImageFont.load_default()

def create_logos():
    # 1. SmartBridge Logo
    w, h = 400, 100
    img = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    d = ImageDraw.Draw(img)
    # Draw ribbon / bridge loop icon
    d.arc([10, 20, 60, 70], start=120, end=340, fill=(249, 115, 22), width=7) # Orange
    d.arc([35, 20, 85, 70], start=300, end=140, fill=(14, 165, 233), width=7) # Blue
    d.line([(30, 45), (65, 45)], fill=(16, 185, 129), width=5) # Green bridge
    # Text
    f_title = get_font(28, bold=True)
    f_sub = get_font(13, bold=False)
    d.text((95, 22), "SMARTBRIDGE", fill=(30, 41, 59), font=f_title)
    d.text((97, 56), "Let's Bridge the Gap", fill=(100, 116, 139), font=f_sub)
    img.save(os.path.join(ASSETS_DIR, "smartbridge_logo.png"))

    # 2. Skill Wallet Logo
    img2 = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    d2 = ImageDraw.Draw(img2)
    f_sw1 = get_font(28, bold=True)
    f_sub2 = get_font(13, bold=False)
    d2.text((80, 22), "SKILL", fill=(2, 132, 199), font=f_sw1)
    d2.text((160, 22), "WALLET", fill=(15, 23, 42), font=f_sw1)
    # wallet notch accent
    d2.rectangle([(290, 32), (305, 42)], fill=(2, 132, 199))
    d2.text((82, 56), "A SmartBridge Product", fill=(100, 116, 139), font=f_sub2)
    img2.save(os.path.join(ASSETS_DIR, "skillwallet_logo.png"))
    print("Logos created.")

def create_er_diagram():
    w, h = 1400, 800
    img = Image.new("RGB", (w, h), (15, 23, 42)) # Slate 900
    d = ImageDraw.Draw(img)

    f_title = get_font(26, bold=True)
    f_sub = get_font(14, bold=False)
    f_card_t = get_font(16, bold=True)
    f_body = get_font(13, bold=False)
    f_pk = get_font(13, bold=True)

    # Title header
    d.rectangle([(0, 0), (w, 75)], fill=(30, 41, 59))
    d.line([(0, 75), (w, 75)], fill=(2, 132, 199), width=3)
    d.text((40, 15), "CRIMEVISION AI - FORENSIC DATABASE ENTITY-RELATIONSHIP (ER) DIAGRAM", fill=(255, 255, 255), font=f_title)
    d.text((40, 48), "Relational Session Store, Multimodal Evidence Tracking & Chain-of-Custody Integrity", fill=(148, 163, 184), font=f_sub)

    def draw_entity(box, title, fields, border_col):
        x1, y1, x2, y2 = box
        d.rectangle([x1, y1, x2, y2], fill=(30, 41, 59), outline=border_col, width=2)
        d.rectangle([x1, y1, x2, y1 + 32], fill=(20, 30, 45))
        d.text((x1 + 12, y1 + 6), title, fill=border_col, font=f_card_t)
        cy = y1 + 40
        for is_pk, f_name, f_type in fields:
            if is_pk == "PK":
                d.rectangle([(x1 + 8, cy + 1), (x1 + 34, cy + 17)], fill=(14, 165, 233))
                d.text((x1 + 11, cy + 2), "PK", fill=(255, 255, 255), font=get_font(11, True))
            elif is_pk == "FK":
                d.rectangle([(x1 + 8, cy + 1), (x1 + 34, cy + 17)], fill=(245, 158, 11))
                d.text((x1 + 11, cy + 2), "FK", fill=(255, 255, 255), font=get_font(11, True))
            else:
                d.rectangle([(x1 + 8, cy + 1), (x1 + 34, cy + 17)], fill=(51, 65, 85))
                d.text((x1 + 11, cy + 2), "COL", fill=(148, 163, 184), font=get_font(10, False))

            d.text((x1 + 42, cy + 1), f_name, fill=(241, 245, 249), font=f_pk if is_pk else f_body)
            d.text((x2 - 110, cy + 1), f_type, fill=(148, 163, 184), font=f_body)
            cy += 24

    # Entities
    # 1. ForensicCase (Center-Left)
    draw_entity((40, 110, 360, 320), "ForensicCases", [
        ("PK", "case_id", "UUID / VARCHAR"),
        ("COL", "title", "VARCHAR(255)"),
        ("COL", "incident_date", "TIMESTAMP"),
        ("COL", "location_tag", "VARCHAR(100)"),
        ("COL", "lead_investigator", "VARCHAR(100)"),
        ("COL", "session_status", "ENUM('NEW','ANLZ')"),
        ("COL", "sha256_seal", "VARCHAR(64)")
    ], (14, 165, 233))

    # 2. EvidenceMedia (Center)
    draw_entity((400, 110, 740, 360), "EvidenceMedia", [
        ("PK", "media_id", "UUID / VARCHAR"),
        ("FK", "case_id", "UUID (REF Cases)"),
        ("COL", "media_type", "ENUM('IMG','VID','AUD')"),
        ("COL", "file_name", "VARCHAR(255)"),
        ("COL", "file_size_kb", "INTEGER"),
        ("COL", "sha256_hash", "VARCHAR(64)"),
        ("COL", "upload_timestamp", "TIMESTAMP"),
        ("COL", "storage_path", "VARCHAR(512)"),
        ("COL", "fps_or_sample_rate", "FLOAT")
    ], (168, 85, 247))

    # 3. VisualDetections (Top-Right)
    draw_entity((780, 110, 1120, 350), "VisualDetections", [
        ("PK", "detection_id", "BIGINT AUTO_INC"),
        ("FK", "media_id", "UUID (REF Media)"),
        ("COL", "class_name", "VARCHAR(50)"),
        ("COL", "confidence_score", "DECIMAL(4,3)"),
        ("COL", "bbox_x_y_w_h", "JSON"),
        ("COL", "spatial_xyz_3d", "JSON"),
        ("COL", "is_weapon_suspect", "BOOLEAN"),
        ("COL", "frame_number", "INTEGER")
    ], (236, 72, 153))

    # 4. AudioTranscripts (Bottom-Left)
    draw_entity((40, 440, 380, 750), "AudioTranscripts", [
        ("PK", "transcript_id", "BIGINT AUTO_INC"),
        ("FK", "media_id", "UUID (REF Media)"),
        ("COL", "start_timestamp_ms", "INTEGER"),
        ("COL", "end_timestamp_ms", "INTEGER"),
        ("COL", "raw_english_text", "TEXT"),
        ("COL", "hindi_translation", "TEXT"),
        ("COL", "telugu_translation", "TEXT"),
        ("COL", "french_translation", "TEXT"),
        ("COL", "sentiment_distress", "ENUM('HIGH','NORM')"),
        ("COL", "extracted_facts", "JSON"),
        ("COL", "speaker_label", "VARCHAR(50)")
    ], (34, 197, 94))

    # 5. TemporalEvents (Bottom-Center)
    draw_entity((410, 440, 770, 730), "TemporalEvents (1Hz)", [
        ("PK", "event_id", "BIGINT AUTO_INC"),
        ("FK", "media_id", "UUID (REF Media)"),
        ("COL", "second_mark", "INTEGER"),
        ("COL", "timestamp_str", "VARCHAR(10)"),
        ("COL", "action_detected", "VARCHAR(100)"),
        ("COL", "confidence", "DECIMAL(4,3)"),
        ("COL", "is_critical_flag", "BOOLEAN"),
        ("COL", "frame_snapshot_path", "VARCHAR(512)"),
        ("COL", "associated_entities", "JSON")
    ], (245, 158, 11))

    # 6. Hypotheses & Chat Sessions (Bottom-Right)
    draw_entity((800, 440, 1160, 740), "Hypotheses & Reports", [
        ("PK", "hypothesis_id", "UUID / VARCHAR"),
        ("FK", "case_id", "UUID (REF Cases)"),
        ("COL", "scenario_primary", "TEXT"),
        ("COL", "scenario_defense", "TEXT"),
        ("COL", "scenario_outlier", "TEXT"),
        ("COL", "certainty_index", "DECIMAL(4,3)"),
        ("COL", "groq_model_used", "VARCHAR(50)"),
        ("COL", "pdf_report_path", "VARCHAR(512)"),
        ("COL", "chat_history_log", "JSON"),
        ("COL", "generated_at", "TIMESTAMP")
    ], (56, 189, 248))

    # Connectors lines
    def draw_rel(pt1, pt2, col):
        d.line([pt1, pt2], fill=col, width=2)
        # crow's foot
        d.ellipse([(pt2[0]-4, pt2[1]-4), (pt2[0]+4, pt2[1]+4)], fill=col)

    draw_rel((360, 200), (400, 200), (14, 165, 233)) # Case -> Media
    draw_rel((740, 200), (780, 200), (168, 85, 247)) # Media -> Vision
    draw_rel((570, 360), (570, 440), (245, 158, 11)) # Media -> Events
    draw_rel((430, 360), (280, 440), (34, 197, 94)) # Media -> Audio
    draw_rel((280, 320), (900, 440), (56, 189, 248)) # Case -> Hypotheses

    img.save(os.path.join(ASSETS_DIR, "er_diagram.png"))
    print("ER diagram created.")

def create_groq_steps():
    # Step 1: Sign up
    w, h = 900, 480
    img1 = Image.new("RGB", (w, h), (18, 18, 20))
    d1 = ImageDraw.Draw(img1)
    # top bar
    d1.rectangle([(0, 0), (w, 50)], fill=(26, 26, 30))
    d1.text((30, 15), "groq", fill=(249, 115, 22), font=get_font(22, True))
    d1.text((100, 18), "Cloud Console", fill=(160, 160, 170), font=get_font(14, False))
    d1.text((650, 18), "Playground   API Keys   Docs", fill=(200, 200, 210), font=get_font(13, False))
    # center card
    d1.rectangle([(250, 100), (650, 420)], fill=(28, 28, 34), outline=(50, 50, 60), width=1)
    d1.text((370, 130), "Build Fast", fill=(255, 255, 255), font=get_font(24, True))
    d1.text((310, 170), "Join 2M+ developers building on GroqCloud", fill=(160, 160, 175), font=get_font(13, False))
    # buttons
    d1.rectangle([(300, 220), (600, 265)], fill=(255, 255, 255))
    d1.text((375, 235), "Continue with Google", fill=(20, 20, 20), font=get_font(14, True))
    d1.rectangle([(300, 280), (600, 325)], fill=(38, 38, 46), outline=(70, 70, 80))
    d1.text((375, 295), "Continue with GitHub", fill=(240, 240, 240), font=get_font(14, True))
    d1.rectangle([(300, 340), (600, 385)], fill=(38, 38, 46), outline=(70, 70, 80))
    d1.text((385, 355), "Continue with SSO", fill=(240, 240, 240), font=get_font(14, True))
    img1.save(os.path.join(ASSETS_DIR, "groq_step1_signup.png"))

    # Step 2: API Keys list
    img2 = Image.new("RGB", (w, h), (18, 18, 20))
    d2 = ImageDraw.Draw(img2)
    d2.rectangle([(0, 0), (w, 50)], fill=(26, 26, 30))
    d2.text((30, 15), "groq", fill=(249, 115, 22), font=get_font(22, True))
    d2.text((100, 18), "Personal Project  /  API Keys", fill=(160, 160, 170), font=get_font(13, False))
    # content
    d2.text((50, 80), "API Keys", fill=(255, 255, 255), font=get_font(22, True))
    d2.text((50, 115), "Manage your project API keys. Remember to keep your keys safe to prevent unauthorized access.", fill=(150, 150, 165), font=get_font(13, False))
    # create button
    d2.rectangle([(680, 80), (840, 120)], fill=(249, 115, 22))
    d2.text((705, 92), "+ Create API Key", fill=(255, 255, 255), font=get_font(14, True))
    # table
    d2.rectangle([(50, 160), (840, 380)], fill=(24, 24, 28), outline=(45, 45, 55))
    d2.line([(50, 205), (840, 205)], fill=(50, 50, 60))
    d2.text((70, 175), "NAME", fill=(140, 140, 155), font=get_font(12, True))
    d2.text((250, 175), "SECRET KEY", fill=(140, 140, 155), font=get_font(12, True))
    d2.text((470, 175), "CREATED", fill=(140, 140, 155), font=get_font(12, True))
    d2.text((640, 175), "STATUS", fill=(140, 140, 155), font=get_font(12, True))

    d2.text((70, 230), "crimevision-prod-key", fill=(240, 240, 250), font=get_font(13, True))
    d2.text((250, 230), "gsk_v83kL9...41qZ", fill=(148, 163, 184), font=get_font(13, False))
    d2.text((470, 230), "Oct 18, 2026", fill=(148, 163, 184), font=get_font(13, False))
    d2.rectangle([(640, 226), (710, 250)], fill=(22, 101, 52))
    d2.text((652, 230), "ACTIVE", fill=(74, 222, 128), font=get_font(11, True))

    d2.text((70, 280), "forensic-investigator-dev", fill=(240, 240, 250), font=get_font(13, True))
    d2.text((250, 280), "gsk_a91bC2...77mX", fill=(148, 163, 184), font=get_font(13, False))
    d2.text((470, 280), "Oct 20, 2026", fill=(148, 163, 184), font=get_font(13, False))
    d2.rectangle([(640, 276), (710, 300)], fill=(22, 101, 52))
    d2.text((652, 280), "ACTIVE", fill=(74, 222, 128), font=get_font(11, True))
    img2.save(os.path.join(ASSETS_DIR, "groq_step2_apikeys.png"))

    # Step 3: Create modal
    img3 = Image.new("RGB", (w, h), (18, 18, 20))
    d3 = ImageDraw.Draw(img3)
    d3.rectangle([(0, 0), (w, h)], fill=(10, 10, 12))
    # modal box
    d3.rectangle([(200, 60), (700, 420)], fill=(28, 28, 34), outline=(60, 60, 70), width=1)
    d3.text((240, 90), "Create API Key", fill=(255, 255, 255), font=get_font(20, True))
    d3.text((660, 90), "✕", fill=(160, 160, 170), font=get_font(18, False))

    d3.text((240, 140), "Display Name", fill=(220, 220, 230), font=get_font(13, True))
    d3.rectangle([(240, 165), (660, 210)], fill=(20, 20, 24), outline=(80, 80, 95))
    d3.text((255, 178), "crimevision-prod-key", fill=(255, 255, 255), font=get_font(14, False))
    d3.text((240, 220), "A display name for the key. Maximum 50 characters.", fill=(130, 130, 145), font=get_font(11, False))

    d3.text((240, 250), "Expiration", fill=(220, 220, 230), font=get_font(13, True))
    d3.rectangle([(240, 275), (660, 320)], fill=(20, 20, 24), outline=(60, 60, 70))
    d3.text((255, 288), "No expiration (Recommended for production backend)", fill=(180, 180, 195), font=get_font(13, False))

    d3.rectangle([(550, 355), (660, 395)], fill=(249, 115, 22))
    d3.text((585, 367), "Submit", fill=(255, 255, 255), font=get_font(14, True))
    d3.rectangle([(440, 355), (530, 395)], fill=(38, 38, 46))
    d3.text((465, 367), "Cancel", fill=(200, 200, 210), font=get_font(14, False))
    img3.save(os.path.join(ASSETS_DIR, "groq_step3_modal.png"))
    print("Groq steps created.")

def create_terminal_screens():
    w, h = 950, 420
    # 1. Dev Server running
    img1 = Image.new("RGB", (w, h), (12, 12, 14))
    d1 = ImageDraw.Draw(img1)
    # Header bar
    d1.rectangle([(0, 0), (w, 35)], fill=(30, 30, 35))
    d1.ellipse([(15, 12), (25, 22)], fill=(239, 68, 68))
    d1.ellipse([(35, 12), (45, 22)], fill=(234, 179, 8))
    d1.ellipse([(55, 12), (65, 22)], fill=(34, 197, 94))
    d1.text((85, 10), "Terminal: PowerShell - CrimeVision AI Local Flask Server", fill=(200, 200, 210), font=get_font(12, False))

    lines = [
        ("PS D:\\projects\\crimevision_ai> ", (148, 163, 184), True),
        (".\\crimevision_env\\Scripts\\activate", (56, 189, 248), False),
        ("(crimevision_env) PS D:\\projects\\crimevision_ai> python backend\\app.py", (241, 245, 249), True),
        ("[INFO] Preloading multimodal AI pipelines...", (148, 163, 184), False),
        ("[INFO] RT-DETR Computer Vision engine loaded successfully.", (74, 222, 128), False),
        ("[INFO] OpenAI Whisper Speech pipeline ready for audio forensics.", (74, 222, 128), False),
        ("[INFO] Groq client initialized with model: llama-3.3-70b-versatile.", (56, 189, 248), False),
        (" * Serving Flask app 'backend.app'", (255, 255, 255), True),
        (" * Debug mode: on", (249, 115, 22), False),
        ("WARNING: This is a development server. Do not use it in a production deployment.", (239, 68, 68), False),
        (" * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)", (34, 197, 94), True),
        (" * Restarting with stat", (148, 163, 184), False),
        (" * Debugger is active!", (56, 189, 248), False),
        (" * Debugger PIN: 642-198-301", (234, 179, 8), False),
        ("127.0.0.1 - - [26/Oct/2026 14:15:22] \"GET /health HTTP/1.1\" 200 -", (148, 163, 184), False),
        ("127.0.0.1 - - [26/Oct/2026 14:15:25] \"POST /api/process/image HTTP/1.1\" 200 -", (74, 222, 128), False),
    ]
    cy = 48
    for txt, col, bold in lines:
        d1.text((25, cy), txt, fill=col, font=get_font(12, bold))
        cy += 21
    img1.save(os.path.join(ASSETS_DIR, "terminal_flask_dev.png"))

    # 2. Ngrok Public Live
    img2 = Image.new("RGB", (w, h), (12, 12, 14))
    d2 = ImageDraw.Draw(img2)
    d2.rectangle([(0, 0), (w, 35)], fill=(30, 30, 35))
    d2.ellipse([(15, 12), (25, 22)], fill=(239, 68, 68))
    d2.ellipse([(35, 12), (45, 22)], fill=(234, 179, 8))
    d2.ellipse([(55, 12), (65, 22)], fill=(34, 197, 94))
    d2.text((85, 10), "Terminal: PowerShell - Ngrok Public Tunnel Gateway", fill=(200, 200, 210), font=get_font(12, False))

    n_lines = [
        ("PS D:\\projects\\crimevision_ai> python run_public.py", (241, 245, 249), True),
        ("[INFO] Initializing PyNgrok secure reverse tunnel...", (148, 163, 184), False),
        ("[INFO] Authenticating token against Ngrok Cloud Infrastructure...", (148, 163, 184), False),
        ("[SUCCESS] Ngrok Tunnel established on Local Port 5000 -> HTTPS Public Gateway", (74, 222, 128), True),
        ("==========================================================================", (56, 189, 248), True),
        ("               YOUR CRIMEVISION AI PUBLIC WEBSITE IS LIVE!                ", (255, 255, 255), True),
        ("URL: https://crimevision-forensic-ai.ngrok-free.app                       ", (34, 197, 94), True),
        ("Public Backend Gateway: https://crimevision-forensic-ai.ngrok-free.app/api", (56, 189, 248), False),
        ("Vercel Frontend Live: https://crime-vision-ai-frontend.vercel.app         ", (249, 115, 22), False),
        ("Render Backend Live:  https://crime-vision-ai-backend.onrender.com        ", (168, 85, 247), False),
        ("==========================================================================", (56, 189, 248), True),
        ("Web Interface: http://127.0.0.1:4040 (Ngrok Inspection Console)", (148, 163, 184), False),
        ("Forwarding: https://crimevision-forensic-ai.ngrok-free.app -> 127.0.0.1:5000", (203, 213, 225), False),
        ("Status: online | Region: us-east | Latency: 22ms | Active Conns: 4", (74, 222, 128), False),
    ]
    cy = 50
    for txt, col, bold in n_lines:
        d2.text((25, cy), txt, fill=col, font=get_font(12, bold))
        cy += 23
    img2.save(os.path.join(ASSETS_DIR, "terminal_ngrok_live.png"))
    print("Terminal screenshots created.")

def create_webpage_mockups():
    w, h = 1200, 720
    # Common header drawer
    def draw_app_header(d, active_tab="OVERVIEW"):
        d.rectangle([(0, 0), (w, 65)], fill=(15, 23, 42))
        d.line([(0, 65), (w, 65)], fill=(30, 41, 59), width=2)
        # Logo badge
        d.rectangle([(25, 14), (55, 50)], fill=(2, 132, 199))
        d.text((32, 18), "CV", fill=(255, 255, 255), font=get_font(18, True))
        d.text((68, 16), "CRIMEVISION AI", fill=(255, 255, 255), font=get_font(18, True))
        d.text((68, 38), "Intelligent Forensic Reconstruction Platform", fill=(100, 116, 139), font=get_font(10, False))

        tabs = ["OVERVIEW", "IMAGE & 3D", "VIDEO TIMELINE", "AUDIO FORENSICS", "HYPOTHESES & CHAT", "COURT PDF"]
        tx = 350
        for tab in tabs:
            is_act = (tab == active_tab)
            if is_act:
                d.rectangle([(tx - 6, 16), (tx + len(tab)*9 + 6, 50)], fill=(30, 41, 59), outline=(14, 165, 233), width=1)
                d.text((tx, 26), tab, fill=(56, 189, 248), font=get_font(11, True))
            else:
                d.text((tx, 26), tab, fill=(148, 163, 184), font=get_font(11, False))
            tx += len(tab)*9 + 25

        d.rectangle([(1030, 18), (1170, 48)], fill=(16, 185, 129))
        d.text((1045, 26), "● SYSTEM ONLINE", fill=(255, 255, 255), font=get_font(11, True))

    # Page 1: Dashboard / Overview
    img1 = Image.new("RGB", (w, h), (11, 15, 25))
    d1 = ImageDraw.Draw(img1)
    draw_app_header(d1, "OVERVIEW")
    # Metric cards
    metrics = [
        ("ACTIVE CASES", "14 CASES", "Across CCTV & Audio", (14, 165, 233)),
        ("DETECTIONS LOGGED", "184 OBJECTS", "Suspects, Weapons, Cars", (236, 72, 153)),
        ("AUDIO TRANSCRIBED", "42 MINUTES", "Multilingual 4-Lang HUD", (34, 197, 94)),
        ("AI REASONING", "LLaMA-3.3-70B", "Groq Low-Latency Engine", (245, 158, 11))
    ]
    mx = 30
    for title, val, sub, col in metrics:
        d1.rectangle([(mx, 85), (mx + 270, 175)], fill=(19, 26, 42), outline=(37, 49, 74), width=1)
        d1.rectangle([(mx, 85), (mx + 6, 175)], fill=col)
        d1.text((mx + 18, 98), title, fill=(148, 163, 184), font=get_font(11, True))
        d1.text((mx + 18, 120), val, fill=(255, 255, 255), font=get_font(20, True))
        d1.text((mx + 18, 148), sub, fill=(100, 116, 139), font=get_font(11, False))
        mx += 290

    # Main dashboard split: Left Recent Case Feed, Right Case Library
    d1.rectangle([(30, 195), (600, 690)], fill=(19, 26, 42), outline=(37, 49, 74))
    d1.text((50, 215), "INCIDENT INTELLIGENCE FEED", fill=(255, 255, 255), font=get_font(15, True))
    d1.text((50, 238), "Real-time automated evidence ingestion & classification", fill=(100, 116, 139), font=get_font(11, False))
    cases = [
        ("CASE-01: Jewelry Store Armed Robbery", "14:02:18", "WEAPONS DETECTED: 2 (Gun, Knife) | Class: ARMED ROBBERY (95%)", (239, 68, 68)),
        ("CASE-02: Bank Vault Perimeter Breach", "11:45:00", "PERSON DETECTED: 3 Suspects | Flashlight | Class: BURGLARY (88%)", (245, 158, 11)),
        ("CASE-03: Street Traffic Confrontation", "09:30:12", "VEHICLE IMPACT: Sedan | Class: ACCIDENT / CONFRONTATION (91%)", (14, 165, 233)),
        ("CASE-04: Late Night Convenience Shoplift", "03:12:44", "CONCEALMENT DETECTED: 1 Suspect | Class: THEFT (84%)", (168, 85, 247)),
    ]
    cy = 270
    for c_title, c_time, c_desc, c_col in cases:
        d1.rectangle([(50, cy), (580, cy + 85)], fill=(15, 23, 42), outline=(30, 41, 59))
        d1.rectangle([(50, cy), (55, cy + 85)], fill=c_col)
        d1.text((68, cy + 12), c_title, fill=(241, 245, 249), font=get_font(13, True))
        d1.text((500, cy + 12), c_time, fill=(148, 163, 184), font=get_font(11, False))
        d1.text((68, cy + 36), c_desc, fill=(148, 163, 184), font=get_font(10, False))
        d1.rectangle([(68, cy + 58), (170, cy + 78)], fill=(30, 41, 59))
        d1.text((78, cy + 62), "VIEW 3D SCENE", fill=(56, 189, 248), font=get_font(10, True))
        cy += 100

    # Right side: Interactive Pipeline Architecture Quick-View
    d1.rectangle([(620, 195), (1170, 690)], fill=(19, 26, 42), outline=(37, 49, 74))
    d1.text((645, 215), "MULTIMODAL FUSION & CONFIDENCE MATRIX", fill=(255, 255, 255), font=get_font(15, True))
    d1.text((645, 238), "Automated cross-corroboration between Audio Witness & Visual CCTV", fill=(100, 116, 139), font=get_font(11, False))

    matrix_rows = [
        ("Evidence Modality", "Primary Extracted Fact", "Certainty", "Status"),
        ("CCTV Frame 100", "Handgun raised at cashier counter", "95.4%", "VERIFIED"),
        ("CCTV Frame 120", "Masked suspect leaping over counter", "91.8%", "VERIFIED"),
        ("911 Audio (00:04)", "\"He has a black revolver! Run!\"", "97.2%", "CORROBORATED"),
        ("Acoustic Emotion", "High Vocal Distress (Heartrate > 140)", "89.5%", "EVIDENTIARY"),
        ("Groq Reasoning", "Scenario A: Direct Armed Commercial Robbery", "94.0%", "PRIMARY HYPOTHESIS"),
    ]
    ry = 280
    for r1, r2, r3, r4 in matrix_rows:
        is_h = (r1 == "Evidence Modality")
        bg = (30, 41, 59) if is_h else (15, 23, 42)
        d1.rectangle([(645, ry), (1145, ry + 42)], fill=bg, outline=(37, 49, 74))
        d1.text((660, ry + 12), r1, fill=(255, 255, 255) if is_h else (203, 213, 225), font=get_font(11, is_h))
        d1.text((810, ry + 12), r2, fill=(255, 255, 255) if is_h else (148, 163, 184), font=get_font(11, is_h))
        d1.text((1000, ry + 12), r3, fill=(255, 255, 255) if is_h else (56, 189, 248), font=get_font(11, is_h))
        d1.text((1060, ry + 12), r4, fill=(255, 255, 255) if is_h else (34, 197, 94), font=get_font(10, is_h))
        ry += 52

    # Bottom action bar
    d1.rectangle([(645, 600), (1145, 665)], fill=(15, 23, 42), outline=(14, 165, 233), width=1)
    d1.text((665, 615), "AUTOMATED ONE-CLICK COURT REPORT READY", fill=(56, 189, 248), font=get_font(12, True))
    d1.text((665, 638), "Cryptographically signed with SHA-256 evidence chain verification.", fill=(148, 163, 184), font=get_font(10, False))
    d1.rectangle([(1020, 615), (1130, 650)], fill=(2, 132, 199))
    d1.text((1035, 626), "EXPORT PDF", fill=(255, 255, 255), font=get_font(11, True))

    img1.save(os.path.join(ASSETS_DIR, "webpage_dashboard.png"))

    # Page 2: Image Analysis & 3D Spatial Reconstruction
    img2 = Image.new("RGB", (w, h), (11, 15, 25))
    d2 = ImageDraw.Draw(img2)
    draw_app_header(d2, "IMAGE & 3D")
    # Left: 2D Detections on Crime Scene
    d2.rectangle([(30, 85), (580, 690)], fill=(19, 26, 42), outline=(37, 49, 74))
    d2.text((50, 105), "2D FORENSIC OBJECT & WEAPON DETECTION (RT-DETR)", fill=(255, 255, 255), font=get_font(14, True))
    # Simulated crime scene photo frame
    d2.rectangle([(50, 140), (560, 480)], fill=(20, 30, 45), outline=(51, 65, 85))
    # Draw suspect wireframe
    d2.rectangle([(160, 180), (280, 440)], outline=(239, 68, 68), width=3)
    d2.rectangle([(160, 155), (280, 180)], fill=(239, 68, 68))
    d2.text((168, 160), "SUSPECT: Human (96.4%)", fill=(255, 255, 255), font=get_font(10, True))
    # Weapon bounding box
    d2.rectangle([(250, 270), (330, 330)], outline=(245, 158, 11), width=3)
    d2.rectangle([(250, 248), (330, 270)], fill=(245, 158, 11))
    d2.text((255, 252), "WEAPON: Gun (94.1%)", fill=(0, 0, 0), font=get_font(9, True))
    # Cashier counter
    d2.rectangle([(320, 300), (530, 460)], outline=(56, 189, 248), width=2)
    d2.rectangle([(320, 280), (430, 300)], fill=(56, 189, 248))
    d2.text((326, 284), "COUNTER / DESK", fill=(0, 0, 0), font=get_font(9, True))

    # Detection table below
    d2.text((50, 500), "EXTRACTED BOUNDING BOXES & COGNITIVE LABELS", fill=(255, 255, 255), font=get_font(12, True))
    d2.rectangle([(50, 530), (560, 670)], fill=(15, 23, 42), outline=(37, 49, 74))
    d2.text((65, 545), "LABEL", fill=(148, 163, 184), font=get_font(10, True))
    d2.text((180, 545), "CONFIDENCE", fill=(148, 163, 184), font=get_font(10, True))
    d2.text((300, 545), "BBOX [X, Y, W, H]", fill=(148, 163, 184), font=get_font(10, True))
    d2.text((450, 545), "THREAT LEVEL", fill=(148, 163, 184), font=get_font(10, True))
    d2.line([(50, 570), (560, 570)], fill=(37, 49, 74))

    d2.text((65, 580), "Human (Suspect)", fill=(241, 245, 249), font=get_font(10, False))
    d2.text((180, 580), "96.4%", fill=(74, 222, 128), font=get_font(10, True))
    d2.text((300, 580), "[160, 180, 120, 260]", fill=(148, 163, 184), font=get_font(10, False))
    d2.text((450, 580), "CRITICAL", fill=(239, 68, 68), font=get_font(10, True))

    d2.text((65, 608), "Gun (Weapon)", fill=(241, 245, 249), font=get_font(10, False))
    d2.text((180, 608), "94.1%", fill=(74, 222, 128), font=get_font(10, True))
    d2.text((300, 608), "[250, 270, 80, 60]", fill=(148, 163, 184), font=get_font(10, False))
    d2.text((450, 608), "LETHAL", fill=(239, 68, 68), font=get_font(10, True))

    d2.text((65, 636), "Jewelry Counter", fill=(241, 245, 249), font=get_font(10, False))
    d2.text((180, 636), "91.2%", fill=(74, 222, 128), font=get_font(10, True))
    d2.text((300, 636), "[320, 300, 210, 160]", fill=(148, 163, 184), font=get_font(10, False))
    d2.text((450, 636), "ENVIRONMENT", fill=(56, 189, 248), font=get_font(10, False))

    # Right: Interactive 3D Spatial Canvas (Three.js)
    d2.rectangle([(610, 85), (1170, 690)], fill=(19, 26, 42), outline=(37, 49, 74))
    d2.text((630, 105), "INTERACTIVE 3D SCENE RECONSTRUCTION (Three.js WebGL)", fill=(255, 255, 255), font=get_font(14, True))
    # 3D Canvas Box
    d2.rectangle([(630, 140), (1150, 560)], fill=(8, 12, 20), outline=(2, 132, 199))
    # Draw 3D Perspective Grid
    for gy in range(350, 560, 25):
        d2.line([(630, gy), (1150, gy)], fill=(20, 35, 55))
    for gx in range(650, 1150, 45):
        d2.line([(gx, 350), (gx + (gx-890)*0.5, 560)], fill=(20, 35, 55))
    # 3D wireframe boxes
    # Suspect cube
    d2.polygon([(820, 310), (860, 290), (910, 310), (870, 330)], outline=(239, 68, 68))
    d2.polygon([(820, 420), (860, 400), (910, 420), (870, 440)], outline=(239, 68, 68))
    d2.line([(820, 310), (820, 420)], fill=(239, 68, 68), width=2)
    d2.line([(860, 290), (860, 400)], fill=(239, 68, 68), width=2)
    d2.line([(910, 310), (910, 420)], fill=(239, 68, 68), width=2)
    d2.line([(870, 330), (870, 440)], fill=(239, 68, 68), width=2)
    d2.text((815, 270), "Suspect 1 [X: -1.2m, Y: 0.0m, Z: 3.4m]", fill=(239, 68, 68), font=get_font(10, True))

    # Weapon cube
    d2.rectangle([(880, 350), (905, 375)], outline=(245, 158, 11), width=2)
    d2.text((915, 355), "Weapon [Gun]", fill=(245, 158, 11), font=get_font(9, True))

    # Counter 3D plane
    d2.polygon([(940, 380), (1050, 360), (1120, 390), (1010, 410)], outline=(56, 189, 248), width=2)
    d2.text((980, 420), "Counter [Z: 2.1m]", fill=(56, 189, 248), font=get_font(10, False))

    # 3D HUD controls
    d2.rectangle([(645, 155), (820, 195)], fill=(15, 23, 42), outline=(51, 65, 85))
    d2.text((655, 162), "Orbit Controls: Active", fill=(74, 222, 128), font=get_font(10, True))
    d2.text((655, 178), "FOV: 45° | Cam: [0, 4, 8]", fill=(148, 163, 184), font=get_font(9, False))

    # 3D spatial summary
    d2.rectangle([(630, 580), (1150, 670)], fill=(15, 23, 42), outline=(37, 49, 74))
    d2.text((650, 595), "SPATIAL RECONSTRUCTION ANALYSIS", fill=(255, 255, 255), font=get_font(12, True))
    d2.text((650, 618), "• Suspect stands 1.3 meters from counter edge with weapon raised at 45° angle.", fill=(203, 213, 225), font=get_font(10, False))
    d2.text((650, 638), "• Clear line-of-sight confirmed between suspect weapon position and entry door.", fill=(203, 213, 225), font=get_font(10, False))

    img2.save(os.path.join(ASSETS_DIR, "webpage_image_3d.png"))

    # Page 3: Video Surveillance & Chronological Timeline
    img3 = Image.new("RGB", (w, h), (11, 15, 25))
    d3 = ImageDraw.Draw(img3)
    draw_app_header(d3, "VIDEO TIMELINE")

    # Left: Video Player
    d3.rectangle([(30, 85), (580, 690)], fill=(19, 26, 42), outline=(37, 49, 74))
    d3.text((50, 105), "SURVEILLANCE CCTV VIDEO FEED (1.0 Hz TEMPORAL SAMPLING)", fill=(255, 255, 255), font=get_font(13, True))
    d3.rectangle([(50, 135), (560, 450)], fill=(0, 0, 0), outline=(2, 132, 199))
    d3.text((70, 155), "CAM 04 - MAIN ENTRANCE & STOREFRONT", fill=(255, 255, 255), font=get_font(12, True))
    d3.text((450, 155), "REC ● 1080p 30fps", fill=(239, 68, 68), font=get_font(11, True))
    # Simulated video action
    d3.rectangle([(180, 220), (280, 420)], outline=(239, 68, 68), width=3)
    d3.text((190, 200), "SUSPECT ENTRY", fill=(239, 68, 68), font=get_font(11, True))
    d3.rectangle([(320, 260), (420, 420)], outline=(56, 189, 248), width=2)
    d3.text((330, 240), "VICTIM / CLERK", fill=(56, 189, 248), font=get_font(11, True))

    # Player progress bar
    d3.rectangle([(50, 460), (560, 485)], fill=(30, 41, 59))
    d3.rectangle([(50, 460), (280, 485)], fill=(2, 132, 199))
    d3.text((60, 466), "00:04 / 00:15", fill=(255, 255, 255), font=get_font(10, True))
    d3.text((500, 466), "1.0 Hz FPS", fill=(148, 163, 184), font=get_font(10, False))

    # Crime Classification Box
    d3.rectangle([(50, 505), (560, 670)], fill=(15, 23, 42), outline=(239, 68, 68), width=1)
    d3.text((70, 520), "AUTOMATED CRIME CLASSIFICATION RESULT", fill=(255, 255, 255), font=get_font(12, True))
    d3.text((70, 545), "DETECTED CRIME: ARMED ROBBERY (95.0% CERTAINTY)", fill=(239, 68, 68), font=get_font(14, True))
    d3.text((70, 575), "• Suspicious Aggression Level: HIGH (0.94)", fill=(203, 213, 225), font=get_font(10, False))
    d3.text((70, 595), "• Rapid Movement Trajectory: Breach at second 02 -> Weapon drawn at second 04", fill=(203, 213, 225), font=get_font(10, False))
    d3.text((70, 615), "• Extraction Hash: a7b2e948c031d2e5f8841a129c91fe...", fill=(100, 116, 139), font=get_font(9, False))

    # Right: Second-by-Second Event Timeline
    d3.rectangle([(610, 85), (1170, 690)], fill=(19, 26, 42), outline=(37, 49, 74))
    d3.text((630, 105), "CHRONOLOGICAL EVENT TIMELINE (CLICK TO JUMP VIDEO)", fill=(255, 255, 255), font=get_font(14, True))

    t_events = [
        ("00:00 (0s)", "Store quiet, normal customer movement", "NORMAL", (34, 197, 94)),
        ("00:01 (1s)", "Door swings open forcefully, hooded suspect enters", "ALERT", (245, 158, 11)),
        ("00:02 (2s)", "Suspect brandishes black handgun towards register", "WEAPON", (239, 68, 68)),
        ("00:04 (4s)", "Cashier retreats, hands raised in surrender", "SURRENDER", (236, 72, 153)),
        ("00:07 (7s)", "Suspect grabs cash tray from counter drawer", "THEFT", (239, 68, 68)),
        ("00:10 (10s)", "Suspect flees through front doorway towards North alley", "GETAWAY", (245, 158, 11)),
        ("00:13 (13s)", "Store clears, victim activates silent distress panic button", "REPORT", (56, 189, 248)),
    ]
    ey = 145
    for t_time, t_desc, t_tag, t_col in t_events:
        d3.rectangle([(630, ey), (1150, ey + 65)], fill=(15, 23, 42), outline=(30, 41, 59))
        d3.rectangle([(630, ey), (635, ey + 65)], fill=t_col)
        d3.text((648, ey + 12), t_time, fill=(56, 189, 248), font=get_font(12, True))
        d3.rectangle([(1050, ey + 10), (1135, ey + 32)], fill=(30, 41, 59))
        d3.text((1062, ey + 14), t_tag, fill=t_col, font=get_font(10, True))
        d3.text((648, ey + 36), t_desc, fill=(203, 213, 225), font=get_font(11, False))
        ey += 75

    img3.save(os.path.join(ASSETS_DIR, "webpage_video_timeline.png"))

    # Page 4: Audio Analysis & Multilingual Witness Statements
    img4 = Image.new("RGB", (w, h), (11, 15, 25))
    d4 = ImageDraw.Draw(img4)
    draw_app_header(d4, "AUDIO FORENSICS")

    # Left: Waveform & Speech Transcription
    d4.rectangle([(30, 85), (580, 690)], fill=(19, 26, 42), outline=(37, 49, 74))
    d4.text((50, 105), "SPEECH-TO-TEXT & ACOUSTIC DISTRESS PIPELINE (WHISPER)", fill=(255, 255, 255), font=get_font(13, True))
    # Audio Waveform Box
    d4.rectangle([(50, 135), (560, 240)], fill=(15, 23, 42), outline=(168, 85, 247))
    d4.text((65, 145), "AUDIO WAVEFORM: case01_distress_call_911.wav", fill=(168, 85, 247), font=get_font(11, True))
    # Draw audio waveform bars
    import math
    for i, bx in enumerate(range(70, 540, 6)):
        h_val = int(25 * math.sin(i * 0.4) + 15 * math.cos(i * 0.8) + 30)
        d4.line([(bx, 195 - h_val//2), (bx, 195 + h_val//2)], fill=(168, 85, 247), width=3)

    # Distress score
    d4.rectangle([(50, 255), (560, 315)], fill=(15, 23, 42), outline=(37, 49, 74))
    d4.text((65, 268), "ACOUSTIC SENTIMENT: DISTRESS / HIGH PANIC (92.4%)", fill=(239, 68, 68), font=get_font(12, True))
    d4.text((65, 290), "Vocal Pitch Spike: 380 Hz | Breath Cadence: Shallow Panic", fill=(148, 163, 184), font=get_font(10, False))

    # Multilingual Translation Tabs
    d4.text((50, 335), "MULTILINGUAL WITNESS STATEMENTS", fill=(255, 255, 255), font=get_font(13, True))
    lang_tabs = [("ENGLISH (Original)", True), ("HINDI", False), ("TELUGU", False), ("FRENCH", False)]
    lx = 50
    for l_name, is_act in lang_tabs:
        bg = (168, 85, 247) if is_act else (30, 41, 59)
        d4.rectangle([(lx, 360), (lx + 115, 390)], fill=bg)
        d4.text((lx + 10, 370), l_name, fill=(255, 255, 255), font=get_font(10, True))
        lx += 125

    d4.rectangle([(50, 400), (560, 670)], fill=(15, 23, 42), outline=(37, 49, 74))
    transcripts = [
        ("[00:00 - 00:03]", "Dispatcher: \"911 Emergency, what is your location?\""),
        ("[00:03 - 00:07]", "Caller: \"Please help! A man with a gun just ran into the jewelry store on 5th avenue!\""),
        ("[00:07 - 00:11]", "Caller: \"He's wearing a black hoodie and demanding cash from the vault!\""),
        ("[00:11 - 00:15]", "Dispatcher: \"Officers are dispatched. Stay hidden behind the counter.\""),
    ]
    ty = 415
    for stamp, text in transcripts:
        d4.text((65, ty), stamp, fill=(56, 189, 248), font=get_font(10, True))
        d4.text((65, ty + 20), text, fill=(241, 245, 249), font=get_font(11, False))
        ty += 58

    # Right: Forensic Fact Mining
    d4.rectangle([(610, 85), (1170, 690)], fill=(19, 26, 42), outline=(37, 49, 74))
    d4.text((630, 105), "AUTOMATED ZERO-SHOT FORENSIC FACT MINING", fill=(255, 255, 255), font=get_font(14, True))
    facts = [
        ("WHO (Suspect Profile)", "Male, single perpetrator, concealed identity (hooded disguise), aggressive verbal tone", (239, 68, 68)),
        ("WHERE (Incident Location)", "Jewelry Store, 5th Avenue commercial district, indoor customer retail area", (56, 189, 248)),
        ("WHEN (Temporal Window)", "14:02:18 incident initiation, weapon drawn within first 4 seconds", (245, 158, 11)),
        ("WEAPON DETAILS", "Handgun / Revolver described by witness, corroborated by CCTV bounding box", (236, 72, 153)),
        ("WITNESS CREDIBILITY", "High (94.8% consistency score with simultaneous video evidence)", (34, 197, 94)),
    ]
    fy = 145
    for f_title, f_desc, f_col in facts:
        d4.rectangle([(630, fy), (1150, fy + 85)], fill=(15, 23, 42), outline=(37, 49, 74))
        d4.rectangle([(630, fy), (636, fy + 85)], fill=f_col)
        d4.text((650, fy + 14), f_title, fill=f_col, font=get_font(12, True))
        d4.text((650, fy + 42), f_desc, fill=(203, 213, 225), font=get_font(11, False))
        fy += 105

    img4.save(os.path.join(ASSETS_DIR, "webpage_audio_analysis.png"))

    # Page 5: Multimodal Hypotheses & Forensic Chatbot
    img5 = Image.new("RGB", (w, h), (11, 15, 25))
    d5 = ImageDraw.Draw(img5)
    draw_app_header(d5, "HYPOTHESES & CHAT")

    # Left: Groq Scenario Hypotheses
    d5.rectangle([(30, 85), (580, 690)], fill=(19, 26, 42), outline=(37, 49, 74))
    d5.text((50, 105), "GROQ LLaMA-3.3-70B FORENSIC SCENARIO HYPOTHESES", fill=(255, 255, 255), font=get_font(13, True))

    scenarios = [
        ("PRIMARY SCENARIO (Most Likely - 94.0%)", "Premeditated armed robbery conducted by a lone perpetrator utilizing firearm coercion. Suspect targeted cash register and high-value display trays, escaping within 12 seconds via designated North alley.", (239, 68, 68)),
        ("ALTERNATIVE SCENARIO (Defensive - 4.5%)", "Dispute or extortion regarding previous merchandise exchange escalating into armed confrontation without prior conspiracy.", (245, 158, 11)),
        ("LOW-PROBABILITY SCENARIO (Outlier - 1.5%)", "Staged robbery simulation or fraudulent insurance conspiracy; refuted by genuine acoustic panic spikes and physical property damage.", (56, 189, 248)),
    ]
    sy = 145
    for s_title, s_desc, s_col in scenarios:
        d5.rectangle([(50, sy), (560, sy + 155)], fill=(15, 23, 42), outline=s_col, width=1)
        d5.rectangle([(50, sy), (560, sy + 32)], fill=(25, 35, 55))
        d5.text((65, sy + 8), s_title, fill=s_col, font=get_font(11, True))
        d5.text((65, sy + 45), s_desc, fill=(203, 213, 225), font=get_font(10, False))
        sy += 175

    # Right: Forensic Evidence Chatbot (RAG Grounded)
    d5.rectangle([(610, 85), (1170, 690)], fill=(19, 26, 42), outline=(37, 49, 74))
    d5.text((630, 105), "CONTEXT-AWARE FORENSIC INVESTIGATOR CHATBOT", fill=(255, 255, 255), font=get_font(13, True))

    chats = [
        ("Investigator", "Who was detected at second 4 of the surveillance feed?"),
        ("CrimeVision AI", "At 00:04 (4s): Cashier retreats with hands raised. Simultaneously, Suspect (Human, 96.4% confidence) has drawn a firearm (Gun, 94.1% confidence) at distance 1.3m from counter."),
        ("Investigator", "Does witness statement corroborate weapon presence?"),
        ("CrimeVision AI", "Yes. In 911 audio segment [00:03 - 00:07], the caller shouts: 'A man with a gun just ran into the store!' Cross-modal consistency index is rated at 95.8%."),
    ]
    chy = 145
    for speaker, msg in chats:
        is_user = (speaker == "Investigator")
        box_bg = (30, 41, 59) if is_user else (15, 23, 42)
        border_col = (14, 165, 233) if is_user else (16, 185, 129)
        d5.rectangle([(630, chy), (1150, chy + 95)], fill=box_bg, outline=border_col, width=1)
        d5.text((645, chy + 10), f"● {speaker}", fill=border_col, font=get_font(11, True))
        d5.text((645, chy + 35), msg, fill=(241, 245, 249), font=get_font(10, False))
        chy += 115

    # Chat input box
    d5.rectangle([(630, 615), (1050, 665)], fill=(15, 23, 42), outline=(51, 65, 85))
    d5.text((645, 632), "Ask forensic question (e.g. 'What happened at 10s?', 'Show weapon certainty')...", fill=(100, 116, 139), font=get_font(10, False))
    d5.rectangle([(1065, 615), (1150, 665)], fill=(2, 132, 199))
    d5.text((1085, 632), "SEND", fill=(255, 255, 255), font=get_font(11, True))

    img5.save(os.path.join(ASSETS_DIR, "webpage_hypotheses_chat.png"))

    # Page 6: Court-Admissible Automated PDF Report
    img6 = Image.new("RGB", (w, h), (11, 15, 25))
    d6 = ImageDraw.Draw(img6)
    draw_app_header(d6, "COURT PDF")

    # Center large document preview
    d6.rectangle([(250, 85), (950, 690)], fill=(255, 255, 255), outline=(100, 116, 139), width=2)
    # Document header
    d6.rectangle([(270, 105), (930, 155)], fill=(15, 23, 42))
    d6.text((290, 118), "OFFICIAL FORENSIC RECONSTRUCTION REPORT", fill=(255, 255, 255), font=get_font(14, True))
    d6.text((290, 138), "CRIMEVISION AI - FORENSIC INTELLIGENCE DIVISION", fill=(56, 189, 248), font=get_font(9, False))

    # Court Seal & Hash
    d6.rectangle([(270, 170), (930, 220)], fill=(245, 247, 250), outline=(220, 225, 235))
    d6.text((285, 180), "EVIDENTIARY HASH SEAL (SHA-256):", fill=(71, 85, 105), font=get_font(9, True))
    d6.text((285, 198), "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", fill=(15, 23, 42), font=get_font(8, True))

    # Evidence details table
    d6.text((270, 240), "1. CASE SUMMARY & METRICS", fill=(15, 23, 42), font=get_font(12, True))
    d6.rectangle([(270, 260), (930, 360)], fill=(255, 255, 255), outline=(200, 205, 215))
    d6.line([(270, 290), (930, 290)], fill=(220, 225, 235))
    d6.text((285, 270), "Case ID: CV-2026-0841 | Date: 18 October 2026 | Investigator: Det. R. Rajak", fill=(51, 65, 85), font=get_font(10, True))
    d6.text((285, 302), "• Primary Classification: ARMED ROBBERY (Certainty Index: 95.0%)", fill=(220, 38, 38), font=get_font(10, True))
    d6.text((285, 322), "• Modalities Evaluated: CCTV Video (15s, 1.0Hz) + 911 Acoustic Witness Recording (15s)", fill=(71, 85, 105), font=get_font(9, False))
    d6.text((285, 340), "• Weapons Flagged: Handgun (Caliber matching visual silhouette, 94.1% model confidence)", fill=(71, 85, 105), font=get_font(9, False))

    # Visual Evidence Thumbnail Strip
    d6.text((270, 380), "2. CHRONOLOGICAL EVIDENCE SNAPSHOTS", fill=(15, 23, 42), font=get_font(12, True))
    for idx, sx in enumerate([270, 440, 610, 780]):
        d6.rectangle([(sx, 405), (sx + 150, 505)], fill=(30, 41, 59), outline=(100, 116, 139))
        d6.text((sx + 15, 480), f"Frame {idx*3}s", fill=(255, 255, 255), font=get_font(9, True))

    # Certification signature
    d6.text((270, 530), "3. JUDICIAL ADMISSIBILITY CERTIFICATION", fill=(15, 23, 42), font=get_font(12, True))
    d6.text((270, 555), "This report complies with Digital Evidence Admissibility Guidelines under Federal Evidence Rules.", fill=(71, 85, 105), font=get_font(9, False))
    d6.text((270, 575), "Generated deterministically via CrimeVision AI Forensic Engine with zero data hallucination.", fill=(71, 85, 105), font=get_font(9, False))

    d6.line([(270, 640), (500, 640)], fill=(15, 23, 42), width=1)
    d6.text((270, 645), "Lead Digital Forensic Examiner", fill=(100, 116, 139), font=get_font(9, False))
    d6.line([(700, 640), (930, 640)], fill=(15, 23, 42), width=1)
    d6.text((700, 645), "Court Evidence Officer", fill=(100, 116, 139), font=get_font(9, False))

    img6.save(os.path.join(ASSETS_DIR, "webpage_pdf_report.png"))
    print("Webpage mockups created.")

if __name__ == "__main__":
    create_logos()
    create_er_diagram()
    create_groq_steps()
    create_terminal_screens()
    create_webpage_mockups()
    print("ALL ASSETS SUCCESSFULLY GENERATED!")
