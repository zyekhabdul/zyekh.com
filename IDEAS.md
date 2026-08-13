# [ IDEAS ] Zyekh.com Enhancement Proposals

Berdasarkan arsitektur Zyekh.com (Zero-Dependency, Local-First, AI-Optimized, Minimalist), berikut adalah ide strategis yang diusulkan:

## 1. Ekspansi Tool Lokal (Zero-Dependency)
- [ DONE ] **Offline Markdown Editor**: Editor markdown lokal dengan live preview dan export HTML. Sangat relevan dengan orientasi situs pada konten LLM (`llms.txt`).
- [ DONE ] **RegEx Pattern Tester**: Tool pengujian Regular Expression yang berjalan murni di memori browser tanpa server backend.
- [ DONE ] **Client-side Image Converter**: Konversi format gambar (misal: JPG/PNG ke WebP) memanfaatkan Vanilla JS Canvas API (100% offline).

## 2. Optimasi CI/CD & SEO Pipeline
- [ DONE ] **Python-based Asset Minifier**: Skrip Python *standalone* di `sync_content.py` untuk minifikasi file CSS/JS. Mempertahankan filosofi *zero-dependency* (tanpa NPM/Node.js).
- [ DONE ] **Automated Subresource Integrity (SRI)**: Penambahan generator hash SHA-384 secara otomatis pada pipeline untuk seluruh aset.
- [ DONE ] **Automated Cloudflare CDN Cache Purge**: Generator otomatis pemicu Purge Cache Cloudflare pasca-push (`sync_content.py --purge-cf`).

## 3. Peningkatan Aksesibilitas & UX
- [ DONE ] **Command Palette / Quick Search (Ctrl+K)**: Sistem pencarian *fuzzy* berbasis Vanilla JS untuk menemukan 42+ tools secara instan.
- [ DONE ] **Local Bookmarking (Pinned Tools)**: Fitur "Favorite Tools" yang menyimpan konfigurasi preferensi pengguna di `localStorage`.
- [ DONE ] **Native Dark/Light Theme Toggle**: Sistem *theming* murni CSS Custom Properties (`:root`) yang merespons `prefers-color-scheme` dan tersimpan persisten di klien.

## 4. Rencana Ekspansi Batch 4 & Simulasi Interaktif
- [ PROPOSED ] **Batch 4 Technical Deep Dives**: 5-10 artikel teknis baru mendalam tentang *Speculative Decoding*, *eBPF LSM Hooks*, *FlashAttention-3*, dan *WASM Edge Sandboxing*.
- [ PROPOSED ] **Speculative Decoding Interactive Simulator**: Widget visualisasi pohon token verifikasi draft model vs target model murni Vanilla JS/CSS.
- [ PROPOSED ] **eBPF XDP Packet Filter Evaluator**: Widget simulator aturan penyaringan paket jaringan eBPF di tingkat kernel NIC.
- [ PROPOSED ] **PWA Offline Audit & Lighthouse 100/100 Locking**: Pengujian menyeluruh fallback Service Worker dan penguncian skor Core Web Vitals.

Seluruh ide di atas sepenuhnya mematuhi protokol ketiadaan dependensi eksternal, performa tinggi, dan bebas elemen *bloat* (termasuk emoji).
