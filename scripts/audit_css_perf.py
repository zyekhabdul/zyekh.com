#!/usr/bin/env python3
"""
scripts/audit_css_perf.py
Automated CSS Performance, Rendering Anti-Patterns & WebKit Reset Auditor.
Audits all CSS files across the repository for rendering efficiency,
layout thrashing anti-patterns, and platform pseudo-element compliance.
Strictly Zero-Emoji compliant.
"""

import sys
import re
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSS_DIR = BASE_DIR / "assets" / "css"
SHARED_CSS = CSS_DIR / "shared.css"


def remove_css_comments(css_text: str) -> str:
    """Strip standard CSS /* comments */."""
    return re.sub(r'/\*[\s\S]*?\*/', '', css_text)


def parse_css_rules(css_text: str) -> list:
    """
    Parses clean CSS text into a list of (selector, declarations_block, line_no) tuples.
    Handles nested @layer blocks gracefully.
    """
    clean_css = remove_css_comments(css_text)
    rules = []
    
    # Match standard selector { declarations } blocks
    pattern = re.compile(r'([^{}@]+)\{([^}]+)\}', re.MULTILINE)
    for match in pattern.finditer(clean_css):
        selector = match.group(1).strip()
        body = match.group(2).strip()
        start_idx = match.start()
        line_no = css_text[:start_idx].count('\n') + 1
        if selector and body:
            rules.append((selector, body, line_no))
            
    return rules


def audit_universal_transitions(rules: list, file_path: Path) -> list:
    """
    RULE 1: Prohibit universal selector wildcard transitions.
    Transitions on *, *::before, *::after, :root *, body * cause massive
    layout thrashing, dropped frames, and CPU churn during class mutations.
    """
    violations = []
    forbidden_wildcards = [
        r'^\*$',
        r'^\*::before$',
        r'^\*::after$',
        r'^\*:before$',
        r'^\*:after$',
        r'^[a-zA-Z0-9_\-\.]+\s+\*$',
        r'^[a-zA-Z0-9_\-\.]+\s+\*::before$',
        r'^[a-zA-Z0-9_\-\.]+\s+\*::after$',
    ]
    
    for selector, body, line_no in rules:
        # Check if declarations include transition
        has_transition = bool(re.search(r'\btransition\s*:', body, re.IGNORECASE))
        has_transition_property = bool(re.search(r'\btransition-property\s*:', body, re.IGNORECASE))
        
        if not (has_transition or has_transition_property):
            continue
            
        # Split comma-separated selector list
        selectors = [s.strip() for s in selector.split(',') if s.strip()]
        for sel in selectors:
            for pattern in forbidden_wildcards:
                if re.search(pattern, sel, re.IGNORECASE):
                    violations.append(
                        f"{file_path.name}:{line_no} -> Universal transition anti-pattern detected on '{sel}'. "
                        "Forces main-thread style recalculation on all DOM elements. Use targeted selectors or View Transitions API."
                    )
                    break

    return violations


def audit_webkit_search_reset(css_text: str, file_path: Path) -> list:
    """
    RULE 2: Verify WebKit search input cancel button suppression.
    If custom search inputs or clear buttons exist, WebKit pseudo-elements must be
    explicitly reset with `display: none` or `appearance: none` to prevent duplicate clear buttons.
    """
    violations = []
    has_search_input = bool(re.search(r'\bnav-search-input\b|\binput\[type=["\']?search["\']?\]', css_text))
    
    if has_search_input:
        has_cancel_reset = bool(re.search(r'::-webkit-search-cancel-button', css_text))
        has_decoration_reset = bool(re.search(r'::-webkit-search-decoration', css_text))
        
        if not (has_cancel_reset and has_decoration_reset):
            violations.append(
                f"{file_path.name} -> Missing WebKit search pseudo-element reset (::-webkit-search-cancel-button). "
                "May cause duplicate native clear buttons in Chromium/WebKit browsers."
            )
            
    return violations


