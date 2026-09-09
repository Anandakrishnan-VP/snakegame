"""
Session State, Active-Topic Memory, and Language-Aware Query Caching.
Maintains context across conversation turns and ensures cache hits correctly update session state.
"""

import hashlib
import json
import re
from typing import Optional, Dict, Any, Tuple
from backend.db.database import get_db_connection

def normalize_text(text: str) -> str:
    """Normalizes whitespace and lowercases query string for hashing."""
    return re.sub(r'\s+', ' ', text.strip().lower())

def make_cache_key(query: str, language: str, persona: str = "general") -> str:
    """Creates a SHA256 composite cache key from normalized text, resolved language, and persona."""
    norm = normalize_text(query)
    persona_norm = (persona or "general").lower().strip()
    raw = f"{norm}::{language.lower().strip()}::{persona_norm}"
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()

def get_or_create_session(session_id: str, persona: str = "general", language: str = "en") -> Dict[str, Any]:
    """Retrieves existing session or creates a new session record with full metadata."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT session_id, active_topic, persona, language, turn_count, turn_history 
        FROM session_state 
        WHERE session_id = ?
    """, (session_id,))
    row = cursor.fetchone()

    if not row:
        cursor.execute("""
            INSERT INTO session_state (session_id, active_topic, persona, language, turn_count, turn_history)
            VALUES (?, NULL, ?, ?, 0, '[]')
        """, (session_id, persona, language))
        conn.commit()
        conn.close()
        return {
            "session_id": session_id,
            "active_topic": None,
            "persona": persona,
            "language": language,
            "turn_count": 0,
            "turn_history": []
        }
    else:
        conn.close()
        try:
            history = json.loads(row["turn_history"] or "[]")
        except Exception:
            history = []
        return {
            "session_id": row["session_id"],
            "active_topic": row["active_topic"],
            "persona": row["persona"],
            "language": row["language"],
            "turn_count": row["turn_count"],
            "turn_history": history
        }

def update_session(
    session_id: str,
    active_topic: Optional[str] = None,
    persona: Optional[str] = None,
    language: Optional[str] = None,
    turn_record: Optional[Dict[str, Any]] = None,
    increment_turn: bool = True
):
    """Updates session parameters, persists turn history, and increments turn count."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # If turn_record is provided, append it to the stored turn_history JSON array
    if turn_record is not None:
        cursor.execute("SELECT turn_history FROM session_state WHERE session_id = ?", (session_id,))
        hist_row = cursor.fetchone()
        existing_history = []
        if hist_row and hist_row["turn_history"]:
            try:
                existing_history = json.loads(hist_row["turn_history"])
            except Exception:
                existing_history = []
        existing_history.append(turn_record)
        cursor.execute("UPDATE session_state SET turn_history = ? WHERE session_id = ?", (json.dumps(existing_history), session_id))

    updates = []
    params = []

    if active_topic is not None:
        updates.append("active_topic = ?")
        params.append(active_topic)

    if persona is not None:
        updates.append("persona = ?")
        params.append(persona)

    if language is not None:
        updates.append("language = ?")
        params.append(language)

    if increment_turn:
        updates.append("turn_count = turn_count + 1")

    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(session_id)

    query = f"UPDATE session_state SET {', '.join(updates)} WHERE session_id = ?"
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def check_cache(query: str, language: str, persona: str = "general") -> Optional[Tuple[Dict[str, Any], Optional[str]]]:
    """
    Checks cache for normalized query, language, and persona.
    Returns (response_dict, active_topic) or None.
    """
    cache_key = make_cache_key(query, language, persona=persona)
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT response_json, active_topic FROM query_cache WHERE cache_key = ?", (cache_key,))
    row = cursor.fetchone()
    conn.close()

    if row:
        try:
            data = json.loads(row["response_json"])
            return data, row["active_topic"]
        except Exception:
            return None
    return None

def write_cache(query: str, language: str, response_data: Dict[str, Any], active_topic: Optional[str] = None, persona: str = "general"):
    """Writes synthesized response to query_cache with composite key (never caches refusals)."""
    if not response_data or response_data.get("guardrail_refusal") or response_data.get("out_of_scope"):
        return
    if response_data.get("provider") == "guardrail-engine":
        return
    if response_data.get("evidence_tag", {}).get("status") == "not determined":
        return

    cache_key = make_cache_key(query, language, persona=persona)
    conn = get_db_connection()
    cursor = conn.cursor()

    from backend.db.database import is_postgres_configured
    if is_postgres_configured():
        cursor.execute("""
            INSERT INTO query_cache (cache_key, query_text, resolved_language, response_json, active_topic)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (cache_key) DO UPDATE SET
                query_text = EXCLUDED.query_text,
                resolved_language = EXCLUDED.resolved_language,
                response_json = EXCLUDED.response_json,
                active_topic = EXCLUDED.active_topic,
                created_at = CURRENT_TIMESTAMP
        """, (cache_key, query, language, json.dumps(response_data), active_topic))
    else:
        cursor.execute("""
            INSERT OR REPLACE INTO query_cache (cache_key, query_text, resolved_language, response_json, active_topic)
            VALUES (?, ?, ?, ?, ?)
        """, (cache_key, query, language, json.dumps(response_data), active_topic))

    conn.commit()
    conn.close()
