# WORKSPACE RULES & SYSTEM ARCHITECTURE — ZYEKH.COM

## 1. PROJECT IDENTITY & CORE ARCHITECTURE
- Type: High-Performance Static Engineering Portfolio, Deep Tech Articles, Web Tools & Systems Architecture Blueprints.
- Primary Theme: Code Efficiency & Extreme Minimalism (Zero Over-engineering, YAGNI).
- Primary Goal: Instant indexing and maximum authority on Search Engines and AI Search Engines (Perplexity, ChatGPT, Claude) via 100/100 Lighthouse performance, WCAG accessibility, Schema.org JSON-LD (`TechArticle`), and RAG entrypoints (`llms.txt`, `llms-full.txt`).
- Tech Stack: Vanilla HTML5, Modern CSS (Baseline 2024+, CSS Custom Properties, `:has()`), Vanilla ES6+ JavaScript, Native Web Components (`<site-nav>`), Service Worker (`sw.js`), GitHub Pages + Cloudflare CDN.
- Production Domain: https://zyekh.com
- Cloudflare Zone ID: 1427afa77c5824ee0c34b514260e2e5d

---

## 2. STRICT GLOBAL BINDING PRINCIPLES (NON-NEGOTIABLE)

1. STRICT NO EMOJI:
   - DILARANG keras menyisipkan karakter emoji pada berkas HTML, CSS, JS, JSON, maupun Markdown.
   - Gunakan penanda teks terstruktur: `[ VERIFIED ]`, `[ NOTE ]`, `[ WARN ]`, `[ INFO ]`, `•`, `->`.

2. ANTI-AI HALLUCINATION & EMPIRICAL DIAGNOSIS:
   - Selalu verifikasi data, path file, certificate, dan nama repository langsung dari filesystem sebelum mengubah kode.
   - Diagnosa di Localhost terlebih dahulu: `python3 -m http.server 8080`. Localhost adalah ground truth (tanpa Service Worker / CDN / browser cache).
   - Keluhan pengguna adalah sinyal gejala, bukan fakta kode. Jika localhost benar, masalah ada pada cache browser klien.

3. CACHE VERSION BUMPING PROTOCOL:
   - Setiap kali memodifikasi file CSS (`assets/css/*.css`) atau JS (`assets/js/*.js`), AI WAJIB:
     a. Menaikkan `CACHE_VERSION` di `sw.js` (misal `v36` -> `v37`).
     b. Memperbarui query parameter `?v=...` pada tag `<link>` dan `<script>` di seluruh file HTML.
   - Script `sync_content.py` menyediakan otomasi `bump_cache_version()`.

4. CLOUDFLARE CACHE PURGE:
   - Setelah setiap push ke remote, purge cache Cloudflare via API pada Zone `1427afa77c5824ee0c34b514260e2e5d`.

5. ONE CHANGE PER COMMIT & ATOMIC WRITES:
   - Jangan membundel perubahan HTML + CSS + SW + JS dalam satu commit saat proses perbaikan/debugging.
   - Batch modifikasi script harus menulis ke temporary file `.tmp` terlebih dahulu dan menggunakan `os.replace` untuk atomic disk write.

6. PROACTIVE & AUTONOMOUS INITIATIVE:
   - AI dilarang pasif menanyakan "mau lanjut?" atau "apa langkah selanjutnya?".
   - Jika menemukan cacat struktural, UI/UX, atau performa, perbaiki langsung secara komprehensif.

7. PRE-PROPOSAL DISCOVERY & ANTI-REDUNDANCY:
   - Sebelum membuat script, tool, atau GitHub Action baru, AI WAJIB memeriksa direktori target (`.github/workflows/`, `scripts/`, `tools/`, `blueprints/`). DILARANG membuat script duplikat jika fungsi serupa sudah ada.

---

## 3. UI/UX DESIGN SYSTEM & LAYOUT LAWS

1. Layout Container Uniformity:
   - Seluruh kontainer utama halaman menggunakan `max-width: 1280px`.
   - DILARANG menyisipkan inline override `max-width: 1100px` atau sejenisnya di file HTML individual.

2. Macro Layout Separation:
   - Grid / Hub Pages (`/`, `/tools/`, `/blog/` index): Wajib dibungkus `<main class="main-container">` dan `<header class="page-header">`.
   - Reading / Prose Pages (Artikel, Blueprint): Wajib dibungkus `<div class="container-blog">` -> `<article class="article-wrapper">` -> `<div class="article-body">`.

3. Navigation Component:
   - DILARANG membuat tag `<nav>` manual. Selalu gunakan custom element: `<site-nav active="page_name"></site-nav>`. Breakpoint mobile drawer terstandarisasi pada `max-width: 960px`.

4. Clickable Card Architecture:
   - Seluruh item dalam grid/list wajib dibungkus tag `<a>` full clickable (bukan hanya judulnya).
   - Standard A (With Image): Digunakan pada `/blog/` (`div.article-item` -> `article.article-card` -> `a`).
   - Standard B (Without Image): Digunakan pada `/tools/` (`div.tool-item` -> `a.tool-card`).

