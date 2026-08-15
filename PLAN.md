# IMPLEMENTATION PLAN: Defense-in-Depth Systemic Hardening & Reliability Suite

- **Target Repository**: `zyekh.com` (`/home/fuckadmin/Projects/zyekh.com`)
- **Theme**: Safety-First, Zero Over-engineering, Empirical Defense-in-Depth

---

## Chunk 1: Dry-Run Mode & Atomic Write Safety Guard in `sync_content.py`
- **Target File**: `sync_content.py`
- **Scope & Specifications**:
  - Add CLI arguments `--dry-run` and `--bump-version`.
  - When `--dry-run` is provided, print the exact proposed modifications (files to update, new cache version, sitemap counts) without writing to disk.
  - Implement atomic write pattern (`write to .tmp then os.replace()`) to eliminate corrupted partial files during interruptions.
- **Definition of Done (DoD)**:
  - `python3 sync_content.py --dry-run` executes cleanly, outputs predicted changes, and modifies 0 files.
  - `python3 sync_content.py` executes atomic writes without error.

---

## Chunk 2: Strict Secret Masking & Error Trace Redaction in `scripts/syndicate.py` & `run_pipeline.py`
- **Target Files**:
  - `scripts/syndicate.py`
  - `run_pipeline.py`
- **Scope & Specifications**:
  - Build `sanitize_secret_log(text)` function that identifies and scrubs Bearer tokens, passwords, and private API keys from all error logs and stdout prints.
  - Wrap remote API `HTTPError` exceptions to log status code and masked sanitized response bodies rather than raw payload dumps.
- **Definition of Done (DoD)**:
  - `python3 scripts/syndicate.py --status` and `python3 run_pipeline.py --help` execute without error and log scrubbing is active.

---

## Chunk 3: Localhost Smoke Tester & HTTP/DOM Suite (`scripts/smoke_test.py` & Check 21)
- **Target Files**:
  - `scripts/smoke_test.py`: Spawns a background `http.server` on an ephemeral localhost port, tests core page archetypes (`/`, `/about/`, `/contact/`, `/links/`, `/tools/`, `/tools/llm-calculator.html`, `/blog/`, `/blog/linux-vps-hardening-guide-2026.html`, `/blueprints/`, `/offline.html`, `/404.html`), checks HTTP 200/404, Content-Type, CSP headers, Anti-Clickjacking presence, and Anti-FOUC presence.
  - `verify_batch.py`: Add **Check 21 (Localhost Live HTTP Server & Architecture Smoke Test)**.
- **Definition of Done (DoD)**:
  - `python3 scripts/smoke_test.py` passes 100% of tested endpoints.
  - `python3 verify_batch.py` (Checks 1-21) passes with 100% success.

---

## Chunk 4: Documentation, Roadmap & Obsidian RAG Memory Sync
- **Target Files**:
  - `IDEAS.md` (Update roadmap status)
  - `AGENTS.md` / `GEMINI.md` (Codify Protocol 46 & 47)
  - `00-AGY-Memory/zyekh.com/` (`STATE.md`, `DECISIONS.md`, `INDEX.md`)
- **Definition of Done (DoD)**:
  - All documentation synchronized and committed locally.
