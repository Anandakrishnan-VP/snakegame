# BIS Saathi — Intelligent Assistant for Indian Standards & BIS Services
**Problem Statement SIH26107**

BIS Saathi is an AI-powered compliance intelligence system built for the Bureau of Indian Standards (BIS). It bridges the gap between Indian Standards, regulatory schemes, MSMEs, startups, and consumers through grounded conversational assistance, deterministic verification, and laboratory discovery.

---

## 🌟 Key Capabilities

1. **Deterministic-First Grounding ("LLM as Interface, Not System of Record")**:
   - Facts, QCO statuses, schemes, and verification records are retrieved strictly from SQLite.
   - Groq (`llama-3.3-70b-versatile`) synthesizes natural language strictly grounded in retrieved records.
2. **The Compliance Chain (§11)**:
   - One connected journey:
     $$\text{Product Description} \rightarrow \text{Attribute Match (M2)} \rightarrow \text{Directory Match (M1)} \rightarrow \text{QCO Status} \rightarrow \text{Certification Steps (M3)} \rightarrow \text{Testing Labs (M5)}$$
3. **Interactive Source & Clause Inspector ("Tap-to-Inspect")**:
   - Every answer contains an **Evidence Tag** (`confirmed`, `needs verification`, `not determined`).
   - Clicking the citation badge opens the **Source Inspector Modal** displaying verbatim clause text, publication page, and Gazetted QCO orders.
4. **Licence & Hallmark Verification Hub (Module 4)**:
   - Prefix-first CM/L extraction (`CML1234567`).
   - 6-character mixed alphanumeric HUID validation (`AB1234`).
   - Electronics CRS R-Number verification (`R-41001234`).
5. **Testing Laboratory Locator (Module 5)**:
   - City $\rightarrow$ State $\rightarrow$ Central Nationwide Lab fallback.
6. **Bilingual & Hinglish Support (§12)**:
   - Translate-before-route pipeline.
   - Protected tokens (IS codes, numbers, units, and HUID are never garbled by translation).
7. **Active-Topic Memory (§13)**:
   - Seamless pronoun resolution (*"Where can I get it tested in Mumbai?"*).
   - Memory updates even on cache hits.

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
