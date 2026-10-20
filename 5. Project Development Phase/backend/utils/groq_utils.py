import os
import json
from config import MODEL_CONFIG
from utils.logger import setup_logger

logger = setup_logger("groq_utils")

_groq_client = None

def get_config():
    return MODEL_CONFIG

def get_groq_client():
    """
    Returns an initialized Groq client instance if API key is present.
    """
    global _groq_client
    api_key = MODEL_CONFIG.get("groq_api_key") or os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
        
    if _groq_client is None:
        try:
            from groq import Groq
            _groq_client = Groq(api_key=api_key)
            logger.info("Groq client initialized successfully.")
        except Exception as e:
            logger.warning(f"Could not initialize Groq client: {e}")
            _groq_client = None
            
    return _groq_client

def execute_groq_prompt(prompt: str, system_prompt: str = "You are a professional forensic crime scene intelligence AI.", temperature: float = 0.1, max_tokens: int = 1024) -> str:
    """
    Executes a prompt against Groq API with low temperature for deterministic answers.
    """
    client = get_groq_client()
    if not client:
        return None

    model = MODEL_CONFIG.get("groq_model", "llama-3.3-70b-versatile")
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        logger.warning(f"Groq API call with {model} failed: {e}. Trying fallback model...")
        fallback_model = MODEL_CONFIG.get("groq_fallback_model", "llama-3.1-8b-instant")
        try:
            completion = client.chat.completions.create(
                model=fallback_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return completion.choices[0].message.content.strip()
        except Exception as e2:
            logger.error(f"Fallback Groq API failed: {e2}")
            return None
