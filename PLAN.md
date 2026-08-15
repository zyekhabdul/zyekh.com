# PLAN: Dynamic Canvas Vertical Budgeting & Multi-Persona Syndication Suite

## Objectives
1. Implement **Dynamic Canvas Vertical Budgeting** in `scripts/generate_social_cards.py` and `scripts/validate_card_manifest.py` ensuring automatic padding and scale adjustments for high-density cards with zero collisions.
2. Implement **Multi-Persona Copywriting & Time-Jitter Throttling** in `scripts/syndicate.py` to support variable copywriting angles (`authority`, `curation`, `quick_tip`) and organic posting jitter (1.5s-4.5s).
3. Validate 100% compliance via `verify_batch.py` (Checks 1-21), 0 emojis, and Obsidian RAG memory sync.

---

## Chunk 1: Dynamic Canvas Vertical Budgeting Engine (`scripts/generate_social_cards.py`)
- **Target File**: `scripts/generate_social_cards.py`
- **Scope**:
  - Compute `available_canvas_height` dynamically after header & title drawing pass.
  - Dynamically adjust container padding (`pad_y = 20-28px`), box vertical gaps (`gap = 18-24px`), and line spacing based on wrapped text line counts.
  - Ensure footer specification bar is strictly guarded with $\ge 30\text{px}$ clearance on both 1:1 Square (2400x2400) and 16:9 Landscape (2400x1260) canvases.
- **DoD**: `scripts/validate_card_manifest.py` passes 100% with $\ge 20\text{px}$ minimum clearance across all 35 articles.

---

## Chunk 2: Multi-Persona Copywriting & Time-Jitter Engine (`scripts/syndicate.py`)
- **Target File**: `scripts/syndicate.py`
- **Scope**:
  - Implement 3 deterministic persona formatters in `scripts/syndicate.py`:
    - `authority`: High-density architectural breakdown with system invariants and production metrics.
    - `curation`: Practical engineering guide summary with actionable takeaways.
    - `quick_tip`: High-impact key command and security invariant summary.
  - Add `--persona [authority|curation|quick_tip|auto]` CLI flag.
  - Add `--jitter` parameter (randomized 1.5s - 4.5s delay via `random.uniform`) in batch syndication loops.
- **DoD**: `python3 scripts/syndicate.py --help` shows new arguments and all persona generators pass syntax and character budget tests.

---

## Chunk 3: Full-System Verification & Memory Checkpoint
- **Target Files**: `IDEAS.md`, `DEVELOPMENT.md`, `AGENTS.md`, `00-AGY-Memory/zyekh.com/`
- **Scope**:
  - Run `python3 scripts/validate_card_manifest.py`.
  - Run `python3 verify_batch.py` (21-Axis QA Gate).
  - Run `python3 check_emojis.py`.
  - Update `IDEAS.md`, `DEVELOPMENT.md`, `AGENTS.md` (ADR-031).
  - Create local git commit (NO git push).
  - Update Obsidian RAG (`INDEX.md`, `STATE.md`, `DECISIONS.md`).
- **DoD**: 100% PASS on all QA checks, 0 emojis, clean git status.
