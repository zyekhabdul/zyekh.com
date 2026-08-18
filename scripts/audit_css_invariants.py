#!/usr/bin/env python3
"""
scripts/audit_css_invariants.py
Automated CSS Property-Pair Invariant, Token Existence & Site-Wide HTML <style> Auditor.
Scans:
1. External CSS files (shared.css, blog.css)
2. All inline <style> blocks and style="..." attributes across all 109 HTML files.
Enforces:
- Rule 1: All var(--xxx) references must exist in shared.css design tokens (prevents phantom variable bugs like var(--bg-main)).
- Rule 2: Interactive states (:hover, :active, .active, :focus) must lock color & background contrast pairs.
- Rule 3: Prohibits pairing var(--accent) with hardcoded #fff or #ffffff (prevents dark mode white-on-white text bugs).
Strictly Zero-Emoji compliant.
"""

import sys
import re
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSS_DIR = BASE_DIR / "assets" / "css"
SHARED_CSS = CSS_DIR / "shared.css"


def extract_registered_css_variables(shared_css_path: Path) -> set:
    """Extracts all defined CSS custom property names (--var-name) from shared.css."""
    if not shared_css_path.exists():
        return set()
    text = shared_css_path.read_text(encoding="utf-8")
    var_defs = re.findall(r'(--[a-zA-Z0-9_\-]+)\s*:', text)
    return set(var_defs)


def remove_css_comments(css_text: str) -> str:
    """Strip CSS /* comments */ while preserving line spacing."""
    return re.sub(r'/\*[\s\S]*?\*/', '', css_text)


def parse_css_rules(css_text: str, source_name: str) -> list:
    """
    Parses clean CSS text into a list of (selector, declarations_block, line_no, source_name) tuples.
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
            rules.append((selector, body, line_no, source_name))
            
    return rules


def audit_property_pair_invariants(rules: list) -> list:
    """
    Checks that interactive rules lock both background and color contrast pairs.
    Flags dangerous var(--accent) + #fff patterns.
    """
    violations = []
    interactive_pseudos = [':hover', ':active', ':focus', ':focus-visible', '.active']
    
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
        r'\.svg-node',
        r'\.svg-link',
        r'tr:hover',
        r'\.matrix-table',
    ]

    for selector, body, line_no, source_name in rules:
        is_interactive = any(p in selector for p in interactive_pseudos)
        if not is_interactive:
            continue
            
        if any(re.search(pat, selector) for pat in whitelist_patterns):
            continue

        # Dangerous Pattern: background: var(--accent) paired with color: #fff/#ffffff
        if re.search(r'background(-color)?\s*:\s*var\(--accent\)', body, re.IGNORECASE):
            if re.search(r'color\s*:\s*(#fff\b|#ffffff\b|white\b)', body, re.IGNORECASE):
                violations.append(
                    f"[{source_name}:{line_no}] Inverted Token Trap in '{selector}': "
                    f"Pairing 'background: var(--accent)' with 'color: #fff' causes white-on-white text in Dark Mode."
                )

        has_bg_mutation = bool(re.search(r'\bbackground(-color)?\s*:', body, re.IGNORECASE))
        has_color_mutation = bool(re.search(r'(?<!-)\bcolor\s*:', body, re.IGNORECASE))

        is_button_or_action = any(tok in selector.lower() for tok in ['button', 'btn', 'filter', 'tab', 'action', 'submit', 'tool'])
        
        if is_button_or_action and has_bg_mutation and not has_color_mutation:
            if 'opacity' not in body and 'transform' not in body:
                violations.append(
                    f"[{source_name}:{line_no}] Unlocked interactive state in '{selector}'. "
                    f"Mutates background without explicitly locking text color: '{body}'"
                )

    return violations


def audit_phantom_variables(html_files: list, registered_vars: set) -> list:
    """
    Checks that every var(--xxx) referenced across all HTML/CSS files is registered in shared.css.
    """
    violations = []
    var_usage_pattern = re.compile(r'var\((--[a-zA-Z0-9_\-]+)')
    
    # Whitelisted browser/native/third-party variables if any
    whitelist_vars = {
        '--transition',
        '--transition-slow',
    }
    
    for hpath in html_files:
        try:
            content = hpath.read_text(encoding="utf-8")
            for match in var_usage_pattern.finditer(content):
                var_name = match.group(1)
                if var_name not in registered_vars and var_name not in whitelist_vars:
                    start_idx = match.start()
                    line_no = content[:start_idx].count('\n') + 1
                    violations.append(
                        f"[{hpath.relative_to(BASE_DIR)}:{line_no}] Phantom CSS Variable '{var_name}' "
                        f"is not defined in shared.css tokens."
                    )
        except Exception as e:
            violations.append(f"[{hpath.name}] Error checking variables: {e}")
            
    return violations


def audit_css_invariants(verbose: bool = True) -> bool:
    """
    Master entry point for CSS Invariants and Phantom Variable Audit.
    """
    if verbose:
        print("=" * 60)
        print("     SITE-WIDE CSS INVARIANT & PHANTOM TOKEN AUDITOR (CHECK 25A) ")
        print("=" * 60)

    registered_vars = extract_registered_css_variables(SHARED_CSS)
    if verbose:
        print(f"[INFO] Loaded {len(registered_vars)} registered CSS tokens from shared.css.")

    total_violations = []
    all_rules = []

    # 1. External CSS
    for css_file in [CSS_DIR / "shared.css", CSS_DIR / "blog.css"]:
        if css_file.exists():
            content = css_file.read_text(encoding="utf-8")
            all_rules.extend(parse_css_rules(content, css_file.name))

    # 2. Extract <style> blocks from all HTML files
    html_files = list(BASE_DIR.glob("**/*.html"))
    html_files = [f for f in html_files if ".git" not in str(f) and ".gemini" not in str(f)]

    style_tag_pattern = re.compile(r'<style[^>]*>([\s\S]*?)</style>', re.IGNORECASE)
    for hpath in html_files:
        try:
            content = hpath.read_text(encoding="utf-8")
            for match in style_tag_pattern.finditer(content):
                style_content = match.group(1)
                rel_path = str(hpath.relative_to(BASE_DIR))
                all_rules.extend(parse_css_rules(style_content, rel_path))
        except Exception as e:
            total_violations.append(f"[{hpath.name}] Style extract error: {e}")

    # Run Invariants on all rules
    invariant_violations = audit_property_pair_invariants(all_rules)
    total_violations.extend(invariant_violations)

    # Run Phantom Variable Audit on all HTML files
    phantom_violations = audit_phantom_variables(html_files, registered_vars)
    total_violations.extend(phantom_violations)

    if verbose:
        if total_violations:
            for v in total_violations:
                print(f"[FAIL] {v}")
            print("=" * 60)
            print(f"RESULT: FAILED ({len(total_violations)} invariant/token violations found across site)")
        else:
            print(f"[PASS] Audited {len(all_rules)} CSS rules and {len(html_files)} HTML documents.")
            print("[PASS] 100% compliant with Property-Pair Invariants, Token Existence & Anti-Trap rules.")
            print("=" * 60)
            print("RESULT: 100% PASS (0 violations)")

    return len(total_violations) == 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit CSS Invariants and Tokens Site-Wide")
    parser.add_argument("--verbose", "-v", action="store_true", default=True, help="Detailed report")
    args = parser.parse_args()

    success = audit_css_invariants(verbose=args.verbose)
    sys.exit(0 if success else 1)
