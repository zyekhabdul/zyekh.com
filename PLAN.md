# PLAN: Implementasi Ground-Truth Metric Parity & Anti-AI Hallucination Engine (Opsi 2)

## [ 1. DATA-BACKED RATIONALE & OBJECTIVE ]
- **Latar Belakang**: Seiring ekspansi repositori secara berkelanjutan, AI coding agent sering rentan mengalami halusinasi metrik (*metric drift* seperti mengutip jumlah tools/artikel lama) atau mengasumsikan nama file / link internal yang tidak eksis (*phantom URLs*).
- **Tujuan**: Membangun engine verifikasi *ground-truth* deterministik mandiri (`scripts/ground_truth.py`) dan mengintegrasikannya sebagai **Check 23** di `verify_batch.py` serta CLI sub-command di `manage_articles.py` dan `run_pipeline.py`.

---

## [ 2. HYPER-GRANULAR EXECUTION CHUNKS ]

### Chunk 1: Pembuatan Core Ground-Truth Engine (`scripts/ground_truth.py`)
* **Target File**: `scripts/ground_truth.py`
* **Scope**:
  1. Ekstrak data absolut langsung dari filesystem (OS metadata & parsing struktur):
     - `tools/*.html` count (53 tools, exclude `index.html`).
     - `blog/*.html` count (45 articles, exclude `index.html`).
     - `blueprints/index.html` card count (12 blueprints).
     - `sitemap.xml` URL count (107 URLs).
     - `feed.xml` / `atom.xml` / `feed.json` count (45 items).
     - `tools/tools-manifest.json` count (53 tools).
     - `sw.js` active `CACHE_VERSION`.
  2. Implementasikan flag CLI:
     - `--summary`: Output ringkas berdensitas tinggi (< 40 baris / < 200 token) untuk *prompt context grounding* AI.
     - `--json`: Output mesin JSON terstruktur untuk otomasi tool calling.
     - `--check`: Linter penegakan konsistensi metrik pada `index.html`, `README.md`, `about/index.html`, `tools/index.html`, `blueprints/index.html`, `llms.txt`, dan footer global.
     - `--find-tool <query>` & `--find-article <query>`: Pencocokan deterministik nama/slug resmi untuk eliminasi *hallucinated cross-links*.
  3. Pastikan kepatuhan Strict Zero-Emoji dan standarisasi ASCII / text tags (`[ VERIFIED ]`, `[ WARN ]`, `[ PASS ]`).

### Chunk 2: Integrasi Check 23 ke Programmatic QA Gate (`verify_batch.py`)
* **Target File**: `verify_batch.py`
* **Scope**:
  1. Tambahkan fungsi `check_metric_parity()` yang memanggil validasi `scripts/ground_truth.py` secara langsung.
  2. Pastikan kegagalan sinkronisasi metrik di halaman utama akan menggagalkan QA Gate sebelum commit/rilis.

### Chunk 3: Integrasi CLI ke `manage_articles.py` dan `run_pipeline.py`
* **Target Files**: `manage_articles.py`, `run_pipeline.py`
* **Scope**:
  1. Tambahkan command `manage_articles.py truth` atau `ground-truth` yang mencetak status ground truth deterministik.
  2. Perbarui `run_pipeline.py --doctor` agar memvalidasi metrik via `scripts/ground_truth.py`.

### Chunk 4: Verifikasi Kualitas Otomatis & Localhost Smoke Test
* **Scope**:
  1. Jalankan `python3 scripts/ground_truth.py --check` dan `python3 scripts/ground_truth.py --summary`.
  2. Jalankan `python3 verify_batch.py` (23 Checks QA Gate 100% PASS).
  3. Jalankan `python3 check_emojis.py`.
  4. Jalankan `python3 scripts/smoke_test.py`.
  5. Local git commit dan update Obsidian RAG checkpoint.

---

## [ 3. DEFINITION OF DONE (DoD) ]
- [ ] Berkas `scripts/ground_truth.py` terimplementasi penuh dengan dukungan flag `--summary`, `--json`, `--check`, `--find-tool`, `--find-article`.
- [ ] Check 23 (Site-Wide Metric Parity & Anti-Hallucination Audit) aktif dan lolos 100% di `verify_batch.py`.
- [ ] `manage_articles.py` dan `run_pipeline.py` terintegrasi dengan engine ground truth.
- [ ] 0 Error, 0 Violations, 0 Emojis di seluruh repositori.
