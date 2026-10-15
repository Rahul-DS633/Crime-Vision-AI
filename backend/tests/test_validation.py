"""
Unit and Integration Tests for CrimeVision AI Forensic Analysis Platform
Validates Activity 6.2 Requirements
"""
import os
import unittest
import json
import sys

# Add backend directory to sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app import app
from services.fusion_service import fusion_service
from services.chat_service import parse_time_from_question, get_event_at_time
from services.pdf_service import generate_forensic_pdf
from video_module.timeline import build_timeline
from audio_module.crime_analysis import extract_crime_intelligence

class TestCrimeVisionValidation(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.fusion_service = fusion_service

    def test_api_health(self):
        """
        Simulate a real browser request to /api/health
        Assert: Server must reply 200 OK
        """
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertIn("service", data)

    def test_fusion_logic_consistency(self):
        """
        Simulate Audio saying "Kitchen" and Text Report saying "Kitchen"
        Assert: Computed match must be True
        """
        audio_mock = [{'facts': {'locations': ['kitchen']}}]
        text_mock = [{'entities': {'locations': ['kitchen']}}]

        consistency = self.fusion_service._check_consistency([], audio_mock, text_mock)
        
        matches = consistency.get("matches", [])
        match_found = any(m.get("type") == "location" and "kitchen" in m.get("values", []) for m in matches)
        self.assertTrue(match_found)
        self.assertGreaterEqual(consistency.get("overall_score", 0.0), 0.8)

    def test_chat_time_based_parsing(self):
        """
        Tests regex extraction of timestamps from natural language investigator questions
        """
        self.assertEqual(parse_time_from_question("Who was there at 5s?"), 5)
        self.assertEqual(parse_time_from_question("What happened at 00:12?"), 12)
        self.assertEqual(parse_time_from_question("At 7 seconds who dropped the bag?"), 7)
        self.assertEqual(parse_time_from_question("Explain the scene at 1:05"), 65)

    def test_timeline_hash_indexing(self):
        """
        Tests 1Hz video timeline construction and second snapping
        """
        captions = [
            {"second": 0, "caption": "A man enters the store"},
            {"second": 5, "caption": "A shopper moves near refrigerator"}
        ]
        detections = [
            {"second": 0, "detections": [{"label": "Human"}]},
            {"second": 5, "detections": [{"label": "Human"}, {"label": "refrigerator"}]}
        ]
        res = build_timeline(captions, detections, duration=5.0)
        timeline = res.get("timeline", [])
        self.assertEqual(len(timeline), 6) # 0 to 5 seconds
        self.assertEqual(timeline[0]["event"], "A man enters the store")
        self.assertEqual(timeline[5]["event"], "A shopper moves near refrigerator")

    def test_pdf_report_generation(self):
        """
        Validates automated generation of court-admissible forensic PDF report
        """
        mock_context = {
            "crime_type": "BURGLARY",
            "location": "jewelry store",
            "visual_summary": "Two masked individuals observed exiting commercial retail premise.",
            "evidence_facts": ["Human", "Weapon", "necklace", "car"],
            "timeline": [
                {"time": "00:00", "event": "Suspects observed at store front"},
                {"time": "00:07", "event": "Suspects fled in dark sedan"}
            ],
            "scenarios": [
                "Scenario 1: Coordinated burglary targeting jewelry merchandise.",
                "Scenario 2: Opportunistic theft during closing hours."
            ]
        }
        pdf_path = generate_forensic_pdf("test_session_123", mock_context)
        self.assertTrue(os.path.exists(pdf_path))
        self.assertGreater(os.path.getsize(pdf_path), 1000)

if __name__ == '__main__':
    unittest.main()
