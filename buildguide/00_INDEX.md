# BIS Saathi — Phase-by-Phase Build Plan (Index)

**Source spec:** `BIS_Saathi_24Hour_Core_Build_Guide.pdf` (SIH26107, Internal Round)
**This document:** Splits that single 24-hour spec into 5 sequential, self-contained build phases, each with its own fully detailed guide file. Each phase has a clear goal, a task breakdown across Data/AI, Backend, and Frontend tracks, a testing checklist, and an exit gate you must clear before starting the next phase.

Why phase it this way: the original roadmap (Section 18) already implies natural checkpoints — but the three parallel columns (Data/AI, Backend, Frontend) make it easy to lose track of *what "done" means* for a given hour block. Each phase file below answers that directly, so at any point in the 24 hours you can open one file and know exactly what to build, in what order, and how to know it's working before you move on.

---

## Phase Map

| Phase | Hours | Focus | File |
|---|---|---|---|
| 1 | 0–4 | Foundation — data model, corpus curation, scaffolding | `PHASE_1_Foundation.md` |
| 2 | 4–9 | Core modules — directory search, attribute matching, router, cache, failover | `PHASE_2_Core_Modules.md` |
| 3 | 9–14 | Connective intelligence — certification, verification, labs, compliance chain, memory | `PHASE_3_Connective_Intelligence.md` |
| 4 | 14–18 | Multilingual hardening, resilience, frontend polish | `PHASE_4_Multilingual_Resilience.md` |
| 5 | 18–24 | Freeze, full dry run, edge-case testing, demo ship | `PHASE_5_Freeze_Test_Ship.md` |

This maps directly onto the original Section 18 sprint roadmap — nothing has been added or removed in scope, it's the same 24 hours, just organized as five gated milestones instead of one long table.

---

## Non-Negotiable Principles (apply in every phase)

These come from Section 3.1 of the source spec and should be re-read at the start of each phase, because time pressure is exactly when they get compromised:

1. **The LLM is the language interface, not the system of record.** Every fact that can be a row in a table (QCO status, a registry record, a clause of text) is retrieved deterministically first, then handed to the model only to be explained in natural language. Never let the LLM "decide" a fact.
2. **Grounded, not generated.** Every factual answer carries a visible source — a standard code, a clause, or a registry record.
3. **Honest about scope.** Deep clause-level detail exists for exactly 2 flagship standards. Everything else is directory-level, and the system says so out loud rather than papering over the gap.
4. **Don't build unused state or speculative schema.** If a table, column, or session field isn't read and acted on by the end of the phase that introduces it, it's a red flag, not a feature.
5. **Simple on the surface.** The user never sees embeddings, routing logic, schema names, or module boundaries — only plain questions and plain answers.

## How to Use These Guides

- Work through phases **in order** — each one assumes the previous phase's exit criteria are met. Don't start Phase 3's compliance chain if Module 1 and Module 2 from Phase 2 aren't returning correct results yet.
- Each phase file has a **Cutline Rule** at the bottom — a fallback if you're running behind schedule. Follow it rather than pushing forward with a shaky foundation.
- The **Testing & Exit Criteria** section at the end of each file is the actual gate. Don't move to the next file until every item passes or is explicitly deferred with a note.
- Section references (e.g. "Section 6.2") point back to the original PDF so you can cross-check exact wording if a task description feels ambiguous.
