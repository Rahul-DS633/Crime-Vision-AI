# pyrefly: ignore [missing-import]
from flask import Blueprint, request, jsonify
from utils.logger import setup_logger
from services.chat_service import query_chat

logger = setup_logger("chat_routes")

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat_bp.route('/<mode>', methods=['POST'])
def chat(mode):
    """
    Forensic Chatbot query endpoint
    Supports mode in ['image', 'audio', 'video']
    """
    try:
        data = request.json or {}
        session_id = data.get('session_id')
        question = data.get('question', '')

        if not question:
            return jsonify({"status": "error", "message": "Question is required"}), 400

        answer = query_chat(session_id, question, mode=mode)
        return jsonify({"status": "success", "answer": answer}), 200

    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
