-- ==============================================================================
-- BIS Saathi — Supabase (PostgreSQL) Schema Definition
-- Run this script in the Supabase SQL Editor (Dashboard -> SQL Editor -> New Query)
-- ==============================================================================

-- 1. Standards Table (Tier A Directory)
CREATE TABLE IF NOT EXISTS standards (
    is_code TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    division TEXT NOT NULL,
    qco_status TEXT NOT NULL, -- 'Mandatory', 'Voluntary', 'Under Consideration'
    qco_reference TEXT,
    related_standards TEXT, -- Comma-separated IS codes
    synonyms TEXT NOT NULL, -- Comma-separated colloquial search terms
    source_url TEXT NOT NULL
);

-- 2. Standard Chunks (Tier B Flagship Deep-Clause Content)
CREATE TABLE IF NOT EXISTS standard_chunks (
    chunk_id TEXT PRIMARY KEY,
    standard_id TEXT NOT NULL REFERENCES standards(is_code) ON DELETE CASCADE,
    clause TEXT NOT NULL,
    sub_clause TEXT,
    page INTEGER,
    content TEXT NOT NULL, -- Original verbatim text from standard
    source TEXT NOT NULL,
    source_url TEXT
);

-- 3. Certification Steps Table
CREATE TABLE IF NOT EXISTS certification_steps (
    step_id TEXT PRIMARY KEY,
    scheme TEXT NOT NULL, -- 'Scheme-I', 'CRS', 'FMCS'
    step_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    applies_to TEXT NOT NULL, -- 'domestic', 'foreign', 'all'
    indicative_timeline TEXT,
    source TEXT NOT NULL
);

-- 4. Verification Registry (Mock BIS CM/L, HUID, CRS Registry)
CREATE TABLE IF NOT EXISTS verification_registry (
    number_type TEXT NOT NULL, -- 'CML', 'HUID', 'CRS'
    number_val TEXT PRIMARY KEY, -- Stored as TEXT to avoid mangling alphanumeric HUIDs
    licensee_name TEXT NOT NULL,
    brand TEXT,
    product_category TEXT NOT NULL,
    is_code TEXT,
    status TEXT NOT NULL, -- 'Active', 'Expired', 'Suspended', 'Operative'
    validity_date TEXT NOT NULL,
    details TEXT
);

-- 5. Testing Labs
CREATE TABLE IF NOT EXISTS testing_labs (
    lab_id TEXT PRIMARY KEY,
    lab_name TEXT NOT NULL,
    lab_type TEXT NOT NULL, -- 'Central', 'Regional', 'Recognized', 'Branch'
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    contact_email TEXT,
    phone TEXT,
    is_nabl_accredited INTEGER DEFAULT 1
);

-- 6. Lab to Standard Join Table (Many-to-Many)
CREATE TABLE IF NOT EXISTS lab_standard_map (
    map_id SERIAL PRIMARY KEY,
    lab_id TEXT NOT NULL REFERENCES testing_labs(lab_id) ON DELETE CASCADE,
    standard_id TEXT NOT NULL REFERENCES standards(is_code) ON DELETE CASCADE
);

-- 7. FAQ Table
CREATE TABLE IF NOT EXISTS faq (
    faq_id TEXT PRIMARY KEY,
    category TEXT NOT NULL, -- 'Consumer', 'Industry', 'MSME', 'StandardsClubs', 'Grievance'
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    source_url TEXT
);

-- 8. Session State & Memory
CREATE TABLE IF NOT EXISTS session_state (
    session_id TEXT PRIMARY KEY,
    active_topic TEXT, -- Most recently identified IS code
    persona TEXT DEFAULT 'general', -- 'consumer', 'msme', 'general'
    language TEXT DEFAULT 'en',
    turn_count INTEGER DEFAULT 0,
    turn_history TEXT DEFAULT '[]',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 9. Query Cache (Language-Aware Composite Key)
CREATE TABLE IF NOT EXISTS query_cache (
    cache_key TEXT PRIMARY KEY, -- SHA256(normalized_text + "::" + resolved_language)
    query_text TEXT NOT NULL,
    resolved_language TEXT NOT NULL,
    response_json TEXT NOT NULL,
    active_topic TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 10. Certification Journey Progress
CREATE TABLE IF NOT EXISTS journey_progress (
    journey_id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    journey_type TEXT NOT NULL, -- 'get_certified' or 'verify_protect'
    standard_id TEXT,
    scheme TEXT,
    steps_json TEXT NOT NULL,
    readiness_score INTEGER DEFAULT 0,
    metadata_json TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for lightning-fast queries
CREATE INDEX IF NOT EXISTS idx_standards_division ON standards(division);
CREATE INDEX IF NOT EXISTS idx_chunks_standard ON standard_chunks(standard_id);
CREATE INDEX IF NOT EXISTS idx_cert_scheme ON certification_steps(scheme, applies_to);
CREATE INDEX IF NOT EXISTS idx_lab_map_std ON lab_standard_map(standard_id);
CREATE INDEX IF NOT EXISTS idx_lab_city ON testing_labs(city);
CREATE INDEX IF NOT EXISTS idx_journey_session ON journey_progress(session_id, journey_type);
