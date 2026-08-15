# PLAN: Container Security & OCI Seccomp Profile Generator (/tools/seccomp-generator.html)

## Objectives
1. Build `tools/seccomp-generator.html` — a zero-dependency, local-first Linux container security and OCI Seccomp JSON profile generator with runtime workload profiles (Go/Rust static binary, Node.js, Python, Nginx, Custom), granular syscall category toggles, defaultAction selectors, Kubernetes SecurityContext export, and Docker CLI run commands.
2. Compile deterministic 2400px social cards (16:9 Dark Landscape + 1:1 Light Square) via `scripts/generate_tools_social_cards.py`.
3. Update `scripts/generate_tools_manifest.py` and compile `tools/tools-manifest.json` (50 total tools milestone).
4. Register the tool in `tools/index.html` under `NETWORK SECURITY & LINUX SYSTEMS`.
5. Update `scripts/inject_tool_bridges.py` to link `linux-seccomp-bpf-syscall-filtering-hardening-guide.html` directly to `/tools/seccomp-generator.html`.
6. Update `scripts/smoke_test.py`, run `sync_content.py`, run 21-Axis QA Gate (`verify_batch.py`), 0-emoji audit (`check_emojis.py`), update Obsidian RAG, and record local git commit.

---

## Chunk 1: Build Interactive Tool (`tools/seccomp-generator.html`)
- **Target File**: `tools/seccomp-generator.html`
- **Scope**:
  - Full SEO/GEO tags: Title, Description, Canonical URL, OpenGraph, Twitter Card, Schema.org `WebApplication` + `BreadcrumbList`.
  - Anti-Clickjacking script and Anti-FOUC theme script.
  - Responsive 2-column layout:
    - Left Column: Workload Preset Selector (`Go/Rust Static`, `Node.js Runtime`, `Python Application`, `Nginx Reverse Proxy`, `Custom Hardening`), Default Action Selector (`SCMP_ACT_ERRNO`, `SCMP_ACT_KILL_PROCESS`, `SCMP_ACT_LOG`), Target Architecture flags (`x86_64`, `aarch64`, `x86`), Granular Syscall category checklist (Process Management, Memory & Virtual Allocations, File & Directory I/O, Network & Sockets, IPC & Synchronization).
    - Right Column: Live Output Tabs (OCI JSON Profile `seccomp.json`, Kubernetes YAML SecurityContext, Docker CLI execution command, Raw Syscall whitelist), 1-click clipboard copy (`[ COPIED ]`), and `.json` file download.
  - Interactive Logic: Pure JavaScript dynamic JSON compilation, debounced live preview via `window.debounceRAF`.
- **DoD**: Tool generates valid OCI-compliant seccomp JSON structures with accurate Linux syscall names and formatted Kubernetes YAML manifests without external libraries.

---

## Chunk 2: Social Card & Manifest Compilation
- **Target Files**: `scripts/generate_tools_manifest.py`, `scripts/generate_tools_social_cards.py`, `tools/tools-manifest.json`, `assets/img/social-cards/tool-seccomp-generator-*.png`
- **Scope**:
  - Add `"seccomp": "Security & Linux Systems"` to `CATEGORY_MAP` in `scripts/generate_tools_manifest.py`.
  - Execute `scripts/generate_tools_social_cards.py` to compile deterministic 2400px cards.
  - Execute `scripts/generate_tools_manifest.py` to update `tools/tools-manifest.json` (50 total tools milestone).
- **DoD**: Cards exist with valid dimensions and MD5 uniqueness; `tools-manifest.json` contains valid schema entry for `seccomp-generator`.

---

## Chunk 3: Directory Registration & Global Sync
- **Target Files**: `tools/index.html`, `scripts/inject_tool_bridges.py`, `scripts/smoke_test.py`, `sync_content.py`, `sw.js`
- **Scope**:
  - Add tool card to `tools/index.html` under `NETWORK SECURITY`.
  - Update `scripts/inject_tool_bridges.py` to bridge `linux-seccomp-bpf-syscall-filtering-hardening-guide.html` to `seccomp-generator.html`.
  - Add `/tools/seccomp-generator.html` to localhost smoke test matrix in `scripts/smoke_test.py`.
  - Run `python3 sync_content.py` to auto-bump `CACHE_VERSION`, compile `sitemap.xml` (94 URLs), feeds, `llms.txt`, and `llms-full.txt`.
- **DoD**: `sitemap.xml` contains 94 URLs; all HTML files have updated `CACHE_VERSION` query strings.

---

## Chunk 4: QA Gate Audit & Memory Synchronization
- **Target Files**: `IDEAS.md`, `00-AGY-Memory/zyekh.com/` (`INDEX.md`, `STATE.md`, `DECISIONS.md` ADR-036, Session Log)
- **Scope**:
  - Run `python3 verify_batch.py` (21-Axis QA Gate, 100% PASS).
  - Run `python3 check_emojis.py` (0 emojis).
  - Update `IDEAS.md` (record proposal as completed).
  - Update Obsidian RAG (`INDEX.md`, `STATE.md`, `DECISIONS.md` ADR-036).
  - Save local git commit (NO git push).
- **DoD**: 100% PASS on all verification checks; clean git status.
