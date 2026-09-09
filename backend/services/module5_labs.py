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

    city_clean = city.strip() if city and city != "All Cities" else ""
    state_clean = state.strip() if state and state != "All States" else ""

    if not city_clean and not state_clean:
        # No location filter: return all labs, prioritizing Central then by city
        labs.sort(key=lambda x: (0 if x["lab_type"] == "Central" else 1, x["city"]))
        return labs

    city_lower = city_clean.lower()
    state_lower = state_clean.lower()

    # Cascade Level 1: Direct city match
    if city_lower:
        city_matches = [l for l in labs if city_lower in l["city"].lower()]
        if city_matches:
            for l in city_matches:
                l["priority"] = 1
                l["match_level"] = "city"
            return city_matches

    # Cascade Level 2: State match
    if state_lower:
        state_matches = [l for l in labs if state_lower in l["state"].lower()]
        if state_matches:
            for l in state_matches:
                l["priority"] = 2
                l["match_level"] = "state"
                if city_clean:
                    l["fallback_note"] = f"No lab directly in {city_clean}; nearest recognized lab in {l['state']}"
            return state_matches

    # Cascade Level 3: Central Laboratory Fallback (CL Sahibabad accepts samples nationwide)
    central_labs = [l for l in labs if l["lab_type"] == "Central"]
    if central_labs:
        for l in central_labs:
            l["priority"] = 3
            l["match_level"] = "central"
            target_loc = city_clean or state_clean
            l["fallback_note"] = f"No local lab in {target_loc}; samples can be submitted to BIS Central Laboratory (accepts nationwide samples)"
        return central_labs

    # If no central lab in standard map, return candidate labs
    return labs
