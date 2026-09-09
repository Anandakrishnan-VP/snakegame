"""
Module 1: Two-Tier Directory Search
Provides deterministic keyword and synonym matching across Indian Standards.
"""

from typing import List, Dict, Any, Optional
from backend.db.database import get_db_connection

def search_directory(query: str, division_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Matches query against is_code, title, and synonyms.
    Returns ranked list of candidate standards.
    """
    if not query or not query.strip():
        return []

    tokens = [t.strip().lower() for t in query.lower().split() if len(t.strip()) > 1]
    if not tokens:
        tokens = [query.lower().strip()]

    conn = get_db_connection()
    cursor = conn.cursor()

    query_sql = """
        SELECT is_code, title, division, qco_status, qco_reference, related_standards, synonyms, source_url
        FROM standards
    """
    params = []
    if division_filter:
        query_sql += " WHERE division LIKE ?"
        params.append(f"%{division_filter}%")

    cursor.execute(query_sql, params)
    rows = cursor.fetchall()
    conn.close()

    scored_results = []
    lower_query = query.lower().strip()

    for row in rows:
        score = 0.0
        is_code = row["is_code"].lower()
        title = row["title"].lower()
        synonyms = [s.strip().lower() for s in row["synonyms"].split(",") if s.strip()]

        # Exact IS code match
        if is_code in lower_query or lower_query in is_code:
            score += 15.0

        # Exact title substring match
        if lower_query in title:
            score += 10.0

        # Synonym matching
        matched_tokens_in_synonyms = set()
        for syn in synonyms:
            if syn == lower_query:
                score += 12.0
            elif syn in lower_query:
                score += 8.0
            else:
                for t in tokens:
                    t_stem = t.rstrip('s') if len(t) > 3 else t
                    if t in syn or (len(t_stem) > 2 and t_stem in syn):
                        matched_tokens_in_synonyms.add(t)

        score += min(len(matched_tokens_in_synonyms) * 3.0, 9.0)

        # Token overlap in title
        for token in tokens:
            if token in title:
                score += 2.0
            if token in is_code:
                score += 4.0

        if score > 0:
            related_list = [r.strip() for r in (row["related_standards"] or "").split(",") if r.strip()]
            scored_results.append({
                "is_code": row["is_code"],
                "title": row["title"],
                "division": row["division"],
                "qco_status": row["qco_status"],
                "qco_reference": row["qco_reference"],
                "related_standards": related_list,
                "synonyms": row["synonyms"],
                "source_url": row["source_url"],
                "score": score
            })

    scored_results.sort(key=lambda x: x["score"], reverse=True)
    return scored_results

def get_standard_by_code(is_code: str) -> Optional[Dict[str, Any]]:
    """Retrieves full record for a specific standard code."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT is_code, title, division, qco_status, qco_reference, related_standards, synonyms, source_url
        FROM standards
        WHERE is_code = ? OR is_code LIKE ?
    """, (is_code, f"%{is_code}%"))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "is_code": row["is_code"],
        "title": row["title"],
        "division": row["division"],
        "qco_status": row["qco_status"],
        "qco_reference": row["qco_reference"],
        "related_standards": [r.strip() for r in (row["related_standards"] or "").split(",") if r.strip()],
        "synonyms": row["synonyms"],
        "source_url": row["source_url"]
    }

def get_flagship_chunks(is_code: str) -> List[Dict[str, Any]]:
    """Retrieves Tier B deep clause chunks for flagship standards."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT chunk_id, standard_id, clause, sub_clause, page, content, source, source_url
        FROM standard_chunks
        WHERE standard_id = ?
        ORDER BY clause ASC
    """, (is_code,))
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "chunk_id": r["chunk_id"],
            "standard_id": r["standard_id"],
            "clause": r["clause"],
            "sub_clause": r["sub_clause"],
            "page": r["page"],
            "content": r["content"],
            "source": r["source"],
            "source_url": r["source_url"]
        }
        for r in rows
    ]

def retrieve_relevant_chunks(standard_id: str, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """
    Explicit clause-level retrieval logic.
    Decides which specific chunk(s) from standard_chunks get passed to the LLM
    for a given question, based on term overlap, keyword relevance, and clause number matching.
    """
    all_chunks = get_flagship_chunks(standard_id)
    if not all_chunks:
        return []

    query_lower = query.lower().strip()
    query_tokens = [t.strip(",.?!:;\"'") for t in query_lower.split() if len(t.strip(",.?!:;\"'")) > 2]

    scored_chunks = []
    for chunk in all_chunks:
        score = 0.0
        content_lower = chunk["content"].lower()
        clause = chunk["clause"].lower()
        sub_clause = (chunk.get("sub_clause") or "").lower()

        # 1. Exact clause number mention in query (e.g. "clause 4.2" or "5.2")
        if clause in query_lower or (sub_clause and sub_clause in query_lower):
            score += 25.0

        # 2. Term overlap against chunk summary text
        for token in query_tokens:
            if token in content_lower:
                score += 3.0
            if token in clause:
                score += 5.0

        # 3. Key domain semantic boosts
        if "thermal" in query_lower or "temperature" in query_lower or "heat" in query_lower:
            if "thermal" in content_lower or "temperature" in content_lower:
                score += 15.0

        if "drop" in query_lower or "impact" in query_lower or "height" in query_lower or "durability" in query_lower:
            if "drop" in content_lower or "impact" in content_lower:
                score += 15.0

        if "choking" in query_lower or "small part" in query_lower or "cylinder" in query_lower:
            if "choking" in content_lower or "small part" in content_lower:
                score += 15.0

        if "edge" in query_lower or "sharp" in query_lower or "point" in query_lower:
            if "edge" in content_lower or "sharp" in content_lower:
                score += 15.0

        if "charging" in query_lower or "continuous" in query_lower:
            if "charging" in content_lower:
                score += 15.0

        if "short circuit" in query_lower or "resistance" in query_lower:
            if "short circuit" in content_lower:
                score += 15.0

        scored_chunks.append({
            **chunk,
            "relevance_score": score
        })

    # Sort by relevance score descending
    scored_chunks.sort(key=lambda x: x["relevance_score"], reverse=True)

    # Return top_k filtered chunks (top 1-3)
    return scored_chunks[:top_k]
