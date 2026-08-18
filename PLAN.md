# PLAN: Implementasi Inline Header Search Bar di zyekh.com (Pengganti Popup Modal)

## [ 1. DATA-BACKED RATIONALE & OBJECTIVE ]
- **Akar Masalah**: Penggunaan `<dialog class="cmd-palette">` memicu popup modal besar dengan backdrop gelap yang menutupi konten halaman, membingungkan alur navigasi, dan tidak responsif terhadap interaksi toggle `Ctrl+K`.
- **Solusi Terpilih (Opsi 3)**: Menghapus popup modal `<dialog>` sepenuhnya dan mengintegrasikan **Inline Search Bar** langsung di dalam navbar `<site-nav>` dengan dropdown hasil pencarian mengambang (*floating dropdown*).
- **Perilaku Shortcut `Ctrl+K`**: Menekan `Ctrl+K` atau `Cmd+K` akan langsung mengarahkan fokus kursor (`.focus()`) ke kolom pencarian di navbar secara instan. Menekan `Ctrl+K` atau `Escape` saat fokus akan menutup dropdown dan melepaskan fokus (`.blur()`).

---

## [ 2. HYPER-GRANULAR EXECUTION CHUNKS ]

### Chunk 1: Refactoring Navbar Web Component & Search Engine (`assets/js/site-nav.js`)
* **Target File**: `assets/js/site-nav.js`
* **Scope**:
  1. Tambahkan container `.nav-search` dengan `<input type="search" id="navSearchInput" class="nav-search-input" placeholder="Search... (Ctrl+K)">` dan `<div id="navSearchResults" class="nav-search-results"></div>` ke dalam template navbar di `SiteNav.connectedCallback()`.
  2. Hapus seluruh logika pembuatan dan pemanggilan `<dialog id="cmdPalette">` (`showModal()`, `dialog.getBoundingClientRect()`, backdrop).
  3. Hubungkan shortcut `Ctrl+K` / `Cmd+K` agar langsung memanggil `focus()` pada `#navSearchInput`. Jika sudah fokus dan terbuka, lakukan `blur()` dan sembunyikan dropdown.
  4. Implementasikan **Tokenized Multi-Word Matcher** (`tokens.every(...)`) dan sanitasi `escapeHTML()`.
  5. Tambahkan navigasi keyboard (`ArrowDown`, `ArrowUp`, `Enter`, `Escape`) pada dropdown hasil pencarian.
  6. Tutup dropdown otomatis saat klik di luar area `.nav-search` atau saat link diklik.

### Chunk 2: Pembaruan CSS Cascade Layers & Dropdown Styling (`assets/css/shared.css`)
* **Target File**: `assets/css/shared.css`
* **Scope**:
  1. Hapus aturan CSS modal dialog usang (`dialog.cmd-palette`, `dialog.cmd-palette::backdrop`).
  2. Tambahkan class styling pada `@layer components`:
     - `.nav-search`: Container flex dengan `position: relative;`.
     - `.nav-search-input`: Input ramping dengan border `var(--border-color)`, background `var(--bg-dark)`, font monospaced badge shortcut `Ctrl+K`.
     - `.nav-search-results`: Floating dropdown box (`position: absolute; top: calc(100% + 6px); left: 0; min-width: 320px; max-width: 450px; max-height: 60vh; overflow-y: auto; background: var(--bg-card); border: 1px solid var(--border-color); border-radius: var(--radius-md); box-shadow: 0 8px 30px rgba(0,0,0,0.4); z-index: 1000;`).
     - `.nav-search-item`, `.nav-search-type`, `.nav-search-title`, `.nav-search-desc`: Styling item hasil pencarian yang terintegrasi dengan tema Dark & Light.
  3. Responsivitas Mobile (`@media (max-width: 960px)`): Kolom pencarian menyesuaikan lebar di dalam menu mobile yang dapat diakses dengan mudah.

### Chunk 3: Perluasan Indeksasi Data Termasuk Blueprints & Halaman Inti (`sync_content.py`)
* **Target File**: `sync_content.py`
* **Scope**:
  1. Perbarui fungsi pembuatan `search-index.json` agar memindai:
     - `tools/*.html` (`type: "Tool"`)
     - `blog/*.html` (`type: "Article"`)
     - `blueprints/*.html` (`type: "Blueprint"`)
     - Halaman inti: `/about/` (`type: "Page"`), `/contact/` (`type: "Page"`), `/links/` (`type: "Hub"`), `/blueprints/` (`type: "Hub"`).
  2. Jalankan `sync_content.py` untuk menghasilkan `search-index.json` lengkap dan minifikasi `site-nav.min.js` & `shared.min.css`.

### Chunk 4: Verifikasi Kualitas Otomatis & Localhost Smoke Test
* **Scope**:
  1. Jalankan `python3 verify_batch.py` untuk memvalidasi 22-axis QA gate (100% lolos).
  2. Jalankan `python3 scripts/smoke_test.py` untuk menguji live HTTP server dan endpoint `/search-index.json`.
  3. Verifikasi ketiadaan error visual atau konsol pada localhost.

---

## [ 3. DEFINITION OF DONE (DoD) ]
- [ ] Tidak ada lagi elemen `<dialog id="cmdPalette">` atau popup modal yang muncul di layar.
- [ ] Kolom pencarian inline terintegrasi rapi di header navbar.
- [ ] Menekan `Ctrl+K` atau `Cmd+K` memfokuskan input pencarian di navbar secara instan.
- [ ] Dropdown mengambang (*floating dropdown*) muncul di bawah input saat pengguna mengetik query.
- [ ] Navigasi panah atas/bawah dan Enter bekerja mulus.
- [ ] Blueprints dan seluruh halaman terindeks 100% di `search-index.json`.
- [ ] Lolos 100% Programmatic QA Audit (`verify_batch.py` Checks 1-22).
