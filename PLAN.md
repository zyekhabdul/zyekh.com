# PLAN: Linux Security sysctl & sshd Hardening Config Builder

## Objectives
1. Build `/tools/linux-hardening-generator.html` — a zero-dependency, local-first, interactive configuration builder for Linux kernel `/etc/sysctl.d/99-hardening.conf` and OpenSSH `/etc/ssh/sshd_config.d/99-hardened.conf`.
2. Generate social share cards (16:9 Dark Landscape + 1:1 Light Square) for the new tool via `scripts/generate_tools_social_cards.py`.
3. Update `scripts/generate_tools_manifest.py` and compile `tools/tools-manifest.json`.
4. Register the new tool in `tools/index.html` with category `NETWORK SECURITY` and full keyword filtering attributes.
5. Synchronize sitemap, feeds, llms.txt, llms-full.txt, and bump `CACHE_VERSION` in `sw.js` and query strings across all HTML files via `sync_content.py`.
6. Run 21-Axis QA Gate (`verify_batch.py`), 0-emoji audit (`check_emojis.py`), update Obsidian RAG, and record local git commit.

---

## Chunk 1: Build Interactive Tool (`tools/linux-hardening-generator.html`)
- **Target File**: `tools/linux-hardening-generator.html`
- **Scope**:
  - Full SEO/GEO tags: Title, Description, Canonical URL, OpenGraph, Twitter Card, Schema.org `WebApplication` + `BreadcrumbList`.
  - Anti-Clickjacking script and Anti-FOUC theme script.
  - Responsive 2-column layout (`.grid-2` with `gap: 1.5rem`):
    - Left Column: Target Workload Profile Select (`Web / API Server`, `High-Performance Database`, `Hardened Bastion Host / Jump Server`, `Edge Gateway / Load Balancer`, `Minimal VPS`), Kernel hardening toggles (`TCP SYN Cookies`, `TCP BBR Congestion`, `Reverse Path Filtering`, `Disable ICMP Redirects`, `Disable Source Routing`, `TCP Timestamps`, `Kernel ASLR Level 2`, `Disable Unprivileged eBPF`, `Restrict dmesg Access`, `Disable Core Dumps`), and SSH Hardening toggles (`Custom Port`, `Disable Root Login`, `Disable Password Auth`, `MaxAuthTries 3`, `Modern Kex/Ciphers`, `AllowAgentForwarding No`, `ClientAliveInterval 300`).
    - Right Column: Live tabbed preview (`/etc/sysctl.d/99-hardening.conf` vs `/etc/ssh/sshd_config.d/99-hardened.conf`), 1-click clipboard copy, and direct `.conf` download buttons.
  - Interactive Logic: Debounced input listeners (`window.debounceRAF`), dynamic config recalculation, clean vanilla JS event handling.
- **DoD**: Tool loads correctly, generates valid Linux config files, and copy/download actions function 100% offline.

---

## Chunk 2: Social Card & Manifest Compilation
- **Target Files**: `scripts/generate_tools_manifest.py`, `scripts/generate_tools_social_cards.py`, `tools/tools-manifest.json`, `assets/img/social-cards/tool-linux-hardening-generator-*.png`
- **Scope**:
  - Add `"linux-hardening": "Security & Linux Systems"` to `CATEGORY_MAP` in `scripts/generate_tools_manifest.py`.
  - Execute `scripts/generate_tools_social_cards.py` to compile deterministic 2400px cards.
  - Execute `scripts/generate_tools_manifest.py` to update `tools/tools-manifest.json`.
- **DoD**: Cards exist with valid dimensions and MD5 uniqueness; `tools-manifest.json` contains valid schema entry for `linux-hardening-generator`.

---

## Chunk 3: Directory Registration & Global Sync
- **Target Files**: `tools/index.html`, `sync_content.py`, `sw.js`
- **Scope**:
  - Add tool card to `tools/index.html` in `.grid-3` under `NETWORK SECURITY`.
  - Run `python3 sync_content.py` to auto-bump `CACHE_VERSION`, compile `sitemap.xml`, `atom.xml`, `feed.json`, `llms.txt`, and `llms-full.txt`.
- **DoD**: `sitemap.xml` contains 89 URLs; all HTML files have updated `CACHE_VERSION` query strings.

---

## Chunk 4: QA Gate Audit & Memory Synchronization
- **Target Files**: `IDEAS.md`, `STATE.md`, `DECISIONS.md` (Obsidian RAG `00-AGY-Memory/zyekh.com/`)
- **Scope**:
  - Run `python3 verify_batch.py` (21-Axis QA Gate, 100% PASS).
  - Run `python3 check_emojis.py` (0 emojis).
  - Update `IDEAS.md` (mark item as [ DONE ]).
  - Update Obsidian RAG (`INDEX.md`, `STATE.md`, `DECISIONS.md` ADR-032).
  - Save local git commit (NO git push).
- **DoD**: 100% PASS on all verification checks; clean git status.
