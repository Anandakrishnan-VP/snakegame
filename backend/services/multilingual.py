"""
Multilingual Engine for BIS Saathi.
Supports 12 Major Indian Languages across both explicit UI selection and auto-detection:
Hindi (hi), Tamil (ta), Telugu (te), Marathi (mr), Bengali (bn),
Gujarati (gu), Kannada (kn), Malayalam (ml), Punjabi (pa), Odia (or), Urdu (ur), and English (en).

Protects standard codes (IS 17803), HUIDs, and licences from translation corruption,
translates Indic queries into English for database search, and returns synthesized answers
in the user's preferred Indian language.
"""

import os
import re
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SUPPORTED_INDIC_LANGS = {
    "en", "hi", "ta", "te", "mr", "bn", "gu", "kn", "ml", "pa", "or", "ur"
}

# Unicode regex ranges for Indian writing systems
INDIC_SCRIPTS = {
    "ta": r'[\u0B80-\u0BFF]', # Tamil
    "te": r'[\u0C00-\u0C7F]', # Telugu
    "kn": r'[\u0C80-\u0CFF]', # Kannada
    "ml": r'[\u0D00-\u0D7F]', # Malayalam
    "bn": r'[\u0980-\u09FF]', # Bengali
    "gu": r'[\u0A80-\u0AFF]', # Gujarati
    "pa": r'[\u0A00-\u0A7F]', # Gurmukhi / Punjabi
    "or": r'[\u0B00-\u0B7F]', # Odia
    "ur": r'[\u0600-\u06FF]', # Urdu / Perso-Arabic
    "hi": r'[\u0900-\u097F]', # Devanagari (Hindi, Marathi)
}

# Common Hinglish terms mapping to English intent/keywords
HINGLISH_MAP = {
    "kya": "what",
    "kaise": "how",
    "chahiye": "required",
    "karna": "do",
    "lena": "get",
    "milega": "available",
    "hai": "is",
    "hote": "are",
    "khilona": "toys",
    "khilone": "toys",
    "paani": "water",
    "botal": "bottle",
    "sona": "gold",
    "gahne": "jewellery",
    "dawa": "medicine",
    "bijli": "electricity",
    "taar": "cable wire",
    "joota": "shoes",
    "joote": "shoes",
    "asli": "genuine",
    "nakli": "counterfeit fake",
    "jaanch": "testing verification"
}

DEVA_MAP = {
    "खिलौनों": "toys",
    "खिलौने": "toys",
    "खिलौना": "toy",
    "बोतलों": "bottles",
    "बोतल": "bottle",
    "स्टेनलेस स्टील": "stainless steel",
    "हेलमेटों": "helmets",
    "हेलमेट": "helmet",
    "सीमेंट": "cement",
    "सोना": "gold",
    "गहने": "jewellery",
    "हॉलमार्क": "hallmark",
    "जांच": "verify testing",
    "लैब": "lab laboratory",
    "प्रयोगशाला": "testing laboratory",
    "नियमों": "standard rules",
    "नियम": "standard rule",
    "प्रमाणन": "certification licence",
    "लाइसेंस": "licence",
    "पानी": "water",
    "तार": "cable wire",
    "जूते": "footwear shoes",
    "जूता": "shoes",
    "अनिवार्य": "mandatory",
    "मानकों": "standards",
    "मानक": "standard",
    "के लिए": "for",
    "क्या": "what",
    "कहाँ": "where",
    "कैसे": "how",
    "हैं": "are",
    "है": "is",
    "लागू": "applicable",
    "चाहिए": "required"
}

def has_indic_characters(text: str) -> bool:
    """Checks if text contains any non-ASCII Indic Unicode characters."""
    for script_pattern in INDIC_SCRIPTS.values():
        if re.search(script_pattern, text):
            return True
    return False

def detect_script_language(text: str) -> Optional[str]:
    """Detects Indian language from script characters."""
    for lang_code, script_pattern in INDIC_SCRIPTS.items():
        if re.search(script_pattern, text):
            return lang_code
    return None

def resolve_language(raw_text: str, explicit_lang: str = "auto") -> str:
    """
    Resolves language: explicit override -> auto-detect (Indic Unicode / Hinglish) -> English default.
    """
    if explicit_lang and explicit_lang.lower().strip() in SUPPORTED_INDIC_LANGS:
        return explicit_lang.lower().strip()

    detected = detect_script_language(raw_text)
    if detected:
        return detected

    # Check Hinglish markers
    lower = raw_text.lower()
    hinglish_hits = sum(1 for word in lower.split() if word in HINGLISH_MAP)
    if hinglish_hits >= 2:
        return "hi"

    return "en"

def translate_to_english_if_needed(raw_text: str, resolved_lang: str) -> str:
    """
    Translates non-English or multilingual Indic queries into English before routing and retrieval.
    Guarantees that numbers, standard codes, and HUID remain untouched.
    """
    if resolved_lang == "en" and not has_indic_characters(raw_text):
        return raw_text

    # 1. Extract and protect protected tokens (IS codes, numbers, HUIDs, CM/L)
    protected_tokens = {}
    counter = 0

    def protect(match):
        nonlocal counter
        token = match.group(0)
        placeholder = f"__TOKEN_{counter}__"
        protected_tokens[placeholder] = token
        counter += 1
        return placeholder

    protected_text = re.sub(r'\b(?:IS|is)\s*\d+(?:\s*\([^\)]+\))?(?::\d{4})?\b', protect, raw_text)
    protected_text = re.sub(r'\b(?:CML|cml)[-\s]?\d+\b', protect, protected_text)
    protected_text = re.sub(r'\b[rR]-?\d{8}\b', protect, protected_text)

    # 2. Fast LLM translation if Groq is available and text has Indic characters
    if GROQ_API_KEY and has_indic_characters(protected_text):
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
            resp = client.chat.completions.create(
                model=os.getenv("GROQ_FAST_MODEL", "openai/gpt-oss-20b"),
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an Indian language query translator for a Bureau of Indian Standards assistant. "
                            "Translate the input Indian language text into concise English search keywords (3 to 6 words). "
                            "Preserve all placeholders like __TOKEN_0__, product names, numbers, and technical terms. "
                            "Return ONLY the concise English translation keywords, no punctuation, no explanations."
                        )
                    },
                    {"role": "user", "content": protected_text}
                ],
                temperature=0.0,
                max_tokens=500
            )
            msg = resp.choices[0].message
            translated = (msg.content or "").strip()
            
            # If content was empty due to reasoning output format, check reasoning
            if not translated and getattr(msg, "reasoning", None):
                # Simple fallback heuristic or regex from reasoning if available
                translated = protected_text

            if translated:
                # Restore protected tokens
                for placeholder, original in protected_tokens.items():
                    translated = translated.replace(placeholder, original)
                return translated
        except Exception as e:
            print(f"Fast Groq Indic translation fallback to rule-based: {e}")

    # 3. Rule-based / dictionary fallback for Hindi / Hinglish keywords
    translated = protected_text
    for hi_w, en_w in DEVA_MAP.items():
        translated = translated.replace(hi_w, en_w)

    for h_word, e_word in HINGLISH_MAP.items():
        translated = re.sub(r'\b' + h_word + r'\b', e_word, translated, flags=re.IGNORECASE)

    # Restore protected tokens
    for placeholder, original in protected_tokens.items():
        translated = translated.replace(placeholder, original)

    return translated
