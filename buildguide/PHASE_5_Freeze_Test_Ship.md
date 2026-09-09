# Phase 5 — Freeze, Full Dry Run, Edge-Case Testing & Demo Ship

**Time budget:** Hours 18–24 of 24
**Source sections:** §18 (Hours 18–22 and 22–24 rows), §19 (Testing & Edge-Case Checklist, full), §20 (3-Minute Demo Script), §21 (Known Limitations & Honest Disclosures), §1 (Traceability Map), §17 (Differentiation Priorities)

## 1. Phase Goal

No new features from this point forward. This phase exists to turn a working system into a **reliable, rehearsed, judge-ready demo**. The single biggest differentiator at this stage, per §17, is not a clever feature — it's a system that doesn't crash, doesn't overclaim, and demos the same way every time. Most competing teams will not manage that under time pressure; this phase is how you do.

## 2. Deliverables Checklist

- [ ] Corpus frozen — no further data edits after Hour ~20
- [ ] Backend and API surface frozen — no further endpoint changes
- [ ] Full pass of the §19 edge-case checklist, all 10 items, with results documented
- [ ] Full dry run of the entire system, start to finish, with any breaks fixed
- [ ] §20's 3-minute demo script rehearsed at least twice within the actual time budget
- [ ] One-page "judge Q&A cheat sheet" prepared (traceability table + honest limitations)
- [ ] Screenshots captured and pitch deck polished
- [ ] Demo queries pre-cached and verified warm in both languages (carried over from Phase 4)

## 3. Freeze (Hours 18–22)

1. **Freeze the corpus** — no more additions or edits to `standards`, `standard_chunks`, `certification_steps`, `verification_registry`, `testing_labs`, or `faq`. Any last-minute data change risks re-breaking something already tested.
2. **Freeze the backend and APIs** — no more endpoint signature changes, no new modules. If something breaks in the dry run below, fix the bug, don't add scope.
3. Run a **full dry run** of the entire system across every module and every language you're supporting. Fix whatever breaks. This is not a repeat of Phase 2–4's unit-level tests — it's the whole system, cold, as a judge would actually use it.

## 4. Full Edge-Case Pass (§19)

Run every one of these explicitly and record pass/fail. Do not skip any — each one maps to a specific failure mode the spec identified as likely:

- [ ] Ask about an industry in the directory with no deep-clause coverage — should return directory metadata, not invented clause detail
- [ ] Ask a deep-clause question about a standard **not** in the flagship set — should say it doesn't have that detail, not guess
- [ ] Ask a product question with an attribute the dictionary doesn't recognize — should still return a ranked directory result, just without the attribute boost, not fail
- [ ] Ask a pronoun-only follow-up right after a standard-specific answer — confirms active-topic tracking
- [ ] Repeat that exact sequence a second time so the first question now comes from cache — confirm the pronoun follow-up still resolves
- [ ] Enter a CM/L or HUID number embedded in a sentence with an earlier unrelated number (a date) present — confirms extraction ordering
- [ ] Enter a HUID with mixed letters and numbers — confirms the field isn't silently truncating to digits-only
- [ ] Ask the same question in English, then again in Hindi — confirm the second answer is genuinely in Hindi, not cached English
- [ ] Ask something entirely unrelated to BIS — should decline politely, not attempt an answer
- [ ] Use an invalid provider key, and separately simulate a timeout — confirm fallback fires in both cases, not only on a rate-limit error

Any item that fails: fix if trivial; otherwise, **document it as a known limitation** (§21) rather than leaving it as a silent gap you get caught on live.

## 5. Demo Rehearsal (Hours 22–24)

Rehearse §20's script exactly, timed to the minute:

| Time | Beat | What to say / do |
|---|---|---|
| 0:00–0:20 | Opening | State the problem in one sentence. Point at the persona toggle. |
| 0:20–0:50 | Product-to-standard | Describe a product in plain words (e.g. "stainless steel bottle for children") — show attribute extraction driving the ranked match, not a keyword hit |
| 0:50–1:15 | Compliance chain | Same answer continues into QCO status, certification scheme, and matched labs — one connected journey, not three separate lookups |
| 1:15–1:40 | Evidence | Click the citation badge — show the exact clause/page or registry record behind the claim |
| 1:40–2:00 | Determinism | Speak a full sentence containing a CM/L or HUID via voice input — confirm transcription, then show the instant database-backed verification |
| 2:00–2:25 | Multilingual + pronoun | Switch to Hindi, ask a follow-up using only "it" — shows translate-before-route and active-topic tracking working together, live |
| 2:25–2:45 | Honesty | Ask something outside the indexed corpus — it should decline rather than guess |
| 2:45–3:00 | Close | "This runs as one modular service today, sized for a working demo; every module boundary here is designed to deepen, not rebuild, in a larger build." |

