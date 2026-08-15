# BINDING DEVELOPMENT PROTOCOL — ZYEKH.COM
> Standard Operational Protocol (SOP) untuk AI Coding Assistant & Developer dalam mengubah kode di zyekh.com.

---

##  1. SERVICE WORKER & ASSET CACHING PROTOCOL (WAJIB)

Setiap kali melakukan perubahan pada kode JavaScript (`assets/js/*.js`) atau CSS (`assets/css/*.css`):

1. **Bump Service Worker Version**:
   - Wajib menaikkan versi `CACHE_VERSION` di `sw.js` (contoh: `v3` -> `v4`).
   - *Alasan*: Tanpa menaikkan `CACHE_VERSION`, Service Worker akan terus menyajikan file lama dari `CacheStorage` browser pengguna.

2. **Update Cache-Buster Query Parameters di Seluruh File HTML**:
   - Seluruh tag `<script src="/assets/js/site-nav.js?v=...">` dan `<link rel="stylesheet" href="/assets/css/shared.css?v=...">` di **seluruh 32 file HTML** wajib diperbarui query versi-nya (contoh: `?v=20260731_v4`).
   - Gunakan skrip Python untuk memperbarui secara otomatis ke 32 file HTML:
     ```python
     import glob, re
     for f in glob.glob('**/*.html', recursive=True):
         c = open(f).read()
         c = re.sub(r'site-nav\.js(\?v=[^\"]*)?', 'site-nav.js?v=VERSION', c)
         c = re.sub(r'shared\.css(\?v=[^\"]*)?', 'shared.css?v=VERSION', c)
         open(f, 'w').write(c)
     ```

---

##  2. CONTAINER WIDTH & LAYOUT STANDARDIZATION PROTOCOL

1. **Lebar Kontainer Seragam**:
   - Seluruh kontainer utama di semua halaman (`index.html`, `/tools/*`, `/blog/*`) WAJIB menggunakan `max-width: 1280px`.
2. **Dilarang Restriksi Inline Style di HTML**:
   - DILARANG keras memasukkan *inline style override* seperti `.main-container { max-width: 1100px; }` atau `.main-container { max-width: 1080px; }` di dalam tag `<style>` internal file HTML individual.
   - Semua aturan layout dasar WAJIB menginduk pada `assets/css/shared.css`.

---

## [ MODULE ] 3. NAVIGATION BAR & RESPONSIVE BREAKPOINT PROTOCOL

1. **Pencegahan Teks Patah (Multi-line Wrapping)**:
   - Aturan `.brand-logo` dan `.nav-link` WAJIB memiliki `white-space: nowrap;` dan `flex-shrink: 0;`.
2. **Fleksibilitas Tinggi Header**:
   - Header `.header-nav` DILARANG menggunakan `height` kaku (seperti `height: 60px`), melainkan wajib `min-height: 60px; padding: 0.65rem 0; box-sizing: border-box;`.
3. **Breakpoint Menu Seluler**:
   - Breakpoint Off-Canvas Drawer seluler diset seragam pada `@media (max-width: 960px)` baik di `assets/css/shared.css` maupun listener resize window di `assets/js/site-nav.js`.

---

##  4. GAPLESS SCROLLSPY & ACTIVE HIGHLIGHT PROTOCOL

1. **Viewport BoundingRect Position Calculation**:
   - ScrollSpy pada homepage (`index.html`) WAJIB menggunakan `sec.getBoundingClientRect()` untuk menghitung posisi riil elemen di layar secara *real-time*.
2. **Click Guard Timeout**:
   - Saat link navigasi diklik (`About`, `Skills`, `Projects`, `Contact`), flag `isClicking` WAJIB diset selama `1000ms` untuk mencegah handler scroll membatalkan status aktif secara tidak sengaja selama proses *smooth scrolling*.
3. **Bottom-of-Page Contact Trigger**:
   - Wajib menyertakan pengecekan terbawah halaman `(window.innerHeight + window.scrollY) >= (document.documentElement.scrollHeight - 60)` untuk mengaktifkan link `Contact`.

