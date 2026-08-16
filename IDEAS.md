# [ IDEAS ] Zyekh.com Enhancement Proposals

Berdasarkan arsitektur Zyekh.com (Zero-Dependency, Local-First, AI-Optimized, Minimalist), berikut adalah peta jalan dan ide strategis:

## 1. Ekspansi Tool Lokal (Zero-Dependency)
- [ DONE ] **Offline Markdown Editor**: Editor markdown lokal dengan live preview dan export HTML (`/tools/markdown.html`).
- [ DONE ] **RegEx Pattern Tester**: Tool pengujian Regular Expression murni di memori browser (`/tools/regex.html`).
- [ DONE ] **Client-side Image Converter**: Konversi format gambar Canvas API (100% offline) (`/tools/image-converter.html`).
- [ DONE ] **Speculative Decoding Interactive Simulator**: Simulator grafis pohon verifikasi token draft vs target model (`/tools/speculative-decoding.html`).
- [ DONE ] **eBPF XDP Packet Filter Evaluator**: Evaluator aturan kernel packet filtering layer NIC (`/tools/ebpf-evaluator.html`).
- [ DONE ] **LLM Token & GPU Inference Cost Calculator 2026**: Kalkulator perbandingan biaya token ($/1M tokens) dan kebutuhan VRAM (Claude 3.7, GPT-4.5, Gemini 2.0 Flash, DeepSeek-R1, Llama 3.3) murni *client-side* (`/tools/llm-calculator.html`).
- [ DONE ] **WebGPU Shader & Inference Latency Profiler**: Profiler akselerasi perangkat keras lokal berbasis WebGPU API (`/tools/webgpu-profiler.html`).

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
- [ DONE ] **Localhost Live HTTP Server Smoke Tester (Check 21)**: Pengujian live server ephemeral localhost via `scripts/smoke_test.py` terintegrasi ke QA Gate untuk memvalidasi seluruh routing arketipe, MIME types, anti-Clickjacking, dan anti-FOUC.
- [ DONE ] **Atomic File Write Pattern & Dry-Run Mode**: Pola penulisan atomik file (`.tmp` + `os.replace`) dan simulasi `--dry-run` di `sync_content.py` untuk menjamin zero-corruption.
- [ DONE ] **Strict Secret Masking & Error Trace Redaction**: Redaksi otomatis token Bearer, API keys, dan kata sandi di seluruh log error `scripts/syndicate.py` dan `run_pipeline.py`.
- [ DONE ] **Content Hash Cache-Busting on OpenGraph & Twitter Tags**: Otomatis menyematkan hash query string `?v=<file_hash>` pada `og:image` dan `twitter:image` di seluruh 91 file HTML agar crawler media sosial (Facebook, LinkedIn, Discord, Telegram, X) tidak menampilkan thumbnail kadaluarsa.
- [ DONE ] **Web AI Agent Tool Manifest (`/tools/tools-manifest.json`)**: Ekstraksi skema JSON terstruktur untuk seluruh 46 client-side tools (parameter, elemen form, model eksekusi client-side) untuk direct tool-calling oleh Browser AI agents (Claude Computer Use, ChatGPT Operator, Gemini Web Agent).
- [ DONE ] **Dynamic Canvas Vertical Budgeting**: Kalkulator layout dinamis fleksibel di Pillow compiler untuk auto-adjust padding ketika judul/konten artikel sangat panjang.


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
- [ DONE ] **shop.zyekh.com Ecosystem Touchpoints**: Pemasangan touchpoints navigasi (`site-nav.js`), kartu unggulan di `links/index.html`, footer navigation di `index.html` dan seluruh 91 HTML files, serta architecture resource callout di `blueprints/index.html`.
- [ DONE ] **Multi-Persona & Time-Jittered Multi-Account Syndication**: Upgrade `scripts/syndicate.py` untuk mengorkestrasi multi-akun media sosial dengan klaster sudut pandang berbeda (Authority, Curation, Quick Tip), variasi copywriting otomatis, penundaan waktu acak (time-jitter 1.5s-4.5s), dan flag CLI `--persona` & `--jitter`.
- [ DONE ] **Linux Security `sysctl` & `sshd` Hardening Config Builder**: Generator konfigurasi interaktif `/etc/sysctl.d/99-hardening.conf` dan `/etc/ssh/sshd_config.d/99-hardened.conf` berbasis use-case (`/tools/linux-hardening-generator.html`).
- [ DONE ] **GitHub Actions Automated CI QA Gate**: Workflow CI otomatis di GitHub Actions untuk memvalidasi `verify_batch.py` (20-axis) pada setiap Pull Request/Commit (`.github/workflows/qa-gate.yml`).
- [ DONE ] **JSON Feed v1.1 & RFC 4287 Atom Feed Modernization**: Penambahan output sindikasi modern `feed.json` dan `atom.xml` di `sync_content.py`, autodiscovery `<link rel="alternate">` tags di 91 file HTML, integrasi robots.txt, sitemap.xml, llms.txt, dan QA Check 17.
- [ DONE ] **Interactive Zero-Trust Architecture Topology Builder**: Utilitas visual Canvas/SVG murni di browser untuk merancang dan mengekspor topologi keamanan ke Mermaid Markdown, SVG, dan ASCII (`/blueprints/topology-builder.html`).

## 6. Web3, DeFi & Decentralized Infrastructure Suite (Roadmap)
- [ BACKLOG ] **Smart Contract Security & EVM Bytecode Hardening**: Mitigasi Reentrancy, Read-Only Reentrancy, Storage Slot Collision, dan Formal Verification menggunakan Slither dan Halmos.
- [ BACKLOG ] **MEV (Maximal Extractable Value) & Mempool Architecture**: Analisis Flashbots, Searchers, Sandwich Attacks, dan arsitektur Private RPC / MEV-Boost relay.
- [ BACKLOG ] **Zero-Knowledge Proofs (zk-SNARKs vs zk-STARKs) in L2 Rollups**: Sirkuit verifikasi matematis, polynomial commitments, dan komparasi overhead komputasi Prover vs Verifier pada zkEVM.
- [ BACKLOG ] **DeFi AMM Mathematics & Concentrated Liquidity**: Analisis matematis Constant Product Invariant ($x \cdot y = k$), tick spacing Uniswap v3, dan dynamic fee routing.
- [ BACKLOG ] **Immutable Decentralized Archiving (IPFS / IPNS / Arweave Mirroring)**: Skrip otomatisasi build snapshot ke IPFS CID dan Arweave permaweb untuk preservasi knowledge base `llms.txt` tanpa runtime overhead ke browser pengunjung.
- [ BACKLOG ] **ENS (Ethereum Name Service) Contenthash Resolution**: Pemetaan domain ENS `zyekh.eth` ke snapshot IPFS CID terbaru.
- [ BACKLOG ] **Cryptographic Content Provenance (Verifiable Signatures)**: Pembuatan SHA-256 digest dan signature digital untuk setiap artikel blog / RAG database untuk integritas data anti-tampering.

## 7. AI Chatbot & Knowledge Base Assistant (Roadmap)
- [ BACKLOG ] **Interactive Site AI Chatbot**: Asisten chatbot cerdas berbasis basis pengetahuan situs (`llms.txt` / `llms-full.txt`) dengan opsi arsitektur zero-dependency (Bring-Your-Own-Key / WebLLM in-browser WebGPU / API-driven) (detail teknis menyusul dari user).

Seluruh ide di atas mematuhi prinsip ketiadaan dependensi eksternal, performa tinggi, dan bebas elemen bloat/emoji.


