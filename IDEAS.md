# [ IDEAS ] Zyekh.com Enhancement Proposals & Master Roadmap

Dokumen ini adalah single source of truth untuk seluruh ide, backlog, dan peta jalan strategis ekosistem **zyekh.com** dan sub-proyek terkait. Seluruh usulan wajib mematuhi filosofi *Zero-Dependency*, *Zero-Framework*, *Local-First*, dan *Strict No-Emoji*.

---

## [ BAGIAN 1 ] Fitur & Infrastruktur yang Telah Selesai (Ground-Truth Verified)

### 1. Client-Side Web Tools (53 Tools Aktif di `/tools/`)
- [ DONE ] **Developer & Syntax Utilities**: JSON Formatter & AST Validator (`json.html`), Diff Checker (`diff-checker.html`), Regex Tester (`regex.html`), Markdown Editor (`markdown.html`), Base64 Tool (`base64.html`), HTML Entity (`html-entity.html`), Case Converter (`case-converter.html`), CSS Minifier (`css-minifier.html`), SQL Formatter (`sql.html`), cURL Builder (`curl.html`), Cron Expression Tester (`cron.html`), Chmod Octal Calculator (`chmod-calculator.html`), UUID Generator (`uuid.html`), URL Encoder (`url.html`), Hash SHA/MD5 (`hash.html`), HMAC Generator (`hmac.html`), Epoch Timestamp (`epoch.html`), Subnet IPv4 (`subnet.html`).
- [ DONE ] **Security & Kernel Generators**: Linux Security sysctl & sshd Generator (`linux-hardening-generator.html`), PAM & Faillock Account Lockout Policy Generator (`pam-generator.html`), Linux Auditd & DFIR Event Rule Generator (`auditd-generator.html`), OCI Container Seccomp Profile Generator (`seccomp-generator.html`), Systemd Service Sandboxing Override Generator (`systemd-generator.html`), WireGuard Mesh & Keypair Generator (`wireguard-generator.html`), JWT Token Decoder (`jwt.html`), Web Crypto Password Generator (`password.html`), eBPF XDP Packet Filter Evaluator (`ebpf-evaluator.html`).
- [ DONE ] **AI & Compute Profilers**: LLM Token & GPU VRAM Inference Cost Calculator 2026 (`llm-calculator.html`), AI Token Counter (`ai-token.html`), Speculative Decoding Interactive Simulator (`speculative-decoding.html`), WebGPU Shader & Inference Latency Profiler (`webgpu-profiler.html`).
- [ DONE ] **Finansial & Ketenagakerjaan**: PPh 21 Tax Calculator (`pph21.html`), KPR Mortgage Calculator (`kpr.html`), JHT BPJS (`jht.html`), JKP BPJS (`jkp.html`), Pesangon UU Cipta Kerja (`pesangon.html`), THR Keagamaan (`thr.html`), Zakat Mal & Fitrah (`zakat.html`), Split Bill (`split-bill.html`).
- [ DONE ] **Media & Productivity Utilities**: Client-side Canvas Image Converter (`image-converter.html`), SVG Converter (`svg-converter.html`), QR Code Generator (`qr.html`), Text-to-Speech Web Speech API (`tts.html`), Pomodoro Timer (`pomodoro.html`), Countdown Timer (`countdown.html`), Counter (`counter.html`), Color Palette Picker (`color.html`), Unit Converter (`converter.html`), Random Picker (`random-picker.html`), Dice Roller (`dice.html`), Lorem Ipsum Generator (`lorem.html`), Env Parser (`env.html`), CSV to JSON Converter (`csv-json.html`).

### 2. Pipeline Otomasi, CI/CD, Minifikasi & QA Gate
- [ DONE ] **Python-based Asset Minifier**: Minifikasi mandiri CSS dan JS tanpa Node.js di `sync_content.py`.
- [ DONE ] **Automated Subresource Integrity (SRI) & CSP**: Generator hash SHA-384 pada aset statis.
- [ DONE ] **Cloudflare Edge Cache Purge**: Otomasi purge cache via API Zone `1427afa77c5824ee0c34b514260e2e5d`.
- [ DONE ] **Decoupled 3-Stage Social Card Generator**: Generator gambar Ultra-HD 2400px (Light Square + Dark Landscape) berbasis `data/social_cards_manifest.json` (ADR-014).
- [ DONE ] **25-Axis Programmatic QA Gate (`verify_batch.py`)**: Validasi 10 komponen SOP, MD5 image uniqueness, WCAG 2.2 AA accessibility, CSS property invariants, headless Playwright probe, dan Check 21 live localhost HTTP smoke test (32 route).
- [ DONE ] **Multi-Format Feed Syndication**: RSS 2.0 (`feed.xml`), RFC 4287 Atom 1.0 (`atom.xml`), dan JSON Feed 1.1 (`feed.json`) terintegrasi autodiscovery `<link rel="alternate">`.
- [ DONE ] **Web AI Agent Tool Manifest (`/tools/tools-manifest.json`)**: Skema JSON terstruktur untuk direct calling oleh Browser AI agents (Claude Computer Use, ChatGPT Operator).
- [ DONE ] **GitHub Actions Automated CI QA Gate**: Workflow CI otomatis di `.github/workflows/qa-gate.yml` dan daily social drip di `.github/workflows/social-syndicate.yml`.