## [ FAST ] 5. STRICT NO-EMOJI & MINIMALIST CODE PROTOCOL (WAJIB)

1. **Dilarang Penggunaan Emoji di Kode & Dokumentasi**:
   - DILARANG keras menyisipkan karakter emoji (seperti ikon grafis, unicode pictographs, dll.) ke dalam berkas HTML, CSS, JavaScript, maupun file dokumentasi di repositori ini.
   - *Alasan*: Menjaga efisiensi token, kesederhanaan *Clean Minimalist FOSS Aesthetic*, dan performa *parsing*.
2. **Gunakan Ikon Teks / SVG / Typography Standard**:
   - Sebagai pengganti emoji, gunakan simbol teks ASCII/Unicode bersih (`•`, `->`, `[ VERIFIED ]`, `[ WARN ]`, `[ INFO ]`, `[ NOTE ]`) atau SVG vektor jika diperlukan.

---

## [ FAST ] 6. MODERN SYNTAX STANDARDS PROTOCOL (BASELINE 2024+)


1. **Centralized Service Worker Registration**:
   - Registrasi Service Worker WAJIB dikelola secara terpusat di dalam komponen `<site-nav>` (`assets/js/site-nav.js`).
   - DILARANG menyisipkan blok tag `<script>` registrasi Service Worker secara manual/terduplikasi di file HTML individual.

2. **Native CSS `:has()` Selector for UI States**:
   - Gunakan CSS `:has()` (seperti `body:has(#navMenu.open) { overflow: hidden; }`) di `assets/css/shared.css` untuk mengunci scroll body.
   - DILARANG memutasi `document.body.style.overflow` secara langsung di JavaScript.

3. **Native HTML5 `<dialog>` & Backdrop Styling**:
   - Modal wajib menggunakan elemen `<dialog>` dengan metode native `.showModal()` dan `.close()`.
   - Latar belakang modal wajib diatur menggunakan CSS `dialog::backdrop`. DILARANG menambah `display:none` inline atau event listener `keydown` (Escape key) manual.

4. **Web Crypto API Buffer Batching**:
   - Pengacakan berbasis kriptografi wajib mengalokasikan memori sekaligus via `crypto.getRandomValues(new Uint32Array(count))` dalam 1 kali panggilan per operasi.

---

##  5. PROGRAMMATIC ARTICLE BATCH PIPELINE PROTOCOL

Setiap kali membangkitkan batch artikel baru untuk `zyekh.com`, WAJIB mengikuti alur eksekusi terstandar berikut (referensi lengkap: `docs/batch_pipeline_sop.md`):

```bash
# 1. Isi materi artikel dalam format JSON terstruktur
# File: batch_data.json

# 2. Bangkitkan file HTML artikel 100% SOP-compliant
python3 generate_batch.py

# 3. Jalankan audit QA otomatis 21-axis (termasuk live localhost HTTP server smoke test)
python3 verify_batch.py

# 4. Sinkronisasi sitemap.xml, feed.xml, llms.txt, sw.js CACHE_VERSION & query version HTML
python3 sync_content.py

# 5. Pinger IndexNow API (HTTP 200 OK)
python3 ping_indexers.py
```

Seluruh artikel yang dihasilkan WAJIB mematuhi **10 Komponen Wajib SOP Gold Standard** (`TechArticle` Schema, OpenGraph Extended, Hero Image WebP/JPG, Exec Summary Box, ToC `nav.toc-card`, Heading IDs `h2[id]`, FAQ `<details>`, Author Bio Card, dan Cross-Links Tools Internal).

---

## [ VERIFIED ] 7. EMPIRICAL VERIFICATION PROTOCOL (SEBELUM MENYATAKAN SELESAI)

Sebelum mengklaim tugas selesai atau mengirimkan laporan ke pengguna, AI WAJIB menjalankan skrip audit di terminal:

```bash
python3 verify_batch.py
python3 check_emojis.py
```
