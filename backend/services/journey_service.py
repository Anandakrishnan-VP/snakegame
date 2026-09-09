"""
Certification Journey Service for BIS Saathi.
Manages persistent compliance readiness roadmaps for MSMEs and Consumers.
Computes readiness scores (0-100%) and tracks progress step-by-step.
"""

import uuid
import json
import sqlite3
from typing import Dict, Any, Optional, List
from datetime import datetime
from backend.db.database import get_db_connection
from backend.services.module1_directory import get_standard_by_code, search_directory
from backend.services.module3_certification import get_certification_steps, get_scheme_overview
from backend.services.module5_labs import find_testing_labs

def start_journey(
    session_id: str,
    journey_type: str = "get_certified",
    standard_id: Optional[str] = None,
    force_new: bool = False
) -> Dict[str, Any]:
    """
    Initializes or resumes a certification or verification journey.
    Guarantees deduplication: resumes existing journey if already started in the same session.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Deduplication check: Resume if already exists for this session & standard
    if not force_new:
        if standard_id:
            cursor.execute("""
                SELECT journey_id, session_id, journey_type, standard_id, scheme, steps_json, readiness_score, metadata_json, created_at, updated_at
                FROM journey_progress
                WHERE session_id = ? AND journey_type = ? AND standard_id = ?
                ORDER BY updated_at DESC LIMIT 1
            """, (session_id, journey_type, standard_id))
        else:
            cursor.execute("""
                SELECT journey_id, session_id, journey_type, standard_id, scheme, steps_json, readiness_score, metadata_json, created_at, updated_at
                FROM journey_progress
                WHERE session_id = ? AND journey_type = ?
                ORDER BY updated_at DESC LIMIT 1
            """, (session_id, journey_type))

        existing = cursor.fetchone()
        if existing:
            conn.close()
            return {
                "journey_id": existing["journey_id"],
                "session_id": existing["session_id"],
                "journey_type": existing["journey_type"],
                "standard_id": existing["standard_id"],
                "scheme": existing["scheme"],
                "steps": json.loads(existing["steps_json"]),
                "readiness_score": existing["readiness_score"],
                "metadata": json.loads(existing["metadata_json"] or "{}"),
                "created_at": existing["created_at"],
                "updated_at": existing["updated_at"],
                "resumed": True
            }

    # 2. Build new journey
    journey_id = str(uuid.uuid4())
    scheme_code = "Scheme-I"
    metadata: Dict[str, Any] = {}
    steps: List[Dict[str, Any]] = []

    if journey_type == "get_certified":
        # Resolve standard details
        standard = None
        if standard_id:
            standard = get_standard_by_code(standard_id)
            if not standard:
                # Fuzzy fallback
                candidates = search_directory(standard_id)
                if candidates:
                    standard = candidates[0]

        if not standard:
            # Default fallback standard (Stainless Steel Water Bottles)
            standard = get_standard_by_code("IS 17803:2022") or {
                "is_code": "IS 17803:2022",
                "title": "Stainless Steel Vacuum Flasks and Insulated Containers",
                "qco_status": "Mandatory",
                "qco_reference": "QCO S.O. 853(E)",
                "source_url": "https://www.bis.gov.in"
            }

        resolved_standard_id = standard.get("is_code")
        qco_status = (standard.get("qco_status") or "").lower()

        # Check for voluntary standard without mandatory scheme
        if "voluntary" in qco_status:
            scheme_code = "Voluntary"
            steps = [
                {
                    "step_id": "step-1",
                    "step_number": 1,
                    "title": "Voluntary Compliance Assessment",
                    "description": "This standard is currently voluntary. No mandatory BIS certification or Quality Control Order enforcement applies. Voluntary ISI mark can be obtained via Scheme-I if market differentiation is desired.",
                    "status": "done",
                    "indicative_timeline": "Immediate",
                    "source_ref": standard.get("source_url") or "https://www.bis.gov.in"
                }
            ]
        else:
            # Determine Scheme (CRS vs Scheme-I)
            is_code_lower = (resolved_standard_id or "").lower()
            title_lower = (standard.get("title") or "").lower()
            if "crs" in is_code_lower or "16046" in is_code_lower or "13252" in is_code_lower or "16102" in is_code_lower or "15885" in is_code_lower:
                scheme_code = "CRS"
            else:
                scheme_code = "Scheme-I"

            scheme_info = get_scheme_overview(scheme_code)
            db_steps = get_certification_steps(scheme_code)

            steps = [
                {
                    "step_id": f"step-{s['step_number']}",
                    "step_number": s["step_number"],
                    "title": s["title"],
                    "description": s["description"],
                    "status": "pending",
                    "indicative_timeline": s.get("indicative_timeline", "Varies"),
                    "source_ref": scheme_info.get("portal") or "https://www.manakonline.in"
                }
                for s in db_steps
            ]

        # Resolve testing labs for this standard
        labs = find_testing_labs(is_code=resolved_standard_id)
        scheme_details = get_scheme_overview(scheme_code)

        metadata = {
            "standard_id": resolved_standard_id,
            "title": standard.get("title", ""),
            "qco_status": standard.get("qco_status", "Mandatory"),
            "qco_reference": standard.get("qco_reference", ""),
            "scheme_name": scheme_details.get("name", scheme_code),
            "governing_law": scheme_details.get("governing_law", "BIS Act, 2016"),
            "portal": scheme_details.get("portal", "https://www.manakonline.in"),
            "msme_benefit": scheme_details.get("msme_benefit", ""),
            "labs": [
                {
                    "name": l.get("lab_name"),
                    "city": l.get("city"),
                    "phone": l.get("phone") or "Official Regional Helpdesk"
                }
                for l in labs[:2]
            ]
        }

    else:
        # Consumer: Verify & Protect Journey
        scheme_code = "Verification"
        resolved_standard_id = standard_id or "General Registry Check"
        steps = [
            {
                "step_id": "step-1",
                "step_number": 1,
                "title": "Identification Code Extraction",
                "description": "Locate the 7-digit CM/L licence number below the ISI mark, the 6-character alphanumeric HUID on gold jewellery, or the R-number on electronic products.",
                "status": "done" if standard_id else "pending",
                "indicative_timeline": "1 minute",
                "source_ref": "https://www.bis.gov.in/consumer-affairs/"
            },
            {
                "step_id": "step-2",
                "step_number": 2,
                "title": "Central Registry Operative Status Check",
                "description": "Verify that the code is currently OPERATIVE and not expired, cancelled, or under stop-marking.",
                "status": "pending",
                "indicative_timeline": "Instant",
                "source_ref": "https://www.manakonline.in"
            },
            {
                "step_id": "step-3",
                "step_number": 3,
                "title": "Licensee Identity & Product Scope Audit",
                "description": "Cross-check brand name, manufacturer details, factory address, and product specification against packaging labels.",
                "status": "pending",
                "indicative_timeline": "5 minutes",
                "source_ref": "https://www.bis.gov.in"
            },
            {
                "step_id": "step-4",
                "step_number": 4,
                "title": "Authenticity Confirmation / Grievance Redressal",
                "description": "If authentic, retain proof of purchase. If counterfeit, unverified, or substandard, file an official grievance on the BIS Care App under Section 29.",
                "status": "pending",
                "indicative_timeline": "As needed",
                "source_ref": "https://www.bis.gov.in/consumer-affairs/grievance-redressal/"
            }
        ]
        metadata = {
            "standard_id": resolved_standard_id,
            "title": "Consumer Quality Assurance & Anti-Counterfeit Verification",
            "qco_status": "Consumer Protection",
            "qco_reference": "BIS Act 2016 Section 17 & 29",
            "scheme_name": "BIS Care Verification & Grievance Mechanism",
            "governing_law": "Consumer Protection Act 2019 & BIS Act 2016",
            "portal": "https://www.bis.gov.in/consumer-affairs/grievance-redressal/",
            "labs": []
        }

    # Calculate initial readiness score
    done_count = sum(1 for s in steps if s.get("status") == "done")
    total_steps = len(steps)
    readiness_score = round((done_count / total_steps) * 100) if total_steps > 0 else 0

    # Persist to database
    cursor.execute("""
        INSERT INTO journey_progress (
            journey_id, session_id, journey_type, standard_id, scheme, steps_json, readiness_score, metadata_json, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
    """, (
        journey_id,
        session_id,
        journey_type,
        resolved_standard_id,
        scheme_code,
        json.dumps(steps),
        readiness_score,
        json.dumps(metadata)
    ))

    conn.commit()
    conn.close()

    return {
        "journey_id": journey_id,
        "session_id": session_id,
        "journey_type": journey_type,
        "standard_id": resolved_standard_id,
        "scheme": scheme_code,
        "steps": steps,
        "readiness_score": readiness_score,
        "metadata": metadata,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "resumed": False
    }

def update_step_status(journey_id: str, step_id: str, status: str) -> Optional[Dict[str, Any]]:
    """
    Toggles step status ('done' | 'pending'), updates timestamp, and recomputes readiness score.
    Free-form checklist: any step can be checked in any sequence.
    """
    clean_status = "done" if status.lower() == "done" else "pending"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT journey_id, session_id, journey_type, standard_id, scheme, steps_json, metadata_json
        FROM journey_progress
        WHERE journey_id = ?
    """, (journey_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return None

    steps = json.loads(row["steps_json"])
    step_found = False

    for s in steps:
        if s.get("step_id") == step_id:
            s["status"] = clean_status
            step_found = True
            break

    if not step_found:
        conn.close()
        return None

    done_count = sum(1 for s in steps if s.get("status") == "done")
    total_steps = len(steps)
    new_score = round((done_count / total_steps) * 100) if total_steps > 0 else 0

    cursor.execute("""
        UPDATE journey_progress
        SET steps_json = ?, readiness_score = ?, updated_at = CURRENT_TIMESTAMP
        WHERE journey_id = ?
    """, (json.dumps(steps), new_score, journey_id))

    conn.commit()
    conn.close()

    return {
        "journey_id": row["journey_id"],
        "session_id": row["session_id"],
        "journey_type": row["journey_type"],
        "standard_id": row["standard_id"],
        "scheme": row["scheme"],
        "steps": steps,
        "readiness_score": new_score,
        "metadata": json.loads(row["metadata_json"] or "{}"),
        "updated_at": datetime.now().isoformat()
    }

def get_journey(journey_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves full journey record for a given journey_id."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT journey_id, session_id, journey_type, standard_id, scheme, steps_json, readiness_score, metadata_json, created_at, updated_at
        FROM journey_progress
        WHERE journey_id = ?
    """, (journey_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "journey_id": row["journey_id"],
        "session_id": row["session_id"],
        "journey_type": row["journey_type"],
        "standard_id": row["standard_id"],
        "scheme": row["scheme"],
        "steps": json.loads(row["steps_json"]),
        "readiness_score": row["readiness_score"],
        "metadata": json.loads(row["metadata_json"] or "{}"),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"]
    }
