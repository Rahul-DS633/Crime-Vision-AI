"""
Audio Service - Speech-to-Text and Fact Extraction
Handles Transformers Whisper and multilingual processing
"""
import os
import time
from typing import Dict, Any, List, Optional
from config import AUDIO_UPLOAD_DIR
from utils.logger import setup_logger
from audio_module.transcription import transcribe_audio
from audio_module.crime_analysis import extract_crime_intelligence, generate_summary, generate_audio_timeline
from services.session_store import session_store

logger = setup_logger("audio_service")

class AudioService:
    """Service for audio processing and transcription using Transformers"""

    def __init__(self):
        self.pipe = None

    def process_audio(self, audio_path: str) -> Dict[str, Any]:
        """
        Processes audio file, performs multilingual transcription,
        extracts 'Who, Where, When' facts and event timeline.
        """
        logger.info(f"Starting audio analysis for: {audio_path}")
        start_time = time.time()
        
        # 1. Transcribe audio
        transcription_res = transcribe_audio(audio_path)
        full_text = transcription_res.get("text", "")
        segments = transcription_res.get("segments", [])
        translations = transcription_res.get("translations", {})
        
        # 2. Extract intelligence via Groq / rule-based engine
        intelligence = extract_crime_intelligence(full_text)
        one_line_summary = generate_summary(full_text)
        
        # 3. Build timestamped event timeline
        timeline = generate_audio_timeline(segments, intelligence.get("actions_detected", []))

        # 4. Map intelligence to expected 'facts' format for frontend compatibility
        facts = {
            "who": [intelligence.get("suspect_description", "Unknown")],
            "where": [intelligence.get("location", "Unknown")],
            "when": [intelligence.get("when", "Unknown")],
            "actions": intelligence.get("actions_detected", []),
            "suspect_description": intelligence.get("suspect_description", ""),
            "crime_type": intelligence.get("crime_type", "ROBBERY"),
            "location_badge": intelligence.get("location_badge", "STORE")
        }

        # 5. Generate dynamic audio scenario hypotheses
        crime_t = intelligence.get("crime_type", "RECORDED_STATEMENT")
        if crime_t == "RECORDED_STATEMENT":
            scenarios = [
                "Scenario 1 (Primary): Direct Oral Statement - Identified speaker providing verbal introduction or official recorded statement.",
                "Scenario 2 (Alternative): Forensic Voiceprint Registration - Audio captured for biometric vocal profiling and speaker verification.",
                "Scenario 3 (Investigative): Non-Hostile Communication - Standard vocal delivery without duress or background acoustic disturbance."
            ]
        elif crime_t in ["ARMED_ROBBERY", "COMMERCIAL_THEFT", "ASSAULT_INCIDENT"]:
            scenarios = [
                "Scenario 1 (Primary): Direct Witness Account - Eyewitness observed active incident and reported key suspect and transit details.",
                "Scenario 2 (Alternative): Post-Incident Reporting - Observer witnessed aftermath or getaway following altercation.",
                "Scenario 3 (Investigative): Emergency Deposition - Urgent verbal statement documented for investigative dispatch."
            ]
        else:
            scenarios = [
                "Scenario 1 (Primary): Ambient Surveillance Audio - Audio channel monitoring environmental and acoustic sector.",
                "Scenario 2 (Alternative): Non-Verbal Acoustic Event - Acoustic frequency analysis without human vocal distress.",
                "Scenario 3 (Investigative): Acoustic Baseline Calibration - Measurement of background noise and room impulse response."
            ]

        result = {
            "status": "success",
            "audio_path": audio_path,
            "transcription": full_text,
            "summary": one_line_summary,
            "crime_type": intelligence.get("crime_type", "ROBBERY"),
            "location": intelligence.get("location_badge", "STORE"),
            "detailed_location": intelligence.get("location", "jewelry store"),
            "facts": facts,
            "timeline": timeline,
            "translations": translations,
            "segments": segments,
            "scenarios": scenarios,
            "processing_time": round(time.time() - start_time, 2)
        }

        # Create session store entry
        session_id = session_store.create_session(result)
        result["session_id"] = session_id
        return result

audio_service = AudioService()
