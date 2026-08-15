# PLAN: WireGuard Mesh & Keypair Configuration Generator (/tools/wireguard-generator.html)

## Objectives
1. Build `tools/wireguard-generator.html` — a zero-dependency, local-first interactive WireGuard VPN configuration suite featuring client-side Curve25519 (X25519) keypair generation, Hub-and-Spoke and Full-Mesh topology builders, PSK support, iptables/nftables NAT rules, and multi-file `.conf` export.
2. Compile deterministic 2400px social cards (16:9 Dark Landscape + 1:1 Light Square) via `scripts/generate_tools_social_cards.py`.
3. Update `scripts/generate_tools_manifest.py` and compile `tools/tools-manifest.json` (49 total tools).
4. Register the tool in `tools/index.html` under `NETWORK SECURITY`.
5. Update `scripts/inject_tool_bridges.py` to link `wireguard-vpn-tunneling-for-secure-vps-mesh-networks.html` directly to `/tools/wireguard-generator.html`.
6. Update `scripts/smoke_test.py`, run `sync_content.py`, run 21-Axis QA Gate (`verify_batch.py`), 0-emoji audit (`check_emojis.py`), update Obsidian RAG, and record local git commit.

---

## Chunk 1: Build Interactive Tool (`tools/wireguard-generator.html`)
- **Target File**: `tools/wireguard-generator.html`
- **Scope**:
  - Full SEO/GEO tags: Title, Description, Canonical URL, OpenGraph, Twitter Card, Schema.org `WebApplication` + `BreadcrumbList`.
  - Anti-Clickjacking script and Anti-FOUC theme script.
  - Responsive 2-column layout:
    - Left Column: Topology Preset Switcher (`Hub & Spoke / Gateway`, `Full Mesh Inter-VPS`, `Site-to-Site Subnet Router`), Server Interface Settings (Endpoint IP/Domain, Port 51820, Tunnel Subnet `10.8.0.0/24`, NAT egress interface `eth0`, DNS servers), Peer Management list (Dynamic peer adding/removing, auto keypair generation with X25519 math, PSK toggle).
    - Right Column: Live Configuration Tabs (Server `wg0.conf`, Peer Configs `client1.conf`, Setup Shell Commands for systemd/sysctl/iptables, JSON Topology Spec), 1-click clipboard copy (`[ COPIED ]`), and `.conf` file downloads.
  - Interactive Logic: Pure JavaScript X25519 scalar multiplication / key derivation using standard RFC 7748 Montgomery ladder curve math in browser memory, debounced live preview via `window.debounceRAF`.
- **DoD**: Tool generates mathematically valid X25519 private/public base64 keypairs, builds ready-to-use `wg0.conf` and client configs, and provides 1-click copy/download without external network calls.

---

## Chunk 2: Social Card & Manifest Compilation
- **Target Files**: `scripts/generate_tools_manifest.py`, `scripts/generate_tools_social_cards.py`, `tools/tools-manifest.json`, `assets/img/social-cards/tool-wireguard-generator-*.png`
- **Scope**:
  - Add `"wireguard": "Security & Linux Systems"` to `CATEGORY_MAP` in `scripts/generate_tools_manifest.py`.
  - Execute `scripts/generate_tools_social_cards.py` to compile deterministic 2400px cards.
  - Execute `scripts/generate_tools_manifest.py` to update `tools/tools-manifest.json`.
- **DoD**: Cards exist with valid dimensions and MD5 uniqueness; `tools-manifest.json` contains valid schema entry for `wireguard-generator`.

---

## Chunk 3: Directory Registration & Global Sync
- **Target Files**: `tools/index.html`, `scripts/inject_tool_bridges.py`, `scripts/smoke_test.py`, `sync_content.py`, `sw.js`
- **Scope**:
  - Add tool card to `tools/index.html` under `NETWORK SECURITY`.
  - Update `scripts/inject_tool_bridges.py` to bridge `wireguard-vpn-tunneling-for-secure-vps-mesh-networks.html` to `wireguard-generator.html`.
  - Add `/tools/wireguard-generator.html` to localhost smoke test matrix in `scripts/smoke_test.py`.
  - Run `python3 sync_content.py` to auto-bump `CACHE_VERSION`, compile `sitemap.xml` (93 URLs), feeds, `llms.txt`, and `llms-full.txt`.
- **DoD**: `sitemap.xml` contains 93 URLs; all HTML files have updated `CACHE_VERSION` query strings.

---

## Chunk 4: QA Gate Audit & Memory Synchronization
- **Target Files**: `IDEAS.md`, `00-AGY-Memory/zyekh.com/` (`INDEX.md`, `STATE.md`, `DECISIONS.md` ADR-035, Session Log)
- **Scope**:
  - Run `python3 verify_batch.py` (21-Axis QA Gate, 100% PASS).
  - Run `python3 check_emojis.py` (0 emojis).
  - Update `IDEAS.md` (mark item as [ DONE ]).
  - Update Obsidian RAG (`INDEX.md`, `STATE.md`, `DECISIONS.md` ADR-035).
  - Save local git commit (NO git push).
- **DoD**: 100% PASS on all verification checks; clean git status.
