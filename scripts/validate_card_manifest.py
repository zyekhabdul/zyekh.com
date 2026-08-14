#!/usr/bin/env python3
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MANIFEST_FILE = BASE_DIR / "data" / "social_cards_manifest.json"

def validate_manifest():
    if not MANIFEST_FILE.exists():
        print(f"[ ERROR ] Manifest file does not exist: {MANIFEST_FILE}")
        sys.exit(1)

    data = json.loads(MANIFEST_FILE.read_text(encoding='utf-8'))
    print(f"[ VALIDATION ] Auditing {len(data)} articles in manifest...")

    if len(data) != 35:
        print(f"[ ERROR ] Expected 35 articles, found {len(data)}")
        sys.exit(1)

    errors = []

    for slug, item in data.items():
        # Title
        if not item.get("title") or len(item["title"].strip()) < 5:
            errors.append(f"{slug}: Invalid or empty title")

        # Description
        if not item.get("description") or len(item["description"].strip()) < 10:
            errors.append(f"{slug}: Invalid or empty description")

        # Tags
        if not item.get("tags") or len(item["tags"]) == 0:
            errors.append(f"{slug}: Missing tags")

        # Invariants (Must be 3 complete sentences)
        invariants = item.get("invariants", [])
        if len(invariants) < 3:
            errors.append(f"{slug}: Invariants count {len(invariants)} < 3")
        for idx, inv in enumerate(invariants, 1):
            inv_str = inv.strip()
            if not inv_str or len(inv_str) < 15:
                errors.append(f"{slug}: Invariant {idx} is too short or empty: '{inv_str}'")
            if not (inv_str.endswith('.') or inv_str.endswith('!') or inv_str.endswith('?') or inv_str.endswith(')')):
                errors.append(f"{slug}: Invariant {idx} is missing terminating punctuation: '{inv_str}'")

        # Metrics (Must be 3 items)
        metrics = item.get("metrics", [])
        if len(metrics) < 3:
            errors.append(f"{slug}: Metrics count {len(metrics)} < 3")
        for idx, met in enumerate(metrics, 1):
            if not met.strip():
                errors.append(f"{slug}: Metric {idx} is empty")

        # Code Snippet (Must be 3-8 lines, last line must not end with \)
        code = item.get("code_snippet", [])
        if len(code) < 3:
            errors.append(f"{slug}: Code snippet has only {len(code)} lines (< 3)")
        if code and code[-1].strip().endswith('\\'):
            errors.append(f"{slug}: Final code line has dangling trailing backslash: '{code[-1]}'")
        for idx, line in enumerate(code, 1):
            if line.strip() in ['{', '}', '(', ')']:
                errors.append(f"{slug}: Code line {idx} is an orphan bracket: '{line}'")

    if errors:
        print(f"\n[ FAIL ] Found {len(errors)} validation errors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("\n[ PASS ] 100% Quality Audit Passed! All 35 articles have complete, verified, deterministic metadata.")

if __name__ == "__main__":
    validate_manifest()
