
# **LangChain-Based PL/SQL Reverse Engineering & Documentation Tool – v1**

This document outlines the updated architecture and implementation plan for building a **PL/SQL reverse engineering and documentation solution** using **LangChain**, **FastAPI (Python)** for the backend, and a **Svelte + TailwindCSS** frontend. The solution focuses on parsing PL/SQL files and generating human-readable documentation, with future extensibility for requirement mapping and gap analysis.

---

## **1. High-Level Architecture**

```
+----------------+       +------------------+       +---------------------+
|    User (UI)   | <---> | Svelte Frontend  | <---> | FastAPI Backend     |
+----------------+       +------------------+       +---------------------+
                                                      |
                                                      V
                               +---------------------------------------+
                               |      LangChain Chains & Tools         |
                               |---------------------------------------|
                               | - PL/SQL Parsing Chain                |
                               | - Documentation Generation Chain      |
                               +---------------------------------------+
                                                      |
                                                      V
                                           +--------------------+
                                           | PL/SQL Codebase    |
                                           +--------------------+
```

---

## **2. Backend: FastAPI + LangChain**

The backend will:

* Accept codebase input via REST API
* Invoke LangChain pipelines (not agents)
* Return real-time updates or final results to the frontend
* Persist intermediate and final outputs (optionally)

### **LangChain Tools and Chains**

#### 🔧 Tools:

* **CodeLoaderTool**: Loads `.sql`, `.pks`, `.pkb` files and extracts code blocks
* **PLSQLStructureExtractorTool**: Uses LLM to extract package/procedure/function/trigger definitions and dependencies
* **MarkdownFormatterTool**: Formats structured content into clean Markdown
* **SummaryInfererTool**: Generates purpose and logic summaries using prompt templates

#### 🔁 Chains:

* `ParsePLSQLChain`: Loads and extracts logical structure from raw PL/SQL files
* `GenerateDocumentationChain`: Converts extracted metadata into readable documentation
* `GenerateCodebaseSummaryChain`: Aggregates file-level summaries into a holistic report

---

## **3. Task Flow (Phase 1)**

1. **Parse Files** → `ParsePLSQLChain`
2. **Generate File-Level Docs** → `GenerateDocumentationChain`
3. **Generate Project Summary** → `GenerateCodebaseSummaryChain`
4. **Return Output to Frontend** via FastAPI

---

## **4. Frontend Architecture**

### **Tech Stack**

* **Frontend**: Svelte + Tailwind CSS
* **Backend**: Python (FastAPI)
* **Design Language**: Based on [Kafene App UI](https://dribbble.com/shots/14284018-Kafene-New-Application), aligned with HCLTech visual themes

---

## **5. UI/UX Requirements**

### 🎨 **Visual Design**

* Soft, professional colors (HCLTech palette)
* Modern UI: cards, shadowed panels, glassmorphism effects (optional)
* Responsive design across devices

---

### 🧩 **UI Components**

#### 🔹 Input Panel

* Directory/file upload or path input
* “Start Analysis” button
* Config toggles (e.g., verbosity, summary-only)

#### 🔹 Activity Timeline

* Log of task stages (e.g., “Parsing file X”, “Extracted procedures Y”)
* Timestamped updates
* Distinct icons for each chain/tool
* Auto-scroll and animation on updates

#### 🔹 Progress Tracker

* Global progress bar
* Step indicators per processing stage

#### 🔹 Output Viewer

* Rendered Markdown viewer for:

  * Per-file documentation
  * Project summary
* Download options: Markdown, PDF

#### 🔹 Notifications

* Success/failure toasts
* Detailed error logs for failures (e.g., parse error, unsupported syntax)

---

## **6. Interaction Flow**

```plaintext
1. User uploads PL/SQL files or specifies directory
2. Frontend sends config/input to FastAPI backend
3. FastAPI invokes:
   - ParsePLSQLChain → extract structure
   - GenerateDocumentationChain → build docs
   - GenerateCodebaseSummaryChain → compile overall summary
4. Backend sends real-time updates via WebSocket or SSE
5. Frontend renders task logs and displays results
6. User can download or view docs
```

---

## **7. Implementation Plan**

### ✅ Phase 1: Core Reverse Engineering Flow

* [ ] Build FastAPI endpoints:

  * `/start-analysis`
  * `/get-status`
  * `/get-results`
* [ ] Implement LangChain tools + chains
* [ ] Setup frontend: file upload, task tracker, output display

### ⏳ Phase 2+: Extend capabilities

* [ ] Jira Integration Chain (via REST + JQL)
* [ ] Requirement Mapping Chain
* [ ] Gap Analysis Chain
* [ ] Report Synthesis Chain

