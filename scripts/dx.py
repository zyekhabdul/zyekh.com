#!/usr/bin/env python3
"""
dx.py — Unified Developer Orchestrator & Fast Verification CLI for zyekh.com
Provides fast incremental builds, automated cache synchronization, and single-command QA gates.

Usage:
  python3 scripts/dx.py --all       # Full pipeline: sync + provenance + emojis + full QA (Checks 1-25)
  python3 scripts/dx.py --fast      # Fast pipeline: sync + provenance + emojis + fast QA (skips Playwright)
  python3 scripts/dx.py --sync      # Sync content, minification & provenance only
  python3 scripts/dx.py --verify    # Run QA verification only
  python3 scripts/dx.py --emojis    # Check emojis only
"""

import sys
import time
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def run_step(name: str, cmd: list[str]) -> bool:
    """Executes a subprocess command with timing feedback."""
    t0 = time.time()
    print(f"[ DX ] Executing {name}...")
    try:
        proc = subprocess.run(cmd, cwd=str(BASE_DIR))
        elapsed = time.time() - t0
        if proc.returncode == 0:
            print(f"[ PASS ] {name} completed in {elapsed:.2f}s.\n")
            return True
        else:
            print(f"[ FAIL ] {name} failed with exit code {proc.returncode} in {elapsed:.2f}s.\n")
            return False
    except Exception as e:
        print(f"[ ERROR ] Could not execute {name}: {e}\n")
        return False

def main():
    t_start = time.time()
    args = sys.argv[1:]
    
    if not args or "--help" in args or "-h" in args:
        print(__doc__.strip())
        sys.exit(0)

    is_all = "--all" in args or "-a" in args
    is_fast = "--fast" in args or "-f" in args
    is_sync = "--sync" in args or "-s" in args or is_all or is_fast
    is_verify = "--verify" in args or "-v" in args or is_all or is_fast
    is_emojis = "--emojis" in args or "-e" in args or is_all or is_fast
    no_cache = "--no-cache" in args

    print("============================================================")
    print("      ZYEKH.COM UNIFIED DEVELOPER ACCELERATOR (DX CLI)      ")
    print("============================================================\n")

    # Step 1: Sync Content & Cache Bumping
    if is_sync:
        if not run_step("Content Sync & Cache Bumping", [sys.executable, "sync_content.py"]):
            sys.exit(1)
        if not run_step("Provenance Manifest Signing", [sys.executable, "scripts/generate_provenance_manifest.py"]):
            sys.exit(1)

    # Step 2: Emoji Compliance Audit
    if is_emojis:
        if not run_step("Zero-Emoji Compliance Audit", [sys.executable, "check_emojis.py"]):
            sys.exit(1)

    # Step 3: QA Verification Gate
    if is_verify:
        verify_cmd = [sys.executable, "verify_batch.py"]
        if is_fast:
            verify_cmd.append("--fast")
        if no_cache:
            verify_cmd.append("--no-cache")
        if not run_step("25-Axis QA Gate Auditor", verify_cmd):
            sys.exit(1)

    total_time = time.time() - t_start
    print("============================================================")
    print(f"SUCCESS: Developer pipeline finished cleanly in {total_time:.2f}s!")
    print("============================================================")

if __name__ == "__main__":
    main()
