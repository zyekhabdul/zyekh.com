# PLAN: Eksekusi Refinement & Optimasi Halaman Inti (Core Landing Pages) — Seksi 11 IDEAS.md

## [ 1. DATA-BACKED RATIONALE & OBJECTIVE ]
- **Latar Belakang**: Seiring ekspansi repositori ke 53 Client-Side Tools, 45 Deep-Dive Technical Articles, 25+ Security Blueprints, dan RAG Knowledge Base, halaman inti portal (`index.html`, `about/index.html`, `contact/index.html`, `tools/index.html`, `blueprints/index.html`) memerlukan sinkronisasi metrik, penguatan visual hierarchy, pembaruan riset sistem (Web3, eBPF, ZK, PQC, LLM Inference), dan integrasi panduan komunikasi terenkripsi PGP.
- **Tujuan**: Memperbarui dan menyelaraskan 5 halaman inti tersebut dengan standar Baseline 2024+, Zero-Emoji, WCAG 2.2 AA accessibility, dan zero-dependency vanilla architecture.

---

## [ 2. HYPER-GRANULAR EXECUTION CHUNKS ]

### Chunk 1: Home Landing Page (`index.html`) Refinement & Visual Hierarchy
* **Target File**: `index.html`
* **Scope**:
  1. Penyelarasan counter metrik hero: 53 Client-Side Tools, 45 Deep-Dive Articles, 25+ Security Blueprints, dan RAG Knowledge Base (`llms.txt`).
  2. Optimalisasi Bento Grid: Tambahkan touchpoint terstruktur yang menyeimbangkan showcase Web Tools, Command Blueprints, Deep-Dive Research, dan Topology Builder.
  3. Perbarui quick-tool pills agar menampilkan representasi tools mutakhir (LLM Calculator, WebGPU Profiler, Linux Hardening, Seccomp Generator, JWT, Subnet).
  4. Perbarui Schema.org `WebSite` JSON-LD agar selaras dengan 53 tools dan 45 articles.

### Chunk 2: About & Experience Page (`about/index.html`) Research Timeline & PGP Card
* **Target File**: `about/index.html`
* **Scope**:
  1. Perbarui **Key Focus & Specialization** dengan klaster riset terkini:
     - *Backend & Distributed Systems* (Laravel 12, Redis, LSM-Trees/B+ Trees, Raft/Paxos consensus, Microservices).
     - *Kernel & Network Hardening* (eBPF XDP, Seccomp BPF, Landlock LSM, Auditd DFIR, PAM Faillock, WireGuard mesh).
     - *Applied Cryptography & Web3* (EVM bytecode security, MEV architecture, zk-SNARKs/STARKs, Post-Quantum ML-KEM/ML-DSA).
     - *AI Systems & Hardware Acceleration* (vLLM PagedAttention, Speculative Decoding, WebGPU WGSL compute, S-LoRA).
  2. Perbarui **Featured Technical Research** mencakup proyek open-source dan sistem riset terverifikasi.
  3. Modernisasi **PGP / Security Verification Card** dengan fingerprint GPG scannable dan copyable, serta command `curl -sL zyekh.com/gpg-key.asc | gpg --import`.
  4. Tingkatkan command parser **Developer Console** untuk mendukung perintah `blueprints`, `crypto`, `security`, `pqc`, `ebpf`, dan `clear`.

### Chunk 3: Contact & Verification Page (`contact/index.html`) Refinement & Secure Comms Guidance
* **Target File**: `contact/index.html`
* **Scope**:
  1. Tambahkan seksi panduan **PGP Encrypted Communications** untuk pelaporan vulnerability (RFC 9116 / `security.txt`) dan konsultasi arsitektur sensitif.
  2. Sempurnakan tampilan card channels verifikasi: LinkedIn, GitHub, Mastodon, Discord, Primary Email, GPG Key, RFC 9116 Security Policy.
  3. Pastikan layout grid, input styling, dan responsivitas mobile selaras 100% dengan `shared.css`.

### Chunk 4: Tools Hub (`tools/index.html`) Category Filtering & Search Optimization
* **Target File**: `tools/index.html`
* **Scope**:
  1. Restrukturisasi kategori filter pill bar agar mencakup seluruh spektrum 53 tools:
     - `Semua (53)`
     - `Security & Linux Hardening`
     - `AI & LLM Infrastructure`
     - `Developer Utilities`
     - `Finansial & Pajak`
     - `Teks & Format`
     - `Generators & Web3`
  2. Pastikan mapping `data-category` dan `data-title` pada seluruh 53 `tool-item` sinkron dengan kategori baru.
  3. Verifikasi performa instant search filtering dan count counter real-time.

### Chunk 5: Blueprints Hub (`blueprints/index.html`) Blueprint Indexing & Category Alignment
* **Target File**: `blueprints/index.html`
* **Scope**:
  1. Perbarui category pill filters: `Semua`, `Kernel & eBPF`, `Zero Trust & Sandboxing`, `Linux Hardening`, `Cloud Native`.
  2. Sinkronkan katalog blueprint cards dengan artikel-artikel blueprint batch terbaru (Auditd DFIR, PAM Faillock, Linux Hardening sysctl/sshd, WireGuard Mesh, Seccomp BPF, Systemd Sandboxing, Post-Quantum TLS).
  3. Pastikan live search dan category filtering berjalan mulus tanpa lag.

### Chunk 6: Pipeline Synchronization, QA Audit & Obsidian Memory Sync
* **Target Files**: `sync_content.py`, `IDEAS.md`, `DECISIONS.md`, `00-AGY-Memory/zyekh-com/STATE.md`
* **Scope**:
  1. Jalankan `python3 sync_content.py` untuk otomatis bump `CACHE_VERSION` di `sw.js`, memperbarui query versioning `?v=...`, dan sync sitemap/feeds.
  2. Jalankan verifikasi 22-axis QA Gate: `python3 verify_batch.py`.
  3. Jalankan audit zero-emoji: `python3 check_emojis.py`.
  4. Jalankan live localhost smoke test: `python3 scripts/smoke_test.py`.
  5. Perbarui `IDEAS.md` (tandai backlog Seksi 11 sebagai `[ DONE ]`) dan catat ADR di `DECISIONS.md` serta checkpoint di Obsidian RAG.

---

## [ 3. DEFINITION OF DONE (DoD) ]
- [ ] Kelima halaman inti (`index.html`, `about/`, `contact/`, `tools/`, `blueprints/`) telah direfine dan tersinkronisasi 100%.
- [ ] Seluruh metrik konsisten (53 Tools, 45 Articles, Zero-Trust Blueprints, RAG Base).
- [ ] Kategori filter di `tools/index.html` dan `blueprints/index.html` mencakup seluruh katalog baru secara presisi.
- [ ] GPG key card & secure communications guidance terpasang rapi di `about/` dan `contact/`.
- [ ] Lolos 100% QA Gate 22-Axis (`verify_batch.py`), Zero-Emoji audit (`check_emojis.py`), dan Smoke Test (`smoke_test.py`).
- [ ] Sinkronisasi cache version dan query string HTML via `sync_content.py`.
