# Phase 2 — Core Modules: Directory Search, Attribute Matching, Router, Cache & Failover

**Time budget:** Hours 4–9 of 24
**Source sections:** §5 (Module 1), §6 (Module 2), §14 (Rate-Limit Armor), §15 (Intent Router), §3.2 (Request Lifecycle, partial), §12.1 (translate-before-route ordering), Appendix (Embeddings/LLM stack)

## 1. Phase Goal

This is where the system starts *thinking* — but still only in deterministic, explainable ways. By the end of this phase, a user should be able to type a product description or a standards question in English and get back a correctly-ranked result, with the system never crashing on a bad API key or a rate limit. No compliance chain, no certification/verification/lab modules, and no real multilingual support yet — those are Phase 3 and Phase 4. Keep scope tight.

## 2. Deliverables Checklist

- [ ] Module 1 (Two-Tier Directory search) implemented and returning ranked results
- [ ] Module 2 (Product-to-Standard Attribute Matching) implemented as deterministic dictionary matching
- [ ] Local embedding index built (all-MiniLM-L6-v2 or equivalent) for router fallback
- [ ] Intent Router implemented: regex fast-path first, embedding fallback second
- [ ] Query cache implemented with a **language-aware** key (text + resolved language, never text alone)
- [ ] 3-tier LLM failover implemented: Groq → Gemini → optional local model
- [ ] Translate-before-route ordering scaffolded (real translation logic lands in Phase 4, but the pipeline position is fixed now)
- [ ] Frontend: chat window with streaming state, message bubble, citation badge shell

## 3. Data / AI Track

### 3.1 Build the local embedding index
Use a CPU-local model (e.g. `all-MiniLM-L6-v2`) — free, unlimited, no rate-limit exposure. This one index powers two things:
- The intent router's fallback (comparing a query against example utterances per intent)
- The retrieval layer for Tier B clause RAG (even though the full RAG answer flow is fleshed out more in later phases, index it now while you're building embeddings infrastructure anyway)

### 3.2 Write Module 2's attribute dictionaries
Per §6.1, build four keyword/pattern sets:

| Attribute | Extraction approach | Effect on ranking |
|---|---|---|
| Product category | Noun-phrase match against a curated category→division dictionary | Filters candidates to the right division first |
| Material | Keyword list (steel, plastic, stainless steel, aluminium, glass, etc.) | Boosts standards whose title/scope mentions that material |
| Intended user / context | Keyword list (children, food-contact, industrial, household) | Boosts matching scope language; can trigger the one allowed clarifying question |
| Activity | manufacture / import / sell / test, from verb keywords | Used only for phrasing the next action, not for ranking |

Keep these dictionaries small and curated rather than exhaustive — the spec is explicit that this is deliberately *not* an LLM call or a separate ML model: a dictionary-based extractor is fully deterministic, free, instant, and fully explainable if a judge asks how it works.

### 3.3 Write router example phrases
For each intent in §15's table (`STANDARD_SEARCH`, `PRODUCT_TO_STANDARD`, `CERTIFICATION_PROCESS`, `VERIFICATION`, `LAB_SEARCH`, `GENERAL_FAQ`, `OUT_OF_SCOPE`), write:
- 3–5 regex/keyword patterns for clearly-worded cases (e.g. "CM/L", "HUID", "testing lab", "which standard")
- 5–8 example utterances to pre-embed for the fallback comparison

## 4. Backend Track

### 4.1 Module 1 — Two-Tier Directory search (§5.1)
Pathway:
1. Match the lower-cased query against `code`, `title`, and `synonyms` together — a hit on any one field counts.
2. If an industry/division filter is available from context, narrow to that division.
3. Return related standards alongside the main hit, so the assistant can mention them proactively rather than only answering the literal question asked.

### 4.2 Module 2 — Attribute Matching (§6.2)
Pathway:
1. Run all four keyword passes (§3.2 above) over the English query text. Attributes not found are left blank — never guessed or defaulted.
2. Use category + material + intended-user matches as a **scoring boost on top of** Module 1's ordinary text match — not as a hard filter. An imperfect extraction should never zero out a correct result.
3. If the top two candidates differ meaningfully in QCO status *and* the missing attribute would resolve which one applies, ask exactly one clarifying question. Otherwise, proceed with the top-ranked candidate and say so plainly — don't over-ask.
4. Pass the extracted attribute set forward (it feeds the evidence object built in Phase 3) so the "why" trail can eventually show which words drove the match.

### 4.3 Intent Router (§15.1)
1. Maintain the small regex/keyword pattern set per intent for clearly-worded cases.
2. If nothing matches confidently, embed the query locally and compare against the pre-embedded example phrases per remaining intent; route to the highest similarity.
3. **Ordering constraint:** this router should only ever need to handle English text — the translate-before-route step (fully implemented in Phase 4) must run before the router in the final pipeline. Build the router assuming English input now; don't let it develop dependencies on raw multilingual text.

### 4.4 Query Cache (§14.1, point 1)
- Build the cache key from **normalized message text AND resolved language together**. Text alone risks returning an answer resolved for the wrong language once multilingual support lands in Phase 4.
- Even though translation isn't fully wired yet, get the key schema right now so Phase 4 doesn't require a cache-format migration.

### 4.5 3-Tier LLM Failover (§14.1, points 2–4)
1. Attempt Groq, then Gemini, then an optional local model, in strict order.
2. Catch **any** failure at each provider — timeouts, invalid keys, server errors — not only a rate-limit-specific code.
3. Fall through to a plain "please try again shortly" message only if every tier fails.
4. Make the final answer-generation function **always return the same shape** — answer text plus citations together, every time, including on the failure path. This consistency is what keeps the frontend simple.

## 5. Frontend Track

1. Build the `ChatView` conversation state and (if time allows) streaming display.
2. Build `MessageBubble` — answer text plus an inline citation badge shell (the badge itself becomes meaningful once the evidence tag lands in Phase 3, but wire the UI slot now).
3. Wire the chat input to actually call `/chat` and render a real response (even if the response content is still basic Module 1/2 output without the full compliance chain).

## 6. Testing & Exit Criteria

Do not proceed to Phase 3 until all of these pass:

- [ ] Query "LED bulb" resolves via synonyms to the correct IS code (Module 1)
- [ ] Query "stainless steel bottle for children" triggers category + material + intended-user boosts, not just a plain text match (Module 2)
- [ ] A query with two top candidates differing in QCO status, where the missing attribute would resolve it, triggers **exactly one** clarifying question — not zero, not several
- [ ] Cache correctly treats the same text in two different resolved languages as two different keys (test this even before full translation is wired — just simulate a second language tag)
- [ ] Simulate an invalid API key and, separately, a timeout — confirm the failover chain attempts all three tiers in order before returning the graceful fallback message, in both cases
- [ ] Router correctly classifies at least 5 sample utterances per intent from §15's table
- [ ] Chat UI sends a real query and renders a real backend response end-to-end

## 7. Cutline Rule

If Module 2's attribute matching isn't reliably boosting the right candidate by the end of this block, **do not chase it further with more dictionary entries** — ship Module 1's plain directory match as the fallback behavior and revisit Module 2 only if Phase 5's freeze window has slack. A correct plain-search answer beats a wrong "smart" one every time a judge tests it live.

## 8. Handoff to Phase 3

Module 1 and Module 2 are working and tested in isolation. The router, cache, and failover chain are in place. Phase 3 connects these to the certification, verification, and lab modules via the compliance chain, and adds session memory so follow-up questions and pronoun references resolve correctly.
