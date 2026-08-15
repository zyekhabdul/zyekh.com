# PLAN: Linux PAM & Faillock Account Lockout Policy Generator (/tools/pam-generator.html)

## Objectives
1. Build `tools/pam-generator.html` — a zero-dependency, local-first Linux PAM (Pluggable Authentication Modules) & `pam_faillock` account lockout policy generator with enterprise security profiles (Strict Bastion, Production Server, High-Availability, Custom), granular directives, brute-force resilience calculator, and multi-format config exporters.
2. Compile deterministic 2400px social cards (16:9 Dark Landscape + 1:1 Light Square) via `scripts/generate_tools_social_cards.py`.
3. Update `scripts/generate_tools_manifest.py` and compile `tools/tools-manifest.json` (**52 total tools milestone**).
4. Register the tool in `tools/index.html` under `NETWORK SECURITY & LINUX SYSTEMS`.
5. Update `scripts/inject_tool_bridges.py` to link `pam-tally2-faillock-account-lockout-policy-guide.html` directly to `/tools/pam-generator.html`.
6. Update `scripts/smoke_test.py`, run `sync_content.py`, run 22-Axis QA Gate (`verify_batch.py`), 0-emoji audit (`check_emojis.py`), update Obsidian RAG, and record local git commit.

---

## Chunk 1: Build Interactive Tool (`tools/pam-generator.html`)
- **Target File**: `tools/pam-generator.html`
- **Scope**:
  - Full SEO/GEO tags: Title, Description, Canonical URL, OpenGraph, Twitter Card, Schema.org `WebApplication` + `BreadcrumbList`.
  - Anti-Clickjacking script and Anti-FOUC theme script.
  - Responsive 2-column layout:
    - Left Column: Workload Preset Selector (`Strict Enterprise Bastion`, `Standard Production Server`, `Permissive High-Availability`, `Custom Policy`), Policy Parameters (`deny`, `unlock_time`, `fail_interval`, `root_unlock_time`), Advanced Security Toggles (`even_deny_root`, `audit`, `silent`, `local_users_only`, `nodelay`), Real-Time Brute-Force Resilience Meter (`[ HIGH RESILIENCE ]`, `[ BALANCED ]`, `[ PERMISSIVE ]`).
    - Right Column: Live Output Tabs (`/etc/security/faillock.conf`, `/etc/pam.d/common-auth` stack, `faillock` Admin CLI Commands, Legacy `pam_tally2` Migration), 1-click clipboard copy (`[ COPIED ]`), and `.conf` file download.
  - Debounced input event listeners (60ms) using `requestAnimationFrame`.

## Chunk 2: Compile Deterministic Social Cards & Manifest
- **Target Files**:
  - `scripts/generate_tools_manifest.py` (Add `"pam": "Security & Linux Systems"`)
  - `tools/tools-manifest.json` (52 tools)
  - `assets/img/social-cards/tool-pam-generator-dark-landscape.png` (2400x1260)
  - `assets/img/social-cards/tool-pam-generator-light-square.png` (2400x2400)
- **DoD**: Manifest generated with 52 tools, cards compiled cleanly.

## Chunk 3: Ecosystem & Cross-Link Integration
- **Target Files**:
  - `tools/index.html` (Register PAM Generator card in `.grid-3`)
  - `scripts/inject_tool_bridges.py` (Map `pam-tally2-faillock-account-lockout-policy-guide` to `/tools/pam-generator.html`)
- **DoD**: Tool card registered, tool bridges injected across 35 articles.

## Chunk 4: QA Gate, Master Sync, Obsidian RAG & Checkpoint
- **Target Files**:
  - `scripts/smoke_test.py` (Add `/tools/pam-generator.html` route)
  - `sync_content.py` (Auto-bump `CACHE_VERSION`, update sitemap to 96 URLs, feeds, `llms.txt`)
  - `generate_llms_full.py` (Regenerate `llms-full.txt`)
  - `verify_batch.py` (Execute 22-Axis QA gate)
  - `check_emojis.py` (Verify 0 emojis)
  - Obsidian RAG Memory (`INDEX.md`, `STATE.md`, `DECISIONS.md` ADR-040, Session Log)
- **DoD**: 100% QA checks pass (22 checks, 31 live smoke test routes, 0 emojis), git commit recorded locally (NO git push).
