"""
FastAPI Server for BIS Saathi.
Implements complete 8-step request lifecycle, compliance chain, verification, and directory endpoints.
"""

import os
import re
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

load_dotenv()

from backend.db.database import init_db, get_db_connection
from backend.services.session_manager import (
    get_or_create_session,
    update_session,
    check_cache,
    write_cache
)
from backend.services.multilingual import (
    resolve_language,
    translate_to_english_if_needed
)
from backend.services.intent_router import route_intent, is_general_inquiry
from backend.services.module1_directory import search_directory, get_standard_by_code, get_flagship_chunks
from backend.services.module3_certification import get_certification_steps, get_scheme_overview
from backend.services.module4_verification import verify_code
from backend.services.module5_labs import find_testing_labs
from backend.services.compliance_chain import run_compliance_chain
from backend.services.llm_groq import synthesize_with_groq, deterministic_synthesis
from backend.services.guardrails import check_pre_retrieval_guardrails, validate_post_llm_grounding
from backend.services.transcription import transcribe_audio
from backend.services.journey_service import start_journey, update_step_status, get_journey
from backend.services.journey_pdf import generate_roadmap_pdf
from backend.services.conversational_handler import classify_conversational, generate_conversational_response
from backend.services.vlm_service import analyze_image_with_vlm

app = FastAPI(
    title="BIS Saathi API",
    description="Intelligent Assistant for Indian Standards and BIS Services",
    version="1.0.0"
)

# Vercel Serverless Path Normalization Middleware
@app.middleware("http")
async def vercel_path_normalization(request: Request, call_next):
    """
    Normalizes incoming request paths across Vercel serverless functions,
    handling cases where rewrites route to /api/index.py.
    Checks:
    1. Query param override (__path__)
    2. Vercel invoked route headers (x-invoke-path, x-forwarded-uri, x-real-url)
    3. Direct root health check
    """
    current_path = request.scope.get("path", "")

    # Only normalize if the path arrived as the handler script directly
    if current_path in ["/api/index.py", "/api/index", "/api/index.py/", "/api/index/"]:
        # 1. Check if Vercel passed __path__ in query parameters
        path_override = request.query_params.get("__path__")
        if path_override:
            request.scope["path"] = path_override.split("?")[0].strip()
        else:
            # 2. Check Vercel headers for the actual invoked route
            candidate_path = None
            for header_name in ["x-invoke-path", "x-forwarded-uri", "x-real-url", "x-original-uri"]:
                val = request.headers.get(header_name)
                if val:
                    val = val.split("?")[0].strip()
                    if val and val not in ["/api/index.py", "/api/index", "/api/index.py/", "/api/index/"]:
                        candidate_path = val
                        break

            if candidate_path:
                request.scope["path"] = candidate_path
            else:
                # If truly visiting /api or /api/index.py directly
                return JSONResponse({"status": "healthy", "service": "BIS Saathi API"})

    return await call_next(request)

# Explicit CORS Origins for Local Dev & Production / Vercel
configured_origins = [
    o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()
]
default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
allowed_origins = list(dict.fromkeys(default_origins + configured_origins))

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https:\/\/.*\.vercel\.app$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup: Ensure DB exists and seeded
@app.on_event("startup")
def startup_event():
    init_db()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    import traceback
    err_trace = traceback.format_exc()
    print(f"Unhandled exception on {request.url.path}: {err_trace}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

# Request/Response Schemas
class ChatRequest(BaseModel):
    query: Optional[str] = ""
    image_base64: Optional[str] = None
    session_id: Optional[str] = None
    persona: Optional[str] = None # 'consumer', 'msme', 'general' (defaults to session persona if None)
    language: Optional[str] = "auto" # 'auto', 'en', 'hi'
    city: Optional[str] = None
    state: Optional[str] = None

class VerifyRequest(BaseModel):
    code: str

class VisionAnalyzeRequest(BaseModel):
    image_base64: str
    query: Optional[str] = ""
    persona: Optional[str] = "general"
    language: Optional[str] = "en"

@app.get("/api")
@app.get("/api/")
@app.get("/health")
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "BIS Saathi API"}

