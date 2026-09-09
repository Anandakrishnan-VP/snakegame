# 🇮🇳 BIS Saathi — Intelligent Assistant for Indian Standards & BIS Services
**Smart India Hackathon Problem Statement: SIH26107**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.0-61DAFB.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-6.0-646CFF.svg)](https://vitejs.dev/)
[![Groq](https://img.shields.io/badge/LLM-Groq%20Cloud-F05A28.svg)](https://groq.com/)
[![Database](https://img.shields.io/badge/Database-SQLite%20%7C%20Supabase%20Postgres-336791.svg)](https://sqlite.org/)
[![Languages](https://img.shields.io/badge/Languages-12%20Indian%20Languages-green.svg)](#-12-major-indian-languages--voice-input)

---

**BIS Saathi** is an AI-powered compliance intelligence system purpose-built for the **Bureau of Indian Standards (BIS)**. It bridges the gap between 21,000+ Indian Standards, statutory Quality Control Orders (QCOs), certification schemes, and testing laboratories for **MSMEs, startups, manufacturers, and everyday consumers**.

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
- [Automated Testing](#-automated-testing)
- [Project Directory Structure](#-project-directory-structure)
- [Cloud Deployment (Vercel)](#-cloud-deployment-vercel)
- [Technical Documentation](#-technical-documentation)

---

## 🌟 Key Features

### 1. 🔗 The Connected Compliance Chain
One connected single-turn journey that eliminates regulatory guesswork:
$$\text{Product Query} \longrightarrow \text{Attribute Match} \longrightarrow \text{Indian Standard (IS)} \longrightarrow \text{QCO Status} \longrightarrow \text{Scheme-I Steps} \longrightarrow \text{Testing Labs}$$

### 2. 🔍 "Tap-to-Inspect" Clause & Source Inspector
- Every recommendation is tagged with an evidence indicator (`confirmed`, `needs verification`, `not determined`).
- Click any **"Tap to Inspect Clause & Order"** badge to open the inspector modal displaying verbatim clause text, publication page, and Gazetted S.O. orders.

### 3. 🛡️ Real-Time Verification Hub
- **BIS CM/L Licences:** Prefix-first CM/L licence extraction and registry verification (e.g., `CML1234567`).
- **Gold Hallmark HUID:** 6-character alphanumeric Hallmarking Unique ID verification (e.g., `AB1234`).
- **Electronics CRS:** Compulsory Registration Scheme R-Numbers (e.g., `R-41001234`).

### 4. 🏢 Hierarchical Testing Lab Locator
- Search 130+ BIS and NABL-recognized testing laboratories.
- Hierarchical fallback: matches labs by city first, expands to state, and falls back to central national laboratories.

### 5. 🌐 12 Major Indian Languages & Voice Input
- Full localization in **12 Indian languages**: English, Hindi (हिन्दी), Tamil (தமிழ்), Telugu (తెలుగు), Marathi (मराठी), Bengali (বাংলা), Gujarati (ગુજરાતી), Kannada (ಕನ್ನಡ), Malayalam (മലയാളം), Punjabi (ਪੰਜਾਬੀ), Odia (ଓଡ଼ିଆ), and Urdu (اردو).
- **Indic Voice-to-Text:** Real-time speech input powered by Groq Whisper Large v3.
- **Protected Technical Tokens:** Standard numbers (`IS 17803:2022`), units, and HUID codes are shielded from mistranslation.

### 6. ⚡ Dual-Engine Database Architecture
- **Local Dev / Offline:** Runs at **0ms** latency using local SQLite (`backend/bis_saathi.db`) with complete offline fallback synthesis.
- **Cloud / Multi-Device:** Optional connection to **Supabase PostgreSQL** for persistent multi-device sessions and cloud deployments.

### 7. 🛡️ Tri-Shield Safety Guardrails
1. **Pre-Guardrail:** Prompt injection interceptor and out-of-scope regulatory boundary enforcement.
2. **Deterministic Grounding:** Database-retrieved evidence passed directly into Groq LLM context.
3. **Post-Guardrail:** Hallucination validator verifying all cited IS codes against the database.

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Client["Frontend Client (React 19 + Vite)"]
        UI["Glassmorphic Responsive UI"]
        Lang["12 Indian Languages Switcher"]
        Tabs["Advisor | Verify | Lab Finder | Directory | Journey"]
        Voice["Groq Whisper Large v3 Voice Input"]
    end

    subgraph API["FastAPI Backend Gateway (Port 8000)"]
        PreGuard["Layer 1: Adversarial & Scope Refusal Guardrail"]
        LangResolve["Language Detection & Token Shielding"]
        Cache["Language-Aware Composite Key Cache"]
        Router["Regex Fast-Path & TF-IDF Semantic Intent Router"]
        
        subgraph Chain["The Compliance Chain Engine"]
            M2["Module 2: Attribute & Keyword Matcher"]
            M1["Module 1: Standards Directory & Tier B Clauses"]
            M3["Module 3: Certification Scheme Mapper"]
            M4["Module 4: Deterministic Registry Verifier"]
            M5["Module 5: Hierarchical Lab Locator"]
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
1. Create and activate a Python virtual environment (recommended):
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
*Backend API runs at: `http://127.0.0.1:8000` (Docs: `http://127.0.0.1:8000/docs`)*

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
- **Select Persona:** Toggle between **MSME / Manufacturer** (compliance steps, licensing, testing costs) and **Consumer** (quality assurance, hallmark checks, complaint filing).
- **Search by Product:** Type what you manufacture or want to buy (e.g., *"I make stainless steel vacuum water bottles for children"* or *"Are helmets mandatory under BIS?"*).
- **Ask Follow-Ups with Context:** The active-topic memory tracks previous turns. You can ask: *"Where can I test this in Mumbai?"* without repeating the standard name.
- **Inspect Citations:** Click the **"Tap to Inspect Clause & Order"** badge on any response to see the exact BIS gazetted notification, clause text, and page references.
- **Voice Query:** Click the microphone icon to speak your question in any supported Indian language.

### 2. 🔍 Verify Licence / HUID (Verification Tab)
- **Check CM/L Number:** Enter any 7-to-8 digit BIS Licence number (e.g., `CML1234567`) to verify manufacturer validity, brand, standard, and expiry.
- **Verify Gold Hallmark:** Enter a 6-character alphanumeric HUID code (e.g., `AB1234`) to verify purity (916/22K, 750/18K), assaying center, and registration date.
- **Check CRS Electronics:** Enter an R-number (e.g., `R-41001234`) to check electronics registration status under Compulsory Registration Scheme.

### 3. 🧪 Testing Laboratory Finder (Lab Finder Tab)
- Search testing labs by **Indian Standard** (e.g., `IS 17803`), **City** (e.g., `Mumbai`, `Bengaluru`), or **State**.
- View complete lab profiles, NABL accreditation status, contact details, and testing scope.

### 4. 📚 Standards Directory (Directory Tab)
- Search and browse through Indian Standards.
- Filter by **Mandatory QCOs** to see which products require compulsory BIS certification before sale or import in India.
- View publication dates, gazetted order numbers, and applicable certification schemes.

### 5. 🗺️ My Journey (Journey Tab)
- Track your step-by-step compliance roadmap from initial inquiry to final ISI Mark / CRS grant.
- Check off completed milestones (sample preparation, testing, factory audit, licence grant).

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

## 🧪 Automated Testing

Run the automated test suite to verify core logic, edge cases, and API endpoints:

```powershell
# 1. Core Module Tests (Directory, Matcher, Schemes, Verification, Labs)
python -m backend.tests.test_core

# 2. Specification §19 Edge-Case Tests (All 10 Edge Cases)
python -m backend.tests.test_edge_cases

# 3. End-to-End FastAPI Endpoint Integration Tests
python -m backend.tests.test_api_endpoints
```

---

## 📁 Project Directory Structure

```
bis/
├── .env.example                # Example environment variables template
├── README.md                   # Clean project documentation & setup guide
├── PRODUCT_INFO.md             # Comprehensive product architecture specification
├── requirements.txt            # Python backend dependencies
├── run_servers.bat             # One-click Windows starter for frontend + backend
├── vercel.json                 # Vercel deployment configuration
├── api/
│   └── index.py                # Serverless entrypoint for cloud hosting
├── backend/
│   ├── main.py                 # FastAPI application, middleware & API routes
│   ├── bis_saathi.db           # Pre-populated SQLite database
│   ├── db/
│   │   ├── database.py         # Dual-engine connection adapter (SQLite / PostgreSQL)
│   │   └── supabase_schema.sql # Cloud PostgreSQL schema DDL
│   ├── services/
│   │   ├── compliance_chain.py # Connected regulatory intelligence engine
│   │   ├── groq_service.py     # Groq LLaMA 3.3 LLM & Whisper STT client
│   │   ├── guardrails.py       # Security, anti-injection & scope enforcement
│   │   ├── intent_router.py    # Fast-path regex & TF-IDF query classifier
│   │   ├── language_service.py # Indic translation & protected token shield
│   │   ├── lab_locator.py      # Geographic lab matching engine
│   │   ├── registry_verifier.py# Deterministic CM/L, HUID & CRS verifier
│   │   ├── scheme_mapper.py    # BIS Scheme-I / Scheme-II workflow steps
│   │   ├── session_manager.py  # Active-topic memory & turn tracker
│   │   └── standards_directory.py # Tier A directory & Tier B clause search
│   └── tests/
│       ├── test_core.py        # Unit tests for core engine modules
│       ├── test_edge_cases.py  # Tests for §19 edge case specifications
│       └── test_api_endpoints.py # Integration tests for FastAPI endpoints
├── frontend/
│   ├── package.json            # Node.js dependencies
│   ├── vite.config.js          # Vite build config with backend proxy
│   └── src/
│       ├── App.jsx             # Main application container & navigation
│       ├── index.css           # Glassmorphic UI design tokens & styling
│       └── components/
│           ├── ChatView.jsx    # Conversational compliance assistant
│           ├── DirectoryBrowser.jsx # Standards catalog & QCO browser
│           ├── LabFinder.jsx   # Testing lab geographical locator
│           ├── VerificationHub.jsx  # CM/L, HUID & CRS registry validator
│           ├── JourneyView.jsx # Compliance milestone progress tracker
│           └── SourceInspectorModal.jsx # Clause & Gazette inspector
└── scripts/
    └── migrate_to_supabase.py  # SQLite to Supabase PostgreSQL migration tool
```

---

## ☁️ Cloud Deployment (Vercel)

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
