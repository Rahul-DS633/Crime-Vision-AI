import os
import json
import time
import uuid
from typing import Dict, Any, Optional
from config import SESSIONS_DIR
from utils.logger import setup_logger

logger = setup_logger("session_store")

class SessionStore:
    def __init__(self, sessions_dir=SESSIONS_DIR):
        self._sessions_dir = str(sessions_dir)
        os.makedirs(self._sessions_dir, exist_ok=True)
        self._store: Dict[str, Any] = {}
        self._load_existing_sessions()

    def _load_existing_sessions(self):
        """Loads sessions from disk into memory on startup."""
        try:
            for fname in os.listdir(self._sessions_dir):
                if fname.startswith("session_") and fname.endswith(".json"):
                    sid = fname[len("session_"):-len(".json")]
                    fpath = os.path.join(self._sessions_dir, fname)
                    with open(fpath, "r", encoding="utf-8") as f:
                        self._store[sid] = json.load(f)
            logger.info(f"Loaded {len(self._store)} cached forensic sessions.")
        except Exception as e:
            logger.warning(f"Error loading existing sessions: {e}")

    def create_session(self, data: dict) -> str:
        """
        Saves the forensic context to a JSON file on disk and caches in memory.
        """
        session_id = str(uuid.uuid4())
        entry = {
            "session_id": session_id,
            "data": data,
            "timestamp": time.time()
        }

        # Store in memory for speed
        self._store[session_id] = entry

        # Persist to disk for forensic durability
        session_path = os.path.join(self._sessions_dir, f"session_{session_id}.json")
        try:
            with open(session_path, "w", encoding="utf-8") as f:
                json.dump(entry, f, indent=2)
            logger.info(f"Created persistent forensic session: {session_id}")
        except Exception as e:
            logger.error(f"Failed to persist session {session_id}: {e}")

        return session_id

    def get_session(self, session_id: str) -> Optional[dict]:
        """
        Retrieves session data by session ID.
        """
        if not session_id:
            return None
            
        if session_id in self._store:
            return self._store[session_id].get("data", {})

        session_path = os.path.join(self._sessions_dir, f"session_{session_id}.json")
        if os.path.exists(session_path):
            try:
                with open(session_path, "r", encoding="utf-8") as f:
                    entry = json.load(f)
                    self._store[session_id] = entry
                    return entry.get("data", {})
            except Exception as e:
                logger.error(f"Failed to read session file {session_path}: {e}")

        return None

    def update_session(self, session_id: str, new_data: dict) -> bool:
        """
        Updates session context with additional data.
        """
        current = self.get_session(session_id) or {}
        current.update(new_data)
        entry = {
            "session_id": session_id,
            "data": current,
            "timestamp": time.time()
        }
        self._store[session_id] = entry
        session_path = os.path.join(self._sessions_dir, f"session_{session_id}.json")
        try:
            with open(session_path, "w", encoding="utf-8") as f:
                json.dump(entry, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to update session {session_id}: {e}")
            return False

session_store = SessionStore()
