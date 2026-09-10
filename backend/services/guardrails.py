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
    r'\b(?:how\s+to\s+)?(?:bypass|evade|bribe)\s+(?:bis|isi|hallmark|customs|inspection|test)\b',
    r'\b(?:how\s+to\s+(?:make|create|print|generate|forge)|how\s+to\s+fake)\s+(?:a\s+)?(?:bis|isi|hallmark|mark|stamp|licence|license)\b',
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

    # 0. Allow legitimate consumer grievance, defect reporting, or counterfeit detection
    # Queries asking how to report, file complaint, spot, or check fake marks are core BIS services
    is_consumer_grievance = bool(re.search(r'\b(?:complaint|grievance|report|defective|substandard|spot\s+fake|check\s+fake|detect\s+fake|misuse\s+of)\b', text, re.IGNORECASE))

    # 1. Jailbreak Check
    if not is_consumer_grievance:
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

def generate_refusal_response(reason: str, language: str = "en", is_grounding_issue: bool = False) -> Dict[str, Any]:
    """Generates an honest, polite, and grounded refusal conforming to the 4-part schema."""
    if is_grounding_issue:
        if language == "hi":
            return {
                "answer": "क्षमा करें, इस उत्पाद या मानक कोड का सत्यापन आधिकारिक बीआईएस डेटाबेस में नहीं हो सका।",
                "what_it_means": f"उत्तर में उल्लिखित मानक आधिकारिक बीआईएस रिकॉर्ड में सत्यापित नहीं है ({reason})।",
                "next_action": "कृपया उत्पाद का सही नाम, सामग्री या सटीक आईएस कोड पुनः दर्ज करें।",
                "evidence_tag": {
                    "source_type": "faq",
                    "reference": "BIS Saathi Grounding Gatekeeper",
                    "status": "not determined",
                    "clause_number": "Grounding Boundary",
                    "clause_summary": f"Refusal enforced: {reason}",
                    "verbatim_excerpt": f"Refusal enforced: {reason}",
                    "source_url": "https://www.bis.gov.in"
                },
                "guardrail_refusal": True,
                "provider": "guardrail-engine"
            }
        return {
            "answer": "I apologize, but the standard referenced could not be verified in the official BIS standards registry.",
            "what_it_means": f"To prevent misinformation, unverified standards are intercepted ({reason}).",
            "next_action": "Please refine your product description, primary materials, or provide a specific Indian Standard (IS) code.",
            "evidence_tag": {
                "source_type": "faq",
                "reference": "BIS Saathi Grounding Gatekeeper",
                "status": "not determined",
                "clause_number": "Grounding Boundary",
                "clause_summary": f"Refusal enforced: {reason}",
                "verbatim_excerpt": f"Refusal enforced: {reason}",
                "source_url": "https://www.bis.gov.in"
            },
            "guardrail_refusal": True,
            "provider": "guardrail-engine"
        }

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
                "clause_summary": f"Refusal enforced: {reason}",
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
            "clause_summary": f"Refusal enforced: {reason}",
            "verbatim_excerpt": f"Refusal enforced: {reason}",
            "source_url": "https://www.bis.gov.in"
        },
        "guardrail_refusal": True,
        "provider": "guardrail-engine"
    }

def validate_post_llm_grounding(
    response_data: Dict[str, Any],
    language: str = "en",
    context_payload: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Post-LLM Guardrail: Verifies that any Indian Standard mentioned in the generated answer
    actually exists in the verified database or retrieved evidence.
    If an unverified standard is mentioned:
    - If context_payload has a verified standard, gracefully falls back to deterministic synthesis.
    - Otherwise, provides a clear, grounded refusal without misclassifying legitimate queries as out-of-domain.
    """
    answer_text = response_data.get("answer", "")
    mentioned_codes = re.findall(r'\b(?:IS|is)\s*(\d{3,5})\b', answer_text)

    if not mentioned_codes:
        return response_data

    # Build context string to check for valid references in retrieved evidence chunks
    import json
    evidence_text = ""
    if context_payload:
        try:
            evidence_text += json.dumps(context_payload)
        except Exception:
            pass
    if "evidence_tag" in response_data:
        try:
            evidence_text += json.dumps(response_data["evidence_tag"])
        except Exception:
            pass

    conn = get_db_connection()
    cursor = conn.cursor()

    unverified_codes = []

    for code_num in mentioned_codes:
        # Check 1: In evidence context / retrieved chunks directly?
        if code_num in evidence_text:
            continue

        # Check 2: In standards table (is_code or related_standards)?
        cursor.execute("SELECT is_code FROM standards WHERE is_code LIKE ? OR related_standards LIKE ?", (f"%{code_num}%", f"%{code_num}%"))
        if cursor.fetchone():
            continue

        # Check 3: In standard_chunks table (verbatim clause citations)?
        cursor.execute("SELECT chunk_id FROM standard_chunks WHERE content LIKE ? OR standard_id LIKE ?", (f"%{code_num}%", f"%{code_num}%"))
        if cursor.fetchone():
            continue

        unverified_codes.append(code_num)

    conn.close()

    # Check: If the generated answer states that no official record was found,
    # clean up the evidence tag so it doesn't stamp an unrelated standard as 'confirmed'
    ans_lower = answer_text.lower()
    if any(phrase in ans_lower for phrase in ["no official bis record was found", "no official record was found", "without a specific indian standard", "not found in the provided context"]):
        response_data["evidence_tag"] = {
            "source_type": "directory",
            "reference": "Unlisted Category",
            "status": "not determined",
            "clause_number": "General Advisory",
            "clause_summary": "No verified mandatory standard found in local BIS directory for this query.",
            "verbatim_excerpt": "Consult BIS Manak Online for unlisted product categories.",
            "source_url": "https://www.manakonline.in"
        }
        return response_data

    if not unverified_codes:
        return response_data

    # An unverified standard was mentioned by the LLM
    print(f"[GUARDRAIL TRIPPED] LLM cited unverified standard code(s): {unverified_codes}.")

    # If context has a valid verified standard, fall back to deterministic synthesis instead of refusing!
    if context_payload and (context_payload.get("standard") or (context_payload.get("evidence_tag", {}).get("status") == "confirmed")):
        from backend.services.llm_groq import deterministic_synthesis
        print("[GUARDRAIL] Falling back to deterministic synthesis to preserve verified answer.")
        fallback = deterministic_synthesis(context_payload, "", target_lang=language)
        fallback["guardrail_intercepted"] = True
        return fallback

    # If no valid standard exists, return a specific grounded refusal
    return generate_refusal_response(
        reason=f"Generated response cited unverified standard IS {', '.join(unverified_codes)} not present in official BIS registry.",
        language=language,
        is_grounding_issue=True
    )
