"""
The Compliance Chain Orchestrator.
Assembles the complete connected intelligence journey:
Product Description -> Attribute Extraction (M2) -> Directory Match (M1) -> 
QCO Status Check -> Certification Scheme & Steps (M3) -> Testing Labs (M5) -> Evidence Tag.
"""

from typing import Dict, Any, Optional
from backend.services.module1_directory import search_directory, get_standard_by_code, get_flagship_chunks, retrieve_relevant_chunks
from backend.services.module2_matcher import match_product_to_standard
from backend.services.module3_certification import get_certification_steps, get_scheme_overview
from backend.services.module5_labs import find_testing_labs

def run_compliance_chain(query: str, city: Optional[str] = None, state: Optional[str] = None, persona: str = "general") -> Dict[str, Any]:
    """
    Executes the end-to-end compliance chain and returns a unified, structured context payload.
    """
    # Step 1: Attribute Extraction & Standard Matching
    match_result = match_product_to_standard(query)
    primary_std = match_result["primary_match"]
    clarifying_q = match_result.get("clarifying_question")

    if not primary_std:
        # Standard not found in Tier A directory
        return {
            "chain_completed": False,
            "status": "not determined",
            "clarifying_question": None,
            "standard": None,
            "qco_status": None,
            "scheme": None,
            "steps": [],
            "labs": [],
            "deep_clauses": [],
            "evidence_tag": {
                "source_type": "directory",
                "reference": "None",
                "status": "not determined",
                "clause_summary": "No registered Indian Standard found for the specified product description in the local BIS registry.",
                "verbatim_excerpt": "No registered Indian Standard found for the specified product description in the local BIS registry.",
                "source_url": "https://www.bis.gov.in"
            }
        }

    is_code = primary_std["is_code"]
    division = primary_std["division"]
    qco_status = primary_std["qco_status"]
    qco_ref = primary_std["qco_reference"]

    # Step 2: Determine Appropriate Certification Scheme & Steps
    is_voluntary = "voluntary" in (qco_status or "").lower()

    if is_voluntary:
        scheme_name = "Voluntary"
        cert_steps = [
            {
                "step_id": "step-1",
                "scheme": "Voluntary",
                "step_number": 1,
                "title": "Voluntary Standard Compliance",
                "description": "This standard is currently voluntary. No mandatory Quality Control Order (QCO) enforcement applies. Manufacturers may voluntarily apply for ISI mark certification under Scheme-I for quality differentiation.",
                "applies_to": "all",
                "indicative_timeline": "Immediate (Optional)",
                "source": primary_std.get("source_url") or "https://www.bis.gov.in"
            }
        ]
        scheme_info = get_scheme_overview("Voluntary")
    elif "CRS" in division or "Electronics" in division:
        scheme_name = "CRS"
        cert_steps = get_certification_steps(scheme=scheme_name, applies_to="domestic")
        scheme_info = get_scheme_overview(scheme_name)
    else:
        scheme_name = "Scheme-I"
        cert_steps = get_certification_steps(scheme=scheme_name, applies_to="domestic")
        scheme_info = get_scheme_overview(scheme_name)

    # Step 4: Fetch Testing Laboratories
    labs = find_testing_labs(is_code=is_code, city=city, state=state)

    # Step 5: Explicit Clause-Level Retrieval (Filtered by query relevance)
    relevant_chunks = retrieve_relevant_chunks(is_code, query, top_k=3)

    # Step 6: Construct Rich Evidence Tag
    if relevant_chunks:
        # Highest ranked chunk for this specific query
        top_chunk = relevant_chunks[0]
        evidence_tag = {
            "source_type": "clause",
            "reference": f"{is_code} Clause {top_chunk['clause']}",
            "status": "confirmed" if not clarifying_q else "needs verification",
            "clause_number": top_chunk["clause"],
            "sub_clause": top_chunk.get("sub_clause"),
            "page": top_chunk.get("page"),
            "clause_summary": top_chunk["content"],
            "verbatim_excerpt": top_chunk["content"], # Alias for backwards compatibility
            "document_title": primary_std["title"],
            "qco_reference": qco_ref,
            "source_url": top_chunk["source_url"] or primary_std["source_url"]
        }
    else:
        # Tier A standard has verified directory & QCO order
        if is_voluntary:
            clause_desc = f"Classified as Voluntary under {qco_ref}. No mandatory Quality Control Order (QCO) enforcement applies."
        else:
            clause_desc = f"Notified under {qco_ref}. Mandatory compliance enforced by BIS."

        evidence_tag = {
            "source_type": "directory",
            "reference": is_code,
            "status": "confirmed" if not clarifying_q else "needs verification",
            "clause_number": "Directory & QCO Reference",
            "sub_clause": None,
            "page": 1,
            "clause_summary": clause_desc,
            "verbatim_excerpt": clause_desc,
            "document_title": primary_std["title"],
            "qco_reference": qco_ref,
            "source_url": primary_std["source_url"]
        }

    return {
        "chain_completed": True,
        "status": evidence_tag["status"],
        "clarifying_question": clarifying_q,
        "standard": primary_std,
        "attributes": match_result["attributes"],
        "qco_status": qco_status,
        "qco_reference": qco_ref,
        "scheme": scheme_info,
        "steps": cert_steps,
        "labs": labs[:4], # top 4 labs
        "deep_clauses": relevant_chunks,
        "evidence_tag": evidence_tag,
        "persona": persona
    }
