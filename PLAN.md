# IMPLEMENTATION PLAN: LLM Token & GPU VRAM Inference Cost Calculator 2026

- **Feature**: In-Browser LLM Token & GPU VRAM Inference Cost Calculator (`/tools/llm-calculator.html`)
- **Repository**: `zyekh.com` (`/home/fuckadmin/Projects/zyekh.com`)
- **Theme**: Zero-Dependency, Local-First, Baseline 2024+, Strict No-Emoji

---

## Chunk 1: Create `tools/llm-calculator.html`
- **Target File**: `tools/llm-calculator.html`
- **Scope & Specifications**:
  - Semantic HTML5 structure with `<site-nav active="tools"></site-nav>` and `.main-container`.
  - Schema JSON-LD `SoftwareApplication` / `WebApplication`.
  - Anti-FOUC script & Anti-Clickjacking headers.
  - Interactive multi-model pricing engine (Claude 3.7, GPT-4.5, Gemini 2.0 Flash/Pro, DeepSeek-R1, Llama 3.3).
  - Accurate GPU VRAM sizing model (Model weights + KV-Cache per context & batch size + CUDA overhead).
  - In-browser subword token chunker with RAF-debounced visual boundary highlighter.
  - Zero external dependencies. Pure standard CSS custom properties from `assets/css/shared.css`.
- **Definition of Done (DoD)**:
  - File exists with valid HTML5 and passing all accessibility/structural standards.

---

## Chunk 2: Register Tool in `tools/index.html` & `search-index.json`
- **Target Files**:
  - `tools/index.html`: Add `.tool-item` card following Standard B layout from `DESIGN_SYSTEM.md`.
  - `search-index.json`: Add searchable metadata object for Command Palette (Ctrl+K).
- **Definition of Done (DoD)**:
  - Tool appears in `tools/index.html` grid and searchable in Command Palette.

---

## Chunk 3: Update `IDEAS.md` Status
- **Target File**: `IDEAS.md`
- **Scope**: Mark `LLM Token & GPU Inference Cost Calculator 2026` as `[ DONE ]`.
- **Definition of Done (DoD)**:
  - `IDEAS.md` line reflects `[ DONE ]`.

---

## Chunk 4: Automated Content Sync & QA Verification
- **Target Execution**:
  - Run `python3 sync_content.py` (bumps `sw.js` `CACHE_VERSION`, updates query strings across all HTML files, regenerates `sitemap.xml`, `feed.xml`, `llms.txt`).
  - Run `python3 generate_llms_full.py`.
  - Run `python3 verify_batch.py` & `python3 check_emojis.py`.
  - Check local git status & commit checkpoint.
- **Definition of Done (DoD)**:
  - 100% QA audit pass, 0 emojis, clean local commit.
