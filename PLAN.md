# PLAN: Linux Auditd & DFIR Event Rule Generator (/tools/auditd-generator.html)

## Objectives
1. Build `tools/auditd-generator.html` — a zero-dependency, local-first Linux Kernel Audit (`auditd`) rule and daemon configuration builder with enterprise compliance profiles (CIS Benchmark Level 2, PCI-DSS v4.0, SOC2 / DFIR Forensics, Custom), granular subsystem watches, real-time performance overhead estimator, and multi-format exporters (`audit.rules`, `auditd.conf`, `ausearch` forensics cheatsheet, Vector log shipper pipeline).
2. Compile deterministic 2400px social cards (16:9 Dark Landscape + 1:1 Light Square) via `scripts/generate_tools_social_cards.py`.
3. Update `scripts/generate_tools_manifest.py` and compile `tools/tools-manifest.json` (**53 total tools milestone**).
4. Register the tool in `tools/index.html` under `NETWORK SECURITY & LINUX SYSTEMS`.
5. Update `scripts/inject_tool_bridges.py` to link `auditd-kernel-event-monitoring-and-dfir-logging.html` and `linux-audit-logging-with-vector-and-clickhouse-dfir.html` directly to `/tools/auditd-generator.html`.
6. Update `scripts/smoke_test.py`, run `sync_content.py`, run 22-Axis QA Gate (`verify_batch.py`), 0-emoji audit (`check_emojis.py`), update Obsidian RAG, and record local git commit.

---

## Chunk 1: Build Interactive Tool (`tools/auditd-generator.html`)
- **Target File**: `tools/auditd-generator.html`
- **Scope**:
  - Full SEO/GEO tags, Schema.org `WebApplication` + `BreadcrumbList`, Anti-Clickjacking script, and Anti-FOUC theme script.
  - Responsive 2-column layout:
    - Left Column: Preset Selector (`CIS Level 2`, `PCI-DSS v4.0`, `DFIR Forensics`, `Custom`), Buffer & Failure Directives (`-b`, `-f`, `-e`), Subsystem Watch Toggles (Identity/Auth, Executions/Syscalls, Kernel Modules, Mounts, Time Modifications, Network Config, SUID/SGID), Performance Impact Meter (`[ LOW OVERHEAD ]`, `[ HIGH-FIDELITY DFIR ]`).
    - Right Column: Live Output Tabs (`/etc/audit/rules.d/audit.rules`, `/etc/audit/auditd.conf`, `ausearch` / `aureport` CLI Commands, Vector Pipeline Config), 1-click clipboard copy (`[ COPIED ]`), and `.rules` file download.
  - Debounced input event listeners (60ms) using `requestAnimationFrame`.

## Chunk 2: Compile Deterministic Social Cards & Manifest
- **Target Files**:
  - `scripts/generate_tools_manifest.py` (Add `"auditd": "Security & Linux Systems"`)
  - `tools/tools-manifest.json` (53 tools)
  - `assets/img/social-cards/tool-auditd-generator-dark-landscape.png` (2400x1260)
  - `assets/img/social-cards/tool-auditd-generator-light-square.png` (2400x2400)
- **DoD**: Manifest generated with 53 tools, cards compiled cleanly.

## Chunk 3: Ecosystem & Cross-Link Integration
- **Target Files**:
  - `tools/index.html` (Register Auditd Generator card in `.grid-3`)
  - `scripts/inject_tool_bridges.py` (Map `auditd-kernel-event-monitoring-and-dfir-logging` and `linux-audit-logging-with-vector-and-clickhouse-dfir` to `/tools/auditd-generator.html`)
- **DoD**: Tool card registered, tool bridges injected across 35 articles.

## Chunk 4: QA Gate, Master Sync, Obsidian RAG & Checkpoint
- **Target Files**:
  - `scripts/smoke_test.py` (Add `/tools/auditd-generator.html` route)
  - `sync_content.py` (Auto-bump `CACHE_VERSION`, update sitemap to 97 URLs, feeds, `llms.txt`)
  - `generate_llms_full.py` (Regenerate `llms-full.txt`)
  - `verify_batch.py` (Execute 22-Axis QA gate)
  - `check_emojis.py` (Verify 0 emojis)
  - Obsidian RAG Memory (`INDEX.md`, `STATE.md`, `DECISIONS.md` ADR-041, Session Log)
- **DoD**: 100% QA checks pass (22 checks, 32 live smoke test routes, 0 emojis), git commit recorded locally (NO git push).
