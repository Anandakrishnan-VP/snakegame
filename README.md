# 🇮🇳 BIS Saathi — Intelligent Assistant for Indian Standards & BIS Services
**Smart India Hackathon Problem Statement: SIH26107**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-6.0-646CFF.svg)](https://vitejs.dev/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Cloud-F05A28.svg)](https://groq.com/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20Supabase%20Postgres-336791.svg)](https://sqlite.org/)
[![Languages](https://img.shields.io/badge/Languages-12%20Indian%20Languages-green.svg)](#-5-12-major-indian-languages--voice-input)

---

**BIS Saathi** is an enterprise-grade AI compliance intelligence system purpose-built for the **Bureau of Indian Standards (BIS)**. It bridges the gap between 21,000+ Indian Standards, statutory Quality Control Orders (QCOs), certification schemes, testing laboratories, and registry verification for **MSMEs, startups, manufacturers, and everyday consumers**.

> 💡 **Architectural Philosophy:**  
> **"The LLM is the linguistic interface, NOT the system of record."**  
> Every standard code, QCO statute, clause requirement, licence validity, and laboratory detail is retrieved deterministically from verified databases. If a query lies outside the statutory scope of BIS, the system refuses politely rather than hallucinating.

---

## 📑 Table of Contents
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Quick Start Guide](#-quick-start-guide)
- [How to Use BIS Saathi](#-how-to-use-bis-saathi)
- [Database Configuration (SQLite vs Supabase)](#-database-configuration)
- [Automated Testing Suite](#-automated-testing-suite)
- [Project Directory Structure](#-project-directory-structure)
- [Cloud Deployment (Vercel & Supabase)](#-cloud-deployment-vercel--supabase)
- [Technical Documentation](#-technical-documentation)

---

## 🌟 Key Features

### 1. 🔗 The Connected Compliance Chain
A seamless single-turn workflow that eliminates regulatory ambiguity:
$$\text{Product Query} \longrightarrow \text{Attribute Match} \longrightarrow \text{Indian Standard (IS)} \longrightarrow \text{QCO Status} \longrightarrow \text{Scheme-I Steps} \longrightarrow \text{Testing Labs}$$
- Supports 3-letter product tokens (`toy`, `gas`, `rod`, `bar`, `pvc`) with intelligent category boosting.
- Distinguishes **Mandatory QCOs** from **Voluntary Standards** (e.g. `IS 10500:2012` municipal drinking water), avoiding misleading mandatory enforcement alerts on optional standards.

### 2. 🔍 "Tap-to-Inspect" Clause & Source Inspector
- Every advisory is tagged with an evidence indicator (`confirmed`, `needs verification`, `not determined`).
- Click any **"Tap to Inspect Clause & Order"** badge to inspect verbatim clause text, publication page, and Gazetted S.O. orders retrieved directly from official BIS specifications.

### 3. 🛡️ Real-Time Registry Verification Hub
- **BIS CM/L Licences:** Prefix-first CM/L licence extraction and registry verification (e.g., `CML1234567`) showing licensee details, product scope, and expiry.
- **Gold Hallmark HUID:** 6-character alphanumeric Hallmarking Unique ID verification (e.g., `AB1234`) displaying purity (916/22K, 750/18K), assaying center, and registration date.
- **Electronics CRS:** Compulsory Registration Scheme R-Numbers (e.g., `R-41001234`) with model approvals and validity.

### 4. 📢 Live Government Gazette Notices & QCO Bulletin
- **Live Gazette Sync:** Fetches official Ministry gazetted notifications and Quality Control Orders from live government feeds.
- **Notification Bell & Unread Tracking:** Dynamic badge counter showing new notifications with persistent read/unread state in local storage.
- **Status Filtering:** Quickly filter orders by **Extended**, **Upcoming Enforcements**, or **Active** standards.
- **Interactive Judge Demo Toggle:** Easily toggle unread notification state for live presentations.

### 5. 🗺️ End-to-End Certification Journey & Official PDF Export
- **Step-by-Step Roadmaps:** Tailored for **Scheme-I Domestic Manufacturers**, **CRS Electronics Importers**, and **Consumer Verify & Protect**.
- **Interactive Progress Tracker:** Check off milestones (Sample Preparation, NABL Lab Testing, Manak Online Form V, Factory Audit) with instant readiness score updates (0% to 100%).
- **Official PDF Generation:** Download a publication-ready compliance report and roadmap powered by ReportLab (`/api/journey/pdf`).

### 6. 📸 Vision AI & Camera Inspector (VLM)
- Inspect physical products directly using live camera capture or device photo uploads.
- Evaluates ISI Mark logos, Gold Hallmarks, and BIS label plates for authenticity and mandatory labeling compliance.

### 7. 🌐 12 Major Indian Languages & Voice Input
- **Full UI & Advisory Localization:** English, Hindi (हिन्दी), Tamil (தமிழ்), Telugu (తెలుగు), Marathi (मराठी), Bengali (বাংলা), Gujarati (ગુજરાતી), Kannada (ಕನ್ನಡ), Malayalam (മലയാളം), Punjabi (ਪੰਜਾਬੀ), Odia (ଓଡ଼ିଆ), and Urdu (اردو).
- **Indic Voice-to-Text:** Real-time speech recognition powered by Groq Whisper Large v3.
- **Protected Technical Tokens:** Standard designations (`IS 17803:2022`), units, and HUID codes are shielded from mistranslation.
- **Overflow-Protected Navbar:** Responsive header pins the single global language switcher and gazette controls, ensuring zero layout breakages on lengthy scripts (e.g. Malayalam).

### 8. 🧠 Context-Aware Topic Memory & Zero Cache Poisoning
- **Context-Topic Cache Isolation:** Follow-up queries (e.g. *"where can I get it tested?"*) are keyed on `norm(query)::lang::persona::context_topic`, preventing cross-session topic poisoning.
- **Natural Lab-Search Intent Routing:** Regex fast-path catches natural inquiries (*"where can I get it tested?"*, *"where to get this tested"*, *"testing facilities"*) and inherits active topic standards without fallback errors.

### 9. 📚 Responsive Two-Card Standards Directory
- Browse the Indian Standards directory filtered by divisions (Consumer Products, Electronics, Transport, Food, Civil, Metallurgical, Electrotechnical).
- Clean, consistent **two-card list layout** (`.directory-grid`) on desktop and tablets that never collapses into a single full-width stretched card.

### 10. ⚡ Dual-Engine Database Architecture
- **Local Dev / Offline:** Runs at **0ms** latency using local SQLite (`backend/bis_saathi.db`) with complete offline fallback synthesis.
- **Cloud / Multi-Device:** Optional connection to **Supabase PostgreSQL** for persistent multi-device sessions and cloud deployments.

### 11. 🛡️ Tri-Shield Safety Guardrails
1. **Pre-Guardrail:** Prompt injection interceptor and out-of-scope regulatory boundary enforcement.
2. **Deterministic Grounding:** Database-retrieved evidence passed directly into Groq LLM context.
3. **Post-Guardrail:** Hallucination validator verifying all cited IS codes against the database.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Client["Frontend Client (React 19 + Vite)"]
        UI["Glassmorphic Responsive UI"]
        Lang["12 Indian Languages Switcher (Single Navbar)"]
        Tabs["Advisor | Verify | Lab Finder | Directory | Journey"]
        Voice["Groq Whisper Large v3 Voice Input"]
        VLM["Live Camera & Image Inspector"]
        GazetteModal["Live Gazette & QCO Bulletin Modal"]
    end

    subgraph API["FastAPI Backend Gateway (Port 8000)"]
        PreGuard["Layer 1: Adversarial & Scope Refusal Guardrail"]
        LangResolve["Language Detection & Token Shielding"]
        Cache["Context-Topic Composite Key Cache"]
        Router["Regex Fast-Path & TF-IDF Semantic Intent Router"]
        
        subgraph Chain["The Compliance Chain Engine"]
            M2["Module 2: Attribute & Keyword Matcher (3-Letter Tokens)"]
            M1["Module 1: Standards Directory & Tier B Clauses"]
            M3["Module 3: Certification Schemes (Scheme-I / CRS / Voluntary)"]
            M4["Module 4: Deterministic Registry Verifier"]
            M5["Module 5: Hierarchical Lab Locator (City -> State -> Central)"]
            QCO["Gazette Bulletin Live Scraper & Feed"]
            Journey["Journey Progress & ReportLab PDF Generator"]
        end

        Synth["Groq Cloud LLM Synthesizer (LLaMA 3.3 70B)"]
        Fallback["Deterministic Offline Fallback Synthesizer"]
        PostGuard["Layer 3: Grounding & Hallucination Interceptor"]
        Session["Session State & Active-Topic Turn Tracker"]
    end

    subgraph Storage["Dual Storage Layer"]
        SQLite[("Local SQLite (bis_saathi.db) - Default")]
        Supabase[("Supabase PostgreSQL (Optional Cloud)")]
    end

    Client <--> API
    API <--> Storage
```

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.10+**
- **Node.js 18+** and `npm`
- **Git**

---

### Step 1: Clone Repository
```bash
git clone https://github.com/Anandakrishnan-VP/snakegame.git
cd snakegame
```

---

### Step 2: Set Up Backend
1. Create and activate a Python virtual environment:
   ```powershell
   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. *(Optional)* Configure environment variables:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Add your Groq API key:
   ```env
   GROQ_API_KEY=gsk_your_groq_key_here
   ```
   > 📌 **Note:** If `GROQ_API_KEY` is not provided, BIS Saathi operates seamlessly using its built-in **100% offline deterministic synthesis engine**.

---

### Step 3: Set Up Frontend
```bash
cd frontend
npm install
cd ..
```

---

### Step 4: Run the Application

#### Option A: One-Click Launch (Windows)
Double-click **`run_servers.bat`** in the root directory. It automatically opens two terminal windows for backend and frontend.

#### Option B: Manual Launch (Two Terminals)

**Terminal 1 — Backend (FastAPI):**
```powershell
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend API runs at: `http://127.0.0.1:8000` (Swagger Docs: `http://127.0.0.1:8000/docs`)*

**Terminal 2 — Frontend (React + Vite):**
```powershell
cd frontend
npm run dev
```
*Frontend runs at: `http://localhost:5173`*

Open **`http://localhost:5173`** in your browser to start using BIS Saathi!

---

## 📖 How to Use BIS Saathi

### 1. 💬 AI Compliance Advisor (Chat Tab)
- **Select Persona:** Toggle between **MSME / Manufacturer** (licensing steps, testing costs, concessions) and **Consumer** (quality marks, hallmark checks, complaint procedures).
- **Search by Product:** Describe what you manufacture or wish to purchase (e.g., *"I make stainless steel vacuum flasks for children"* or *"Are two-wheeler helmets mandatory under BIS?"*).
- **Ask Follow-Ups with Context:** The conversation memory tracks the active standard. You can simply ask: *"Where can I get it tested?"* without repeating the standard code.
- **Inspect Citations:** Click the **"Tap to Inspect Clause & Order"** badge to inspect the exact gazetted notification, clause text, and page references.
- **Voice & Camera AI:** Click the microphone icon for speech input in any of the 12 languages, or the camera icon to inspect physical mark labels.

### 2. 🔍 Verify Licence / HUID / CRS (Verification Tab)
- **Check CM/L Number:** Enter any 7-to-8 digit BIS Licence number (e.g., `CML1234567`) to verify manufacturer validity, brand, standard, and expiry.
- **Verify Gold Hallmark:** Enter a 6-character alphanumeric HUID code (e.g., `AB1234`) to verify purity (916/22K, 750/18K), assaying center, and registration date.
- **Check CRS Electronics:** Enter an R-number (e.g., `R-41001234`) to check registration status under the Compulsory Registration Scheme.

### 3. 🧪 Testing Laboratory Finder (Lab Finder Tab)
- Search testing labs by **Indian Standard** (e.g., `IS 17803`), **City** (e.g., `Mumbai`, `Bengaluru`), or **State**.
- View complete lab profiles, NABL accreditation status, contact details, and testing scope.

### 4. 📚 Standards Directory (Directory Tab)
- Search and browse through Indian Standards in a clean **two-card list layout**.
- Filter by division (Consumer Products, Electronics, Transport, Food, Civil, Metallurgical, Electrotechnical) or search by IS code/keywords.
- Inspect mandatory QCO order dates, gazetted order numbers, and applicable certification schemes.

### 5. 🗺️ My Certification Journey (Journey Tab)
- Track your step-by-step compliance roadmap from initial inquiry to final ISI Mark / CRS grant.
- Check off completed milestones (sample preparation, testing, factory audit, licence grant).
- Download your official compliance roadmap as a publication-ready PDF.

### 6. 📢 Live Gazette Bulletin (Top Navbar Bell)
- Click the notification bell in the top navbar to view the latest Quality Control Orders and gazetted amendments.
- Filter by extended or upcoming orders, or click **"Sync with Live Gazette"** to refresh.

---

## 🗄️ Database Configuration

BIS Saathi includes a **dual-engine database architecture**:

| Feature | Local SQLite (Default) | Supabase PostgreSQL (Optional) |
|---|---|---|
| **Use Case** | Local development, offline demos, zero setup | Multi-device deployments, cloud hosting |
| **Response Time** | `~0ms` (local disk) | Network dependent (~50-200ms) |
| **Setup Required** | None (pre-populated `bis_saathi.db`) | Provide `DATABASE_URL` in `.env` |
| **Offline Support** | ✅ 100% Offline | ❌ Requires Internet |

### Using Local SQLite (Recommended for Local Dev)
Ensure `DATABASE_URL` is commented out or blank in your `.env` file:
```env
# DATABASE_URL=postgresql://...
```
The app will automatically use `backend/bis_saathi.db`.

### Using Supabase PostgreSQL (Cloud Database)
1. Run the schema script `backend/db/supabase_schema.sql` in your Supabase SQL Editor.
2. Run the migration script to copy all standards and clauses:
   ```bash
   python scripts/migrate_to_supabase.py "postgresql://postgres.xxx:password@aws-0-region.pooler.supabase.com:6543/postgres"
   ```
3. Set `DATABASE_URL` in your `.env` file:
   ```env
   DATABASE_URL="postgresql://postgres.xxx:password@aws-0-region.pooler.supabase.com:6543/postgres"
   ```

---

## 🧪 Automated Testing Suite

BIS Saathi includes an exhaustive automated test suite covering unit logic, edge cases, session persistence, journey services, and guardrails:

```powershell
# 1. Specification & Persona Edge-Case Tests (All 15 Edge Cases - 100% Pass)
python backend/tests/test_edge_cases.py

# 2. Live Multi-Turn Session Persona Persistence & Cross-Session Cache Isolation
python -m backend.tests.test_session_persona

# 3. Core Engine Module Tests (Directory, Matcher, Schemes, Verification, Labs)
python -m backend.tests.test_core

# 4. Certification Journey & PDF Generator Tests
python -m backend.tests.test_journey

# 5. Tri-Shield Guardrail & Anti-Injection Tests
python -m backend.tests.test_guardrails

# 6. Clause-Level Semantic & Keyword Retrieval Tests
python -m backend.tests.test_clause_retrieval

# 7. End-to-End FastAPI Endpoint Integration Tests
python -m backend.tests.test_api_endpoints
```

---

## 📁 Project Directory Structure

```
bis/
├── .env.example                     # Example environment variables template
├── README.md                        # Project documentation & setup guide
├── PRODUCT_INFO.md                  # Detailed product architecture specification
├── requirements.txt                 # Python backend dependencies
├── run_servers.bat                  # One-click Windows starter for frontend + backend
├── vercel.json                      # Vercel deployment configuration
├── api/
│   └── index.py                     # Serverless entrypoint for cloud hosting
├── backend/
│   ├── main.py                      # FastAPI app, routing lifecycle & cache integration
│   ├── bis_saathi.db                # Pre-populated SQLite database
│   ├── db/
│   │   ├── database.py              # Dual-engine database adapter (SQLite / PostgreSQL)
│   │   └── supabase_schema.sql      # Cloud PostgreSQL schema DDL
│   ├── services/
│   │   ├── compliance_chain.py      # Connected regulatory intelligence chain
│   │   ├── conversational_handler.py# Pleasantry & chit-chat classifier
│   │   ├── guardrails.py            # Security, anti-injection & scope enforcement
│   │   ├── intent_router.py         # Regex fast-path & TF-IDF query classifier
│   │   ├── journey_pdf.py           # ReportLab PDF roadmap export generator
│   │   ├── journey_service.py       # Journey milestone & readiness score engine
│   │   ├── llm_groq.py              # Groq LLaMA 3.3 LLM & deterministic synthesis
│   │   ├── module1_directory.py     # Standards directory & Tier B clause search
│   │   ├── module2_matcher.py       # Product attribute & keyword matching engine
│   │   ├── module3_certification.py # BIS Scheme-I, CRS & Voluntary workflow steps
│   │   ├── module4_verification.py  # Deterministic CM/L, HUID & CRS verifier
│   │   ├── module5_labs.py          # Hierarchical lab locator (City -> State -> Central)
│   │   ├── multilingual.py          # Indic translation & protected token shield
│   │   ├── qco_bulletin.py          # Live Gazette notification scraper & feed
│   │   ├── session_manager.py       # Context-topic memory & composite cache
│   │   ├── transcription.py         # Groq Whisper Large v3 voice transcription
│   │   ├── vlm_service.py           # Vision AI inspection service
│   │   └── web_search.py            # External regulatory portal fallback search
│   └── tests/
│       ├── test_edge_cases.py       # Specification §19 edge case tests (15 cases)
│       ├── test_session_persona.py  # Multi-turn persistence & cache isolation tests
│       ├── test_core.py             # Core compliance chain module tests
│       ├── test_journey.py          # Certification roadmap & PDF tests
│       ├── test_guardrails.py       # Adversarial prompt injection & scope tests
│       ├── test_clause_retrieval.py # Clause-level retrieval unit tests
│       └── test_api_endpoints.py    # FastAPI endpoint integration tests
├── frontend/
│   ├── package.json                 # React 19, Lucide, Vite dependencies
│   ├── vite.config.js               # Vite build config with API proxy
│   └── src/
│       ├── App.jsx                  # Main app shell, responsive header & navigation
│       ├── index.css                # Glassmorphic UI design tokens & two-column grid
│       ├── api/
│       │   └── config.js            # Dynamic backend API URL configuration
│       ├── i18n/
│       │   └── translations.js      # 100% key parity dictionary for 12 Indian languages
│       └── components/
│           ├── CameraModal.jsx      # Live camera capture & image upload modal
│           ├── ChatView.jsx         # Conversational compliance assistant
│           ├── DirectoryBrowser.jsx # Standards catalog with responsive 2-card grid
│           ├── Footer.jsx           # Official BIS Saathi footer & navigation links
│           ├── JourneyView.jsx      # Compliance milestone tracker & PDF export
│           ├── LabFinder.jsx        # Testing lab geographical locator
│           ├── QcoBulletinModal.jsx # Live Gazette bulletin with unread badge & demo toggle
│           ├── SourceInspectorModal.jsx # Clause & Gazette order inspector modal
│           ├── VerificationPanel.jsx# CM/L, HUID & CRS registry verification hub
│           └── VoiceModal.jsx       # Groq Whisper voice input modal
└── scripts/
    └── migrate_to_supabase.py       # SQLite to Supabase PostgreSQL migration tool
```

---

## ☁️ Cloud Deployment (Vercel & Supabase)

BIS Saathi is pre-configured for full-stack deployment on Vercel:

1. Push your repository to GitHub:
   ```bash
   git push origin main
   ```
2. Import repository into [Vercel](https://vercel.com).
3. Set environment variables in the Vercel dashboard:
   - `GROQ_API_KEY`: Your Groq Cloud API key.
   - `DATABASE_URL`: *(Optional)* Your Supabase PostgreSQL connection string.
4. Click **Deploy**. Vercel will build the React SPA frontend and deploy the FastAPI backend serverlessly via `/api/index.py`.

---

## 📖 Technical Documentation

For an exhaustive technical specification covering the mathematical formulations, TF-IDF ranking algorithms, gazetted QCO references, and data dictionary, please consult:
- 📘 [PRODUCT_INFO.md](PRODUCT_INFO.md)

---

## ⚖️ License & Disclaimer

- Built for the **Smart India Hackathon (Problem Statement SIH26107)**.
- **Disclaimer:** BIS Saathi is an AI compliance assistant intended for guidance and informational purposes. Regulatory applicants should confirm specific legal obligations with the [official Bureau of Indian Standards portal](https://www.bis.gov.in).
