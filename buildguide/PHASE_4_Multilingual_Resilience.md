# Phase 4 — Multilingual Hardening, Resilience & Frontend Polish

**Time budget:** Hours 14–18 of 24
**Source sections:** §12 (Multilingual Engine, full), §14 (Rate-Limit Armor, real-world hardening), §15 (Out-of-scope handling), §16 (Voice input, evidence-tag polish), §18.1 (Cutline Rules), §21 (Known Limitations)

## 1. Phase Goal

Everything built in Phases 1–3 worked in English, under friendly conditions. This phase makes it survive contact with reality: real API failures (not simulated ones), genuinely correct Hindi responses (not cached English), and out-of-scope questions that decline gracefully instead of confidently guessing. This is also the phase where you explicitly apply the cutline rules from §18.1 — if something here isn't solid, the answer is to scope it down honestly, not to fake it on stage.

## 2. Deliverables Checklist

- [ ] Full translate-before-route pipeline working for Hindi
- [ ] Numbers, units, and standard/clause identifiers protected from translation in both directions
- [ ] Fail-open behavior confirmed: translation failure runs original text through untranslated, doesn't crash
- [ ] Explicit decision made and documented on Module 1/4/5's English-only reply templates (localize or disclose as scope boundary)
- [ ] Real (not simulated) failover tested against an actually invalid key and an actual timeout
- [ ] Out-of-scope questions decline politely and consistently
- [ ] Demo queries pre-cached in both English and Hindi
- [ ] Voice input wired (stretch — only if core chat is stable)
- [ ] Evidence-tag click-through UI polished

## 3. Backend / AI Track

### 3.1 Full Multilingual Pipeline (§12.1)
1. Auto-detect language, or use the explicit dropdown built in Phase 1 that lists English as its own option — not only "Auto-detect." Short English text can otherwise misdetect with no way for the user to correct it.
2. Translate the query to English **before** it reaches routing or retrieval — the router's keywords, the embedding fallback, and the directory's text search are all English-only by design (this ordering was scaffolded in Phase 2; now make it real).
3. Keep the **original-language text** for the final LLM call and session history. The model should generate the reply **directly in the target language** using the English-retrieved context — it should not machine-translate a separately generated English answer. This distinction matters for tone and accuracy; test it explicitly.
4. Explicitly instruct the model to protect numbers, units, and standard/clause identifiers from translation, regardless of response language. An IS code or a HUID should never come back garbled or transliterated.
5. **Fail open:** if translation itself fails, run the original text through untranslated rather than crashing the turn.

### 3.2 Known Boundary — Localize or Disclose
Modules 1, 4, and 5 format their own reply text directly (not via the LLM). Unless you also localize those templates, these three branches will keep answering in English even after the translation fix works everywhere else. **Make an explicit decision now:**
- Option A: Localize the English/Hindi template strings for these three modules (higher effort, more consistent UX)
- Option B: Leave them as a disclosed scope boundary and be ready to say so plainly if asked

Either is acceptable — what's not acceptable is discovering this gap live during a Hindi demo. Document your choice in your team's notes for Phase 5's Q&A prep.

### 3.3 Harden Failover Against Real Failures (§14.1)
Phase 2 built and simulated the 3-tier failover (Groq → Gemini → local). Now test it against **actual** failure conditions, not just mocked error codes:
- An actually invalid API key (not a simulated 401)
- An actual network timeout (throttle or disconnect briefly, don't just inject a fake delay)
- Confirm the fallback message fires only after all three tiers genuinely fail, and that the final answer-generation function still returns the same shape (answer + citations) on this path

### 3.4 Out-of-Scope Handling (§15)
Tune the `OUT_OF_SCOPE` intent's decline behavior. It should:
- Decline politely and briefly, without attempting a partial or hedged answer
- Not loop the user into repeated clarifying questions
- Be consistent across English and Hindi

### 3.5 Pre-Cache Demo Queries
Per §14.1's final point: pre-run and cache your rehearsed demo questions in every language you plan to demonstrate, before going on stage. Remember the cache is language-aware by design — **warming English does not also warm Hindi.** Run your actual demo script (finalized in Phase 5) through both languages now so the live demo hits warm cache, not cold API calls.

## 4. Frontend Track

1. **Voice input** (stretch layer, only if core chat is already stable per the cutline rule below): wire it in, and always show a glance-confirm transcript before sending — a misheard product name or number should be catchable before it reaches the backend.
2. **Evidence-tag click-through polish**: make the citation badge from Phase 3 actually expandable/clickable to show the underlying clause, page, or registry record — this was functional but rough in Phase 3; polish it here.
3. Verify the language selector and persona toggle (scaffolded in Phase 1) are now fully wired to the real pipeline behavior built in this phase.

## 5. Testing & Exit Criteria

Do not proceed to Phase 5 until all of these pass:

- [ ] Ask the same question in English, then again in Hindi — confirm the second answer is **genuinely in Hindi**, not cached English
- [ ] Confirm numbers, units, and standard/clause codes are preserved correctly, untranslated, in the Hindi response
- [ ] Deliberately break translation (e.g. point at an invalid endpoint) — confirm the system runs the original text through untranslated rather than crashing
- [ ] Use an actually invalid provider key, and separately an actual timeout — confirm fallback fires correctly in both real cases, not only simulated ones
- [ ] Ask something entirely unrelated to BIS — confirm a polite decline, not an attempted answer, in both English and Hindi
- [ ] Confirm cache warming in English does not incorrectly serve as a Hindi cache hit
- [ ] If voice input is implemented: confirm the glance-confirm transcript step actually blocks send until confirmed

## 6. Cutline Rules (apply explicitly in this phase, per §18.1)

| If… | Then… |
|---|---|
| Core chat/search isn't stable by the start of this phase | Stop all bonus work (voice input, tag polish) immediately and go back to stabilizing Phases 2–3 |
| Evidence tag isn't working reliably | Prioritize fixing it over building voice input |
| Multilingual is unreliable after honest effort in this phase | **Drop to English-only** for the demo rather than presenting fake or broken Hindi coverage on stage |

These are not soft suggestions — a disclosed, correct English-only system is a stronger demo than a Hindi feature that breaks live.

## 7. Handoff to Phase 5

The full pipeline — English and (if stable) Hindi, real failover, honest out-of-scope handling, polished evidence display — is working end to end. Phase 5 freezes everything built so far, runs the complete edge-case checklist, and rehearses the actual demo.