@app.post("/api/vision/analyze")
def api_vision_analyze(req: VisionAnalyzeRequest):
    """
    Direct Vision-Language Model endpoint.
    Visually inspects photographs for products, labels, and BIS marks.
    """
    lang = req.language or "en"
    if req.query and req.language == "auto":
        lang = resolve_language(req.query, explicit_lang=req.language)
    elif lang == "auto":
        lang = "en"
    return analyze_image_with_vlm(
        image_base64=req.image_base64,
        user_query=req.query,
        persona=req.persona or "general",
        target_lang=lang
    )

@app.post("/api/transcribe")
async def api_transcribe(
    file: UploadFile = File(...),
    language: Optional[str] = Form("auto")
):
    """
    Speech-to-text endpoint powered by Groq Whisper Large v3.
    Accepts audio recordings and returns high-accuracy transcripts across Indian languages.
    """
    audio_bytes = await file.read()
    filename = file.filename or "audio.webm"
    result = transcribe_audio(audio_bytes, filename=filename, language=language)
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "Transcription failed"))
    return result

@app.post("/api/verify")
def api_verify(req: VerifyRequest):
    """Instant deterministic lookup for CM/L, HUID, or CRS R-Numbers."""
    return verify_code(req.code)

@app.get("/api/directory")
def api_directory(search: Optional[str] = None, division: Optional[str] = None):
    """Lists standards with optional search query or division filter."""
    if search:
        return search_directory(search, division_filter=division)
    conn = get_db_connection()
    cursor = conn.cursor()
    if division:
        cursor.execute("SELECT is_code, title, division, qco_status, qco_reference, synonyms, source_url FROM standards WHERE division LIKE ?", (f"%{division}%",))
    else:
        cursor.execute("SELECT is_code, title, division, qco_status, qco_reference, synonyms, source_url FROM standards ORDER BY is_code ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/labs")
def api_labs(is_code: Optional[str] = None, city: Optional[str] = None, state: Optional[str] = None):
    """Returns testing labs with City -> State -> Central fallback."""
    return find_testing_labs(is_code=is_code, city=city, state=state)

