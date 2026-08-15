# PLAN: WebGPU Shader & Inference Latency Profiler (/tools/webgpu-profiler.html)

## Objectives
1. Build `tools/webgpu-profiler.html` — a zero-dependency, local-first hardware diagnostic and compute benchmarking tool using native WebGPU API (`navigator.gpu`).
2. Provide hardware adapter capabilities discovery (`adapter.info`, GPU limits, `shader-f16` and subgroup feature detection), WGSL compute shader compilation benchmarking, parallel matrix multiplication (GEMM) GFLOPS throughput test, and VRAM memory transfer bandwidth (GB/s) profiling.
3. Generate deterministic 2400px social cards (16:9 Dark Landscape + 1:1 Light Square) via `scripts/generate_tools_social_cards.py`.
4. Update `scripts/generate_tools_manifest.py` and compile `tools/tools-manifest.json` (48 total tools).
5. Register the new tool in `tools/index.html` under category `AI INFRASTRUCTURE`.
6. Update `scripts/smoke_test.py`, run `sync_content.py`, run 21-Axis QA Gate (`verify_batch.py`), 0-emoji audit (`check_emojis.py`), update Obsidian RAG, and record local git commit.

---

## Chunk 1: Build Interactive Tool (`tools/webgpu-profiler.html`)
- **Target File**: `tools/webgpu-profiler.html`
- **Scope**:
  - Full SEO/GEO tags: Title, Description, Canonical URL, OpenGraph, Twitter Card, Schema.org `WebApplication` + `BreadcrumbList`.
  - Anti-Clickjacking script and Anti-FOUC theme script.
  - Responsive 2-column layout (`.grid-2` with `gap: 1.5rem`):
    - Left Column: WebGPU Adapter & Feature Inspector (GPU Vendor, Device, Architecture, Max Buffer Limits, FP16 support flag, Subgroups flag) + Benchmark Control Panel (`Matrix Size`, `Iteration Count`, `[ Run WebGPU Benchmark ]` button).
    - Right Column: Real-time Performance Metrics (GEMM Compute Throughput in GFLOPS/TFLOPS, Shader Compilation Time in ms, VRAM-to-RAM Readback Bandwidth in GB/s, Projected LLM Tokens/sec Matrix for 1B/3B/7B models) + JSON Diagnostic Report Exporter.
  - Interactive Logic: WGSL compute shader execution, buffer mapping (`mapAsync`), fallback graceful message if WebGPU is unsupported, debounced updates via `window.debounceRAF`.
- **DoD**: Tool loads cleanly, detects WebGPU or displays fallback diagnostics, computes real GFLOPS when WebGPU is available, and generates valid benchmark reports.

---

## Chunk 2: Social Card & Manifest Compilation
- **Target Files**: `scripts/generate_tools_manifest.py`, `scripts/generate_tools_social_cards.py`, `tools/tools-manifest.json`, `assets/img/social-cards/tool-webgpu-profiler-*.png`
- **Scope**:
  - Add `"webgpu": "AI & LLM Inference"` to `CATEGORY_MAP` in `scripts/generate_tools_manifest.py`.
  - Execute `scripts/generate_tools_social_cards.py` to compile deterministic 2400px cards.
  - Execute `scripts/generate_tools_manifest.py` to update `tools/tools-manifest.json`.
- **DoD**: Cards exist with valid dimensions and MD5 uniqueness; `tools-manifest.json` contains valid schema entry for `webgpu-profiler`.

---

## Chunk 3: Directory Registration & Global Sync
- **Target Files**: `tools/index.html`, `scripts/smoke_test.py`, `sync_content.py`, `sw.js`
- **Scope**:
  - Add tool card to `tools/index.html` under `AI INFRASTRUCTURE`.
  - Add `/tools/webgpu-profiler.html` to localhost smoke test matrix in `scripts/smoke_test.py`.
  - Run `python3 sync_content.py` to auto-bump `CACHE_VERSION`, compile `sitemap.xml` (92 URLs), feeds, `llms.txt`, and `llms-full.txt`.
- **DoD**: `sitemap.xml` contains 92 URLs; all HTML files have updated `CACHE_VERSION` query strings.

---

## Chunk 4: QA Gate Audit & Memory Synchronization
- **Target Files**: `IDEAS.md`, `00-AGY-Memory/zyekh.com/` (`INDEX.md`, `STATE.md`, `DECISIONS.md` ADR-034, Session Log)
- **Scope**:
  - Run `python3 verify_batch.py` (21-Axis QA Gate, 100% PASS).
  - Run `python3 check_emojis.py` (0 emojis).
  - Update `IDEAS.md` (mark item as [ DONE ]).
  - Update Obsidian RAG (`INDEX.md`, `STATE.md`, `DECISIONS.md` ADR-034).
  - Save local git commit (NO git push).
- **DoD**: 100% PASS on all verification checks; clean git status.
