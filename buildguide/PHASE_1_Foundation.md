# Phase 1 — Foundation: Data Model, Corpus Curation & Scaffolding

**Time budget:** Hours 0–4 of 24
**Source sections:** §2 (Solution Philosophy), §4 (Data Model), §16.1 (Frontend components), §18 (Hours 0–4 row), Appendix (Tech Stack)

## 1. Phase Goal

Nothing in this phase is "smart" yet — no routing, no LLM calls, no compliance chain. The entire goal is to have a **queryable, honest, seeded database** and a **running skeleton** of both backend and frontend that Phase 2 can immediately start wiring logic into. If Phase 1 slips, everything downstream slips with it — protect this phase's timebox strictly.

The single most important decision made in this phase is **which 2 standards become your flagship deep-clause standards** (§2.1, Tier B). Everything else in the demo's credibility depends on this choice being defensible and genuinely well-covered.

## 2. Deliverables Checklist

- [ ] SQLite database created with all 8 tables from §4, exact fields
- [ ] 2 flagship standards selected and justified in writing (one paragraph each)
- [ ] Tier A broad directory seeded across multiple divisions (target: 15–25 entries minimum)
- [ ] Tier B clause chunks manually curated and source-verified for the 2 flagship standards
- [ ] `verification_registry` seeded with mock CM/L, HUID, and CRS records
- [ ] `testing_labs` + `lab_standard_map` seeded (Central/Regional/Recognized types)
- [ ] `certification_steps` seeded for Scheme-I, CRS, FMCS (domestic + foreign tagged)
- [ ] `faq` table seeded (Standards Clubs, NITS, Grievance Filing at minimum)
- [ ] FastAPI project scaffolded with CORS enabled for the Vite dev origin
- [ ] `/chat`, `/verify`, `/directory` endpoints exist and return stub 200 responses
- [ ] Vite + React + Tailwind scaffolded with HomeView, empty ChatView shell
- [ ] Persona toggle and language selector exist as UI stubs (no pipeline wiring yet)

## 3. Data / AI Track

### 3.1 Choose the 2 flagship standards
This decision drives Tier B for the rest of the build. Pick standards that are:
- Genuinely public enough that you can source-verify every clause chunk before demo day (§2.1 — "small enough that every chunk can be manually checked")
- Relatable in a live demo (a consumer product category judges will immediately understand, e.g. something in the same spirit as the "stainless steel bottle for children" example used throughout the spec)
- Different enough from each other to show breadth (e.g. one household/consumer-safety standard, one electronics/CRS-adjacent standard)

Write one paragraph per standard justifying the choice — you'll want this on hand if a judge asks "why these two?"

### 3.2 Build the Tier A broad directory
Per §5, every entry needs three independent ways to be found: **formal code**, **formal title**, and **everyday synonyms**. The synonym field is the one naive implementations skip, and it's exactly what the product-recommendation bullet in the problem statement depends on.

For each `standards` row, populate:
- `is_code` — formal identifier (e.g. `IS 4151:2015`)
- `title` — formal standard title
- `division` — cement, steel, electronics, food, textiles, chemicals, etc.
- `qco_status` + `qco_reference` — mandatory / voluntary / unknown, plus notification reference if mandatory
- `related_standards` — other codes commonly referenced alongside this one
- `synonyms` — plain product terms a real user would type (this is the field that makes "LED bulb" find "Electric Lamps and Lamp Holders")
- `source_url` — your own verification trail

Spread entries across as many divisions as you can source-verify in the time available. Breadth here is what lets the system credibly claim "spans every BIS-regulated industry at the metadata level" (§2.1) even though depth is reserved for the 2 flagship standards.

### 3.3 Curate Tier B deep-clause content
For each flagship standard, manually chunk the actual clause text into `standard_chunks`:
- `chunk_id`, `standard_id`, `clause`, `sub_clause`, `page`, `content`, `source`

Every chunk must be checked against a real source before it goes in — this is the one place in the entire system where a hallucinated fact would be most damaging, since it's presented as "deep" verified content.

### 3.4 Seed the deterministic-lookup tables
These three tables exist so Modules 3, 4, and 5 (built in Phase 3) never have to guess:

**`certification_steps`** — per §7, store each scheme's steps as an ordered list of short, individually-citable rows:
- Scheme-I (domestic manufacturers) — identify IS code → test at NABL + BIS-recognized lab → apply via Manak Online Form V → pay fees → factory inspection → licence granted (indicative 35–65 days, flagged as "verify current" not exact)
- CRS (electronics/IT, with MeitY) — confirm CRO coverage → test at recognized lab (foreign manufacturers appoint an Authorized Indian Representative) → file via CRS portal → self-declaration, no factory audit → R-number issued
- FMCS (foreign manufacturers) — same as Scheme-I but overseas factory audit + mandatory Authorized Indian Representative
- Tag every row `applies_to` = domestic/foreign and cite a `source`
- **Do not** let the LLM invent a process step later — this table is the only source Module 3 may cite

