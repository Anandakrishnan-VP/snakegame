"""
BIS Saathi Vision-Language Model (VLM) Service
Powered by Groq Multimodal Vision (Qwen 3.8 27B / Qwen 3.6 27B).
Analyzes user images of products, labels, packaging, ISI marks, Hallmarks, and certificates
to detect compliance, applicable Indian Standards, and mandatory Quality Control Orders (QCOs).
"""

import os
import re
import json
import base64
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from backend.services.module1_directory import search_directory, get_standard_by_code
from backend.services.module5_labs import find_testing_labs

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_VISION_MODELS = ["qwen/qwen3.6-27b", "qwen/qwen3.8-27b"]

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

def clean_base64_image(image_raw: str) -> str:
    """Ensures base64 string is formatted as a valid data URL for Groq image_url."""
    image_raw = image_raw.strip()
    if image_raw.startswith("data:image/"):
        return image_raw
    # If raw base64 string without header, infer jpeg
    return f"data:image/jpeg;base64,{image_raw}"

def analyze_image_with_vlm(
    image_base64: str,
    user_query: Optional[str] = "",
    persona: str = "general",
    target_lang: str = "en"
) -> Dict[str, Any]:
    """
    Multimodal analysis of an uploaded or camera-captured product image.
    Detects product type, printed quality marks, IS codes, and compliance status.
    """
    if not image_base64 or not image_base64.strip():
        return {
            "answer": "No image data was provided for visual compliance inspection.",
            "what_it_means": "Please upload a clear photograph or use the camera button to capture an image of the product, packaging, or certification label.",
            "next_action": "Click the '+' button and select 'Take Photo' or 'Upload Image'.",
            "evidence_tag": {
                "source_type": "vlm",
                "reference": "Image Input Required",
                "status": "not determined",
                "clause_summary": "Missing image input payload.",
                "verbatim_excerpt": "Missing image input payload.",
                "source_url": "https://www.bis.gov.in"
            }
        }

    if not GROQ_API_KEY:
        return fallback_vlm_analysis(user_query, persona, target_lang)

    formatted_image_url = clean_base64_image(image_base64)
    target_lang_desc = INDIC_LANGUAGE_NAMES.get(target_lang, "English")

    persona_directive = (
        """
TARGET PERSONA: CONSUMER / CITIZEN BUYER
- Focus: Consumer safety, how to tell if this item is genuine, what marks are missing or present, and how to verify on the BIS Care app.
"""
        if persona == "consumer"
        else """
TARGET PERSONA: MSME / INDUSTRIAL MANUFACTURER
- Focus: Manufacturing compliance, factory audit obligations, mandatory QCO regulations, testing lab parameters, and MSME fee subsidies.
"""
    )

    system_prompt = f"""You are the expert Vision-Language Model (VLM) for BIS Saathi, the official intelligent assistant for the Bureau of Indian Standards (BIS).
Your job is to visually inspect photographs of physical products, industrial goods, labels, packaging boxes, gold jewellery, or certificates.

{persona_directive}

MANDATORY INSPECTION RULES:
1. ALWAYS IDENTIFY THE PRODUCT:
   - What physical product or item is shown in the image? (e.g. Motorcycle / Two-Wheeler Protective Helmet, Stainless Steel Water Bottle, Children's Toy, Packaged Drinking Water, Gold Ring / Jewellery, Electric Iron, Ceiling Fan, Cement Bag, etc.)
   - The very first sentence of "answer" MUST explicitly name the detected product! (e.g., "This image displays a Motorcycle / Two-Wheeler Protective Helmet.")
2. ALWAYS SPECIFY THE APPLICABLE INDIAN STANDARD (IS CODE):
   - Even if the standard number is NOT written on the product, you must state the governing Indian Standard:
     * Two-wheeler / motorcycle helmets: IS 4151:2015 (Protective Helmets for Motorcycle Riders)
     * Stainless steel vacuum water bottles: IS 17803:2022
     * Toys: IS 9873 (Parts 1-9)
     * Gold jewellery hallmarking: IS 1417
     * Packaged drinking water: IS 14543
     * Pressure cookers: IS 2347
     * Electric iron: IS 302 (Part 2/Sec 3)
     * Cement: IS 1489 / IS 269
3. VISUAL QUALITY MARK DETECTION (PRESENT vs MISSING):
   - Inspect the image for:
     * Rectangular ISI Mark logo
     * 7-digit CM/L license number (e.g., CM/L-1234567)
     * 6-digit Hallmark HUID code (e.g., AB1234)
     * CRS 'R-XXXXXXXX' registration number for electronics
   - If NO mark is visible in the provided photo, clearly explain:
     * State that no ISI mark or CM/L license is visible on this angle of the item.
     * State whether this product category is under a mandatory Quality Control Order (QCO). For two-wheeler helmets, it is STRICTLY MANDATORY under the Ministry of Road Transport & Highways (MoRTH) QCO 2020. Riding or selling a non-ISI helmet is illegal in India!
     * Instruct the user where to look (e.g. for helmets, the ISI mark is stamped on the rear outer shell).

REQUIRED JSON OUTPUT SCHEMA:
You MUST output ONLY a valid JSON object matching this exact structure:
{{
  "detected_product": "Exact product name (e.g. 'Motorcycle Protective Helmet', 'Stainless Steel Water Bottle')",
  "detected_marks": ["List of any detected marks, IS codes, or CM/L numbers; or ['None Visible'] if no mark on shell"],
  "is_code": "Governing standard code e.g. 'IS 4151:2015' or 'IS 17803:2022'",
  "is_qco_mandatory": true,
  "answer": "Clear summary starting with the identified product name, governing Indian Standard, whether quality marks are visible, and mandatory QCO compliance.",
  "what_it_means": "Detailed explanation tailored to the persona (safety impact & box/shell check for consumers; factory audit & Scheme-I licence obligations for MSME).",
  "next_action": "One concrete next action (e.g. Check the rear of the helmet for the ISI mark and verify the CM/L number on the BIS Care App).",
  "evidence_tag": {{
    "source_type": "vlm_inspection",
    "reference": "Governing IS code e.g. IS 4151:2015",
    "status": "confirmed",
    "clause_summary": "Statutory regulation under Indian Standards and Quality Control Orders.",
    "verbatim_excerpt": "Visual inspection finding.",
    "source_url": "https://www.bis.gov.in"
  }}
}}

LANGUAGE RULE:
Write 'answer', 'what_it_means', and 'next_action' directly in {target_lang_desc}.
Preserve standard codes (e.g., 'IS 4151:2015') and numbers unchanged.
Do NOT enclose output in Markdown code blocks (```json). Output pure JSON only.
"""

    user_text = user_query.strip() if user_query and user_query.strip() else "Please identify what product is shown in this image, check the applicable Indian Standard (IS code), inspect any visible or missing ISI marks/CM/L numbers, and evaluate compliance."

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_text},
                {"type": "image_url", "image_url": {"url": formatted_image_url}}
            ]
        }
    ]

    try:
        from groq import Groq
        client = Groq(api_key=GROQ_API_KEY)

        parsed_data = None
        for model_name in GROQ_VISION_MODELS:
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=messages,
                    temperature=0.2,
                    max_tokens=1000
                )
                raw_text = response.choices[0].message.content.strip()
                
                # Strip think blocks if model output them
                if "<think>" in raw_text and "</think>" in raw_text:
                    raw_text = raw_text.split("</think>")[-1].strip()

                # Clean markdown backticks if any
                if raw_text.startswith("```json"):
                    raw_text = raw_text[7:]
                if raw_text.startswith("```"):
                    raw_text = raw_text[3:]
                if raw_text.endswith("```"):
                    raw_text = raw_text[:-3]
                raw_text = raw_text.strip()

                # Extract first { ... } block
                json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                if json_match:
                    parsed_data = json.loads(json_match.group(0))
                    parsed_data["provider"] = f"groq_vlm_{model_name}"
                    break
            except Exception as model_err:
                print(f"Groq Vision model {model_name} error: {model_err}")
                continue

        if not parsed_data or not parsed_data.get("answer"):
            return fallback_vlm_analysis(user_query, persona, target_lang)

        # Cross-reference with our official SQLite database if standard or product was identified
        is_code = parsed_data.get("is_code")
        if is_code in ["null", "None", "none", "", None]:
            is_code = None
        
        product_name = parsed_data.get("detected_product", "")
        if product_name in ["null", "None", "none", "", None]:
            product_name = ""

        db_match = None

        if is_code:
            db_match = get_standard_by_code(is_code)
        
        if not db_match and product_name:
            candidates = search_directory(product_name)
            if candidates:
                db_match = candidates[0]

        # Also search in user query or answer for product keywords if not matched yet
        if not db_match:
            full_text = f"{product_name} {parsed_data.get('answer', '')} {user_text}".lower()
            for kw in ["helmet", "bottle", "toy", "gold", "jewellery", "water", "cooker", "iron", "cable", "cement", "battery"]:
                if kw in full_text:
                    cands = search_directory(kw)
                    if cands:
                        db_match = cands[0]
                        break

        if db_match:
            # Enrich evidence tag with official statutory data
            parsed_data["active_topic"] = db_match.get("is_code")
            parsed_data["is_code"] = db_match.get("is_code")
            if not parsed_data.get("detected_product"):
                parsed_data["detected_product"] = db_match.get("title")

            ev = parsed_data.get("evidence_tag", {}) or {}
            ev["reference"] = db_match.get("is_code", "Bureau of Indian Standards")
            ev["source_url"] = db_match.get("source_url", "https://www.bis.gov.in")
            ev["status"] = "confirmed"
            if db_match.get("qco_reference"):
                ev["qco_reference"] = db_match["qco_reference"]
                ev["clause_summary"] = f"Governed under statutory QCO: {db_match['qco_reference']}. Standard: {db_match['is_code']} ({db_match['title']}). Compliance is legally mandatory in India."
            parsed_data["evidence_tag"] = ev

            # Guarantee product and standard are stated in the answer
            ans = parsed_data.get("answer", "")
            if db_match["is_code"].lower() not in ans.lower():
                prefix = f"Identified Product: {db_match['title']} ({db_match['is_code']}). "
                parsed_data["answer"] = prefix + ans

        return parsed_data

    except Exception as e:
        print(f"VLM Analysis top-level exception: {e}")
        return fallback_vlm_analysis(user_query, persona, target_lang)

