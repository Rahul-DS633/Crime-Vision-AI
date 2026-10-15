"""
Chat Service - Context-Aware Forensic Evidence Chatbot
Combines Regex temporal direct lookup with strict RAG grounded Groq querying
"""
import re
import json
from typing import Optional, Dict, Any, List
from utils.logger import setup_logger
from utils.groq_utils import get_groq_client, execute_groq_prompt
from services.session_store import session_store

logger = setup_logger("chat_service")

def parse_time_from_question(question: str) -> Optional[int]:
    """
    Detects time-based queries (e.g., MM:SS or '5s' or 'at 12 seconds') via Regex.
    """
    if not question:
        return None

    # Matches "00:12" or "1:05"
    m_colon = re.search(r'\b(\d{1,2}):(\d{2})\b', question)
    if m_colon:
        minutes = int(m_colon.group(1))
        seconds = int(m_colon.group(2))
        return minutes * 60 + seconds

    # Matches "5s", "5 sec", "5 seconds", "at 5"
    m_sec = re.search(r'\b(?:at\s+)?(\d+)\s*(?:s|sec|seconds)?\b', question, re.IGNORECASE)
    if m_sec:
        try:
            val = int(m_sec.group(1))
            # Sanity check for reasonable second range
            if "sec" in question.lower() or "s" in question.lower() or "at " in question.lower():
                return val
        except ValueError:
            pass

    return None

def get_event_at_time(timeline: List[Dict[str, Any]], detected_sec: int) -> str:
    """
    Direct timeline lookup for exact event at given timestamp.
    """
    if not timeline:
        return f"No timeline data available for timestamp {detected_sec}s."

    # Look for matching second
    for item in timeline:
        sec = item.get("seconds")
        if sec == detected_sec:
            time_str = item.get("time", f"00:{sec:02d}")
            event = item.get("event", "No event recorded")
            return f"At {time_str} ({sec}s): {event}"

    # Find closest second
    closest = min(timeline, key=lambda x: abs(x.get("seconds", 0) - detected_sec))
    return f"At {closest.get('time', '')}: {closest.get('event', '')}"

def query_chat(session_id: str, question: str, mode: str = "video") -> str:
    """
    Queries Groq LLM using analysis results as context.
    Prioritizes direct timeline lookup for time-based queries in video mode.
    """
    context = session_store.get_session(session_id) or {}
    logger.info(f"Chat query received. Mode: {mode}, Session: {session_id}, Question: {question}")

    # --- VIDEO MODE: TIME-BASED QUERY DETECTION ---
    if mode == "video":
        detected_sec = parse_time_from_question(question)
        if detected_sec is not None:
            timeline = context.get("timeline", [])
            if timeline:
                event = get_event_at_time(timeline, detected_sec)
                return event

    # --- FORENSIC PROMPTING: Strictly Grounded Responses ---
    prompt = f"""Answer based ONLY on these results:
{json.dumps(context, indent=2)}

Rule: Do NOT hallucinate. If not found, say "Information not found".
Answer precisely: {question}"""

    # Call Groq with low temperature (0.1) for deterministic output
    client = get_groq_client()
    if client:
        try:
            ans = execute_groq_prompt(prompt, temperature=0.1)
            if ans and len(ans.strip()) > 0:
                return ans.strip()
        except Exception as e:
            logger.warning(f"Groq chat completion error: {e}")

    # Deterministic fallback response generation based on grounded context
    q_lower = question.lower()
    if "object" in q_lower or "seen" in q_lower or "items" in q_lower:
        facts = context.get("evidence_facts") or context.get("unique_objects") or context.get("scene_intelligence", {}).get("objects_detect")
        if facts:
            if isinstance(facts, list):
                return f"The objects detected in the scene are: {', '.join(facts)}."
            return f"The objects detected in the scene are: {facts}."
    
    if "person" in q_lower or "people" in q_lower or "who" in q_lower:
        people = context.get("people_count") or context.get("scene_intelligence", {}).get("people_count")
        suspect = context.get("facts", {}).get("suspect_description")
        if suspect:
            return f"Suspect information: {suspect}"
        if people is not None:
            return f"There were {people} person(s) detected in the scene."

    if "location" in q_lower or "where" in q_lower:
        loc = context.get("location") or context.get("scene_intelligence", {}).get("location")
        if loc:
            return f"The verified location is: {loc}."

    if "action" in q_lower or "what happened" in q_lower or "summary" in q_lower:
        summary = context.get("visual_summary") or context.get("summary") or context.get("ai_visual_summary")
        if summary:
            return f"Forensic summary: {summary}"

    return "Information not found in the verified forensic evidence context."
