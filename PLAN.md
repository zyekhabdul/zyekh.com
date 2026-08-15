# PLAN: Interactive Zero-Trust Architecture Topology Builder (/blueprints/topology-builder.html)

## Objectives
1. Build `blueprints/topology-builder.html` — a zero-dependency, local-first interactive visual editor for designing zero-trust cloud security and kernel architectures.
2. Provide interactive drag-and-drop SVG topology canvas with multi-node linking, custom security subsystems, and 4 architectural presets.
3. Provide live, real-time deterministic multi-format exports: Mermaid.js Markdown, Clean SVG Vector Download, Monospace ASCII Network Map, and JSON Topology Schema.
4. Integrate `blueprints/topology-builder.html` into `blueprints/index.html`, `sitemap.xml`, `llms.txt`, `llms-full.txt`, and synchronize `CACHE_VERSION` in `sw.js` and query strings across all HTML files via `sync_content.py`.
5. Verify 100% compliance across 21-Axis QA Gate (`verify_batch.py`), 0-emoji audit (`check_emojis.py`), update Obsidian RAG, and record local git commit.

---

## Chunk 1: Build Interactive Visual Blueprint (`blueprints/topology-builder.html`)
- **Target File**: `blueprints/topology-builder.html`
- **Scope**:
  - Full SEO/GEO tags: Title, Description, Canonical URL, OpenGraph, Twitter Card, Schema.org `WebApplication` + `BreadcrumbList`.
  - Anti-Clickjacking script and Anti-FOUC theme script.
  - Interactive SVG Canvas with grid rendering, node dragging, dynamic Bezier linking curves, and state store.
  - 4 Pre-built Architecture Presets: Cloud-Native Zero-Trust Mesh, eBPF & Kernel LSM Defense, Vault CA & Bastion Jump Host, and Edge AI & Wasm Sandbox.
  - 4 Multi-Format Live Export Tabs:
    - Tab 1: Mermaid.js Markdown graph code with 1-click copy.
    - Tab 2: Standalone SVG Vector with 1-click `.svg` file download.
    - Tab 3: Monospace ASCII Flow Map with 1-click copy.
    - Tab 4: JSON Topology Spec with import/export capability.
- **DoD**: Tool renders cleanly on localhost, supports smooth node manipulation, generates valid Mermaid/SVG/ASCII outputs, and works 100% offline.

---

## Chunk 2: Directory Integration & Ecosystem Cross-Linking
- **Target Files**: `blueprints/index.html`, `scripts/smoke_test.py`
- **Scope**:
  - Add Featured Interactive Topology Builder banner/card in `blueprints/index.html`.
  - Add `/blueprints/topology-builder.html` to localhost smoke test matrix in `scripts/smoke_test.py`.
- **DoD**: Route `/blueprints/topology-builder.html` returns HTTP 200 OK in live smoke test.

---

## Chunk 3: Global Synchronization & QA Audit Gate
- **Target Files**: `sync_content.py`, `generate_llms_full.py`, `sw.js`, `sitemap.xml`, `llms.txt`, `llms-full.txt`
- **Scope**:
  - Run `python3 sync_content.py` (auto-bump `CACHE_VERSION`, compile `sitemap.xml` with 90 URLs, feeds, `llms.txt`).
  - Run `python3 generate_llms_full.py`.
  - Run `python3 verify_batch.py` (21-Axis QA Gate).
  - Run `python3 check_emojis.py` (0 emojis).
- **DoD**: 100% PASS on all 21 QA checks; 0 emojis detected.

---

## Chunk 4: Memory Synchronization & Local Commit Checkpoint
- **Target Files**: `IDEAS.md`, `00-AGY-Memory/zyekh.com/` (`INDEX.md`, `STATE.md`, `DECISIONS.md` ADR-033, Session Log)
- **Scope**:
  - Update `IDEAS.md` (mark item as [ DONE ]).
  - Record ADR-033 in Obsidian `DECISIONS.md`.
  - Update `INDEX.md` and `STATE.md` with new commit hash.
  - Create local git commit (NO git push).
- **DoD**: Clean git working tree; Obsidian RAG synchronized.
