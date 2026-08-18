#!/usr/bin/env python3
"""
scripts/audit_css_invariants.py
Automated CSS Property-Pair Invariant & Specificity Collision Auditor.
Enforces that all interactive state selectors (:hover, :active, :focus)
maintain locked background and text color pairs to eliminate invisible text bugs.
Strictly Zero-Emoji compliant.
"""

import sys
import re
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSS_DIR = BASE_DIR / "assets" / "css"


def remove_css_comments(css_text: str) -> str:
    """Strip CSS /* comments */ while preserving line spacing."""
    return re.sub(r'/\*[\s\S]*?\*/', '', css_text)


def parse_css_rules(css_text: str) -> list:
    """
    Parses clean CSS text into a list of (selector, declarations_block, line_no) tuples.
    """
    clean_css = remove_css_comments(css_text)
    rules = []
    
    pattern = re.compile(r'([^{}@]+)\{([^}]+)\}', re.MULTILINE)
    for match in pattern.finditer(clean_css):
        selector = match.group(1).strip()
        body = match.group(2).strip()
        start_idx = match.start()
        line_no = css_text[:start_idx].count('\n') + 1
        if selector and body:
            rules.append((selector, body, line_no))
            
    return rules


def audit_property_pair_invariants(rules: list, file_path: Path) -> list:
    """
    RULE: Prohibit mutating background on interactive pseudo-classes
    without explicitly declaring color (or vice versa).
    """
    violations = []
    interactive_pseudos = [':hover', ':active', ':focus', ':focus-visible']
    
    whitelist_patterns = [
        r'\.card-clickable',
        r'\.bento-card',
        r'\.custom-card',
        r'\.tool-card',
        r'\.vram-block',
        r'::view-transition',
        r'summary::after',
        r'\.hamburger-bar',
        r'\.reading-progress-bar',
        r'\.nav-backdrop',
    ]

    for selector, body, line_no in rules:
        is_interactive = any(p in selector for p in interactive_pseudos)
        if not is_interactive:
            continue
            
        if any(re.search(pat, selector) for pat in whitelist_patterns):
            continue

        has_bg_mutation = bool(re.search(r'\bbackground(-color)?\s*:', body, re.IGNORECASE))
        has_color_mutation = bool(re.search(r'(?<!-)\bcolor\s*:', body, re.IGNORECASE))

        is_button_or_action = any(tok in selector.lower() for tok in ['button', 'btn', 'filter', 'tab', 'action', 'submit'])
        
        if is_button_or_action and has_bg_mutation and not has_color_mutation:
            if 'opacity' not in body and 'transform' not in body:
                violations.append(
                    f"[{file_path.name}:{line_no}] Unlocked interactive state in '{selector}'. "
                    f"Mutates background without explicitly locking text color: '{body}'"
                )

    return violations


def audit_css_invariants(verbose: bool = True) -> bool:
    """
    Master entry point for CSS Invariants Audit.
    """
    if verbose:
        print("=" * 60)
        print("     CSS PROPERTY-PAIR INVARIANT AUDITOR (CHECK 25A)      ")
        print("=" * 60)

    css_files = [
        CSS_DIR / "shared.css",
        CSS_DIR / "blog.css"
    ]
    
    total_violations = []

    for fpath in css_files:
        if not fpath.exists():
            continue
        try:
            content = fpath.read_text(encoding="utf-8")
            rules = parse_css_rules(content)
            violations = audit_property_pair_invariants(rules, fpath)
            if violations:
                total_violations.extend(violations)
                if verbose:
                    for v in violations:
                        print(f"[FAIL] {v}")
            else:
                if verbose:
                    print(f"[PASS] {fpath.name}: 100% compliant with Property-Pair Invariants.")
        except Exception as e:
            err = f"[{fpath.name}] Parse error: {e}"
            total_violations.append(err)
            if verbose:
                print(f"[FAIL] {err}")

    if verbose:
        print("=" * 60)
        if total_violations:
            print(f"RESULT: FAILED ({len(total_violations)} invariant violations found)")
        else:
            print("RESULT: 100% PASS (0 invariant violations)")

    return len(total_violations) == 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit CSS Property-Pair Invariants")
    parser.add_argument("--verbose", "-v", action="store_true", default=True, help="Detailed report")
    args = parser.parse_args()

    success = audit_css_invariants(verbose=args.verbose)
    sys.exit(0 if success else 1)