@app.get("/api/clause/{chunk_id}")
def api_clause(chunk_id: str):
    """Returns full original clause content for Tap-to-Inspect Source Inspector."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.chunk_id, c.standard_id, c.clause, c.sub_clause, c.page, c.content, c.source, c.source_url,
               s.title as standard_title, s.qco_status, s.qco_reference
        FROM standard_chunks c
        JOIN standards s ON c.standard_id = s.is_code
        WHERE c.chunk_id = ?
    """, (chunk_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Clause chunk not found")
    return dict(row)

def augment_query_if_followup(query: str, active_topic: Optional[str]) -> str:
    """
    Intelligently augments queries with active topic ONLY for pronouns or follow-up inquiries.
    Prevents new product inquiries or typos (e.g. 'electrnoics') from being polluted
    with previous unrelated session topics (e.g. helmets).
    """
    if not active_topic:
        return query

    # 0. Conversational pleasantries / acknowledgments should never be augmented
    if classify_conversational(query):
        return query

    # General institutional, app, or portal inquiries should never be augmented with product topics
    if is_general_inquiry(query):
        return query

    lower = query.lower().strip()

    # 1. Anaphora / Pronoun check: explicit reference to previous topic
    if re.search(r'\b(?:it|its|this|that|these|them|the product|the item|the standard|the licence|the license|the lab|the labs|the steps|same|above|here|there)\b', lower):
        return f"{active_topic} {query}"

    # 2. Check if the query on its own matches a standard in the directory with decent score
    # (e.g. user typed "electronics", "electrnoics", "water bottle", "cement", "IS 9873")
    candidates = search_directory(query)
    if candidates and candidates[0]["score"] >= 5.0:
        return query

    # 3. If query is a general procedural question without a product (e.g., "where is the testing lab in mumbai?", "how to get certified?", "what is the fee structure?")
    if re.search(r'\b(?:where is the lab|testing lab in|how to apply|what are the fees|how much does it cost|timeline|process|steps|procedure|validity)\b', lower):
        return f"{active_topic} {query}"

    # If the query contains substantive word(s) that didn't match, keep it clean so matcher handles it
    tokens = [t for t in lower.split() if len(t) >= 4]
    if tokens:
        return query

    return f"{active_topic} {query}"

@app.post("/api/chat")
def api_chat(req: ChatRequest):
    """
    Main conversational endpoint implementing full 8-step lifecycle:
    1. Session lookup/create
    2. Language resolution
    3. Composite cache check
    4. Translate-before-route
    5. Intent routing
    6. Active-topic memory augmentation
    7. Modular retrieval / Compliance Chain
    8. Groq synthesis, cache & session update
    """
    session_id = req.session_id or str(uuid.uuid4())
    raw_query = (req.query or "").strip()

    # Multimodal VLM Inspection Branch
    if req.image_base64 and req.image_base64.strip():
        session = get_or_create_session(session_id, persona=req.persona or "general", language=req.language or "en")
        current_persona = req.persona or session.get("persona", "general")
        resolved_lang = resolve_language(raw_query, explicit_lang=req.language) if raw_query else (req.language or "en")
        if resolved_lang == "auto":
            resolved_lang = "en"

        vlm_res = analyze_image_with_vlm(
            image_base64=req.image_base64,
            user_query=raw_query,
            persona=current_persona,
            target_lang=resolved_lang
        )

        detected_topic = vlm_res.get("active_topic") or session.get("active_topic")
        turn_rec = {
            "query": raw_query or "[Uploaded Product Image for Inspection]",
            "intent": "VLM_IMAGE_INSPECTION",
            "active_topic": detected_topic,
            "language": resolved_lang
        }
        update_session(
            session_id,
            active_topic=detected_topic,
            persona=current_persona,
            language=resolved_lang,
            turn_record=turn_rec,
            increment_turn=True
        )
        vlm_res["session_id"] = session_id
        vlm_res["resolved_language"] = resolved_lang
        vlm_res["active_topic"] = detected_topic
        vlm_res["from_cache"] = False
        vlm_res["persona"] = current_persona
        return vlm_res

    if not raw_query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Step 1: Session Fetch / Create
    session = get_or_create_session(session_id, persona=req.persona or "general", language=req.language or "en")
    active_topic = session["active_topic"]
    current_persona = req.persona or session.get("persona", "general")
    if req.persona and req.persona != session.get("persona"):
        update_session(session_id, persona=req.persona, increment_turn=False)
        session["persona"] = req.persona

    # Step 2: Language Resolution
    resolved_lang = resolve_language(raw_query, explicit_lang=req.language)

    # Guardrail Layer 1: Adversarial, Jailbreak, & Out-of-Domain Refusal Shield
    is_safe, refusal_response = check_pre_retrieval_guardrails(raw_query, language=resolved_lang)
    if not is_safe:
        refusal_response["session_id"] = session_id
        refusal_response["resolved_language"] = resolved_lang
        refusal_response["active_topic"] = active_topic
        refusal_response["from_cache"] = False
        return refusal_response

    # Step 2.5: Conversational Fast-Path ("ok", "got it", "thank you", "bye", "hi", etc.)
    # Gracefully replies to user acknowledgments without repeating previous answers or spitting out irrelevant standard info
    conv_type = classify_conversational(raw_query)
    if not conv_type and resolved_lang != "en":
        english_check = translate_to_english_if_needed(raw_query, resolved_lang)
        conv_type = classify_conversational(english_check)

    if conv_type:
        conv_resp = generate_conversational_response(
            conv_type=conv_type,
            raw_query=raw_query,
            active_topic=active_topic,
            persona=current_persona,
            language=resolved_lang
        )
        conv_resp["session_id"] = session_id
        conv_resp["intent"] = f"CONVERSATIONAL_{conv_type}"
        conv_resp["resolved_language"] = resolved_lang
        conv_resp["active_topic"] = active_topic  # Preserve active topic!
        conv_resp["from_cache"] = False

        turn_rec = {
            "query": raw_query,
            "intent": f"CONVERSATIONAL_{conv_type}",
            "active_topic": active_topic,
            "language": resolved_lang
        }
        update_session(
            session_id,
            active_topic=active_topic,
            persona=current_persona,
            language=resolved_lang,
            turn_record=turn_rec,
            increment_turn=True
        )
        return conv_resp

    # Step 3: Cache Check (Language-Aware & Persona-Aware Composite Key)
    cached_result, cached_active_topic = check_cache(raw_query, resolved_lang, persona=current_persona) or (None, None)
    if cached_result:
        # Crucial §3.2 rule: Update turn and active topic even on cache hit!
        turn_rec = {
            "query": raw_query,
            "intent": cached_result.get("intent", "CACHE_HIT"),
            "active_topic": cached_active_topic or active_topic,
            "language": resolved_lang
        }
        update_session(
            session_id,
            active_topic=cached_active_topic or active_topic,
            persona=current_persona,
            language=resolved_lang,
            turn_record=turn_rec,
            increment_turn=True
        )
        cached_result["from_cache"] = True
        cached_result["session_id"] = session_id
        return cached_result

    # Step 4: Translate to English for Retrieval
    english_query = translate_to_english_if_needed(raw_query, resolved_lang)

    # Step 5: Intent Routing on English query
    routing_result = route_intent(english_query)
    intent = routing_result["intent"]

    # Step 6: Active-Topic Augmentation for pronouns / follow-ups
    augmented_query = augment_query_if_followup(english_query, active_topic)

    # Step 7: Modular Execution
    resolved_standard_code = active_topic
    context_payload = {"persona": current_persona}

    if intent == "OUT_OF_SCOPE":
        context_payload = {
            "out_of_scope": True,
            "persona": current_persona,
            "evidence_tag": {
                "source_type": "faq",
                "reference": "Scope Boundary",
                "status": "not determined",
                "clause_summary": "Out of scope query declined.",
                "verbatim_excerpt": "Out of scope query declined.",
                "source_url": "https://www.bis.gov.in"
            }
        }

    elif intent == "VERIFICATION":
        ver_result = verify_code(raw_query)
        context_payload = {
            "verification": ver_result,
            "persona": current_persona,
            "evidence_tag": {
                "source_type": "registry",
                "reference": ver_result.get("extracted_code") or "None",
                "status": "confirmed" if ver_result.get("found") else "not determined",
                "clause_summary": ver_result.get("message"),
                "verbatim_excerpt": ver_result.get("message"),
                "source_url": "https://www.manakonline.in"
            }
        }
        if ver_result.get("is_code"):
            resolved_standard_code = ver_result["is_code"]

    elif intent == "LAB_SEARCH":
        labs = find_testing_labs(is_code=active_topic, city=req.city, state=req.state)
        context_payload = {
            "intent": "LAB_SEARCH",
            "standard_code": active_topic,
            "labs": labs[:5],
            "persona": current_persona,
            "evidence_tag": {
                "source_type": "directory",
                "reference": active_topic or "BIS Recognized Testing Labs",
                "status": "confirmed" if labs else "not determined",
                "clause_summary": f"Found {len(labs)} accredited testing facilities mapped in the BIS Laboratory Recognition Scheme.",
                "verbatim_excerpt": f"Found {len(labs)} accredited testing facilities mapped in the BIS Laboratory Recognition Scheme.",
                "source_url": "https://www.bis.gov.in/laboratory-recognition-scheme/"
            }
        }

    elif intent == "CERTIFICATION_PROCESS":
        steps = get_certification_steps("Scheme-I" if "crs" not in augmented_query.lower() else "CRS")
        scheme_info = get_scheme_overview("Scheme-I" if "crs" not in augmented_query.lower() else "CRS")
        context_payload = {
            "intent": "CERTIFICATION_PROCESS",
            "scheme": scheme_info,
            "steps": steps,
            "persona": current_persona,
            "evidence_tag": {
                "source_type": "directory",
                "reference": scheme_info["governing_law"],
                "status": "confirmed",
                "clause_summary": f"Operating under {scheme_info['governing_law']}. Application via {scheme_info['portal']}.",
                "verbatim_excerpt": f"Operating under {scheme_info['governing_law']}. Application via {scheme_info['portal']}.",
                "source_url": scheme_info["portal"]
            }
        }

    elif intent == "GENERAL_FAQ":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT category, question, answer, source_url FROM faq")
        faqs = [dict(r) for r in cursor.fetchall()]
        conn.close()

        q_lower = augmented_query.lower()
        source_url = "https://www.bis.gov.in"
        source_ref = "Bureau of Indian Standards (BIS Act 2016)"

        if any(w in q_lower for w in ["app", "mobile", "bis care", "android", "ios", "play store", "download"]):
            source_url = "https://www.bis.gov.in/consumer-affairs/bis-care-app/"
            source_ref = "BIS Care App (Official Mobile App)"
        elif any(w in q_lower for w in ["manak online", "manakonline", "portal", "website"]):
            source_url = "https://www.manakonline.in"
            source_ref = "BIS Manak Online Portal"
        elif any(w in q_lower for w in ["hallmark", "huid", "gold"]):
            source_url = "https://www.bis.gov.in/hallmarking/overview/"
            source_ref = "BIS Gold Hallmarking Scheme"
        elif any(w in q_lower for w in ["isi mark", "isi"]):
            source_url = "https://www.bis.gov.in/product-certification/overview/"
            source_ref = "BIS Scheme-I (ISI Mark)"
        elif any(w in q_lower for w in ["complaint", "grievance"]):
            source_url = "https://www.bis.gov.in/consumer-affairs/grievance-redressal/"
            source_ref = "BIS Consumer Grievance Portal"

        context_payload = {
            "intent": "GENERAL_FAQ",
            "faqs": faqs,
            "institutional_overview": {
                "organization": "Bureau of Indian Standards (BIS)",
                "statutory_mandate": "National Standard Body of India established under the BIS Act 2016 (originally founded as the Indian Standards Institution - ISI in 1947), operating under the Ministry of Consumer Affairs, Food & Public Distribution, Government of India.",
                "headquarters": "Manak Bhavan, 9 Bahadur Shah Zafar Marg, New Delhi 110002.",
                "official_app": {
                    "app_name": "BIS Care App",
                    "platforms": "Available for free on Android (Google Play Store) and iOS (Apple App Store)",
                    "purpose": "Official mobile app for Indian citizens and consumers to verify product quality marks and report counterfeits.",
                    "features": [
                        "Verify ISI Mark authenticity by entering the 7-digit CM/L licence number.",
                        "Verify Gold Hallmark purity, fineness, and registered jeweller by entering the 6-character alphanumeric HUID code.",
                        "Verify Compulsory Registration Scheme (CRS) electronics by entering the 8-digit R-number.",
                        "Locate BIS-recognized and accredited testing laboratories across India.",
                        "Lodge consumer quality complaints and track grievance redressal status directly with BIS officers."
                    ],
                    "download_url": "https://www.bis.gov.in/consumer-affairs/bis-care-app/"
                },
                "official_portals": [
                    {"name": "BIS Official Portal", "url": "https://www.bis.gov.in", "purpose": "Standards catalog, QCO notifications, institutional information"},
                    {"name": "Manak Online", "url": "https://www.manakonline.in", "purpose": "e-BIS online licensing (Form V), audit tracking, laboratory testing, standards sales"},
                    {"name": "CRS Portal", "url": "https://www.crsbis.in", "purpose": "Compulsory Registration Scheme for electronics, IT goods, and solar modules"}
                ]
            },
            "persona": current_persona,
            "evidence_tag": {
                "source_type": "faq",
                "reference": source_ref,
                "status": "confirmed",
                "clause_number": "Citizen Advisory",
                "clause_summary": f"Official institutional guidelines and services of the {source_ref}.",
                "verbatim_excerpt": f"Official institutional guidelines and services of the {source_ref}.",
                "source_url": source_url
            }
        }

    else:
        # Default: PRODUCT_TO_STANDARD or STANDARD_SEARCH -> Run the Compliance Chain!
        chain_result = run_compliance_chain(
            query=augmented_query,
            city=req.city,
            state=req.state,
            persona=current_persona
        )
        context_payload = chain_result
        context_payload["persona"] = current_persona
        if chain_result.get("standard"):
            resolved_standard_code = chain_result["standard"]["is_code"]
        else:
            # Tier-2 Fallback: Live Official BIS Web Search
            # Strictly Second-Option: executed ONLY when local SQLite produces 0 standard hits
            from backend.services.web_search import search_bis_web
            web_match = search_bis_web(english_query)
            if web_match:
                context_payload = web_match
                context_payload["persona"] = current_persona
                resolved_standard_code = web_match.get("is_code")

    # Step 8: Synthesis via Groq (with deterministic fallback)
    if context_payload.get("source_type") == "live_web":
        from backend.services.llm_groq import synthesize_web_fallback
        response_data = synthesize_web_fallback(context_payload, raw_query, persona=current_persona, target_lang=resolved_lang)
    else:
        response_data = synthesize_with_groq(context_payload, raw_query, target_lang=resolved_lang)

    # Guardrail Layer 3: Post-LLM Grounding & Hallucination Interceptor
    if context_payload.get("source_type") != "live_web":
        response_data = validate_post_llm_grounding(response_data, language=resolved_lang, context_payload=context_payload)

    # Attach metadata
    response_data["session_id"] = session_id
    response_data["intent"] = intent
    response_data["resolved_language"] = resolved_lang
    response_data["active_topic"] = resolved_standard_code
    response_data["from_cache"] = False

    # Update session state and write to language-aware cache
    turn_rec = {
        "query": raw_query,
        "intent": intent,
        "active_topic": resolved_standard_code,
        "language": resolved_lang
    }
    update_session(
        session_id,
        active_topic=resolved_standard_code,
        persona=current_persona,
        language=resolved_lang,
        turn_record=turn_rec,
        increment_turn=True
    )
    if not response_data.get("guardrail_refusal"):
        write_cache(raw_query, resolved_lang, response_data, active_topic=resolved_standard_code, persona=current_persona)

    return response_data

@app.get("/api/session/{session_id}")
def api_get_session(session_id: str):
    """Returns stored session state including persona, language, active_topic, and turn_history."""
    return get_or_create_session(session_id)

# --- Certification Journey Wizard Endpoints ---

class StartJourneyRequest(BaseModel):
    session_id: str
    journey_type: str = "get_certified"
    standard_id: Optional[str] = None
    force_new: bool = False

class UpdateStepRequest(BaseModel):
    status: str

@app.post("/api/journey/start")
def api_start_journey(req: StartJourneyRequest):
    """Starts or resumes a persistent compliance journey with deduplication."""
    return start_journey(
        session_id=req.session_id,
        journey_type=req.journey_type,
        standard_id=req.standard_id,
        force_new=req.force_new
    )

@app.patch("/api/journey/{journey_id}/step/{step_id}")
def api_update_step(journey_id: str, step_id: str, req: UpdateStepRequest):
    """Toggles step completion status and recalculates readiness score (0-100%)."""
    updated = update_step_status(journey_id, step_id, req.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Journey or step not found.")
    return updated

@app.get("/api/journey/{journey_id}")
def api_get_journey(journey_id: str):
    """Retrieves current state of a certification journey."""
    journey = get_journey(journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found.")
    return journey

@app.get("/api/journey/{journey_id}/pdf")
def api_get_journey_pdf(journey_id: str):
    """Generates and streams a downloadable 1-page roadmap PDF."""
    journey = get_journey(journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found.")
    
    pdf_bytes = generate_roadmap_pdf(journey)
    filename = f"bis_saathi_roadmap_{journey_id[:8]}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@app.get("/api/qco-bulletin")
def api_get_qco_bulletin(refresh: bool = False):
    """
    Returns live Gazette and Quality Control Order notifications.
    Supports on-demand real-time re-sync via ?refresh=true.
    """
    from backend.services.qco_bulletin import get_qco_bulletin
    return get_qco_bulletin(force_refresh=refresh)

# Static Frontend Mount & SPA Fallback (When deployed or serving locally)
FRONTEND_DIST = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    assets_dir = FRONTEND_DIST / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Never intercept API routes
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API endpoint not found")
        # If static file exists directly (e.g. favicon.svg, icons.svg)
        target = FRONTEND_DIST / full_path
        if target.is_file():
            return FileResponse(str(target))
        # Fallback to index.html for SPA client-side routes
        return FileResponse(str(FRONTEND_DIST / "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
