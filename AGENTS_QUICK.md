# AGENTS_QUICK.md — BACA INI SEBELUM MULAI (ATURAN KRITIKAL)

File ini adalah versi ringkas dari AGENTS.md. Hanya berisi aturan yang jika
dilanggar akan menyebabkan blast radius besar (kerusakan sitewide).

---

## 1. DIAGNOSIS — Localhost Dulu, Bukan Screenshot
```
python3 -m http.server 8080
```
Buka localhost:8080/halaman-masalah. Jika localhost benar -> masalah adalah
browser/CDN cache. Jangan edit kode berdasarkan screenshot saja.

## 2. SEBELUM PROPOSE SOLUSI — Cek Standar yang Ada
```bash
grep -n "keyword" assets/css/shared.css
grep -n "keyword" DESIGN_SYSTEM.md
```
Jika standar belum ada: BERITAHU USER terlebih dahulu. Jangan langsung
implement solusi baru tanpa approval.

## 3. SURVEY BUILD PIPELINE DULU — Jangan Buat Tooling Baru
```bash
find . -name "*.py" -o -name "*.sh" -o -name "Makefile" | grep -v .git
```
Build pipeline resmi ada di `sync_content.py`. Jalankan SELALU setelah
modifikasi CSS/JS.

## 4. SETELAH EDIT CSS/JS — WAJIB Jalankan Pipeline Resmi
```bash
python3 -c "from sync_content import sync_all; sync_all(bump_version=True)"
```
JANGAN menulis minifier ad-hoc. Pipeline ini menangani:
- Minifikasi CSS/JS
- Generasi SRI hash (sha384)
- Update ?v= query string di 76+ HTML files
- Bump CACHE_VERSION di sw.js

Melanggar aturan ini = SRI mismatch = CSS diblokir browser = seluruh situs
kehilangan styling.

## 5. SATU PERUBAHAN PER COMMIT
Jangan bundle HTML + CSS + JS + SW dalam satu commit saat debugging. Isolasi
setiap variabel.

## 6. JIKA STANDAR BELUM ADA
Protokol wajib:
1. Nyatakan: "Standar untuk X belum ada di design system."
2. Tanya: tambah ke shared.css (global) atau lokal saja?
3. Baru eksekusi setelah user approve.

---

Untuk aturan lengkap: baca AGENTS.md dan DESIGN_SYSTEM.md.