### 3. UI/UX, Navigasi & Standar Baseline 2024+
- [ DONE ] **Custom Web Component `<site-nav>`**: Navigasi responsif terpusat dengan mobile drawer breakpoint `max-width: 960px`.
- [ DONE ] **CSS Cascade Layers (`@layer`)**: Pemisahan `@layer reset, base, components, utilities;` di `assets/css/shared.css` untuk eliminasi spesifisitas.
- [ DONE ] **Native Search & Instant Mark**: Input pencarian dengan tombol reset native WebKit suppressed dan highlight token `<mark>`.
- [ DONE ] **GPU View-Transition API**: Transisi tema gelap/terang mulus tanpa frame drop.
- [ DONE ] **Native Lightbox `<dialog>`**: Zoom gambar arsitektur murni native browser tanpa library eksternal.
- [ DONE ] **Self-Hosted Link Hub (`/links/`)**: Pengganti Linktree murni Vanilla HTML5/CSS dengan microformats `rel="me"`.
- [ DONE ] **Interactive Zero-Trust Topology Builder (`/blueprints/topology-builder.html`)**: Desainer diagram topologi jaringan visual SVG/Canvas dengan ekspor Mermaid, SVG, dan ASCII.

### 4. Deep-Tech Articles (45 Artikel Lengkap di `/blog/`)
- [ DONE ] **Batch 1 (Sysadmin & Linux Security)**: Linux VPS Hardening 2026, UFW Firewall, Fail2ban, PAM faillock, Systemd Sandboxing, Auditd DFIR, eBPF Monitoring, SSH Certificates Vault CA, FIDO2 SSH-CA.
- [ DONE ] **Batch 2 (Cloud Native & Network Security)**: eBPF XDP DDoS Mitigation, Cilium eBPF Tetragon, Linux Seccomp BPF, Landlock LSM Sandboxing, Chroot & Namespaces Isolation, Kubernetes PSS, Cosign SLSA Provenance, Nginx Hardening, HTTP/3 QUIC 0-RTT, Strict CSP, WireGuard VPN Mesh.
- [ DONE ] **Batch 3 (AI & LLM Infrastructure)**: vLLM PagedAttention Tuning, Speculative Decoding & Medusa, MoE Mixture of Experts Routing, S-LoRA Adapter Multiplexing, WebGPU LLM Browser Sandbox, KV Cache INT4 Quantization, ColBERT Late-Interaction RAG, DSPy Prompt Optimization, OmniRouter Gateway Fallback, Structured Output Generation, Multi-Agent Swarm Patterns.
- [ DONE ] **Batch 4 (Web3, Cryptography & Storage Engines)**: Smart Contract Security EVM Bytecode, MEV & Private Mempool, zk-SNARKs vs zk-STARKs L2 Rollups, DeFi AMM Concentrated Liquidity, Cross-Chain Bridges Light Client, Account Abstraction ERC-4337, Post-Quantum Cryptography ML-KEM/ML-DSA, Database Storage Engines LSM-Trees vs B+ Trees, Distributed Consensus Raft vs Paxos, Rust in Linux Kernel Memory Safety.

---

## [ BAGIAN 2 ] Peta Jalan & Backlog Aktif per Domain Target (Active Roadmap)

### Domain A: `zyekh.com` Web Hub (Zero-Dependency Static Site)

#### Cluster 1: Web3 & Client-Side Cryptography Tools
- [ BACKLOG ] **Solidity Storage Slot & Layout Calculator (`/tools/solidity-storage-calculator.html`)**: Tool interaktif browser untuk memetakan packing variabel Solidity 32-byte slots, keccak256 mapping slot calculation, array dinamis, dan ERC-7201 namespaced storage.
- [ BACKLOG ] **Ethereum ABI & Calldata Encoder / Decoder (`/tools/abi-decoder.html`)**: Parser calldata offline untuk mendecode function selector 4-byte, tuples, dynamic arrays, dan pembuatan payload multisig.
- [ BACKLOG ] **Ed25519 & Secp256k1 WebCrypto Keypair Generator (`/tools/crypto-keypair-generator.html`)**: Pembangkit pasangan kunci kriptografis murni berbasis native `window.crypto.subtle` tanpa library eksternal.

