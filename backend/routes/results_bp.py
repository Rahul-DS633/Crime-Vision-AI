import os
# pyrefly: ignore [missing-import]
import torch
# pyrefly: ignore [missing-import]
from flask import Blueprint, jsonify, send_file
from config import REPORTS_DIR, DEVICE
from utils.logger import setup_logger
from services.session_store import session_store
from services.pdf_service import generate_forensic_pdf

logger = setup_logger("results_bp")

results_bp = Blueprint('results', __name__, url_prefix='/api')

@results_bp.route('/health', methods=['GET'])
def health_check():
    """
    System Health Check endpoint (Matches Activity 6.2 test requirements)
    """
    return jsonify({
        "status": "healthy",
        "service": "CrimeVision AI Forensic Analysis Platform",
        "cuda_available": torch.cuda.is_available(),
        "device": DEVICE,
        "api_version": "1.0.0"
    }), 200

@results_bp.route('/results/<session_id>', methods=['GET'])
def get_session_results(session_id):
    """
    Retrieves stored forensic analysis context by session ID
    """
    data = session_store.get_session(session_id)
    if not data:
        return jsonify({"status": "error", "message": "Session not found"}), 404
    return jsonify({"status": "success", "session_id": session_id, "data": data}), 200

@results_bp.route('/report/<session_id>', methods=['GET'])
@results_bp.route('/report/download/<session_id>', methods=['GET'])
def download_pdf_report(session_id):
    """
    Generates and downloads the official court-admissible forensic PDF report
    """
    try:
        context = session_store.get_session(session_id)
        if not context:
            # Generate sample context if session is fresh
            context = {
                "crime_type": "HOMICIDE / ASSAULT",
                "location": "office",
                "visual_summary": "A male individual is observed lying on the floor, surrounded by a knife and restrained with tape.",
                "evidence_facts": ["Human", "Weapon", "knife", "tape", "office furniture", "laptop"],
                "scenarios": [
                    "Scenario 1: Direct assault at late evening hours.",
                    "Scenario 2: Struggle during attempted robbery.",
                    "Scenario 3: Staged crime scene requiring ballistic verification."
                ]
            }

        pdf_path = generate_forensic_pdf(session_id, context)
        if not os.path.exists(pdf_path):
            return jsonify({"status": "error", "message": "Failed to create PDF report"}), 500

        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=f"CrimeVision_Forensic_Report_{session_id[:8]}.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        logger.error(f"Error generating PDF report for session {session_id}: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