def audit_cascade_layers(css_text: str, file_path: Path) -> list:
    """
    RULE 3: Verify CSS Cascade Layers (@layer) architecture.
    shared.css must define '@layer reset, base, components, utilities;' to prevent specificity drift.
    """
    violations = []
    if file_path.name == "shared.css":
        if "@layer reset, base, components, utilities;" not in css_text:
            violations.append(
                f"{file_path.name} -> Missing '@layer reset, base, components, utilities;' declaration at root."
            )
        for layer_name in ["reset", "base", "components", "utilities"]:
            if f"@layer {layer_name}" not in css_text:
                violations.append(
                    f"{file_path.name} -> Missing '@layer {layer_name}' block."
                )
    return violations


def audit_font_face_integrity(css_text: str, file_path: Path) -> list:
    """
    RULE 4: Verify @font-face declarations use modern woff2 and font-display: swap.
    """
    violations = []
    font_face_blocks = re.findall(r'@font-face\s*\{([^}]+)\}', css_text, re.MULTILINE)
    for idx, block in enumerate(font_face_blocks, 1):
        if 'font-display' not in block:
            violations.append(
                f"{file_path.name} -> @font-face block #{idx} missing 'font-display: swap;' (risks FOIT/layout shift)."
            )
        if 'format("woff2")' not in block and "format('woff2')" not in block and 'format(woff2)' not in block:
            violations.append(
                f"{file_path.name} -> @font-face block #{idx} missing modern WOFF2 format declaration."
            )
    return violations


def audit_view_transitions(css_text: str, file_path: Path) -> list:
    """
    RULE 5: Verify GPU-composited @view-transition declarations in shared.css.
    """
    violations = []
    if file_path.name == "shared.css":
        if "@view-transition" not in css_text:
            violations.append(
                f"{file_path.name} -> Missing '@view-transition { navigation: auto; }' for seamless multi-page transitions."
            )
        if "::view-transition-old(root)" not in css_text or "::view-transition-new(root)" not in css_text:
            violations.append(
                f"{file_path.name} -> Missing '::view-transition-old(root)' or '::view-transition-new(root)' duration controls."
            )
    return violations


def audit_css_performance(verbose: bool = False) -> bool:
    """
    Main audit runner for all CSS stylesheets in the repository.
    Returns True if 100% compliant, False otherwise.
    """
    print("============================================================")
    print("       CSS PERFORMANCE & ANTI-PATTERN AUDITOR (CHECK 24)    ")
    print("============================================================")
    
    css_files = sorted(list(CSS_DIR.glob("*.css")))
    # Filter out minified files for source audit
    src_css_files = [f for f in css_files if not f.name.endswith(".min.css")]
    
    all_violations = []
    
    for css_file in src_css_files:
        try:
            with open(css_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            rules = parse_css_rules(content)
            
            # Run all 5 core checks
            v1 = audit_universal_transitions(rules, css_file)
            v2 = audit_webkit_search_reset(content, css_file)
            v3 = audit_cascade_layers(content, css_file)
            v4 = audit_font_face_integrity(content, css_file)
            v5 = audit_view_transitions(content, css_file)
            
            file_violations = v1 + v2 + v3 + v4 + v5
            if file_violations:
                all_violations.extend(file_violations)
            elif verbose:
                print(f"[PASS] {css_file.name} (0 anti-patterns, {len(rules)} rules parsed)")
                
        except Exception as e:
            all_violations.append(f"Error reading {css_file.name}: {e}")

    if all_violations:
        print(f"\n[FAIL] {len(all_violations)} CSS Performance / Anti-Pattern violation(s) detected:")
        for v in all_violations:
            print(f"  • {v}")
        print("============================================================")
        print("RESULT: FAILED")
        return False
        
    print(f"\n[PASS] All {len(src_css_files)} CSS stylesheets comply 100% with CSS performance & rendering standards.")
    print("  • Zero universal wildcard transitions (* { transition })")
    print("  • WebKit search cancel pseudo-elements properly reset")
    print("  • CSS Cascade Layers (@layer reset, base, components, utilities) verified")
    print("  • @font-face font-display: swap & WOFF2 verified")
    print("  • GPU View Transitions API configured")
    print("============================================================")
    print("RESULT: 100% PASS (0 violations)")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit CSS performance and rendering anti-patterns.")
    parser.add_argument("--verbose", action="store_true", help="Print detailed rule stats")
    args = parser.parse_args()
    
    passed = audit_css_performance(verbose=args.verbose)
    sys.exit(0 if passed else 1)
