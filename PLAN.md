# RFC & PLAN: Modern CSS Cascade Layers (@layer) Architecture Refactoring

## 1. Data-Backed Rationale (Why)
- **Problem**: `assets/css/shared.css` historically styles bare HTML type selectors (`input[type="text"]`, `button`, `table`, `select`, `textarea`). This creates an uncontained global blast radius where every new widget, modal, or interactive tool inadvertently inherits unwanted margins (e.g. `margin-bottom: 0.8rem`) or button paddings, causing layout shifts and specificity collisions.
- **Modern Baseline 2024+ Standard**: CSS Cascade Layers (`@layer`) explicitly decouples base browser element defaults from modular components by design. Styles defined in `@layer components` naturally and cleanly override `@layer base` regardless of selector specificity, completely eliminating specificity wars and the need for `:not(...)` exclusion chains.
- **Preserved Core Philosophy**: Zero dependencies, 100% vanilla CSS, 0% framework bloat, 100% backward compatibility with all 53 tools and 35 blog articles.

## 2. Impact & Risk Assessment
- **Benefits**:
  - Permanently eliminates global style bleeding into current and future interactive components.
  - Removes fragile `:not(...)` selector chains.
  - Maintains exact pixel-perfect design parity across all 99 HTML files.
- **Risk & Blast Radius**: Modifying `shared.css` touches the entire repository.
- **Mitigation Strategy**: Full empirical validation via 22-Axis QA Audit (`verify_batch.py`), 32 live localhost HTTP smoke tests (`scripts/smoke_test.py`), and WCAG 2.2 AA Contrast Checker (`scripts/audit_accessibility.py`).

---

## 3. Hyper-Granular Task Breakdown (PLAN)

### Chunk 1: Structure `assets/css/shared.css` into Modern CSS Cascade Layers
- **Target File**: `assets/css/shared.css`
- **Scope**:
  - Declare layer hierarchy at the top: `@layer reset, base, components, utilities;`
  - Encapsulate CSS variables (`:root`, `[data-theme="light"]`) and global resets (`*`, `html`, `body`) inside `@layer reset`.
  - Encapsulate generic element type selectors (`h1-h4`, `p`, `a`, `img`, `pre`, `code`, `table`, `input`, `button`, `select`, `textarea`, `details`, `summary`) inside `@layer base`.
  - Encapsulate modular component classes (`.site-nav`, `.theme-toggle`, `.tool-card`, `.article-card`, `.custom-card`, `.cmd-palette`, `.faq-card`, `.filter-btn`, `.bento-card`, etc.) inside `@layer components`.
  - Encapsulate utility and grid classes (`.grid-2`, `.grid-3`, `.flex-row`, `.text-muted`, `.w-full`, spacing helpers) inside `@layer utilities`.
- **DoD**: Clean CSS layer syntax, valid CSS parsing, zero syntax errors.

### Chunk 2: Streamline Widget & Component Selectors
- **Target Files**:
  - `assets/css/shared.css`
  - `assets/js/chat-widget.min.js`
- **Scope**:
  - Clean up long `:not(...)` chains from base button and input selectors.
  - Verify `.zyekh-chat-input-area`, `.zyekh-chat-input`, and `.zyekh-chat-send` interact seamlessly with `@layer components`.
- **DoD**: Zero `!important`, clean readable selectors, perfect vertical & horizontal centering.

### Chunk 3: Master Asset Synchronization & 22-Axis QA Gate
- **Target Files**:
  - `sync_content.py` (Execute automated minification `shared.min.css`, auto-bump `sw.js` `CACHE_VERSION`, update SRI SHA-384 hashes and `?v=...` query strings across all 99 HTML files).
  - `verify_batch.py` (Run 22-axis QA gate including Check 21 live HTTP server smoke test on 32 archetype routes and Check 22 WCAG 2.2 AA contrast audit).
  - `check_emojis.py` (Enforce 0 emoji compliance).
- **DoD**: 100% QA checks pass (22/22 checks), zero regressions.

### Chunk 4: Obsidian RAG Sync & Local Git Checkpoint
- **Target Files**:
  - `00-AGY-Memory/zyekh.com/DECISIONS.md` (Record ADR-043: CSS Cascade Layers `@layer` Modern Architecture Refactoring).
  - `00-AGY-Memory/zyekh.com/STATE.md` (Update active state and commit hash).
  - `00-AGY-Memory/zyekh.com/INDEX.md` (Sync commit timestamp).
- **DoD**: Memory synchronized with latest commit hash, local commit created (Strictly NO git push).