Rehearse this **at least twice**, live, using the actual deployed system — not a mocked walkthrough. If a beat consistently fails or runs long, adjust the script rather than the underlying system this late.

## 6. Judge Q&A Prep

### 6.1 Traceability cheat sheet (§1)
Print or keep on-screen the mapping from each official problem-statement bullet to the module that answers it, so any "does it do X" question gets a one-line, specific answer instead of a description of the whole system:

| Official requirement | Built by | Depth in this build |
|---|---|---|
| Answer questions on Indian Standards | Module 1 + Module 2 deep clause RAG | Full for 2 flagship standards; metadata-level for everything else |
| Recommend applicable standards from product descriptions | Module 2 | Deterministic attribute extraction + re-ranked directory match |
| Guidance on BIS certification schemes | Module 3 | Scheme-I, CRS, FMCS — structured, sourced steps |
| Explain certification processes | Module 3 | Same table, explained conversationally over stored steps |
| Answer consumer-related queries | Module 6 (FAQ) | Grievance filing, general BIS awareness |
| Guide on hallmarking | Module 3 + Module 4 | Process guidance plus live-feeling HUID lookup |
| Suggest testing laboratories | Module 5 | City → state → central fallback, chained off an active standard |
| Support multilingual interaction | §12 Multilingual Engine | English + Hindi committed; voice input as a stretch layer |

### 6.2 Known Limitations, ready to state plainly (§21)
Be ready to say these honestly if asked — overclaiming to a technically literate judge is the fastest way to lose credibility:
- Mock registry is illustrative demo data; a live registry integration is a post-hackathon step
- Deep clause coverage is limited to 2 flagship standards
- Certification fees/timelines vary by source — verify before presenting any figure as exact
- Attribute extraction is a curated dictionary, not open NLU — works well for common product vocabulary, may miss unusual phrasing without breaking the fallback
- Deterministic modules (verification, directory, labs) format replies in English internally, unless you chose to localize them in Phase 4 — state whichever is true for your build
- The router is a heuristic, not a guarantee — genuinely ambiguous or compound questions may route imperfectly, a disclosed trade-off against a per-turn LLM router call

### 6.3 The growth story, in one line
"What you're seeing today is the core of a system we designed to grow — not a prototype we'll have to rebuild if we're selected." Have this ready as your closing line, and be ready to gesture at the module-boundary table from your planning docs if a judge asks what specifically deepens later.

## 7. Final Priority Check (§17)

With whatever time remains, confirm effort was allocated correctly — don't let a lower-priority item consume time a higher one needed:

| Priority | Feature | Status check |
|---|---|---|
| Highest | Product-to-standard attribute matching | Must be rock-solid |
| Highest | Evidence tag + citation badge | Must be rock-solid |
| High | Compliance chain | Should work reliably on the rehearsed demo path at minimum |
| Medium-High | Multilingual (English + Hindi) | Working, or honestly scoped to English-only per Phase 4's cutline |
| Medium | Voice input | Nice to have — cut without guilt if anything above is shaky |
| Low | Related-standards nudges, extra formatting polish | Only if everything above is solid |

## 8. Exit Criteria — You Are Ready When:

- [ ] All 10 edge cases in §19 pass, or have a documented, honest fallback behavior
- [ ] The 3-minute demo script has been rehearsed twice, live, within time budget
- [ ] The judge Q&A cheat sheet (traceability + limitations) is ready and the team has reviewed it
- [ ] The system has run cold (fresh session, no warm state) at least once successfully in the final hour
- [ ] No outstanding "we'll just avoid asking about that" gaps — every known limitation has an honest, prepared answer

This is the end of the 24-hour build. If your team is using this to qualify for a 36-hour final round, keep this frozen build and these phase files as your baseline — the 36-hour extension deepens each module boundary established here without rebuilding any of it.
