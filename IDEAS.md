# [ IDEAS ] Zyekh.com Enhancement Proposals

Berdasarkan arsitektur Zyekh.com (Zero-Dependency, Local-First, AI-Optimized, Minimalist), berikut adalah peta jalan dan ide strategis:

## 1. Ekspansi Tool Lokal (Zero-Dependency)
- [ DONE ] **Offline Markdown Editor**: Editor markdown lokal dengan live preview dan export HTML (`/tools/markdown.html`).
- [ DONE ] **RegEx Pattern Tester**: Tool pengujian Regular Expression murni di memori browser (`/tools/regex.html`).
- [ DONE ] **Client-side Image Converter**: Konversi format gambar Canvas API (100% offline) (`/tools/image-converter.html`).
- [ DONE ] **Speculative Decoding Interactive Simulator**: Simulator grafis pohon verifikasi token draft vs target model (`/tools/speculative-decoding.html`).
- [ DONE ] **eBPF XDP Packet Filter Evaluator**: Evaluator aturan kernel packet filtering layer NIC (`/tools/ebpf-evaluator.html`).
- [ DONE ] **LLM Token & GPU Inference Cost Calculator 2026**: Kalkulator perbandingan biaya token ($/1M tokens) dan kebutuhan VRAM (Claude 3.7, GPT-4.5, Gemini 2.0 Flash, DeepSeek-R1, Llama 3.3) murni *client-side* (`/tools/llm-calculator.html`).
- [ BACKLOG ] **WebGPU Shader & Inference Latency Profiler**: Profiler akselerasi perangkat keras lokal berbasis WebGPU API.

## 2. Optimasi CI/CD, SEO & Distribusi Otomatis
- [ DONE ] **Python-based Asset Minifier**: Skrip mandiri di `sync_content.py` untuk minifikasi CSS/JS tanpa Node.js.
- [ DONE ] **Automated Subresource Integrity (SRI)**: Generator hash SHA-384 otomatis pada seluruh aset statis.
- [ DONE ] **Automated Cloudflare CDN Cache Purge**: Pemicu Purge Cache Cloudflare otomatis via API.
- [ DONE ] **Decoupled 3-Stage Manifest-Driven Social Card Generator**: Generator gambar Ultra-HD 2400px (Light Square untuk Bluesky + Dark Landscape untuk OpenGraph/Mastodon) berbasis `data/social_cards_manifest.json` (ADR-014).
- [ DONE ] **Automated Data Desynchronization Guard (Check 16 in `verify_batch.py`)**: Validasi otomatis keutuhan kartu media sosial, manifest JSON, dan limit ukuran file < 950KB sebelum rilis artikel.
- [ DONE ] **Dual-Pass File Size Quantization Guard**: Kompresi palet otomatis ke 256 warna (`MEDIANCUT`) di `generate_social_cards.py` jika ukuran file > 800KB untuk memastikan selalu lolos limit API Bluesky (1.0MB) dan Mastodon.
- [ DONE ] **Safe Unicode Glyph Sanitization (`extract_card_manifest.py`)**: Normalisasi otomatis karakter smart quotes (`”`, `“`), em-dash (`—`), dan panah (`→`) ke format teks teknis bersih untuk mencegah glik/tofu `[?]`.
- [ DONE ] **Bundled Local TTF Font Distribution (`assets/fonts/ttf/`)**: Pustaka font mandiri (`JetBrainsMono`, `DejaVuSans`) di repositori untuk menjamin rendering konsisten di semua OS dan CI/CD runner.
- [ DONE ] **Automated Multi-Channel Broadcast Pipeline**: Orkestrasi otomatis `ping_indexers.py` (IndexNow Bing/Yandex) dan `scripts/syndicate.py` (Bluesky & Mastodon) pasca-rilis artikel.
- [ BACKLOG ] **Content Hash Cache-Busting on OpenGraph Tags**: Otomatis menyematkan hash query string `?v=<hash>` pada `og:image` di seluruh HTML agar crawler media sosial (Facebook, LinkedIn, Discord, Telegram) tidak menampilkan thumbnail kadaluarsa.
- [ BACKLOG ] **Dynamic Canvas Vertical Budgeting**: Kalkulator layout dinamis fleksibel di Pillow compiler untuk auto-adjust padding ketika judul/konten artikel sangat panjang.


## 3. Peningkatan Aksesibilitas & UX
- [ DONE ] **Command Palette / Quick Search (Ctrl+K)**: Pencarian cepat berbasis Vanilla JS untuk 46+ tools.
- [ DONE ] **Local Bookmarking (Pinned Tools)**: Fitur favorit dengan penyimpanan lokal `localStorage` dan ikon SVG vektor.
- [ DONE ] **Native Dark/Light Theme Toggle**: Theming CSS Custom Properties merespons `prefers-color-scheme`.
- [ DONE ] **Self-Hosted Link Hub (`/links/`)**: Pengganti Linktree murni Vanilla HTML5/CSS dengan microformats `rel="me"`.

## 4. Ekspansi Konten GEO & Technical Deep-Dives (Batch 4)
- [ BACKLOG ] **FlashAttention-3 Deep Dive**: Asynchronous FP8 Tensor Cores & Warp-Specialization in Hopper Architecture.
- [ BACKLOG ] **Linux LSM BPF Security Policies**: Runtime kernel security hooks without kernel module recompilation.
- [ BACKLOG ] **Wasm Component Model Polyglot Sandboxing**: Secure sandboxing on Cloudflare Edge Workers.
- [ BACKLOG ] **FP8 vs INT4 KV-Cache Quantization**: Memory bandwidth vs perplexity trade-offs in high-throughput inference.

## 5. Proposal Tambahan & Inovasi Fitur (Backlog Aktif)
- [ BACKLOG ] **Linux Security `sysctl` & `sshd` Hardening Config Builder**: Generator konfigurasi interaktif `/etc/sysctl.d/99-hardening.conf` dan `/etc/ssh/sshd_config.d/99-hardened.conf` berbasis use-case (`/tools/linux-hardening-generator.html`).
- [ BACKLOG ] **GitHub Actions Automated CI QA Gate**: Workflow CI otomatis di GitHub Actions untuk memvalidasi `verify_batch.py` (16-axis) dan `check_emojis.py` pada setiap Pull Request/Commit (`.github/workflows/ci-qa-gate.yml`).
- [ BACKLOG ] **JSON Feed v1.1 & RFC 4287 Atom Feed Modernization**: Penambahan output sindikasi modern `feed.json` dan `atom.xml` di `sync_content.py`.
- [ BACKLOG ] **Interactive Zero-Trust Architecture Topology Builder**: Utilitas visual Canvas/SVG murni di browser untuk merancang dan mengekspor topologi keamanan ke Mermaid Markdown, SVG, dan ASCII (`/blueprints/topology-builder.html`).

Seluruh ide di atas mematuhi prinsip ketiadaan dependensi eksternal, performa tinggi, dan bebas elemen bloat/emoji.

