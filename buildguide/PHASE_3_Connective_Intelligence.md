# Phase 3 — Connective Intelligence: Certification, Verification, Labs, Compliance Chain & Memory

**Time budget:** Hours 9–14 of 24
**Source sections:** §7 (Module 3), §8 (Module 4), §9 (Module 5), §11 (Compliance Chain & Evidence Tagging), §13 (Multi-Turn Memory & Active-Topic), §3.2 (full request lifecycle), §16.2 (Answer pattern)

## 1. Phase Goal

This is the phase the whole pitch depends on. Individually, Modules 3–5 are simple lookups. What makes BIS Saathi more than "six disconnected features" is the **Compliance Chain** — one function that strings Modules 1, 2, 3, and 5 together into a single connected journey — plus **active-topic memory** so a follow-up like "does it apply to export models too?" doesn't lose all context. Both land in this phase. By the end of it, the core demo journey (product description → standard → QCO status → certification steps → labs, in one answer) should work start to finish.

## 2. Deliverables Checklist

- [ ] Module 3 (Certification & Licensing Knowledge) implemented, reading only from the `certification_steps` table
- [ ] Module 4 (Deterministic Verification Engine) implemented with correct extraction ordering
- [ ] Module 5 (Testing Lab Suggester) implemented with city → state → central fallback
- [ ] Compliance Chain function implemented, calling Modules 1, 2, 3, 5 in sequence
- [ ] Evidence Tag object implemented with the three-word status vocabulary
- [ ] Active-topic tracking implemented end-to-end, including on cache hits
- [ ] Full request lifecycle (§3.2) wired in the correct step order
- [ ] Frontend: VerificationPanel, LabFinder, and the four-part Answer Pattern template

## 3. Backend Track