**`verification_registry`** — mock but realistic records:
- Include at least one CM/L record (`number_type = CML`, text field, recognizable prefix like `CML1234567`)
- Include at least one HUID record — **6-character alphanumeric, mixed letters and numbers**, stored as `TEXT` not `INTEGER` (a numeric field will silently mangle a real HUID)
- Include at least one CRS record
- Include one deliberately "not found" test case (a number that should return a clean miss, not a fabricated result)

**`testing_labs` + `lab_standard_map`** — model as many-to-many from day one (§9): a comma-separated list on the lab record breaks down almost immediately, so use the join table now rather than retrofitting later. Include at least one Central lab (accepts samples nationwide) and a few Regional/Recognized labs across different cities so the city → state → central fallback in Phase 3 has real data to fall through.

**`faq`** — flat table, no chunking needed: `faq_id`, `category`, `question`, `answer`, `source_url`. Minimum content per §10: BIS Standards Clubs, NITS, Consumer Grievance Filing.

### 3.5 What NOT to build (§4 "Deliberately left out")
- No separate QCO table — status lives as two columns directly on `standards`
- No scheme table — schemes are represented as tagged rows in `certification_steps`
- No amendments table
This is the single biggest schema simplification versus a production design, and it's correct for a 24-hour build. Resist the urge to normalize further.

## 4. Backend Track

1. Scaffold FastAPI project structure (routers/, models/, db/).
2. Create the SQLite database with all 8 tables exactly as specified in §4:
   `standards`, `standard_chunks`, `certification_steps`, `verification_registry`, `testing_labs`, `lab_standard_map`, `faq`, `session_state`, `query_cache`.
3. Stub three endpoints — bodies can be placeholders that return fixed JSON for now:
   - `POST /chat`
   - `POST /verify`
   - `GET /directory`
4. Implement basic `session_state` creation/fetch logic. Even though the full request lifecycle isn't wired until Phase 2, get the ordering habit right now: **a session is created or fetched first, before anything touches the cache** (§3.2, step 1) — this is what lets active-topic tracking update correctly on a cache hit later.
5. **Enable CORS explicitly** for the Vite dev server's origin. The spec calls this out directly: without it, every request between Vite and FastAPI on a different port is silently blocked, and it's invisible during backend-only testing until the one moment it matters on stage (§16.2 callout). Do this now, not later.
6. Add `.env` / config scaffolding for Groq and Gemini API keys — placeholders only, don't wire the actual failover chain yet (that's Phase 2).

## 5. Frontend Track

1. Scaffold Vite + React + Tailwind.
2. Build `HomeView`: prompt box + quick-action buttons (§16.1) — e.g. "Check if certification is needed," "Find a testing lab," "Verify a BIS mark."
3. Build an empty `ChatView` shell — layout only, no streaming or state logic yet.
4. Add a **Persona toggle** stub (Consumer / Business) — UI only; per §16.1 this changes tone and quick actions later, never the retrieval pipeline.
5. Add a **Language selector** stub with an explicit **English** option alongside "Auto-detect" (§12.1) — don't make auto-detect the only path, since short English text can misdetect with no way to correct it.

## 6. Testing & Exit Criteria

Do not proceed to Phase 2 until all of these pass:

- [ ] All 8 tables exist and can be queried with real seed data (not empty)
- [ ] FastAPI `/docs` loads; `/chat`, `/verify`, `/directory` all return stub 200 responses
- [ ] A fetch from the Vite dev origin to FastAPI succeeds (CORS actually verified, not assumed)
- [ ] Frontend home screen renders with visible quick-action buttons
- [ ] 2 flagship standards are chosen, documented, and their clause chunks are source-verified
- [ ] At least 15–25 directory entries exist across multiple divisions, each with a real `source_url`
- [ ] At least one HUID test record has mixed letters and numbers and is stored correctly as text (query it back and confirm no truncation)
- [ ] At least one deliberate "not found" verification test case exists

## 7. Cutline Rule

If corpus curation is eating more than half of this 4-hour block, **stop expanding Tier A breadth** and protect Tier B depth on the 2 flagship standards instead — a narrow, fully verified deep-clause set is more defensible on stage than a wide, half-checked directory. You can always add more Tier A rows in Phase 5's freeze window if time remains; you cannot un-embarrass a wrong flagship clause in front of a technical judge.

## 8. Handoff to Phase 2

By the end of this phase, the schema is **frozen** — Phase 2 reads from it, it does not redesign it. Phase 2 begins wiring the actual intelligence: Module 1 (directory search), Module 2 (attribute matching), the intent router, the cache, and the LLM failover chain.
