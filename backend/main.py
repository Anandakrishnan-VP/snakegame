"""
FastAPI Server for BIS Saathi.
Implements complete 8-step request lifecycle, compliance chain, verification, and directory endpoints.
"""

import os
import uuid
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
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
from backend.services.intent_router import route_intent
from backend.services.module1_directory import search_directory, get_standard_by_code, get_flagship_chunks
from backend.services.module3_certification import get_certification_steps, get_scheme_overview
from backend.services.module4_verification import verify_code
from backend.services.module5_labs import find_testing_labs
from backend.services.compliance_chain import run_compliance_chain
from backend.services.llm_groq import synthesize_with_groq, deterministic_synthesis
from backend.services.guardrails import check_pre_retrieval_guardrails, validate_post_llm_grounding

app = FastAPI(
    title="BIS Saathi API",
    description="Intelligent Assistant for Indian Standards and BIS Services",
    version="1.0.0"
)

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

# Request/Response Schemas
class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    persona: Optional[str] = "general" # 'consumer', 'msme', 'general'
    language: Optional[str] = "auto" # 'auto', 'en', 'hi'
    city: Optional[str] = None
    state: Optional[str] = None

class VerifyRequest(BaseModel):
    code: str

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "BIS Saathi API"}

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
    raw_query = req.query.strip()
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

    # Step 3: Cache Check (Language-Aware Composite Key)
    cached_result, cached_active_topic = check_cache(raw_query, resolved_lang) or (None, None)
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
    augmented_query = english_query
    if active_topic:
        # Unconditionally prepend active topic to improve retrieval context
        augmented_query = f"{active_topic} {english_query}"

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
        cursor.execute("SELECT question, answer, source_url FROM faq")
        faqs = [dict(r) for r in cursor.fetchall()]
        conn.close()
        context_payload = {
            "intent": "GENERAL_FAQ",
            "faqs": faqs,
            "persona": current_persona,
            "evidence_tag": {
                "source_type": "faq",
                "reference": "BIS Citizen Charter & Consumer FAQ",
                "status": "confirmed",
                "clause_summary": "Guidelines sourced directly from BIS Consumer Affairs and Training manuals.",
                "verbatim_excerpt": "Guidelines sourced directly from BIS Consumer Affairs and Training manuals.",
                "source_url": "https://www.bis.gov.in/consumer-affairs/"
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

    # Step 8: Synthesis via Groq (with deterministic fallback)
    response_data = synthesize_with_groq(context_payload, raw_query, target_lang=resolved_lang)

    # Guardrail Layer 3: Post-LLM Grounding & Hallucination Interceptor
    response_data = validate_post_llm_grounding(response_data, language=resolved_lang)

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
    write_cache(raw_query, resolved_lang, response_data, active_topic=resolved_standard_code)

    return response_data

@app.get("/api/session/{session_id}")
def api_get_session(session_id: str):
    """Returns stored session state including persona, language, active_topic, and turn_history."""
    return get_or_create_session(session_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
