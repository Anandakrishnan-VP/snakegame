"""
Groq LLM Synthesis Service with 4-Part Answer Pattern and Deterministic Fallback.
Adheres strictly to the principle: "The LLM is the language interface, not the system of record."
Outputs consistent schema: { answer, what_it_means, next_action, evidence_tag }.
"""

import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_PRIMARY_MODEL = os.getenv("GROQ_PRIMARY_MODEL", "openai/gpt-oss-120b")
GROQ_FAST_MODEL = os.getenv("GROQ_FAST_MODEL", "openai/gpt-oss-20b")

def get_candidate_models():
    """Returns ordered list of candidate Groq models."""
    models = [GROQ_PRIMARY_MODEL, GROQ_FAST_MODEL, "qwen/qwen3.6-27b"]
    # De-duplicate while preserving order
    seen = set()
    return [m for m in models if m and not (m in seen or seen.add(m))]

def synthesize_with_groq(context_payload: Dict[str, Any], user_query: str, target_lang: str = "en") -> Dict[str, Any]:
    """
    Calls Groq API to synthesize the conversational response
    strictly grounded in the provided context_payload.
    Attempts primary model, fast model, and qwen fallback before deterministic synthesis.
    """
    if not GROQ_API_KEY or GROQ_API_KEY.strip() == "" or context_payload.get("out_of_scope") or context_payload.get("status") == "not determined":
        return deterministic_synthesis(context_payload, user_query, target_lang)

    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)

        evidence = context_payload.get("evidence_tag", {})
        persona = context_payload.get("persona", "general")

        INDIC_LANGUAGE_NAMES = {
            "en": "English",
            "hi": "Hindi (Devanagari script - हिन्दी)",
            "ta": "Tamil (தமிழ்)",
            "te": "Telugu (తెలుగు)",
            "mr": "Marathi (मराठी)",
            "bn": "Bengali (বাংলা)",
            "gu": "Gujarati (ગુજરાતી)",
            "kn": "Kannada (ಕನ್ನಡ)",
            "ml": "Malayalam (മലയാളം)",
            "pa": "Punjabi (ਪੰਜਾਬੀ)",
            "or": "Odia (ଓଡ଼ିଆ)",
            "ur": "Urdu (اردو)"
        }
        target_lang_desc = INDIC_LANGUAGE_NAMES.get(target_lang, "English")

        system_prompt = f"""You are BIS Saathi, an official AI assistant for the Bureau of Indian Standards (BIS).
Your goal is to provide accurate, grounded, and source-backed guidance strictly on Indian Standards, certification schemes, testing laboratories, and consumer affairs.

CRITICAL GUARDRAIL RULES:
1. STRICT GROUNDING: You are strictly an explanation interface. All facts, standard codes, clauses, and laboratory names MUST come directly from the official database context provided below. Do not invent, assume, or fabricate any facts outside the context.
2. REFUSAL MANDATE: If the user asks about anything not contained in the retrieved context (e.g., non-BIS topics, financial advice, coding, general trivia, unverified products), you MUST explicitly state that no official BIS record was found and politely decline.
3. Structure your reply strictly in the 4-Part Answer Pattern:
   - answer: 1-2 plain-language sentences directly answering the user based only on the context.
   - what_it_means: Simple translation of the standard or regulatory requirement for an MSME, startup, or consumer.
   - next_action: One concrete, actionable step the user should take right now.
4. Language constraint: You MUST write the entire JSON response (answer, what_it_means, next_action) directly in {target_lang_desc}.
   CRITICAL PRESERVATION: PRESERVE all Indian Standard codes (e.g., 'IS 9873 (Part 1):2019', 'IS 17803:2022'), clause numbers, HUIDs, licence numbers (CM/L), and statutory QCO numbers (e.g., 'S.O. 853(E)') completely unromanized and unchanged.
5. Output MUST be valid JSON conforming to:
{{
  "answer": "...",
  "what_it_means": "...",
  "next_action": "..."
}}
"""

        user_prompt = f"""User Persona: {persona}
User Query: {user_query}

Retrieved Verified BIS Context:
{json.dumps(context_payload, indent=2)}

Please synthesize the response JSON based solely on this verified context."""

        # Attempt candidate models in sequence
        candidate_models = get_candidate_models()
        last_error = None

        for model_id in candidate_models:
            try:
                completion = client.chat.completions.create(
                    model=model_id,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )

                raw_json = completion.choices[0].message.content
                parsed = json.loads(raw_json)

                return {
                    "answer": parsed.get("answer", ""),
                    "what_it_means": parsed.get("what_it_means", ""),
                    "next_action": parsed.get("next_action", ""),
                    "evidence_tag": evidence,
                    "provider": f"groq-{model_id}"
                }
            except Exception as model_err:
                print(f"Groq model '{model_id}' failed: {model_err}. Trying fallback...")
                last_error = model_err

        raise last_error or Exception("All candidate Groq models failed.")

    except Exception as e:
        print(f"Groq API call failed or unavailable ({e}), falling back to deterministic synthesis.")
        return deterministic_synthesis(context_payload, user_query, target_lang)