5. CSS Vertical Centering:
   - Gunakan `top:0; bottom:0; display:flex; align-items:center` untuk absolute overlay.
   - DILARANG menggunakan `top:50%; transform:translateY(-50%)` (menimbulkan subpixel misalignment).

6. Grid Blowout Prevention:
   - Setiap grid child yang mengandung blok `<pre>` atau `<code>` WAJIB menyertakan `min-width: 0;` (contoh: `.tool-item { display: flex; flex-direction: column; min-width: 0; }`).

7. Code Block & Copy Button Standard:
   - Tombol Copy harus disuntikkan sebagai sibling terhadap `<pre>`, bukan child.
   - Tag `<pre>` di dalam card harus menyertakan `padding-right: 3.5rem` dan `white-space: pre-wrap;` untuk mencegah overlap dengan tombol Copy.

8. Anti-FOUC Theme Initialization:
   - Script sinkron pendek di `<head>` wajib dijalankan sebelum render body untuk membaca `localStorage.getItem('theme')`.

9. Color & Typography Design Tokens:
   - Body Background: `var(--bg-main)`
   - Card/Surface Background: `var(--bg-card)`
   - Primary Text: `var(--text-main)` (`#f4f4f5`)
   - Muted/Meta Text: `var(--text-muted)` (`#a1a1aa`)
   - Border Idle: `var(--border-color)` | Border Hover: `var(--border-hover)`
   - Transition: `var(--transition)` (`0.2s cubic-bezier(0.16, 1, 0.3, 1)`)

---

## 4. CONTENT PIPELINE & SYNDICATION PROTOCOLS

1. Programmatic Article Batch Pipeline:
   - Alur pembuatan konten baru:
     Step 1: Isi data artikel pada `batch_data.json`
     Step 2: Jalankan `python3 generate_batch.py`
     Step 3: Verifikasi via QA gate `python3 verify_batch.py`
     Step 4: Sinkronisasi sitemap, feeds, dan llms via `python3 sync_content.py`
     Step 5: Ping mesin pencari via `python3 ping_indexers.py`

2. 10 Gold Standard Article Components:
   - Setiap artikel wajib memiliki: (1) JSON-LD `TechArticle` Schema, (2) OpenGraph Extended Tags, (3) Hero Image WebP/JPG, (4) Executive Summary Box (`.exec-summary`), (5) Sticky ToC (`nav.toc-card`), (6) Structured Heading IDs (`h2[id]`), (7) Interactive FAQ `<details>`, (8) Author Bio Card, (9) Internal Cross-Links ke Tools, (10) Autodiscovery Feeds link.

3. Tri-Feed Syndication:
   - Semua artikel wajib otomatis dipublikasikan ke RSS 2.0 (`feed.xml`), Atom 1.0 (`atom.xml`), dan JSON Feed 1.1 (`feed.json`).

4. Social Card Compilation Architecture:
   - 3-Stage Compilation: `extract_card_manifest.py` -> `validate_card_manifest.py` -> `generate_social_cards.py`.
   - Card 1:1 Square (2400x2400): Layout 4-tier (Header + 740px Terminal Code + 2-Box Invariants/Metrics + Spec Footer Bar).
   - Image Uniqueness: Semua hero image wajib memiliki MD5 hash 100% unik (Check 15 pada `verify_batch.py`).
   - Font Binding: Wajib mengarah langsung ke static TrueType binaries (`Outfit-Bold.ttf`, `Inter-Regular.ttf`, `JetBrainsMono-Regular.ttf`).

5. Social Syndication Drip Protocol:
   - Dilarang membanjiri linimasa feed eksternal. Cron harian menjalankan syndication dengan `--limit 1` (FIFO queue dari `data/syndication_history.json`).
   - Bluesky/ATProto batas 280 byte status text. Mastodon batas 500 karakter.

---

## 5. PROHIBITED AI ANTI-PATTERNS
- AP-01: Merusak atau menimpa manual metadata pada `llms-full.txt` atau `README.md` secara buta.
- AP-02: Memodifikasi CSS/JS tanpa menaikkan cache string di Service Worker dan HTML.
- AP-03: Double Debouncing (membungkus `setTimeout` di dalam `requestAnimationFrame`).
- AP-04: Credential Spraying / Regex harvesting token dari file konfigurasi.
- AP-05: Hardcoding credential/password dalam script otomatisasi atau file `/tmp`.
- AP-06: Mengabaikan context saat grep (mengambil kesimpulan dari satu baris tanpa melihat 10 baris sekitarnya).

---

## 6. ESSENTIAL VERIFICATION COMMANDS
```bash
# Test localhost live server
python3 -m http.server 8080

# Audit QA 21-Axis & Live HTTP Smoke Test
python3 verify_batch.py

# Audit Emoji Leakage
python3 check_emojis.py

# Live Localhost HTTP Smoke Test
python3 scripts/smoke_test.py

# Sinkronisasi Global Feed & Metadata
python3 sync_content.py
```
