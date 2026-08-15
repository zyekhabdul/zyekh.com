# PLAN: Systemd Service Sandboxing & Security Override Generator (/tools/systemd-generator.html)

## Objectives
1. Build `tools/systemd-generator.html` — a zero-dependency, local-first Linux systemd service unit hardening generator and security override builder with workload profiles (Web/API Backend, Database Server, Background Worker, Minimal Daemon, Custom), granular sandboxing directives, dynamic `systemd-analyze security` exposure score calculator (0.0 to 10.0), and drop-in `override.conf` export.
2. Compile deterministic 2400px social cards (16:9 Dark Landscape + 1:1 Light Square) via `scripts/generate_tools_social_cards.py`.
3. Update `scripts/generate_tools_manifest.py` and compile `tools/tools-manifest.json` (51 total tools milestone).
4. Register the tool in `tools/index.html` under `NETWORK SECURITY & LINUX SYSTEMS`.
5. Update `scripts/inject_tool_bridges.py` to link `systemd-service-sandboxing-and-security-hardening.html` directly to `/tools/systemd-generator.html`.
6. Update `scripts/smoke_test.py`, run `sync_content.py`, run 21-Axis QA Gate (`verify_batch.py`), 0-emoji audit (`check_emojis.py`), update Obsidian RAG, and record local git commit.

---

## Chunk 1: Build Interactive Tool (`tools/systemd-generator.html`)
- **Target File**: `tools/systemd-generator.html`
- **Scope**:
  - Full SEO/GEO tags: Title, Description, Canonical URL, OpenGraph, Twitter Card, Schema.org `WebApplication` + `BreadcrumbList`.
  - Anti-Clickjacking script and Anti-FOUC theme script.
  - Responsive 2-column layout:
    - Left Column: Workload Preset Selector (`Web API Backend`, `Database Engine`, `Background Worker`, `Minimal Daemon`, `Custom`), Service Name input (`my-app`), Dynamic `systemd-analyze security` Exposure Meter (0.0 to 10.0 score with color rating), Granular Sandboxing Checkboxes (Filesystem, Privileges, Kernel/Devices, Network/Syscalls).
    - Right Column: Live Output Tabs (Drop-in `override.conf`, Full `<service>.service` unit, Deployment Shell Script, Directives Checklist), 1-click clipboard copy (`[ COPIED ]`), and `.conf` file download.
  - Interactive Logic: Dynamic score computation and template string generation with debounced updates via `window.debounceRAF`.
- **DoD**: Tool generates mathematically accurate systemd directives and formatted `override.conf` drop-in configurations without external libraries.

---

## Chunk 2: Social Card & Manifest Compilation
- **Target Files**: `scripts/generate_tools_manifest.py`, `scripts/generate_tools_social_cards.py`, `tools/tools-manifest.json`, `assets/img/social-cards/tool-systemd-generator-*.png`
- **Scope**:
  - Add `"systemd": "Security & Linux Systems"` to `CATEGORY_MAP` in `scripts/generate_tools_manifest.py`.
  - Execute `scripts/generate_tools_social_cards.py` to compile deterministic 2400px cards.
  - Execute `scripts/generate_tools_manifest.py` to update `tools/tools-manifest.json` (51 total tools).
- **DoD**: Cards exist with valid dimensions and MD5 uniqueness; `tools-manifest.json` contains valid schema entry for `systemd-generator`.

---

## Chunk 3: Directory Registration & Global Sync
- **Target Files**: `tools/index.html`, `scripts/inject_tool_bridges.py`, `scripts/smoke_test.py`, `sync_content.py`, `sw.js`
- **Scope**:
  - Add tool card to `tools/index.html` under `NETWORK SECURITY`.
  - Update `scripts/inject_tool_bridges.py` to bridge `systemd-service-sandboxing-and-security-hardening.html` to `systemd-generator.html`.
  - Add `/tools/systemd-generator.html` to localhost smoke test matrix in `scripts/smoke_test.py`.
  - Run `python3 sync_content.py` to auto-bump `CACHE_VERSION`, compile `sitemap.xml` (95 URLs), feeds, `llms.txt`, and `llms-full.txt`.
- **DoD**: `sitemap.xml` contains 95 URLs; all HTML files have updated `CACHE_VERSION` query strings.

---

## Chunk 4: QA Gate Audit & Memory Synchronization
- **Target Files**: `IDEAS.md`, `00-AGY-Memory/zyekh.com/` (`INDEX.md`, `STATE.md`, `DECISIONS.md` ADR-037, Session Log)
- **Scope**:
  - Run `python3 verify_batch.py` (21-Axis QA Gate, 100% PASS).
  - Run `python3 check_emojis.py` (0 emojis).
  - Update `IDEAS.md` (record proposal as completed).
  - Update Obsidian RAG (`INDEX.md`, `STATE.md`, `DECISIONS.md` ADR-037).
  - Save local git commit (NO git push).
- **DoD**: 100% PASS on all verification checks; clean git status.
