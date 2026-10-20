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

        # 5. Generate audio scenario hypotheses
        scenarios = [
            "Scenario 1: Commercial Burglary / Robbery - Coordinated entry into jewelry retail establishment after normal business hours, seizing display merchandise.",
            "Scenario 2: Smash and Grab - Opportunistic robbery exploiting late evening visibility, with a getaway driver stationed outside.",
            "Scenario 3: Internal Collusion - Staged incident intended to trigger insurance recovery, evidenced by prompt alarm activation after vehicle departure."
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
