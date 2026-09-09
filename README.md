# BIS Saathi — Intelligent Assistant for Indian Standards & BIS Services
**Problem Statement SIH26107**

BIS Saathi is an AI-powered compliance intelligence system built for the Bureau of Indian Standards (BIS). It bridges the gap between Indian Standards, regulatory schemes, MSMEs, startups, and consumers through grounded conversational assistance, deterministic verification, and laboratory discovery.

---

> **📖 Complete Documentation**: For an exhaustive, encyclopedic guide to every system component, database schema, and feature, see [PRODUCT_INFO.md](file:///d:/DevAk/bis/PRODUCT_INFO.md).

---

## 🌟 Key Capabilities

1. **Deterministic-First Grounding ("LLM as Linguistic Interface, Not System of Record")**:
   - Facts, QCO statutes, licensing procedures, and verification records are retrieved strictly from SQLite.
   - Groq (`openai/gpt-oss-120b`) synthesizes natural language strictly grounded in retrieved evidence.
2. **The Compliance Chain (§11)**:
   - One connected single-turn journey:
     $$\text{Product Description} \rightarrow \text{Attribute Match} \rightarrow \text{Standard Code} \rightarrow \text{QCO Status} \rightarrow \text{Scheme-I Steps} \rightarrow \text{Testing Labs}$$
3. **Interactive Source & Clause Inspector ("Tap-to-Inspect")**:
   - Every answer contains an interactive **Evidence Tag** (`confirmed`, `needs verification`, `not determined`).
   - Clicking the badge opens the **Source Inspector Modal** displaying verbatim clause text, publication page, and Gazetted QCO orders.
4. **Licence & Hallmark Verification Hub (Module 4)**:
   - Prefix-first CM/L licence extraction (`CML1234567`).
   - 6-character mixed alphanumeric HUID gold hallmark validation (`AB1234`).
   - Electronics CRS R-Number verification (`R-41001234`).
5. **Testing Laboratory Locator (Module 5)**:
   - Hierarchical City $\rightarrow$ State $\rightarrow$ Central Nationwide Lab fallback with NABL recognition.
6. **12 Major Indian Languages & Cross-Language Intelligence (§12)**:
   - Complete UI localization in 12 languages: English, Hindi, Tamil, Telugu, Marathi, Bengali, Gujarati, Kannada, Malayalam, Punjabi, Odia, Urdu.
   - Cross-language typing and speaking tolerance: choose any page language and type/speak in any other language.
   - Protected tokens: IS codes, numbers, units, and HUIDs are never garbled by translation.
7. **Groq Whisper Large v3 Voice Input**:
   - Real-time Indic speech-to-text with multi-dialect support.
8. **Active-Topic Contextual Memory (§13)**:
   - Seamless pronoun resolution (*"Where can I get it tested in Mumbai?"*).
   - Memory updates even on cache hits.
9. **3-Layer Guardrail & Scope Refusal Shield**:
   - Adversarial prompt injection defense, hallucination interceptor, and polite out-of-scope refusal.
10. **Deterministic Offline Fallback Synthesizer**:
    - Generates full 4-part cards directly from SQLite records if API or network is unavailable.

---

## 🚀 Quick Start

### 1. Configure Groq API (Optional)
Copy `.env.example` to `.env` in `bis/`:
```bash
GROQ_API_KEY=your_groq_api_key_here
```
*(If no key is provided, the system seamlessly runs on its offline deterministic synthesis engine).*

### 2. Start Both Servers
Double click `run_servers.bat` or run:
```powershell
# Backend (FastAPI)
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload

# Frontend (React + Vite)
cd frontend
npm run dev
```

Visit: **`http://localhost:5173`**

---

## 🧪 Automated Testing

Run unit tests and full edge-case checklist:
```powershell
# Core backend tests
python -m backend.tests.test_core

# All 10 specification §19 edge-case tests
python -m backend.tests.test_edge_cases

# End-to-end FastAPI endpoint integration tests
python -m backend.tests.test_api_endpoints
```

---

## ⏱️ 3-Minute Golden Demo Script (§20)

| Time | Action | What to Demonstrate |
|---|---|---|
| **0:00–0:20** | **Intro & Persona** | Show the Persona Toggle (MSME vs Consumer) and explain the need for accurate standard discovery. |
| **0:20–0:50** | **Product-to-Standard** | Type: *"I am manufacturing stainless steel vacuum water bottles for kids."* Point out deterministic attribute extraction (*bottle*, *stainless steel*, *kids*). |
| **0:50–1:15** | **Compliance Chain** | Show the unified response: `IS 17803:2022` $\rightarrow$ Mandatory QCO $\rightarrow$ Scheme-I Form V steps $\rightarrow$ Testing Labs in one single answer. |
| **1:15–1:40** | **Tap-to-Inspect Source** | Click the **"Tap to Inspect Clause & Order"** badge. Show the slide-in modal with verbatim Clause 4.1 text and the Gazette QCO order. |
| **1:40–2:00** | **Licence & HUID Verification** | Switch to the **Verify Licence / HUID** tab. Click sample `CML1234567` (Milton) and `AB1234` (Tanishq Hallmark) to show instant registry validation. |
| **2:00–2:25** | **Multilingual + Memory** | Switch language to **हिन्दी**. Ask a pronoun follow-up: *"Where can I test it in Mumbai?"*. Show active-topic memory retaining `IS 17803:2022` and returning Western Regional Lab Mumbai. |
| **2:25–2:45** | **Scope Honesty** | Ask an out-of-scope question (e.g. *"Tell me a movie review"*). Show polite, clear scope boundary rejection. |
| **2:45–3:00** | **Closing** | Emphasize: *"The LLM is the language interface, not the system of record. Every fact is grounded in verified BIS databases."* |
