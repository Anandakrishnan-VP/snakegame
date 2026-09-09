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

        if context_payload.get("intent") == "GENERAL_FAQ":
            persona_directive = """
TARGET INQUIRY: GENERAL BIS INSTITUTIONAL / CITIZEN / APP GUIDANCE
- The user is asking a general informational question about the Bureau of Indian Standards (e.g. what BIS is, official mobile apps like the BIS Care App, web portals like Manak Online, ISI marks, or consumer grievance mechanisms).
- This is NOT a product compliance query. Do NOT state that "no standard was found for this product".
- "answer": Directly, clearly, and concisely answer the question asked using the provided institutional overview, FAQs, and your knowledge of BIS.
- "what_it_means": Explain why this matters (e.g. how the BIS Care App protects consumers from counterfeit goods, or the role of BIS in safeguarding national quality and safety).
- "next_action": Provide a concrete, helpful action step for the user (e.g., "Download the 'BIS Care App' from the Google Play Store or Apple App Store", or "Visit www.bis.gov.in for more details").
"""
        elif persona == "consumer":
            persona_directive = """
TARGET PERSONA: CONSUMER / BUYER / CITIZEN
- Primary Mission: Consumer safety, buyer protection, what to inspect on packaging, and licence verification.
- "answer": State which Indian Standard protects consumers for this product, whether the ISI mark / Hallmark / CRS mark is legally mandatory on this item, and what consumer health/safety hazards it prevents.
- "what_it_means": Explain what quality, health, and material safety guarantees the consumer receives (e.g., non-toxic food-grade materials, child safety, no electric shocks, fire safety). Crucially, explain what to look for on the product/box: the official ISI mark alongside the mandatory 7-digit CM/L licence number (or 6-character HUID for gold, or R-number for electronics).
- "next_action": Provide a concrete buyer verification step: instruct the consumer to download the official BIS Care App and enter the 7-digit CM/L number to verify manufacturer authenticity before buying, or lodge a quality grievance on the BIS Care portal if substandard.
"""
        else:
            persona_directive = """
TARGET PERSONA: MSME / MANUFACTURER / STARTUP
- Primary Mission: Industrial compliance, factory readiness, Scheme-I/CRS certification, and legal manufacturing roadmap.
- "answer": State the exact Indian Standard, statutory Quality Control Order (QCO) gazette order, and whether compliance is mandatory before manufacturing, importing, or selling in India.
- "what_it_means": Explain manufacturing and factory-level obligations: applicable certification scheme (Scheme-I ISI Mark or CRS), factory quality control audit readiness, in-house testing equipment requirements, raw material specifications, and legal liability under the BIS Act 2016. Explicitly highlight applicable MSME fee concessions (50% fee subsidy for Micro enterprises, 20% for Small & Startups).
- "next_action": Provide a concrete manufacturer roadmap step: submit Form V on the BIS Manak Online portal (www.manakonline.in), upload the factory test equipment list, claim MSME fee concessions, and schedule sample prototype testing at a recognized lab.
"""

        system_prompt = f"""You are BIS Saathi, an official AI assistant for the Bureau of Indian Standards (BIS).
Your goal is to provide accurate, grounded, and source-backed guidance strictly on Indian Standards, certification schemes, testing laboratories, and consumer affairs.

{persona_directive}

CRITICAL GUARDRAIL RULES:
1. STRICT GROUNDING: All facts, standard codes, clauses, portal names, and laboratory names MUST come directly from the official database context provided below or official BIS statutory knowledge. Do not invent unverified facts.
2. REFUSAL MANDATE: If the user asks about completely non-BIS topics (e.g., recipes, movies, programming, general trivia, financial investments), politely decline. For general BIS organizational, portal, and app inquiries, answer them thoroughly and helpfully using the context.
3. Structure your reply strictly in the 4-Part Answer Pattern:
   - answer: 1-2 plain-language sentences directly answering the user based only on the context and tailored to the persona.
   - what_it_means: Clear explanation tailored to the target persona (manufacturing obligations & fee subsidies for MSME; packaging marks & health safety for Consumer).
   - next_action: One concrete, actionable step the user should take right now (Form V on Manak Online for MSME; BIS Care App verification for Consumer).
4. Language constraint: You MUST write the entire JSON response (answer, what_it_means, next_action) directly in {target_lang_desc}.
   CRITICAL PRESERVATION: PRESERVE all Indian Standard codes (e.g., 'IS 9873 (Part 1):2019', 'IS 17803:2022'), clause numbers, HUIDs, licence numbers (CM/L), and statutory QCO numbers (e.g., 'S.O. 853(E)') completely unromanized and unchanged.
5. Output MUST be valid JSON conforming to:
{{
  "answer": "...",
  "what_it_means": "...",
  "next_action": "..."
}}
"""

        user_prompt = f"""Target Persona: {persona.upper()}
User Query: {user_query}

Retrieved Verified BIS Context:
{json.dumps(context_payload, indent=2)}

Please synthesize the response JSON specifically tailored for this {persona.upper()} persona based solely on this verified context."""

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
                    "persona": persona,
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

    persona = context_payload.get("persona", "general")

    if context_payload.get("intent") == "GENERAL_FAQ":
        q_clean = user_query.lower().strip()
        # 1. App query
        if any(w in q_clean for w in ["app", "mobile", "play store", "ios", "android", "download"]):
            if target_lang == "hi":
                return {
                    "answer": "हाँ, भारतीय मानक ब्यूरो का आधिकारिक मोबाइल ऐप 'BIS Care App' है, जो एंड्रॉइड (Google Play Store) और iOS (Apple App Store) दोनों पर निःशुल्क उपलब्ध है।",
                    "what_it_means": "BIS Care App के जरिए उपभोक्ता 7-अंकीय CM/L नंबर से ISI मार्क, 6-अंकीय HUID से सोने की शुद्धता (हॉलमार्क) और 8-अंकीय R-नंबर से इलेक्ट्रॉनिक्स CRS पंजीकरण की जांच कर सकते हैं, तथा घटिया सामान की सीधी शिकायत दर्ज कर सकते हैं।",
                    "next_action": "Google Play Store या Apple App Store से 'BIS Care App' डाउनलोड करें अथवा https://www.bis.gov.in/consumer-affairs/bis-care-app/ पर जाएं।",
                    "evidence_tag": evidence,
                    "persona": persona,
                    "provider": "deterministic-fallback"
                }
            return {
                "answer": "Yes, the official mobile application of the Bureau of Indian Standards is the **'BIS Care App'**, available for free on both Android (Google Play Store) and iOS (Apple App Store).",
                "what_it_means": "The BIS Care App empowers citizens to verify product authenticity in real time: verify 7-digit CM/L licence numbers for ISI marks, verify 6-character HUID codes for Gold Hallmarking, verify 8-digit R-numbers for electronics (CRS), locate accredited testing labs, and lodge quality complaints directly with BIS officers.",
                "next_action": "Download the **BIS Care App** from the Google Play Store or Apple App Store, or visit https://www.bis.gov.in/consumer-affairs/bis-care-app/.",
                "evidence_tag": evidence,
                "persona": persona,
                "provider": "deterministic-fallback"
            }

        # 2. What is BIS query
        if any(w in q_clean for w in ["what is bis", "about bis", "who is bis", "what does bis do", "full form of bis", "role of bis", "functions of bis"]):
            if target_lang == "hi":
                return {
                    "answer": "भारतीय मानक ब्यूरो (Bureau of Indian Standards - BIS) भारत का राष्ट्रीय मानक निकाय है, जो उपभोक्ता मामले, खाद्य एवं सार्वजनिक वितरण मंत्रालय के अंतर्गत BIS अधिनियम 2016 के तहत कार्य करता है।",
                    "what_it_means": "बीआईएस देश भर में वस्तुओं के मानकीकरण, गुणवत्ता प्रमाणन (ISI मार्क, CRS), स्वर्ण हॉलमार्किंग (HUID), और प्रयोगशाला परीक्षण के माध्यम से उपभोक्ताओं के स्वास्थ्य और सुरक्षा की रक्षा करता है।",
                    "next_action": "आधिकारिक भारतीय मानकों और प्रमाणन सेवाओं की जानकारी के लिए बीआईएस पोर्टल (https://www.bis.gov.in) पर जाएं।",
                    "evidence_tag": evidence,
                    "persona": persona,
                    "provider": "deterministic-fallback"
                }
            return {
                "answer": "The **Bureau of Indian Standards (BIS)** is the National Standard Body of India, established under the *BIS Act 2016* under the Ministry of Consumer Affairs, Food & Public Distribution, Government of India.",
                "what_it_means": "BIS is responsible for the harmonious development of standardization, product quality certification (ISI Mark, Compulsory Registration Scheme), Gold & Silver Hallmarking (HUID), and laboratory testing, ensuring high safety and reliability standards across India.",
                "next_action": "Explore official standards, QCO orders, and certification services at the official BIS portal (https://www.bis.gov.in) or apply for licences on Manak Online (https://www.manakonline.in).",
                "evidence_tag": evidence,
                "persona": persona,
                "provider": "deterministic-fallback"
            }

        # 3. Manak Online / Portals
        if any(w in q_clean for w in ["manak online", "manakonline", "portal", "website"]):
            return {
                "answer": "**Manak Online** (www.manakonline.in) is the official comprehensive e-governance portal of the Bureau of Indian Standards.",
                "what_it_means": "It provides a paperless digital workflow for manufacturers to submit Form V licence applications, pay statutory fees, book audit inspections, manage lab tests, and track certification renewals.",
                "next_action": "Visit https://www.manakonline.in to access e-BIS licensing, standards sales, and citizen grievance modules.",
                "evidence_tag": evidence,
                "persona": persona,
                "provider": "deterministic-fallback"
            }

        # 4. ISI Mark
        if any(w in q_clean for w in ["isi mark", "what is isi"]):
            return {
                "answer": "The **ISI mark** is India's premier industrial and consumer product quality certification mark governed under BIS Scheme-I.",
                "what_it_means": "It guarantees that a manufactured product conforms to the relevant Indian Standard (IS) for performance, electrical safety, and health. Products carrying the ISI mark must also display the manufacturer's unique 7-digit CM/L licence number.",
                "next_action": "Verify any ISI-marked product by checking its 7-digit CM/L number on the BIS Care App or on https://www.manakonline.in.",
                "evidence_tag": evidence,
                "persona": persona,
                "provider": "deterministic-fallback"
            }

        # 5. Hallmarking
        if any(w in q_clean for w in ["hallmark", "huid", "gold"]):
            return {
                "answer": "**Gold Hallmarking** is the official purity certification of gold jewellery in India, mandated by BIS.",
                "what_it_means": "Hallmarked jewellery features the BIS logo, purity grade (e.g., 22K916), and a laser-engraved 6-character alphanumeric Hallmark Unique Identification (HUID) code unique to each piece.",
                "next_action": "Verify any 6-character HUID code instantly using the BIS Care App or the BIS Saathi Verification tab.",
                "evidence_tag": evidence,
                "persona": persona,
                "provider": "deterministic-fallback"
            }

        # Default FAQ match from database
        faqs = context_payload.get("faqs", [])
        if faqs:
            best_faq = faqs[0]
            return {
                "answer": best_faq.get("answer", "BIS operates various citizen and industrial certification services across India."),
                "what_it_means": f"Sourced from BIS Citizen Charter & Consumer FAQ under category '{best_faq.get('category', 'General')}'.",
                "next_action": f"Visit {best_faq.get('source_url', 'https://www.bis.gov.in')} for more details.",
                "evidence_tag": evidence,
                "persona": persona,
                "provider": "deterministic-fallback"
            }

    if standard:
        is_code = standard.get("is_code", "")
        title = standard.get("title", "")
        qco = standard.get("qco_status", "Mandatory")
        qco_ref = standard.get("qco_reference", "BIS Mandatory Order")

        lab_summary = f"Testing is available at {labs[0]['lab_name']} ({labs[0]['city']})" if labs else "Samples can be tested at BIS Central Laboratory (CL Sahibabad)."

        if persona == "consumer":
            if target_lang == "hi":
                ans = f"उपभोक्ता सुरक्षा हेतु, इस उत्पाद के लिए भारतीय मानक {is_code} ({title}) निर्धारित है। यह {qco} प्रमाणन के अंतर्गत आता है।"
                meaning = f"यह मानक सुनिश्चित करता है कि उत्पाद विषैले तत्वों से मुक्त और उपयोग में पूर्णतः सुरक्षित है। खरीदते समय पैकेजिंग पर आधिकारिक ISI मार्क और उसके साथ 7-अंकीय CM/L लाइसेंस नंबर अवश्य देखें।"
                action = f"खरीदने से पहले आधिकारिक 'BIS Care App' पर CM/L नंबर दर्ज कर निर्माता की प्रमाणिकता सत्यापित करें।"
            else:
                ans = f"For consumer health and safety, this product is governed by Indian Standard {is_code}: '{title}' under {qco.upper()} certification."
                meaning = f"This standard protects consumers against substandard materials and hazardous chemical leaching. When buying, always verify the official ISI mark alongside the mandatory 7-digit CM/L licence number printed on the package."
                action = f"Download the BIS Care App and enter the 7-digit CM/L number to verify manufacturer authenticity before purchasing, or file a complaint on the BIS Care portal if defective."
        else:
            if target_lang == "hi":
                ans = f"विनिर्माताओं और MSME के लिए लागू मानक {is_code} ({title}) है। {qco_ref} के तहत इसका अनुपालन {qco} है।"
                meaning = f"भारत में निर्माण या बिक्री हेतु Scheme-I (ISI मार्क) अनिवार्य है। कारखाने में इन-हाउस परीक्षण उपकरण और गुणवत्ता नियंत्रण आवश्यक है। सूक्ष्म उद्यमों को 50% और लघु/स्टार्टअप को 20% शुल्क छूट प्राप्त है। {lab_summary}"
                action = f"मानक ऑनलाइन (www.manakonline.in) पर फॉर्म V भरकर आवेदन करें, MSME छूट का दावा करें और अधिकृत लैब में नमूना परीक्षण बुक करें।"
            else:
                ans = f"For MSMEs and manufacturers, the applicable standard is {is_code}: '{title}'. Certification is {qco.upper()} under {qco_ref}."
                meaning = f"Manufacturing, importing, or selling this item requires Scheme-I (ISI Mark) licensing. Requires factory quality control readiness and in-house testing equipment. Micro enterprises receive a 50% fee concession (20% for Small/Startups). {lab_summary}"
                action = f"Submit Form V on BIS Manak Online (www.manakonline.in), upload your factory test equipment list, claim MSME fee concessions, and schedule prototype testing at an accredited lab."

        return {
            "answer": ans,
            "what_it_means": meaning,
            "next_action": action,
            "evidence_tag": evidence,
            "persona": persona,
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
