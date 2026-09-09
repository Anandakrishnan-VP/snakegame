"""
The Compliance Chain Orchestrator.
Assembles the complete connected intelligence journey:
Product Description -> Attribute Extraction (M2) -> Directory Match (M1) -> 
QCO Status Check -> Certification Scheme & Steps (M3) -> Testing Labs (M5) -> Evidence Tag.
"""

from typing import Dict, Any, Optional
from backend.services.module1_directory import search_directory, get_standard_by_code, get_flagship_chunks
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
                "verbatim_excerpt": "No registered Indian Standard found for the specified product description in the local BIS registry.",
                "source_url": "https://www.bis.gov.in"
            }
        }

    is_code = primary_std["is_code"]
    division = primary_std["division"]
    qco_status = primary_std["qco_status"]
    qco_ref = primary_std["qco_reference"]

    # Step 2: Determine Appropriate Certification Scheme
    if "CRS" in division or "Electronics" in division:
        scheme_name = "CRS"
    else:
        scheme_name = "Scheme-I"

    # Step 3: Fetch Certification Steps
    cert_steps = get_certification_steps(scheme=scheme_name, applies_to="domestic")
    scheme_info = get_scheme_overview(scheme_name)

    # Step 4: Fetch Testing Laboratories
    labs = find_testing_labs(is_code=is_code, city=city, state=state)

    # Step 5: Check for Tier B Deep-Clause Content
    deep_chunks = get_flagship_chunks(is_code)

    # Step 6: Construct Rich Evidence Tag
    if deep_chunks:
        # Flagship standard has verified deep clause
        top_chunk = deep_chunks[0]
        evidence_tag = {
            "source_type": "clause",
            "reference": f"{is_code} Clause {top_chunk['clause']}",
            "status": "confirmed" if not clarifying_q else "needs verification",
            "clause_number": top_chunk["clause"],
            "sub_clause": top_chunk.get("sub_clause"),
            "page": top_chunk.get("page"),
            "verbatim_excerpt": top_chunk["content"],
            "document_title": primary_std["title"],
            "qco_reference": qco_ref,
            "source_url": top_chunk["source_url"] or primary_std["source_url"]
        }
    else:
        # Tier A standard has verified directory & QCO order
        evidence_tag = {
            "source_type": "directory",
            "reference": is_code,
            "status": "confirmed" if not clarifying_q else "needs verification",
            "clause_number": "Directory & QCO Reference",
            "sub_clause": None,
            "page": 1,
            "verbatim_excerpt": f"Notified under {qco_ref}. Mandatory compliance enforced by BIS.",
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
        "deep_clauses": deep_chunks,
        "evidence_tag": evidence_tag,
        "persona": persona
    }
