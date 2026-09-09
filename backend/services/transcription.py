"""
Audio Transcription Service powered by Groq Whisper Large v3.
Provides high-accuracy Speech-to-Text for Indian languages with BIS domain prompt biasing.
Supports Hindi, Tamil, Telugu, Marathi, Bengali, Gujarati, Kannada, Malayalam, Punjabi, Urdu, and English.
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_WHISPER_MODEL = os.getenv("GROQ_WHISPER_MODEL", "whisper-large-v3")

# Domain prompt biasing to guide Whisper towards BIS terminology & Indian Standard codes
BIS_DOMAIN_PROMPT = (
    "Bureau of Indian Standards, BIS Saathi, Indian Standard, IS code, QCO, "
    "ISI mark, HUID, Form V, Manak Online, Scheme-I, CRS, hallmarking, testing laboratory."
)

# Standard Indic language mapping
INDIC_LANGUAGE_CODES = {
    "hi": "Hindi",
    "en": "English",
    "ta": "Tamil",
    "te": "Telugu",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu"
}

def transcribe_audio(
    audio_bytes: bytes,
    filename: str = "audio.webm",
    language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Transcribes audio bytes using Groq Whisper Large v3.
    """
    if not GROQ_API_KEY or GROQ_API_KEY.strip() == "":
        return {
            "success": False,
            "error": "GROQ_API_KEY is not configured on the server.",
            "text": ""
        }

    if not audio_bytes or len(audio_bytes) < 100:
        return {
            "success": False,
            "error": "Audio recording is empty or too short. Please speak clearly into the microphone.",
            "text": ""
        }

    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)

        # Normalize language parameter
        lang_code = language.strip().lower() if language and language.strip().lower() != "auto" else None
        if lang_code and lang_code not in INDIC_LANGUAGE_CODES:
            lang_code = None

        candidate_models = [GROQ_WHISPER_MODEL, "whisper-large-v3-turbo", "whisper-large-v3"]
        # De-duplicate while preserving order
        seen = set()
        models_to_try = [m for m in candidate_models if m and not (m in seen or seen.add(m))]

        last_err = None
        for model in models_to_try:
            try:
                # Transcribe with domain vocabulary prompt
                res = client.audio.transcriptions.create(
                    file=(filename, audio_bytes),
                    model=model,
                    prompt=BIS_DOMAIN_PROMPT,
                    response_format="verbose_json",
                    language=lang_code,
                    temperature=0.0
                )

                text = getattr(res, "text", "") or ""
                detected_lang = getattr(res, "language", lang_code or "en")
                duration = getattr(res, "duration", None)

                return {
                    "success": True,
                    "text": text.strip(),
                    "language": detected_lang,
                    "duration": duration,
                    "model": model
                }
            except Exception as model_err:
                print(f"Groq Whisper model '{model}' failed: {model_err}. Trying fallback...")
                last_err = model_err

        raise last_err or Exception("All Whisper models failed.")

    except Exception as e:
        print(f"Speech transcription failed: {e}")
        return {
            "success": False,
            "error": f"Transcription error: {str(e)}",
            "text": ""
        }
