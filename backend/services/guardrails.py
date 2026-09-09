"""
Ironclad Guardrail & Refusal Engine for BIS Saathi.
Implements a 3-tier shield:
1. Pre-retrieval Adversarial & Jailbreak Shield
2. Out-of-Domain Strict Refusal Filter
3. Post-Retrieval Grounding Gatekeeper & Post-LLM Hallucination Validator
"""

import re
from typing import Dict, Any, Optional, Tuple
from backend.db.database import get_db_connection

# 1. Adversarial, Jailbreak, and Prompt Injection Patterns
JAILBREAK_PATTERNS = [
    r'\bignore\s+(all\s+)?(?:previous|prior|above)\s+instructions?\b',
    r'\b(?:system\s+prompt|reveal\s+(?:your\s+)?prompt|show\s+prompt)\b',
    r'\bact\s+as\s+(?:an?\s+)?(?:unrestricted|dan|jailbroken|evil)\b',
    r'\bpretend\s+you\s+(?:are|can)\b',
    r'\b(?:bypass|fake|counterfeit|forge)\s+(?:bis|isi|hallmark|customs|inspection|test)\b',
    r'\bhow\s+to\s+(?:cheat|forge|evade|bribe)\b'
]

# 2. Clear Out-of-Domain Non-BIS Topics
OUT_OF_DOMAIN_PATTERNS = [
    # Tax / Finance / Crypto
    r'\b(?:gst\s+rate|income\s+tax|stock\s+market|crypto|bitcoin|mutual\s+funds?|loan\s+interest)\b',
    # Politics / Government officials
    r'\b(?:who\s+is\s+the\s+prime\s+minister|who\s+is\s+the\s+minister|election\s+results?|bjp|congress|political\s+party)\b',
    # Coding / Math / Homework
    r'\b(?:write\s+(?:a\s+)?(?:python|javascript|c\+\+|java)\s+code|solve\s+(?:this\s+)?equation|binary\s+search|algorithm)\b',
    # Creative writing / Entertainment / Trivia
    r'\b(?:write\s+(?:a\s+)?(?:poem|story|song|essay|joke)|tell\s+me\s+a\s+joke|movie\s+review|netflix|actor|actress)\b',
    # Cooking / Food recipes
    r'\b(?:recipe\s+for|how\s+to\s+cook|ingredients\s+of\s+biryani|baking\s+cake)\b',
    # Medical advice
    r'\b(?:prescribe\s+medicine|diagnose\s+symptoms|headache\s+treatment|dosage)\b'
]

def check_pre_retrieval_guardrails(query: str, language: str = "en") -> Tuple[bool, Optional[Dict[str, Any]]]:
    """
    Checks user query for prompt injection or off-domain topics before retrieval or LLM execution.
    Returns (is_safe: bool, refusal_payload: Optional[Dict]).
    """
    text = query.strip().lower()

    # 1. Jailbreak Check
    for pat in JAILBREAK_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return False, generate_refusal_response(
                reason="Adversarial or security boundary violation detected.",
                language=language
            )

    # 2. Out-of-Domain Topic Check
    for pat in OUT_OF_DOMAIN_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            return False, generate_refusal_response(
                reason="Query is outside the scope of Bureau of Indian Standards services.",
                language=language
            )

    return True, None

def generate_refusal_response(reason: str, language: str = "en") -> Dict[str, Any]:
    """Generates an honest, polite, and grounded refusal conforming to the 4-part schema."""
    if language == "hi":
        return {
            "answer": "मैं बीआईएस साथी हूँ, और मैं केवल भारतीय मानकों (Indian Standards), बीआईएस प्रमाणन, हॉलमार्किंग और प्रयोगशाला परीक्षण से संबंधित आधिकारिक प्रश्नों के उत्तर देने के लिए अधिकृत हूँ।",
            "what_it_means": "आपका प्रश्न भारतीय मानक ब्यूरो (BIS) के नियामक दायरे से बाहर है। नीति के अनुसार मैं अप्रासंगिक या अनधिकृत विषयों पर प्रतिक्रिया नहीं दे सकता।",
            "next_action": "कृपया किसी उत्पाद के मानक, ISI लाइसेंस सत्यापन (CM/L), 6-अंकीय HUID, या परीक्षण प्रयोगशालाओं से संबंधित प्रश्न पूछें।",
            "evidence_tag": {
                "source_type": "faq",
                "reference": "BIS Saathi Scope Guardrail",
                "status": "not determined",
                "clause_number": "Scope Boundary",
                "verbatim_excerpt": f"Refusal enforced: {reason}",
                "source_url": "https://www.bis.gov.in"
            },
            "guardrail_refusal": True,
            "provider": "guardrail-engine"
        }

    return {
        "answer": "I am BIS Saathi, an official assistant strictly dedicated to Indian Standards, BIS certification schemes, testing laboratories, and hallmarking.",
        "what_it_means": "Your query falls outside the official regulatory jurisdiction of the Bureau of Indian Standards (BIS). By policy, I refuse off-domain, unverified, or adversarial topics.",
        "next_action": "Please ask a question related to product compliance, Indian Standards (IS codes), licence verification (CM/L / HUID), or test requirements.",
        "evidence_tag": {
            "source_type": "faq",
            "reference": "BIS Saathi Scope Guardrail",
            "status": "not determined",
            "clause_number": "Scope Boundary",
            "verbatim_excerpt": f"Refusal enforced: {reason}",
            "source_url": "https://www.bis.gov.in"
        },
        "guardrail_refusal": True,
        "provider": "guardrail-engine"
    }

def validate_post_llm_grounding(response_data: Dict[str, Any], language: str = "en") -> Dict[str, Any]:
    """
    Post-LLM Guardrail: Verifies that any Indian Standard mentioned in the generated answer
    actually exists in the verified database. Replaces hallucinated standards with grounded refusal.
    """
    answer_text = response_data.get("answer", "")
    mentioned_codes = re.findall(r'\b(?:IS|is)\s*(\d{3,5})\b', answer_text)

    if not mentioned_codes:
        return response_data

    conn = get_db_connection()
    cursor = conn.cursor()

    for code_num in mentioned_codes:
        cursor.execute("SELECT is_code FROM standards WHERE is_code LIKE ?", (f"%{code_num}%",))
        row = cursor.fetchone()
        if not row:
            # The LLM generated a standard code that DOES NOT exist in the official DB!
            conn.close()
            print(f"[GUARDRAIL TRIPPED] LLM hallucinated unverified standard IS {code_num}. Intercepting.")
            return generate_refusal_response(
                reason=f"Generated response cited unverified standard IS {code_num} not present in official BIS registry.",
                language=language
            )

    conn.close()
    return response_data
