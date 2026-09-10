"""
Module 3: Certification & Licensing Knowledge
Retrieves deterministic certification workflows from SQLite (Scheme-I, CRS, FMCS).
Never lets LLM invent bureaucratic steps; embeds MSME concession details.
"""

from typing import List, Dict, Any, Optional
from backend.db.database import get_db_connection

def get_certification_steps(scheme: str = "Scheme-I", applies_to: str = "domestic") -> List[Dict[str, Any]]:
    """
    Fetches ordered certification steps for a specific scheme and entity type.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT step_id, scheme, step_number, title, description, applies_to, indicative_timeline, source
        FROM certification_steps
        WHERE scheme = ? AND (applies_to = ? OR applies_to = 'all')
        ORDER BY step_number ASC
    """
    cursor.execute(query, (scheme, applies_to))
    rows = cursor.fetchall()
    conn.close()

    steps = [
        {
            "step_id": r["step_id"],
            "scheme": r["scheme"],
            "step_number": r["step_number"],
            "title": r["title"],
            "description": r["description"],
            "applies_to": r["applies_to"],
            "indicative_timeline": r["indicative_timeline"],
            "source": r["source"]
        }
        for r in rows
    ]
    return steps

def get_scheme_overview(scheme: str) -> Dict[str, Any]:
    """Provides high-level guidance, portal links, and MSME benefits for a scheme."""
    overviews = {
        "Scheme-I": {
            "name": "Scheme-I (ISI Mark Product Certification)",
            "governing_law": "BIS (Conformity Assessment) Regulations, 2018",
            "target": "Domestic & Foreign Manufacturers",
            "portal": "https://www.manakonline.in",
            "form": "Form V (e-BIS Portal)",
            "audit_required": True,
            "msme_benefit": "50% concession on application fee, licence fee, and minimum marking fee for Micro enterprises; 20% concession for Small enterprises and DPIIT-recognized Startups.",
            "indicative_duration": "35–65 days (indicative, subject to lab test duration)"
        },
        "CRS": {
            "name": "Compulsory Registration Scheme (CRS)",
            "governing_law": "MeitY CRO Orders & BIS (Conformity Assessment) Regulations, Scheme-II",
            "target": "Electronics and IT Goods Manufacturers (Domestic & Overseas)",
            "portal": "https://www.crsbis.in",
            "form": "Self-Declaration of Conformity (SDoC)",
            "audit_required": False,
            "msme_benefit": "Paperless online submission; no factory inspection required. Rapid R-Number generation upon valid lab test report.",
            "indicative_duration": "15–20 days from lab report upload"
        },
        "FMCS": {
            "name": "Foreign Manufacturers Certification Scheme (FMCS)",
            "governing_law": "Scheme-I provisions adapted for non-Indian manufacturing premises",
            "target": "Overseas manufacturing units exporting to India",
            "portal": "https://www.manakonline.in (FMCD Section)",
            "form": "FMCD Application + AIR Nomination",
            "audit_required": True,
            "msme_benefit": "Requires mandatory Authorized Indian Representative (AIR) and Performance Bank Guarantee.",
            "indicative_duration": "90–120 days (dependent on international auditor travel)"
        },
        "Voluntary": {
            "name": "Voluntary Compliance / Optional Scheme-I",
            "governing_law": "Voluntary Adoption (No mandatory QCO enforcement)",
            "target": "Domestic & Foreign Manufacturers seeking voluntary quality assurance",
            "portal": "https://www.manakonline.in",
            "form": "Form V (e-BIS Portal - Optional)",
            "audit_required": False,
            "msme_benefit": "Standard MSME fee concessions apply if voluntary Scheme-I ISI mark is pursued.",
            "indicative_duration": "Voluntary compliance is self-determined unless formal ISI mark is requested."
        }
    }
    return overviews.get(scheme, overviews["Scheme-I"])