def fallback_vlm_analysis(user_query: str, persona: str, target_lang: str) -> Dict[str, Any]:
    """Fallback response if vision model is unreachable."""
    is_consumer = persona == "consumer"
    return {
        "detected_product": "Product Image Received",
        "detected_marks": ["ISI / Hallmark Inspection"],
        "answer": (
            "Image received. To inspect compliance, look for the official rectangular ISI mark alongside the mandatory 7-digit CM/L licence number (or 6-character HUID code for gold jewellery)."
            if is_consumer else
            "Image received. For industrial manufacturing, check whether your product category falls under mandatory Quality Control Orders (QCO) requiring Scheme-I ISI Mark certification."
        ),
        "what_it_means": (
            "Every authentic ISI-marked product must have the standard IS code printed on top and the manufacturer's unique 7-digit CM/L number printed directly below the logo."
            if is_consumer else
            "Under the BIS Act 2016, manufacturing or importing products without mandatory ISI mark or CRS registration carries heavy legal liabilities. MSME fee subsidies of 20% to 50% are available."
        ),
        "next_action": (
            "Download the official BIS Care mobile application and select 'Verify Licence (CM/L)' or 'Verify HUID' to check manufacturer authenticity."
            if is_consumer else
            "Visit the BIS Manak Online portal (www.manakonline.in) to file Form V and check in-house test equipment requirements."
        ),
        "evidence_tag": {
            "source_type": "vlm_inspection",
            "reference": "Bureau of Indian Standards Act 2016",
            "status": "confirmed",
            "clause_summary": "Statutory marking regulations under the BIS Act 2016 and mandatory Quality Control Orders.",
            "verbatim_excerpt": "Official verification of marking on products and packaging.",
            "source_url": "https://www.bis.gov.in"
        },
        "provider": "deterministic_vlm_fallback"
    }
