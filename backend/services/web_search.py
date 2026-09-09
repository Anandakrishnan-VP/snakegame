"""
Tier-2 Live BIS Web Intelligence Fallback.
Queries official government domains (bis.gov.in, standards.bis.gov.in, manakonline.in, services.bis.gov.in)
via Tavily API when a product standard is outside the local 20 SQLite seed standards.
Strictly executed as a Second Option after local database lookup.
"""

import os
import re
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

ALLOWED_OFFICIAL_DOMAINS = [
    "bis.gov.in",
    "standards.bis.gov.in",
    "manakonline.in",
    "services.bis.gov.in",
    "www.bis.gov.in"
]

# Conversational filler to remove so search engines receive targeted keywords
FILLER_PATTERNS = [
    r'\b(?:i\s+am\s+|i\s+want\s+to\s+)?(?:manufacturing|manufacture|making|producing|selling|importing)\b',
    r'\bwhat\s+(?:is|are)\s+the\s+(?:rules|regulations|standards|mandate)(?:\s+(?:for|about))?\b',
    r'\bwhat\s+is\s+the\s+indian\s+standard(?:\s+(?:for|about))?\b',
    r'\btell\s+me\s+(?:about|the\s+rules\s+for|standards\s+for)\b',
    r'\bwhich\s+standard\s+(?:applies\s+to|is\s+used\s+for)\b',
    r'\bhow\s+can\s+i\s+(?:get\s+certified|apply\s+for)\b',
    r'\bwhere\s+can\s+i\s+test\b',
    r'\bplease\s+(?:help|tell|guide)\b'
]

# Regex pattern for Indian Standards (e.g. IS 17652:2021, IS 9873 (Part 1):2019, IS 4246, IS 14286)
IS_CODE_REGEX = re.compile(
    r'\b(IS\s*(?:\/|\s*)?(?:ISO\s*|IEC\s*)?\d{3,5}(?:\s*\([^\)]+\))?(?::\d{4})?)\b',
    re.IGNORECASE
)

def clean_search_query(user_query: str) -> str:
    """Strips conversational filler, acronym noise, and constructs a targeted BIS search query."""
    text = re.sub(r'[\?\,\.\!\;]', ' ', user_query.strip().lower())
    for pat in FILLER_PATTERNS:
        text = re.sub(pat, ' ', text)
    # Remove redundant acronyms 'bis' and 'isi' since domain whitelist already targets bis.gov.in
    text = re.sub(r'\b(?:bis|b\.i\.s\.|isi)\b', ' ', text)
    cleaned = ' '.join(text.split())
    if not cleaned:
        cleaned = user_query.strip()
    if "solar" in cleaned and "photovoltaic" not in cleaned:
        cleaned = f"{cleaned} photovoltaic"
    return f"{cleaned} Indian Standard"

def is_allowed_domain(url: str) -> bool:
    """Verifies that a URL belongs strictly to authorized official government portals."""
    lower_url = url.lower()
    return any(domain in lower_url for domain in ALLOWED_OFFICIAL_DOMAINS)

def search_bis_web(
    query: str,
    timeout_seconds: float = 4.0
) -> Optional[Dict[str, Any]]:
    """
    Executes live web search against official BIS portals using Tavily.
    Returns structured standard data and official citation URL, or None.
    Strictly Second-Option: only called when local SQLite search produces 0 hits.
    """
    api_key = os.getenv("TAVILY_API_KEY") or TAVILY_API_KEY
    if not api_key or not api_key.strip():
        # Tavily not configured; gracefully skip web search
        return None

    search_term = clean_search_query(query)

    try:
        import httpx

        payload = {
            "api_key": api_key.strip(),
            "query": search_term,
            "include_domains": ALLOWED_OFFICIAL_DOMAINS,
            "search_depth": "basic",
            "max_results": 5
        }

        with httpx.Client(timeout=timeout_seconds) as client:
            resp = client.post("https://api.tavily.com/search", json=payload)
            if resp.status_code != 200:
                print(f"[WebSearch] Tavily returned status {resp.status_code}: {resp.text[:150]}")
                return None
            data = resp.json()

        results = data.get("results", [])
        if not results:
            return None

        # Filter strictly by official domains and extract Indian Standard patterns
        valid_candidates = []
        for r in results:
            url = r.get("url", "")
            title = r.get("title", "")
            content = r.get("content", "")

            if not is_allowed_domain(url):
                continue

            combined_text = f"{title} {content}"
            match = IS_CODE_REGEX.search(combined_text)
            standard_code = match.group(1).upper() if match else None

            # Detect if this is a gazette QCO notification or product specification
            is_mandatory = bool(re.search(r'\b(?:mandatory|order|qco|gazette|s\.o\.)\b', combined_text, re.IGNORECASE))

            valid_candidates.append({
                "is_code": standard_code,
                "title": title.strip(),
                "snippet": content.strip()[:350],
                "source_url": url,
                "is_mandatory": is_mandatory
            })

        if not valid_candidates:
            return None

        # Rank candidates: prioritize candidates that match query keywords in title/snippet and have an explicit IS code
        def score_candidate(cand):
            text_lower = f"{cand['title']} {cand['snippet']}".lower()
            query_words = [w for w in search_term.lower().split() if len(w) >= 4 and w not in ('indian', 'standard')]
            keyword_hits = sum(1 for w in query_words if w in text_lower)
            return (
                keyword_hits * 10
                + (8 if cand["is_code"] else 0)
                + (3 if cand["is_mandatory"] else 0)
            )

        valid_candidates.sort(key=score_candidate, reverse=True)
        best_candidate = valid_candidates[0]

        is_code_val = best_candidate["is_code"] or "Official BIS Record"
        doc_title = best_candidate["title"]
        source_url = best_candidate["source_url"]
        snippet = best_candidate["snippet"]

        return {
            "source_type": "live_web",
            "is_code": is_code_val,
            "standard_code": is_code_val,
            "title": doc_title,
            "document_title": doc_title,
            "snippet": snippet,
            "source_url": source_url,
            "qco_status": "Mandatory" if best_candidate["is_mandatory"] else "Voluntary / Applicable",
            "qco_reference": "Official BIS Gazette / Standards Portal",
            "evidence_tag": {
                "source_type": "live_web",
                "reference": is_code_val,
                "status": "confirmed",
                "clause_number": "Official Gazette Notification",
                "clause_summary": snippet,
                "verbatim_excerpt": snippet,
                "document_title": doc_title,
                "qco_reference": "Official BIS Gazette / Standards Portal",
                "source_url": source_url
            }
        }

    except Exception as e:
        print(f"[WebSearch] Error during BIS web lookup: {e}")
        return None
