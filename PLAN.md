# IMPLEMENTATION PLAN: Automated Multi-Channel Broadcast Pipeline Integration

- **Feature**: Automated Multi-Channel Broadcast Pipeline (`run_pipeline.py` + `scripts/syndicate.py`)
- **Repository**: `zyekh.com` (`/home/fuckadmin/Projects/zyekh.com`)
- **Protocol**: Adaptive AI Workflow Standard & Zero Over-Engineering

---

## Chunk 1: Upgrade `run_pipeline.py` CLI Interface & Flag Orchestration
- **Target File**: `run_pipeline.py` (Lines 1-77)
- **Scope & Objectives**:
  - Replace naive `sys.argv` inspection with standard `argparse` module.
  - Implement granular flags:
    - `--syndicate`: Trigger parallel social API syndication via `scripts/syndicate.py`.
    - `--slug <slug_name>`: Target a specific article slug for syndication (default: latest published article).
    - `--social-card`: Auto-generate dual-theme OpenGraph & square card attachments before syndicating.
    - `--skip-qa`: Skip QA step (only for quick local testing, defaults to strict QA).
    - `--purge-cf`: Standalone Cloudflare CDN cache purge.
    - `--deploy`: Commit and deploy checkpoint (strictly adhering to user permission rules).
- **Zero-Ambiguity Implementation**:
  - Add `def run_syndication(slug=None, generate_cards=True)` that delegates to `sys.executable scripts/syndicate.py --publish` with appropriate arguments.
  - Parse credentials securely from `.env` using existing `load_dotenv()` pattern.
  - Ensure zero emoji usage across all stdout/stderr messages.
- **Definition of Done (DoD)**:
  - `python3 run_pipeline.py --help` outputs all flags with zero errors.
  - `python3 check_emojis.py` confirms 0 emojis in `run_pipeline.py`.

---

## Chunk 2: Enhance `scripts/syndicate.py` Robustness & Dual Config Fallback
- **Target File**: `scripts/syndicate.py` (Lines 28-37, 353-405)
- **Scope & Objectives**:
  - Update `load_dotenv()` to support fallback checking against structured JSON configs if `.env` keys are missing.
  - Add graceful error handling so missing optional tokens (e.g. Bluesky if user only uses Mastodon/Dev.to) emit `[ WARN ]` rather than failing the entire pipeline.
  - Return proper exit codes (0 for success/graceful skip, non-zero for fatal parse error).
- **Definition of Done (DoD)**:
  - `python3 scripts/syndicate.py --latest` runs cleanly and outputs ASCII intent URLs and API status without uncaught exceptions.

---

## Chunk 3: Update Documentation & Roadmap in `IDEAS.md`
- **Target File**: `IDEAS.md` (Line 19)
- **Scope & Objectives**:
  - Mark `[ BACKLOG ] Automated Multi-Channel Broadcast Pipeline` as `[ DONE ]`.
- **Definition of Done (DoD)**:
  - Line 19 of `IDEAS.md` reads `- [ DONE ] **Automated Multi-Channel Broadcast Pipeline**: ...`

---

## Chunk 4: Automated Verification & Dry-Run Test
- **Target Scope**: End-to-end pipeline validation
- **Execution**:
  - Run `python3 verify_batch.py` (15-axis QA).
  - Run `python3 check_emojis.py`.
  - Test `python3 run_pipeline.py --help`.
  - Test dry-run of pipeline without destructive push.
- **Definition of Done (DoD)**:
  - All tests exit code 0.
