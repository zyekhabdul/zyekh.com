# PLAN: Implementasi Komprehensif UI/UX Enhancement Suite (Paket 1 + 2 + 3)

## [ 1. DATA-BACKED RATIONALE & OBJECTIVE ]
- **Latar Belakang**: Berdasarkan audit UI/UX pada 109 dokumen HTML dan komponen stylesheet/skrip, terdapat beberapa titik friksi interaksi pengguna: pencarian dropdown tanpa reset instan/mark token highlight, TOC artikel blog tanpa scroll-spy aktif, ketiadaan image lightbox pada diagram teknis, dan keterbatasan produktivitas keyboard (`Ctrl+Enter` & auto-growing textarea) pada tools.
- **Tujuan**: Menerapkan optimasi menyeluruh Paket 1, 2, dan 3 dengan arsitektur zero-dependency, vanilla modern JavaScript (IntersectionObserver, native `<dialog>`), strict zero-emoji, dan validasi penuh pada 23-axis QA Gate.

---

## [ 2. HYPER-GRANULAR EXECUTION CHUNKS ]

### Chunk 1: Paket 1 — Core Navigation, Search & Global Interaction Polish
* **Target Files**: `assets/css/shared.css`, `assets/js/site-nav.js`
* **Scope**:
  1. **Instant Search Clear Button & Token Highlighting**:
     - Tambahkan tombol clear `[ × ]` di `#navSearch` yang muncul saat input terisi, serta dukungan tombol `Escape` untuk reset instan.
     - Bungkus token pencarian yang cocok di dropdown dengan `<mark class="search-match">`.
  2. **Theme Switch Transition Smoothing**:
     - Pasang class `.theme-transitioning` ke `<html>` selama 300ms saat toggle tema aktif untuk transisi warna CSS variables yang mulus tanpa kedip (*flicker-free*).
  3. **Focus-Visible & Micro-Feedback**:
     - Pertajam kontras outline `:focus-visible` dan animasikan tombol copy saat status `copied` aktif.

### Chunk 2: Paket 2 — Blog Deep-Dive Reading Experience (TOC Scroll-Spy & Diagram Lightbox)
* **Target Files**: `assets/css/shared.css`, `assets/js/site-nav.js`
* **Scope**:
  1. **Desktop TOC Scroll-Spy via IntersectionObserver**:
     - Pantau elemen `h2[id], h3[id]` di dalam `.article-body` dan sematkan kelas `.active-toc-item` ke link TOC yang sedang aktif dibaca.
  2. **Native `<dialog>` Architecture Diagram Lightbox**:
     - Inject `<dialog id="imgLightbox" class="img-lightbox">` native tanpa dependensi pihak ketiga.
     - Gambar di artikel blog dapat diklik untuk memperbesar diagram arsitektur ke resolusi penuh.

### Chunk 3: Paket 3 — Utility Tools Productivity (Keyboard Shortcuts & Auto-Resize)
* **Target Files**: `assets/css/shared.css`, `assets/js/site-nav.js`
* **Scope**:
  1. **Global `Ctrl+Enter` / `Cmd+Enter` Execution Trigger**:
     - Listen `keydown` pada form dan container `.tool-box` untuk memicu tombol aksi utama tool (`.btn-primary` atau tombol kalkulasi/format/generate).
  2. **Auto-Growing Textarea Elasticity**:
     - Auto-resize otomatis pada textarea utility tools sesuai panjang konten input dengan batas maksimal (`max-height: 480px`).

### Chunk 4: Pipeline Synchronization, 23-Axis QA Gate & Obsidian Memory
* **Target Files**: `sw.js`, seluruh berkas HTML, `verify_batch.py`, Obsidian RAG
* **Scope**:
  1. Eksekusi `python3 sync_content.py` (auto-bump `CACHE_VERSION` & query parameter `?v=...` di 109 file HTML).
  2. Jalankan `python3 scripts/ground_truth.py --check` (Check 23 metric parity).
  3. Jalankan `python3 verify_batch.py` (Checks 1-23 100% PASS).
  4. Jalankan `python3 check_emojis.py` (Strict Zero-Emoji).
  5. Jalankan `python3 scripts/smoke_test.py` (Live HTTP test).
  6. Git commit lokal dan perbarui ADR-046 di Obsidian RAG memory.

---

## [ 3. DEFINITION OF DONE (DoD) ]
- [x] Paket 1, 2, dan 3 aktif dan teruji fungsional di seluruh halaman.
- [x] 23-Axis QA Gate lolos 100% PASS (Checks 1-23).
- [x] 0 Emojis di seluruh codebase.
- [x] Localhost live smoke test 32/32 routes lolos tanpa regresi.
- [x] Pipeline disinkronkan dan CACHE_VERSION di-bump.