#### Cluster 2: Content GEO Batch 5 (10 Artikel Deep-Tech)
- [ BACKLOG ] **EIP-4844 Proto-Danksharding & Blobspace Architecture**: Ephemeral data blobs, KZG polynomial commitments, dan `blob_base_fee`.
- [ BACKLOG ] **Solana Sealevel Parallel Runtime & Transaction Pipeline**: Memory model non-overlapping accounts, Gulf Stream, dan Proof of History.
- [ BACKLOG ] **Cosmos Tendermint / CometBFT Consensus & IBC Relayers**: State Machine Replication BFT 2/3 voting power dan ICS-20 cross-chain token transfers.
- [ BACKLOG ] **Fully Homomorphic Encryption (FHE) & Confidential EVM Computing**: TFHE/CKKS schemes dan confidential smart contracts.
- [ BACKLOG ] **Restaking Mechanics & Actively Validated Services (EigenLayer AVS)**: Slashing conditions, dual staking, dan AVS operator delegation.
- [ BACKLOG ] **Decentralized Oracle Networks (Chainlink DON vs Pyth Pull Oracles)**: OCR2 threshold signatures dan high-frequency price feeds.
- [ BACKLOG ] **Bitcoin Lightning Network HTLCs & Payment Channel Factories**: Hashed Time-Locked Contracts, Eltoo, dan Taproot factories.
- [ BACKLOG ] **Threshold Cryptography (MPC-TSS vs Multi-sig Wallets)**: FROST / GG20 threshold signatures, Shamir secret sharing, dan DKG.
- [ BACKLOG ] **Decentralized Storage Internals (IPFS BitSwap, Filecoin & Arweave)**: UnixFS DAG, PoSt, PoRep, dan SPoRA permaweb mechanics.
- [ BACKLOG ] **ZK-Rollup Sequencer Decentralization & Shared Sequencing**: Based Rollups, Espresso / Radius shared sequencer networks, dan L2 PBS.

#### Cluster 3: Decentralized Archiving & Cryptographic Provenance
- [ BACKLOG ] **Immutable Decentralized Archiving (IPFS / IPNS / Arweave Mirroring)**: Skrip build snapshot ke IPFS CID dan Arweave permaweb untuk preservasi knowledge base `llms.txt`.
- [ BACKLOG ] **ENS Contenthash Resolution**: Pemetaan domain ENS `zyekh.eth` ke snapshot IPFS terbaru.
- [ BACKLOG ] **Cryptographic Content Provenance Manifest (`/data/provenance-manifest.json`)**: Generator digest SHA-256 dan signature PGP otomatis untuk seluruh artikel blog, feeds, dan `llms.txt` yang terekam pada manifest tanda tangan terverifikasi.

#### Cluster 4: Custom ArchISO & FOSS Distribution Hub
- [ BACKLOG ] **Custom ArchISO & Linux Build Distribution Hub (`/downloads/` atau `/dist/`)**: Halaman katalog dan mirror download terverifikasi untuk custom image ArchISO, script deploy Linux, dan tooling FOSS karya pengembang.
- [ BACKLOG ] **FOSS Artifact Cryptographic Checksum & Signature Verification**: SHA-256 / SHA-512 checksums, Minisign / PGP signature blocks, dan mirror links terverifikasi.
- [ BACKLOG ] **FOSS Philosophy & Open Source Advocacy Statement**: Penegasan posisi zyekh.com sebagai platform independen pro-FOSS dan software bebas.

#### Cluster 5: UI/UX Micro-Enhancements
- [ BACKLOG ] **Professional Social Media Placement**: Penambahan link profil media sosial profesional (LinkedIn, GitHub, GitLab, Codeberg) secara elegan pada Quick Links / Bento Grid di `index.html`.
- [ BACKLOG ] **Client-Side AI Knowledge Assistant**: Asisten chat cerdas berbasis `llms.txt` dengan arsitektur zero-dependency (BYOK / WebLLM in-browser WebGPU) yang di-load murni saat interaksi pengguna (lazy-loaded).

---

### Domain B: `shop.zyekh.com-theme` (Shopify Liquid 2.0 Storefront)
*Catatan Arsitektur: Seluruh item di domain ini berada di repositori terisolasi `Projects/shop.zyekh.com-theme` untuk menjaga kemurnian statis domain root.*

- [ BACKLOG ] **Bundle & Save Multi-Pack Tier**: Komponen diskon kuantitas bertingkat pada PDP untuk melipatgandakan Average Order Value (AOV).
- [ BACKLOG ] **Geo-IP Delivery Date Guarantee Widget**: Kalkulator estimasi tanggal tiba dinamis berbasis lokasi IP pengunjung untuk menekan *cart abandonment*.
- [ BACKLOG ] **Sticky Express Purchase Bar**: Bilah ATC melayang bergaya glassmorphism untuk checkout cepat impulsif di perangkat seluler.

