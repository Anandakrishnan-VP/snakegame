"""
One-click migration script to seed all BIS Saathi data into Supabase (PostgreSQL).
Usage:
    python scripts/migrate_to_supabase.py [optional: postgresql_url]
Or ensure DATABASE_URL is set in your .env file.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure root directory in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

load_dotenv()

from backend.db.seed_data import (
    STANDARDS_SEED,
    CHUNKS_SEED,
    CERTIFICATION_STEPS_SEED,
    VERIFICATION_REGISTRY_SEED,
    TESTING_LABS_SEED,
    LAB_STANDARD_MAP_SEED,
    FAQ_SEED
)

def migrate():
    # Retrieve DATABASE_URL
    db_url = None
    if len(sys.argv) > 1 and sys.argv[1].startswith("postgres"):
        db_url = sys.argv[1]
    else:
        db_url = os.getenv("DATABASE_URL")

    if not db_url:
        print("Error: DATABASE_URL not provided.")
        print("Please provide it as an argument or set DATABASE_URL in .env")
        print("Example:")
        print("  python scripts/migrate_to_supabase.py 'postgresql://postgres.xxx:password@aws-0-region.pooler.supabase.com:6543/postgres'")
        sys.exit(1)

    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
    except ImportError:
        print("Error: psycopg2 is not installed. Run: pip install psycopg2-binary")
        sys.exit(1)

    print(f"Connecting to Supabase PostgreSQL database...")
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = False
        cursor = conn.cursor()
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    print("Connected successfully!")

    # 1. Apply Schema
    schema_path = ROOT_DIR / "backend" / "db" / "supabase_schema.sql"
    if schema_path.exists():
        print("Applying schema (creating tables and indexes)...")
        with open(schema_path, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        cursor.execute(schema_sql)
        conn.commit()
        print("Schema applied successfully.")

    # 2. Seed standards
    print(f"Seeding {len(STANDARDS_SEED)} standards...")
    for s in STANDARDS_SEED:
        cursor.execute("""
            INSERT INTO standards (is_code, title, division, qco_status, qco_reference, related_standards, synonyms, source_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (is_code) DO UPDATE SET
                title = EXCLUDED.title,
                division = EXCLUDED.division,
                qco_status = EXCLUDED.qco_status,
                qco_reference = EXCLUDED.qco_reference,
                related_standards = EXCLUDED.related_standards,
                synonyms = EXCLUDED.synonyms,
                source_url = EXCLUDED.source_url;
        """, (
            s["is_code"], s["title"], s["division"], s["qco_status"],
            s["qco_reference"], s["related_standards"], s["synonyms"], s["source_url"]
        ))
    conn.commit()

    # 3. Seed standard_chunks
    print(f"Seeding {len(CHUNKS_SEED)} standard clause chunks...")
    for c in CHUNKS_SEED:
        cursor.execute("""
            INSERT INTO standard_chunks (chunk_id, standard_id, clause, sub_clause, page, content, source, source_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (chunk_id) DO UPDATE SET
                standard_id = EXCLUDED.standard_id,
                clause = EXCLUDED.clause,
                sub_clause = EXCLUDED.sub_clause,
                page = EXCLUDED.page,
                content = EXCLUDED.content,
                source = EXCLUDED.source,
                source_url = EXCLUDED.source_url;
        """, (
            c["chunk_id"], c["standard_id"], c["clause"], c["sub_clause"],
            c["page"], c["content"], c["source"], c["source_url"]
        ))
    conn.commit()

    # 4. Seed certification_steps
    print(f"Seeding {len(CERTIFICATION_STEPS_SEED)} certification steps...")
    for cs in CERTIFICATION_STEPS_SEED:
        cursor.execute("""
            INSERT INTO certification_steps (step_id, scheme, step_number, title, description, applies_to, indicative_timeline, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (step_id) DO UPDATE SET
                scheme = EXCLUDED.scheme,
                step_number = EXCLUDED.step_number,
                title = EXCLUDED.title,
                description = EXCLUDED.description,
                applies_to = EXCLUDED.applies_to,
                indicative_timeline = EXCLUDED.indicative_timeline,
                source = EXCLUDED.source;
        """, (
            cs["step_id"], cs["scheme"], cs["step_number"], cs["title"],
            cs["description"], cs["applies_to"], cs["indicative_timeline"], cs["source"]
        ))
    conn.commit()

    # 5. Seed verification_registry
    print(f"Seeding {len(VERIFICATION_REGISTRY_SEED)} verification records...")
    for v in VERIFICATION_REGISTRY_SEED:
        cursor.execute("""
            INSERT INTO verification_registry (number_type, number_val, licensee_name, brand, product_category, is_code, status, validity_date, details)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (number_val) DO UPDATE SET
                number_type = EXCLUDED.number_type,
                licensee_name = EXCLUDED.licensee_name,
                brand = EXCLUDED.brand,
                product_category = EXCLUDED.product_category,
                is_code = EXCLUDED.is_code,
                status = EXCLUDED.status,
                validity_date = EXCLUDED.validity_date,
                details = EXCLUDED.details;
        """, (
            v["number_type"], v["number_val"], v["licensee_name"], v["brand"],
            v["product_category"], v["is_code"], v["status"], v["validity_date"], v["details"]
        ))
    conn.commit()

    # 6. Seed testing_labs
    print(f"Seeding {len(TESTING_LABS_SEED)} testing laboratories...")
    for lab in TESTING_LABS_SEED:
        cursor.execute("""
            INSERT INTO testing_labs (lab_id, lab_name, lab_type, address, city, state, contact_email, phone, is_nabl_accredited)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (lab_id) DO UPDATE SET
                lab_name = EXCLUDED.lab_name,
                lab_type = EXCLUDED.lab_type,
                address = EXCLUDED.address,
                city = EXCLUDED.city,
                state = EXCLUDED.state,
                contact_email = EXCLUDED.contact_email,
                phone = EXCLUDED.phone,
                is_nabl_accredited = EXCLUDED.is_nabl_accredited;
        """, (
            lab["lab_id"], lab["lab_name"], lab["lab_type"], lab["address"],
            lab["city"], lab["state"], lab["contact_email"], lab["phone"], lab["is_nabl_accredited"]
        ))
    conn.commit()

    # 7. Seed lab_standard_map
    print(f"Seeding {len(LAB_STANDARD_MAP_SEED)} lab-to-standard mappings...")
    # Clear and repopulate join table
    cursor.execute("DELETE FROM lab_standard_map;")
    for m in LAB_STANDARD_MAP_SEED:
        cursor.execute("""
            INSERT INTO lab_standard_map (lab_id, standard_id)
            VALUES (%s, %s);
        """, (m["lab_id"], m["standard_id"]))
    conn.commit()

    # 8. Seed FAQs
    print(f"Seeding {len(FAQ_SEED)} FAQs...")
    for f in FAQ_SEED:
        cursor.execute("""
            INSERT INTO faq (faq_id, category, question, answer, source_url)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (faq_id) DO UPDATE SET
                category = EXCLUDED.category,
                question = EXCLUDED.question,
                answer = EXCLUDED.answer,
                source_url = EXCLUDED.source_url;
        """, (
            f["faq_id"], f["category"], f["question"], f["answer"], f["source_url"]
        ))
    conn.commit()

    print("\n✅ Migration complete! Supabase database is fully seeded and ready for production.")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    migrate()
