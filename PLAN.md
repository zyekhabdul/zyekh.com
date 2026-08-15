# IMPLEMENTATION PLAN: Social Card Cache-Busting & Web AI Agent Tool Manifest Suite

- **Target Repository**: `zyekh.com` (`/home/fuckadmin/Projects/zyekh.com`)
- **Theme**: Performance, Zero Over-engineering, AI-Agent Ingestion Optimization (GEO)

---

## Chunk 1: OpenGraph & Twitter Social Card Cache-Busting in `sync_content.py`
- **Target File**: `sync_content.py`
- **Scope & Specifications**:
  - In `sync_content.py` HTML rewriting pass, detect `<meta property="og:image">` and `<meta name="twitter:image">`.
  - Append/synchronize `?v=<version>` query parameter to ensure external crawlers (Discord, Telegram, X, LinkedIn, Facebook) never serve stale social card previews when images are updated.
  - Apply across all 91 HTML files using `atomic_write()`.
- **Definition of Done (DoD)**:
  - `python3 sync_content.py --dry-run` shows predicted `og:image` updates.
  - `python3 sync_content.py` applies query strings cleanly across all HTML files.

---

## Chunk 2: Web AI Agent Tool Manifest Generator (`scripts/generate_tools_manifest.py`) & GEO Integration
- **Target Files**:
  - `scripts/generate_tools_manifest.py`: Extracts structured JSON schema for all 43 client-side tools (parameters, input fields, descriptions, execution model) into `tools/tools-manifest.json`.
  - `sync_content.py`: Invoke tool manifest generator during automated content synchronization.
  - `llms.txt` & `robots.txt`: Expose direct reference to `/tools/tools-manifest.json` for Browser AI agents.
  - `verify_batch.py`: Check 18 verifies that `tools/tools-manifest.json` exists and covers 100% of tools in `tools/*.html`.
- **Definition of Done (DoD)**:
  - `tools/tools-manifest.json` generated containing all 43 tools.
  - `verify_batch.py` passes 100% with tool manifest validation.

---

## Chunk 3: Full-System Empirical Verification & Obsidian RAG Sync
- **Target Files**:
  - `IDEAS.md`
  - `DEVELOPMENT.md`
  - `00-AGY-Memory/zyekh.com/` (`INDEX.md`, `STATE.md`, `DECISIONS.md`)
- **Definition of Done (DoD)**:
  - `python3 verify_batch.py` (Checks 1-21) passes 100%.
  - `python3 check_emojis.py` reports 0 emojis.
  - Local git commit created (No git push).
  - Obsidian RAG synchronized.