---

### Domain C: `zyekhabdul` GitHub Ecosystem & Python Security Frameworks
*Catatan Arsitektur: Seluruh item di domain ini berada di repositori Python DFIR terpisah (`vol3-ebpf-detector`, `volatility3-ai-triage`).*

- [ DONE ] **Volatility 3 Cyber Suite Consolidation**: Penggabungan repositori `vol3-ebpf-detector` dan `volatility3-ai-triage` menjadi satu framework Python terpadu (`volatility3-cyber-suite`) dengan CLI seragam (`vol3-suite`), parser STIX 2.1, eBPF JIT carver, heuristic memory injection correlation, dan Web Dashboard lokal.
- [ BACKLOG ] **PyPI Package Distribution**: Publikasi paket resmi ke Python Package Index (`pip install vol3-ebpf-detector` dan `pip install volatility3-ai-triage`).
- [ BACKLOG ] **Terminal Recording & Visual Demo Artifacts**: Pembuatan demonstrasi visual terminal via VHS / asciinema (GIF/SVG) untuk landing page dan README repositori.
- [ BACKLOG ] **Curated Awesome-Lists Inclusion**: Pengajuan Pull Request resmi untuk mendaftarkan proyek ke `awesome-ebpf`, `awesome-forensics`, `awesome-incident-response`, dan `awesome-laravel`.
- [ BACKLOG ] **Technical Deep-Dive Community Writeups**: Penyusunan artikel "Show HN" untuk Hacker News dan serial tulisan teknis di komunitas Reddit (`r/netsec`, `r/ReverseEngineering`, `r/cybersecurity`, `r/Python`).

---

### Domain D: VPS Runtime & Mobile Client (`agy` Mobile Assistant)
*Catatan Arsitektur: Seluruh item di domain ini berada di stack VPS daemon & aplikasi mobile terpisah.*

- [ DONE ] **Self-Hosted Sovereign Dynamic QRIS Engine (`zyekh-ai-core`)**: Modul EMVCo Dynamic QRIS generator mandiri dengan injeksi Tag 54, checksum CRC16-CCITT, dan resolusi kode unik 3-digit untuk bypass ketergantungan pihak ketiga (`zyekh-ai-core/qrisEngine.js`).
- [ DONE ] **Omnichannel Mutation Ingestor & Auto-Dispatcher**: Hub pembayaran terpadu yang memproses webhook mutasi bank/e-wallet dan melakukan dispatch produk digital otomatis ke Bot Telegram, Bot WhatsApp (`bot-whatsapp`), dan Web Storefront (`shop.zyekh.com`).
- [ BACKLOG ] **VPS AI Engine to Mobile App (Play Store & App Store)**: Integrasi engine AI bot berbasis Antigravity CLI (`agy` / Gemini) yang berjalan di VPS menjadi backend API untuk aplikasi mobile (Android/iOS).
- [ BACKLOG ] **Headless AGY Daemon with Strict Chat-Only Sandboxing**: Lightweight bridge daemon (Node.js/Go/Python) dengan Server-Sent Events (SSE) / WebSocket streaming, process pool, session isolation, dan penonaktifan akses command berbahaya untuk pengguna publik.
- [ BACKLOG ] **Cross-Platform Mobile Client (Flutter / React Native)**: Frontend chat native dengan markdown & code syntax highlighting, real-time token streaming, sinkronisasi histori sesi, dan integrasi Play Billing / Apple IAP.

---

### Domain E: Arsitektur Hosting & Edge Delivery Standards (Hybrid Edge + VPS Indo)
*Catatan Arsitektur: Standar deployment resmi untuk proyek open-source dan aplikasi web dengan backend terpisah.*

- [ BACKLOG ] **Decoupled Architecture Standard (GitHub + Cloudflare Pages + VPS Indo)**: Menetapkan pola standar deployment di mana repositori kode publik tetap berada di GitHub (untuk exposure open-source, portofolio dev, dan CI/CD trigger), frontend statis/SPA di-deploy ke Cloudflare Pages (Anycast Edge CDN Jakarta, native SPA routing, zero-hack `_headers` CORS, custom domain SSL), dan backend komputasi/API hosted di VPS Indonesia (`api.domain.com`) untuk menjamin latensi transaksi data terendah bagi pengguna lokal tanpa limitasi routing/CORS di GitHub Pages.
- [ DONE ] **Cloudflare Pages Deployment Migration & Static Headers Standard**: Migrasi konfigurasi edge hosting ke Cloudflare Pages dengan file `_headers` (granular `Cache-Control`, strict CSP, HSTS, Permissions-Policy) dan `_redirects` terstandarisasi untuk kecepatan akses Anycast Edge, eliminasi origin hop, dan zero-downtime custom domain routing.


