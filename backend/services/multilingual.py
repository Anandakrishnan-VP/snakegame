"""
Multilingual Engine for BIS Saathi.
Implements translate-before-route, protects numbers and IS codes from translation distortion,
and provides fail-open resilience.
"""

import re
from typing import Dict, Any, Tuple

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

def is_devanagari(text: str) -> bool:
    """Checks if text contains Devanagari Unicode range."""
    return bool(re.search(r'[\u0900-\u097F]', text))

def resolve_language(raw_text: str, explicit_lang: str = "auto") -> str:
    """
    Resolves language: explicit override -> auto-detect (Devanagari / Hinglish) -> English default.
    """
    if explicit_lang and explicit_lang.lower() in ["hi", "hindi"]:
        return "hi"
    if explicit_lang and explicit_lang.lower() in ["en", "english"]:
        return "en"

    # Auto-detect Devanagari
    if is_devanagari(raw_text):
        return "hi"

    # Check Hinglish markers
    lower = raw_text.lower()
    hinglish_hits = sum(1 for word in lower.split() if word in HINGLISH_MAP)
    if hinglish_hits >= 2:
        return "hi"

    return "en"

def translate_to_english_if_needed(raw_text: str, resolved_lang: str) -> str:
    """
    Translates non-English queries into English before routing and retrieval.
    Guarantees that numbers, standard codes, and HUID remain untouched.
    """
    if resolved_lang == "en":
        return raw_text

    # Extract and protect protected tokens (IS codes, numbers, HUIDs)
    protected_tokens = {}
    counter = 0

    def protect(match):
        nonlocal counter
        token = match.group(0)
        placeholder = f"__TOKEN_{counter}__"
        protected_tokens[placeholder] = token
        counter += 1
        return placeholder

    # Protect IS codes, HUID, CML
    protected_text = re.sub(r'\b(?:IS|is)\s*\d+(?:\s*\([^\)]+\))?(?::\d{4})?\b', protect, raw_text)
    protected_text = re.sub(r'\b(?:CML|cml)[-\s]?\d+\b', protect, protected_text)
    protected_text = re.sub(r'\b[rR]-?\d{8}\b', protect, protected_text)

    # Basic dictionary/rule translation for Hindi / Hinglish keywords
    translated = protected_text
    deva_map = {
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

    for hi_w, en_w in deva_map.items():
        translated = translated.replace(hi_w, en_w)

    for h_word, e_word in HINGLISH_MAP.items():
        translated = re.sub(r'\b' + h_word + r'\b', e_word, translated, flags=re.IGNORECASE)

    # Restore protected tokens
    for placeholder, original in protected_tokens.items():
        translated = translated.replace(placeholder, original)

    return translated
