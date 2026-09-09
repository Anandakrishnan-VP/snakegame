"""
Database management and initialization module for BIS Saathi.
Connects to SQLite and populates seed data on first run.
"""

import sqlite3
import os
from pathlib import Path
from backend.db.schema import SCHEMA_SQL
from backend.db.seed_data import (
    STANDARDS_SEED,
    CHUNKS_SEED,
    CERTIFICATION_STEPS_SEED,
    VERIFICATION_REGISTRY_SEED,
    TESTING_LABS_SEED,
    LAB_STANDARD_MAP_SEED,
    FAQ_SEED
)

DB_PATH = Path(__file__).resolve().parent.parent / "bis_saathi.db"

def get_db_connection():
    """Returns a sqlite3 connection with dict-like row factory."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force_reseed: bool = False):
    """Initializes schema and seeds all tables."""
    if force_reseed and DB_PATH.exists():
        try:
            os.remove(DB_PATH)
        except Exception as e:
            print(f"Warning removing old DB: {e}")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.executescript(SCHEMA_SQL)

    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM standards")
    count = cursor.fetchone()[0]

    if count == 0:
        print("Seeding BIS Saathi database...")

        # 1. Seed standards
        for std in STANDARDS_SEED:
            cursor.execute("""
                INSERT OR REPLACE INTO standards 
                (is_code, title, division, qco_status, qco_reference, related_standards, synonyms, source_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                std["is_code"], std["title"], std["division"], std["qco_status"],
                std["qco_reference"], std["related_standards"], std["synonyms"], std["source_url"]
            ))

        # 2. Seed standard_chunks (Tier B Deep Clauses)
        for chunk in CHUNKS_SEED:
            cursor.execute("""
                INSERT OR REPLACE INTO standard_chunks 
                (chunk_id, standard_id, clause, sub_clause, page, content, source, source_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                chunk["chunk_id"], chunk["standard_id"], chunk["clause"], chunk["sub_clause"],
                chunk["page"], chunk["content"], chunk["source"], chunk["source_url"]
            ))

        # 3. Seed certification_steps
        for step in CERTIFICATION_STEPS_SEED:
            cursor.execute("""
                INSERT OR REPLACE INTO certification_steps
                (step_id, scheme, step_number, title, description, applies_to, indicative_timeline, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                step["step_id"], step["scheme"], step["step_number"], step["title"],
                step["description"], step["applies_to"], step["indicative_timeline"], step["source"]
            ))

        # 4. Seed verification_registry
        for reg in VERIFICATION_REGISTRY_SEED:
            cursor.execute("""
                INSERT OR REPLACE INTO verification_registry
                (number_type, number_val, licensee_name, brand, product_category, is_code, status, validity_date, details)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                reg["number_type"], reg["number_val"], reg["licensee_name"], reg["brand"],
                reg["product_category"], reg["is_code"], reg["status"], reg["validity_date"], reg["details"]
            ))

        # 5. Seed testing_labs
        for lab in TESTING_LABS_SEED:
            cursor.execute("""
                INSERT OR REPLACE INTO testing_labs
                (lab_id, lab_name, lab_type, address, city, state, contact_email, phone, is_nabl_accredited)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                lab["lab_id"], lab["lab_name"], lab["lab_type"], lab["address"],
                lab["city"], lab["state"], lab["contact_email"], lab["phone"], lab["is_nabl_accredited"]
            ))

        # 6. Seed lab_standard_map
        for m in LAB_STANDARD_MAP_SEED:
            cursor.execute("""
                INSERT INTO lab_standard_map (lab_id, standard_id)
                VALUES (?, ?)
            """, (m["lab_id"], m["standard_id"]))

        # 7. Seed faq
        for f in FAQ_SEED:
            cursor.execute("""
                INSERT OR REPLACE INTO faq (faq_id, category, question, answer, source_url)
                VALUES (?, ?, ?, ?, ?)
            """, (f["faq_id"], f["category"], f["question"], f["answer"], f["source_url"]))

        conn.commit()
        print("BIS Saathi database successfully seeded!")
    else:
        print("Database already contains data, skipping reseed.")

    conn.close()

if __name__ == "__main__":
    init_db(force_reseed=True)
