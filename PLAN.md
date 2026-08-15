# PLAN: JSON Feed v1.1 & Atom RFC 4287 Feed Modernization Suite

## Objectives
1. Implement RFC 4287 compliant `atom.xml` and JSON Feed v1.1 compliant `feed.json` alongside existing RSS 2.0 `feed.xml` in `sync_content.py`.
2. Inject multi-format feed autodiscovery `<link rel="alternate">` tags (`application/rss+xml`, `application/atom+xml`, `application/feed+json`) across all HTML files.
3. Integrate `atom.xml` and `feed.json` into `sitemap.xml`, `robots.txt`, `llms.txt`, `scripts/smoke_test.py`, and `verify_batch.py` (Check 17).
4. Verify 100% PASS on 21-Axis QA Gate, 0 emojis, and commit locally (NO git push).

---

## Chunk 1: Feed Generator Engine in `sync_content.py`
- **Target File**: `sync_content.py`
- **Scope**:
  - Extract ISO 8601 timestamps and social image references for all 35 blog articles.
  - Implement deterministic generation of `atom.xml` (RFC 4287 Atom 1.0).
  - Implement deterministic generation of `feed.json` (JSON Feed v1.1).
  - Inject autodiscovery `<link rel="alternate">` tags for RSS, Atom, and JSON Feed in `<head>` loop.
- **DoD**: `atom.xml` and `feed.json` generated atomically with 35 articles.

---

## Chunk 2: Integration with Robots, Sitemap, Smoke Test & QA Gate
- **Target Files**: `robots.txt`, `scripts/smoke_test.py`, `verify_batch.py`, `llms.txt`
- **Scope**:
  - In `robots.txt`, add pointers for `Feed-RSS`, `Feed-Atom`, `Feed-JSON`.
  - In `scripts/smoke_test.py`, add `/atom.xml` and `/feed.json` to the live HTTP probe matrix.
  - In `verify_batch.py` Check 17, validate XML well-formedness of `atom.xml` and JSON schema validity of `feed.json`.
  - In `sync_content.py`, update `sitemap.xml` and `llms.txt` references.
- **DoD**: QA Gate Check 17 and Check 21 live smoke test pass with 100% success.

---

## Chunk 3: Full-System Verification & Memory Checkpoint
- **Target Files**: `IDEAS.md`, `DEVELOPMENT.md`, `AGENTS.md`, `00-AGY-Memory/zyekh.com/`
- **Scope**:
  - Run `python3 sync_content.py` (atomic execution).
  - Run `python3 verify_batch.py` (21-Axis QA Gate).
  - Run `python3 check_emojis.py`.
  - Update `IDEAS.md`, `AGENTS.md` (ADR-030).
  - Commit locally (NO git push).
  - Update Obsidian RAG (`INDEX.md`, `STATE.md`, `DECISIONS.md`).
- **DoD**: 100% PASS on all QA checks, 0 emojis, clean working tree.