### 3.1 Module 3 — Certification & Licensing Knowledge (§7)
This module has no "logic" to speak of — its entire job is to retrieve the right ordered steps from `certification_steps` and let the LLM explain them conversationally. Implementation notes:
- Filter by `scheme` and `applies_to` (domestic/foreign)
- **Never let the LLM invent a process step at answer time** — `certification_steps` is the only source it may cite for certification questions
- When a fee or timeline figure is requested, prefer surfacing the stored "indicative, verify current schedule" framing over a bare number (per §7's accuracy note) — this is a scope-honesty behavior, not just a data question

### 3.2 Module 4 — Deterministic Verification Engine (§8.1)
A CM/L or HUID check is a database lookup — never something the LLM answers from pattern-matching. Pathway, in strict order:
1. Never pass the whole message into the lookup — extract the code first.
2. For **HUID**: look for a 6-character alphanumeric run.
3. For **CM/L**: require a recognizable prefix (e.g. starting with "CML") before falling back to a bare-digit pattern. This ordering matters — without the prefix-first rule, an incidental number elsewhere in the sentence (a date, a quantity) can get grabbed instead. **Test this ordering explicitly** with a sentence containing both an unrelated number and a real CM/L number.
4. Normalize (uppercase, strip stray punctuation) before comparing against the registry.
5. If nothing plausible can be extracted, ask the user to share the number directly rather than failing silently.
6. On a lookup miss, return a clear "not found" — never a fabricated licensee.

### 3.3 Module 5 — Testing Lab Suggester (§9.1)
1. If no standard is known yet in the conversation, don't return an empty result silently — ask which standard or product needs testing.
2. Otherwise, look up labs mapped to that standard, preferring: user's stated city → state → BIS Central labs (which accept samples nationwide) as the final fallback.
3. City matching is a simple keyword check against your own finite city list — no general-purpose location extraction needed for a closed list you control.

### 3.4 The Compliance Chain (§11.1)
This is one function, not a new table or a rules engine:

```
product description
  -> Module 2 attribute extraction
  -> Module 1 ranked standard candidate
  -> read qco_status directly off that standard's row
  -> IF mandatory: pull matching certification_steps by scheme
  -> pull labs mapped to that standard (Module 5)
  -> assemble one connected answer with a status tag
```

Implement this as a single orchestration function that calls Modules 1, 2, 3, and 5 in sequence and hands the combined result to the LLM as **one context block** — not as separate answers stitched together across multiple turns. This is what turns eight problem-statement bullets into one coherent product.

### 3.5 Evidence Tag (§11.2)
A lightweight structured object attached to every synthesized answer:

| Field | Example |
|---|---|
| `source_type` | directory / clause / registry / faq |
| `reference` | IS 4151:2015, or clause 5.2, or CML1234567 |
| `status` | confirmed / needs verification / not determined |

Status vocabulary — use these exact three states, no more, no fewer:
- **Confirmed** — directly supported by a stored record
- **Needs verification** — a candidate match exists but depends on a detail the user hasn't given
- **Not determined** — no matching record; say so rather than guessing

This costs almost nothing to implement and is one of the more convincing trust signals in front of a judge — don't skip it under time pressure.

### 3.6 Full Request Lifecycle Wiring (§3.2)
Wire the complete sequence now that all modules exist:
1. Create or fetch the session for the session ID **first**, before anything touches the cache.
2. Resolve language (manual override → auto-detect → English fallback). *(Real translation lands in Phase 4; for now, ensure the resolved-language value flows correctly into the cache key.)*
3. Check the cache using the text+language key.
4. **On a cache hit:** still update turn history, and if the cached answer carried a standard citation, update the active topic before returning. A cache hit must never silently skip state updates — test this explicitly (see §6 below).
5. On a miss, non-English text would be translated here in the full pipeline (Phase 4); keep the original text preserved for the final LLM call and session history regardless.
6. Classify intent on the English text, then **unconditionally** prepend the session's active topic to the retrieval query — whether or not a pronoun is present. Don't try to detect pronouns; that detection is itself failure-prone across phrasings.
7. Route to the matching module(s), run the compliance chain if the intent is product-to-standard or QCO-related, update the active topic if a standard was confidently resolved, generate the final answer, then write the turn to history and the cache before returning.

### 3.7 Active-Topic Memory (§13.1)
1. Track a single `active_topic` value in session state — the most recently identified standard.
2. Prepend it to the raw message unconditionally when building the retrieval query.
3. With no active topic yet, the prepended text is simply empty — nothing is lost on a fresh topic.
4. Update the active topic whenever Module 1 or the deep-clause module confidently resolves a standard — **including on cache hits**. Skipping this on the very first repeated question in a session silently breaks the next pronoun follow-up, which is a specific failure mode worth testing directly.

## 4. Frontend Track

1. Build `VerificationPanel` — number input + deterministic result, visually distinct from the chat flow (per §16.1, this should not look like an LLM-generated chat bubble; it should read as a database result).
2. Build `LabFinder` — location-aware lab results panel.
3. Implement the four-part **Answer Pattern** (§16.2) in `MessageBubble`:
   1. **Answer** — one or two plain-language sentences
   2. **What this means** — the technical concept restated simply
   3. **What to do next** — one concrete action
   4. **Why we say this** — the evidence tag from §3.5 above, clickable
4. This is pure response formatting on top of existing backend logic — no new backend work required — but it's the single most visible way to make "grounded, not generated" a felt experience rather than a claim in the pitch deck. Don't shortchange it.

## 5. Testing & Exit Criteria

Do not proceed to Phase 4 until all of these pass (these are pulled directly from §19's edge-case checklist, scoped to what this phase builds):

- [ ] A pronoun-only follow-up right after a standard-specific answer resolves correctly (active-topic tracking works)
- [ ] Repeat that exact sequence a second time so the first question now comes from cache — confirm the pronoun follow-up **still** resolves (cache-hit state update works)
- [ ] A CM/L or HUID number embedded in a sentence with an earlier unrelated number (a date) present extracts the *correct* number, not the date
- [ ] A HUID with mixed letters and numbers round-trips correctly — confirm the field isn't silently truncating to digits-only
- [ ] End-to-end compliance chain test: a product description produces one connected answer covering standard → QCO status → certification steps → matched labs, not three separate disconnected answers
- [ ] Evidence tag correctly shows all three status values across three different test cases (one confirmed, one needs-verification, one not-determined)
- [ ] Ask a deep-clause question about a standard **not** in the flagship set — system says it doesn't have that detail rather than guessing

## 6. Cutline Rule

If the Compliance Chain is flaky by the end of this block, **fall back to answering the three modules separately** rather than shipping a broken connected flow. Per §18.1: a correct disconnected answer beats a confident wrong connected one. The chain is a differentiator, not a dependency — the individual modules must work regardless.

## 7. Handoff to Phase 4

The core product loop — product description in, connected compliance answer out, with memory and evidence — is working in English. Phase 4 makes this reliable under real-world failure conditions (bad keys, real timeouts) and extends it to Hindi without breaking anything built here.
