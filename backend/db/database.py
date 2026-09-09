"""
Database management and initialization module for BIS Saathi.
Connects to SQLite and populates seed data on first run.
"""

import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
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

import shutil

SOURCE_DB_PATH = Path(__file__).resolve().parent.parent / "bis_saathi.db"

def get_db_path() -> Path:
    """
    Returns the SQLite database path.
    On Vercel (or AWS Lambda) where the deployment directory is read-only, copies
    the seeded database to /tmp/bis_saathi.db so both reads and writes (sessions, journeys, cache) succeed.
    """
    if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        tmp_dir = Path("/tmp") if os.name != "nt" else Path(os.getenv("TEMP", "C:/tmp"))
        tmp_dir.mkdir(parents=True, exist_ok=True)
        tmp_db = tmp_dir / "bis_saathi.db"
        if not tmp_db.exists() and SOURCE_DB_PATH.exists():
            try:
                shutil.copy2(str(SOURCE_DB_PATH), str(tmp_db))
            except Exception as e:
                print(f"Warning: Failed to copy SQLite DB to /tmp: {e}")
                return SOURCE_DB_PATH
        return tmp_db
    return SOURCE_DB_PATH

class PostgresCursorWrapper:
    """Wraps a psycopg2 DictCursor to provide transparent SQLite compatibility (? -> %s)."""
    def __init__(self, raw_cursor):
        self._cursor = raw_cursor

    def execute(self, sql, params=None):
        pg_sql = sql.replace("?", "%s")
        if params is not None:
            return self._cursor.execute(pg_sql, params)
        return self._cursor.execute(pg_sql)

    def executemany(self, sql, seq_of_params):
        pg_sql = sql.replace("?", "%s")
        return self._cursor.executemany(pg_sql, seq_of_params)

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def close(self):
        return self._cursor.close()

    @property
    def rowcount(self):
        return self._cursor.rowcount

class PostgresConnectionWrapper:
    """Wraps a psycopg2 connection to provide dict-like row factory and standard methods."""
    def __init__(self, raw_conn):
        self._conn = raw_conn

    def cursor(self):
        from psycopg2.extras import DictCursor
        raw_cur = self._conn.cursor(cursor_factory=DictCursor)
        return PostgresCursorWrapper(raw_cur)

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def close(self):
        return self._conn.close()

def is_postgres_configured() -> bool:
    """Checks if a PostgreSQL / Supabase connection URL is configured."""
    db_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")
    return bool(db_url and db_url.strip().startswith("postgres"))

def get_db_connection():
    """
    Returns a database connection with dict-like row factory.
    If DATABASE_URL is configured (Supabase), connects to Postgres.
    Otherwise, defaults to local SQLite.
    """
    if is_postgres_configured():
        db_url = os.getenv("DATABASE_URL") or os.getenv("SUPABASE_DB_URL")
        try:
            import psycopg2
            raw_conn = psycopg2.connect(db_url)
            return PostgresConnectionWrapper(raw_conn)
        except Exception as e:
            print(f"Warning: Failed to connect to Supabase/Postgres ({e}). Falling back to local SQLite.")

    # Default to local SQLite
    db_path = get_db_path()
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force_reseed: bool = False):
    """Initializes schema and seeds all tables for the active database engine."""
    if is_postgres_configured():
        # Supabase/PostgreSQL is persistent and managed remotely via scripts/migrate_to_supabase.py.
        # Avoid running heavy migrations during the serverless request lifecycle or cold starts.
        return

    # Fallback / Local SQLite initialization
    conn = get_db_connection()
    if isinstance(conn, sqlite3.Connection):
        cursor = conn.cursor()
        cursor.executescript(SCHEMA_SQL)
        try:
            cursor.execute("PRAGMA table_info(session_state)")
            cols = [row["name"] for row in cursor.fetchall()]
            if "turn_history" not in cols:
                cursor.execute("ALTER TABLE session_state ADD COLUMN turn_history TEXT DEFAULT '[]'")
                conn.commit()
        except Exception as e:
            print(f"Session state schema check: {e}")

    if force_reseed:
        tables = ["standards", "standard_chunks", "certification_steps", "verification_registry", "testing_labs", "lab_standard_map", "faq"]
        for t in tables:
            try:
                cursor.execute(f"DELETE FROM {t}")
            except Exception:
                pass
        conn.commit()

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
