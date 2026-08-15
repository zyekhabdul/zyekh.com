# PLAN: shop.zyekh.com Decoupled Ecosystem Touchpoints & Global Footer Modernization

## Objectives
1. Implement seamless, decoupled cross-domain touchpoints to `https://shop.zyekh.com` across `site-nav.js`, `links/index.html`, `index.html`, `blueprints/index.html`.
2. Standardize and automate footer links and accurate counts (`46 Web Tools`, `35 Articles`, `Official Store`) across all 91 HTML files via `sync_content.py`.
3. Preserve 100% static zero-dependency purity, 0 emojis, strict CSP compliance, and 100/100 Lighthouse performance.

---

## Chunk 1: Site Navigation Menu (`assets/js/site-nav.js`)
- **Target File**: `assets/js/site-nav.js`
- **Scope**:
  - Add `{ href: 'https://shop.zyekh.com', label: 'Store', key: 'shop', external: true }` to `links` array.
  - Support `target="_blank" rel="noopener noreferrer"` attribute on external links.
  - Re-minify to `assets/js/site-nav.min.js` and compute updated SHA-384 SRI hash.
- **DoD**: `assets/js/site-nav.min.js` generated and SRI integrity hash updated in `sync_content.py`.

---

## Chunk 2: Bio Link Hub (`links/index.html`) & Ecosystem Showcase (`index.html`)
- **Target Files**: `links/index.html`, `index.html`
- **Scope**:
  - Add Official Store & Merchandise card in `links/index.html` with clean microformat attributes (`rel="noopener noreferrer"`).
  - Update `index.html` footer with `Official Store` link.
- **DoD**: Cards render cleanly with high-contrast typography and no layout shifts.

---

## Chunk 3: Global Footer Sync in `sync_content.py` & Blueprints Callout
- **Target Files**: `sync_content.py`, `blueprints/index.html`
- **Scope**:
  - In `sync_content.py`, standardize footer link replacements across all 91 HTML files:
    - Update `25 Articles` / `34 Articles` -> `35 Articles`
    - Update `42 Web Tools` / `43 Web Tools` -> `46 Web Tools`
    - Ensure `Official Store` link exists in all footer navigation lists.
  - In `blueprints/index.html`, add clean technical architecture merchandise resource callout.
- **DoD**: All 91 HTML files have 100% consistent footer metrics and store links.

---

## Chunk 4: Full-System Verification & Obsidian Memory Sync
- **Target Files**: `verify_batch.py`, `IDEAS.md`, `DEVELOPMENT.md`, `00-AGY-Memory/zyekh.com/`
- **Scope**:
  - Run `python3 sync_content.py` and verify atomic updates.
  - Run `python3 verify_batch.py` (21-Axis QA Gate).
  - Run `python3 check_emojis.py`.
  - Record ADR-029 in `DECISIONS.md` and update `STATE.md`, `INDEX.md`.
  - Create local git commit (NO git push).
- **DoD**: 100% PASS on all 21 checks, 0 emojis, clean git tree.
