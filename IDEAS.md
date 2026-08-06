# [ IDEAS ] Zyekh.com Enhancement Proposals

Berdasarkan arsitektur Zyekh.com (Zero-Dependency, Local-First, AI-Optimized, Minimalist), berikut adalah ide strategis yang diusulkan:

## 1. Ekspansi Tool Lokal (Zero-Dependency)
- [ ADD ] **Offline Markdown Editor**: Editor markdown lokal dengan live preview dan export HTML. Sangat relevan dengan orientasi situs pada konten LLM (`llms.txt`).
- [ ADD ] **RegEx Pattern Tester**: Tool pengujian Regular Expression yang berjalan murni di memori browser tanpa server backend.
- [ ADD ] **Client-side Image Converter**: Konversi format gambar (misal: JPG/PNG ke WebP) memanfaatkan Vanilla JS Canvas API (100% offline).

## 2. Optimasi CI/CD & SEO Pipeline
- [ OPTIMIZE ] **Python-based Asset Minifier**: Skrip Python *standalone* di GitHub Actions untuk minifikasi file CSS/JS. Mempertahankan filosofi *zero-dependency* (tanpa NPM/Node.js).
- [ OPTIMIZE ] **Dynamic Resource Preloading**: Pembaruan pada `generate_batch.py` untuk menyuntikkan `<link rel="preload">` pada aset render-blocking demi mengunci skor Lighthouse 100/100.
- [ SECURITY ] **Automated Subresource Integrity (SRI)**: Penambahan generator hash SHA-384 secara otomatis pada pipeline untuk seluruh aset.

## 3. Peningkatan Aksesibilitas & UX
- [ UX ] **Command Palette / Quick Search (Ctrl+K)**: Sistem pencarian *fuzzy* berbasis Vanilla JS untuk menemukan 42+ tools secara instan.
- [ UX ] **Local Bookmarking (Pinned Tools)**: Fitur "Favorite Tools" yang menyimpan konfigurasi preferensi pengguna di `localStorage`.
- [ UX ] **Native Dark/Light Theme Toggle**: Sistem *theming* murni CSS Custom Properties (`:root`) yang merespons `prefers-color-scheme` dan tersimpan persisten di klien.

Seluruh ide di atas sepenuhnya mematuhi protokol ketiadaan dependensi eksternal, performa tinggi, dan bebas elemen *bloat* (termasuk emoji).
