"""
Module 4: Deterministic Verification Engine
Extracts and validates BIS Mark Licences (CM/L), Gold Hallmark (HUID), and CRS R-Numbers.
Strict prefix-first extraction prevents incidental numbers (dates, quantities) from being misinterpreted.
"""

import re
from typing import Dict, Any, Optional
from backend.db.database import get_db_connection

def extract_licence_code(text: str) -> Optional[Dict[str, str]]:
    """
    Extracts code type and normalized identifier using strict prefix-first patterns.
    Ordering:
    1. CRS: R-XXXXXXXX pattern
    2. CM/L with explicit prefix (e.g. CM/L-1234567, CML1234567, CML-1234567)
    3. HUID: exactly 6 alphanumeric characters (mixed letters and numbers, excluding clear words)
    4. Fallback: bare 7-digit CM/L only if explicit keyword 'licence' or 'cml' is nearby
    """
    cleaned = text.strip()

    # 1. CRS Pattern: R- followed by 8 digits
    crs_match = re.search(r'\b[rR]-?(\d{8})\b', cleaned)
    if crs_match:
        return {"type": "CRS", "code": f"R-{crs_match.group(1)}"}

    # 2. CM/L with explicit prefix: CML or CM/L followed by 7-8 digits
    cml_prefix_match = re.search(r'\b(?:CM/?L)[-\s]?(\d{7,8})\b', cleaned, re.IGNORECASE)
    if cml_prefix_match:
        return {"type": "CML", "code": f"CML{cml_prefix_match.group(1)}"}

    # 3. HUID: 6 characters alphanumeric (at least one letter and at least one digit)
    # e.g., AB1234, K7M2P9, XY9876
    huid_candidates = re.findall(r'\b([A-Za-z0-9]{6})\b', cleaned)
    for cand in huid_candidates:
        cand_upper = cand.upper()
        has_alpha = any(c.isalpha() for c in cand_upper)
        has_digit = any(c.isdigit() for c in cand_upper)
        # Avoid common 6-letter English words by requiring BOTH letters and digits
        if has_alpha and has_digit:
            return {"type": "HUID", "code": cand_upper}

    # 4. Bare 7-digit CM/L only if context mentions licence/cml/isi
    if re.search(r'\b(?:licence|license|cml|cml\s*no|isi)\b', cleaned, re.IGNORECASE):
        bare_match = re.search(r'\b(\d{7})\b', cleaned)
        if bare_match:
            return {"type": "CML", "code": f"CML{bare_match.group(1)}"}

    return None

def verify_code(raw_input: str) -> Dict[str, Any]:
    """
    Validates a licence or hallmark code against the verification_registry table.
    """
    extracted = extract_licence_code(raw_input)
    if not extracted:
        return {
            "found": False,
            "extracted_code": None,
            "code_type": None,
            "message": "No recognizable BIS licence (CM/L), 6-character HUID, or CRS R-number found in your query. Please provide a valid code like 'CML1234567', 'AB1234', or 'R-41001234'."
        }

    code_val = extracted["code"]
    code_type = extracted["type"]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT number_type, number_val, licensee_name, brand, product_category, is_code, status, validity_date, details
        FROM verification_registry
        WHERE number_val = ? OR number_val = ?
    """, (code_val, code_val.replace("CML", "")))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return {
            "found": False,
            "extracted_code": code_val,
            "code_type": code_type,
            "message": f"Verification status: NOT FOUND. The {code_type} identifier '{code_val}' is not registered in the official database or may be counterfeit/invalid."
        }

    return {
        "found": True,
        "extracted_code": row["number_val"],
        "code_type": row["number_type"],
        "licensee_name": row["licensee_name"],
        "brand": row["brand"],
        "product_category": row["product_category"],
        "is_code": row["is_code"],
        "status": row["status"],
        "validity_date": row["validity_date"],
        "details": row["details"],
        "message": f"Verified Genuine: {row['licensee_name']} ({row['brand'] or 'Standard'}) holds an {row['status']} {row['number_type']} licence for {row['product_category']}."
    }