def deterministic_synthesis(context_payload: Dict[str, Any], user_query: str, target_lang: str = "en") -> Dict[str, Any]:
    """
    Deterministic rule-based generator that guarantees 100% reliable 4-part answers
    even with no external API keys or offline environment.
    """
    evidence = context_payload.get("evidence_tag", {})
    standard = context_payload.get("standard")
    steps = context_payload.get("steps", [])
    labs = context_payload.get("labs", [])
    clarifying_q = context_payload.get("clarifying_question")
    out_of_scope = context_payload.get("out_of_scope", False)

    if out_of_scope:
        if target_lang == "hi":
            return {
                "answer": "मैं बीआईएस साथी हूँ, जो केवल भारतीय मानकों, बीआईएस सेवाओं, प्रमाणन और गुणवत्ता परीक्षण से संबंधित प्रश्नों में सहायता करता हूँ।",
                "what_it_means": "आपका प्रश्न बीआईएस नियामक अधिकार क्षेत्र से बाहर है।",
                "next_action": "कृपया किसी उत्पाद, भारतीय मानक (IS कोड), हॉलमार्किंग या प्रयोगशाला परीक्षण से संबंधित प्रश्न पूछें।",
                "evidence_tag": {
                    "source_type": "faq",
                    "reference": "Scope Boundary",
                    "status": "not determined",
                    "verbatim_excerpt": "Out of scope request declined in accordance with BIS Saathi scope guidelines.",
                    "source_url": "https://www.bis.gov.in"
                },
                "provider": "deterministic-fallback"
            }
        return {
            "answer": "I am BIS Saathi, dedicated specifically to Indian Standards, BIS certification, hallmarking, testing labs, and consumer quality affairs.",
            "what_it_means": "Your query is outside the scope of Bureau of Indian Standards services.",
            "next_action": "Please ask a question related to product compliance, Indian Standards (IS codes), licence verification, or testing.",
            "evidence_tag": {
                "source_type": "faq",
                "reference": "Scope Boundary",
                "status": "not determined",
                "verbatim_excerpt": "Out of scope request declined in accordance with BIS Saathi scope guidelines.",
                "source_url": "https://www.bis.gov.in"
            },
            "provider": "deterministic-fallback"
        }

    if clarifying_q:
        if target_lang == "hi":
            return {
                "answer": f"आपके उत्पाद के लिए मानक निर्धारित करने हेतु एक अतिरिक्त जानकारी की आवश्यकता है: {clarifying_q}",
                "what_it_means": "उत्पाद के सटीक उपयोग या सामग्री के आधार पर लागू बीआईएस मानक और QCO आदेश भिन्न हो सकते हैं।",
                "next_action": "कृपया स्पष्ट करें ताकि सही मानक और प्रमाणन प्रक्रिया सुझाई जा सके।",
                "evidence_tag": evidence,
                "provider": "deterministic-fallback"
            }
        return {
            "answer": f"To confirm the applicable standard, please clarify: {clarifying_q}",
            "what_it_means": "Different variations or materials fall under distinct Indian Standards with differing mandatory QCO timelines.",
            "next_action": "Please reply with this detail so we can confirm the exact certification path.",
            "evidence_tag": evidence,
            "provider": "deterministic-fallback"
        }

    if standard:
        is_code = standard.get("is_code", "")
        title = standard.get("title", "")
        qco = standard.get("qco_status", "Mandatory")
        qco_ref = standard.get("qco_reference", "BIS Mandatory Order")

        lab_summary = f"Testing is available at {labs[0]['lab_name']} ({labs[0]['city']})" if labs else "Samples can be tested at BIS Central Laboratory (CL Sahibabad)."

        if target_lang == "hi":
            ans = f"आपके उत्पाद के लिए लागू भारतीय मानक {is_code} ({title}) है। यह {qco} प्रमाणन के अंतर्गत आता है ({qco_ref})।"
            meaning = f"यदि आप इस उत्पाद का भारत में निर्माण, आयात या विक्रय करते हैं, तो मानक {is_code} का अनुपालन अनिवार्य है। {lab_summary}"
            action = f"मानक ऑनलाइन (www.manakonline.in) पर फॉर्म V भरकर आवेदन करें या नमूना परीक्षण हेतु अधिकृत प्रयोगशाला से संपर्क करें।"
        else:
            ans = f"The applicable Indian Standard for your product is {is_code}: '{title}'. This standard is under {qco.upper()} certification per {qco_ref}."
            meaning = f"Manufacturing, importing, or selling this item in India requires compliance with {is_code}. {lab_summary}"
            action = f"Submit Form V via BIS Manak Online portal (www.manakonline.in) and arrange prototype testing at an accredited lab."

        return {
            "answer": ans,
            "what_it_means": meaning,
            "next_action": action,
            "evidence_tag": evidence,
            "provider": "deterministic-fallback"
        }

    # Generic or not found
    if target_lang == "hi":
        return {
            "answer": "आपके द्वारा खोजे गए उत्पाद का रिकॉर्ड स्थानीय बीआईएस निर्देशिका में नहीं मिला।",
            "what_it_means": "उत्पाद विवरण के लिए कोई विशिष्ट भारतीय मानक प्रत्यक्ष रूप से मैप नहीं हुआ।",
            "next_action": "कृपया उत्पाद का सटीक तकनीकी नाम या संबंधित श्रेणी प्रदान करें।",
            "evidence_tag": evidence,
            "provider": "deterministic-fallback"
        }
    return {
        "answer": "No registered Indian Standard was found matching your exact product description in our current directory.",
        "what_it_means": "The product may fall under a specialized division or a broader generic category.",
        "next_action": "Try describing the primary material (e.g., stainless steel, plastic) and intended use, or search by exact IS code.",
        "evidence_tag": evidence,
        "provider": "deterministic-fallback"
    }
