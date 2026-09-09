"""
Module 5: Testing Laboratory Suggester
Finds BIS-recognized and central testing laboratories mapped to specific Indian Standards.
Implements the City -> State -> Central nationwide fallback cascade.
"""

from typing import List, Dict, Any, Optional
from backend.db.database import get_db_connection

def find_testing_labs(is_code: Optional[str] = None, city: Optional[str] = None, state: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Finds testing labs for a given standard code with location prioritization.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if is_code:
        # Join query
        query = """
            SELECT l.lab_id, l.lab_name, l.lab_type, l.address, l.city, l.state, l.contact_email, l.phone, l.is_nabl_accredited
            FROM testing_labs l
            JOIN lab_standard_map m ON l.lab_id = m.lab_id
            WHERE m.standard_id = ? OR m.standard_id LIKE ?
        """
        cursor.execute(query, (is_code, f"%{is_code}%"))
    else:
        # General lab query
        query = """
            SELECT lab_id, lab_name, lab_type, address, city, state, contact_email, phone, is_nabl_accredited
            FROM testing_labs
        """
        cursor.execute(query)

    rows = cursor.fetchall()
    conn.close()

    labs = [
        {
            "lab_id": r["lab_id"],
            "lab_name": r["lab_name"],
            "lab_type": r["lab_type"],
            "address": r["address"],
            "city": r["city"],
            "state": r["state"],
            "contact_email": r["contact_email"],
            "phone": r["phone"],
            "is_nabl_accredited": bool(r["is_nabl_accredited"]),
            "priority": 3 # default priority
        }
        for r in rows
    ]

    # Prioritize:
    # 1. Exact city match
    # 2. State match
    # 3. Central lab (accepts samples nationwide)
    # 4. Other regional labs
    city_lower = city.lower().strip() if city else ""
    state_lower = state.lower().strip() if state else ""

    for lab in labs:
        if city_lower and city_lower in lab["city"].lower():
            lab["priority"] = 1
        elif state_lower and state_lower in lab["state"].lower():
            lab["priority"] = 2
        elif lab["lab_type"] == "Central":
            lab["priority"] = 2.5
        else:
            lab["priority"] = 4

    labs.sort(key=lambda x: x["priority"])
    return labs
