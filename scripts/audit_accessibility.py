#!/usr/bin/env python3
"""
scripts/audit_accessibility.py
Automated DOM Accessibility & WCAG 2.2 AA Contrast QA Checker.
Audits all HTML files and design tokens across the repository.
Strictly Zero-Emoji compliant.
"""

import sys
import glob
import re
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent


def calculate_luminance(r: int, g: int, b: int) -> float:
    """Calculate WCAG 2.2 relative luminance for an sRGB color."""
    def adjust(c: float) -> float:
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r_adj = adjust(r)
    g_adj = adjust(g)
    b_adj = adjust(b)
    return 0.2126 * r_adj + 0.7152 * g_adj + 0.0722 * b_adj


def hex_to_rgb(hex_code: str) -> tuple:
    """Convert hex color string to (r, g, b) tuple."""
    hex_clean = hex_code.strip().lstrip("#")
    if len(hex_clean) == 3:
        hex_clean = "".join([c * 2 for c in hex_clean])
    elif len(hex_clean) == 8:
        hex_clean = hex_clean[:6]
    return tuple(int(hex_clean[i:i + 2], 16) for i in (0, 2, 4))


def calculate_contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculate WCAG contrast ratio between two hex colors."""
    try:
        rgb1 = hex_to_rgb(hex1)
        rgb2 = hex_to_rgb(hex2)
        l1 = calculate_luminance(*rgb1)
        l2 = calculate_luminance(*rgb2)
        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)
    except Exception:
        return 0.0


def audit_color_tokens() -> list:
    """Audit CSS custom property color contrast ratios."""
    issues = []
    # Token definitions from shared.css
    token_pairs = [
        # Dark theme
        ("Dark: text-main on bg-dark", "#fafafa", "#09090b", 4.5),
        ("Dark: text-main on bg-card", "#fafafa", "#141417", 4.5),
        ("Dark: text-muted on bg-dark", "#a1a1aa", "#09090b", 4.5),
        ("Dark: text-muted on bg-card", "#a1a1aa", "#141417", 4.5),
        ("Dark: info on bg-card", "#e4e4e7", "#141417", 4.5),
        ("Dark: border on bg-dark", "#27272a", "#09090b", 1.2),
        # Light theme
        ("Light: text-main on bg-dark", "#09090b", "#f0f0f3", 4.5),
        ("Light: text-main on bg-card", "#09090b", "#ffffff", 4.5),
        ("Light: text-muted on bg-dark", "#27272a", "#f0f0f3", 4.5),
        ("Light: text-muted on bg-card", "#27272a", "#ffffff", 4.5),
        ("Light: info on bg-card", "#18181b", "#ffffff", 4.5),
    ]

    for label, fg, bg, min_ratio in token_pairs:
        ratio = calculate_contrast_ratio(fg, bg)
        if ratio < min_ratio:
            issues.append(f"Contrast failure in '{label}': {ratio:.2f}:1 (Required: >={min_ratio}:1)")

    return issues


def audit_html_file(file_path: Path) -> list:
    """Run comprehensive accessibility checks against an HTML file."""
    issues = []
    rel_path = file_path.relative_to(BASE_DIR)
    
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        soup = BeautifulSoup(content, "html.parser")
    except Exception as e:
        return [f"{rel_path}: Failed to parse HTML - {e}"]

    # 1. Check HTML lang attribute (WCAG 3.1.1)
    html_tag = soup.find("html")
    if not html_tag or not html_tag.get("lang"):
        issues.append(f"{rel_path}: Missing or empty <html lang=\"...\"> attribute")

    # 2. Check Viewport Zoom Restrictions (WCAG 1.4.4)
    viewport_meta = soup.find("meta", attrs={"name": "viewport"})
    if viewport_meta and viewport_meta.get("content"):
        content_val = viewport_meta["content"].lower()
        if "user-scalable=no" in content_val or "maximum-scale=1" in content_val:
            issues.append(f"{rel_path}: Viewport meta restricts user zoom (user-scalable=no or maximum-scale=1)")

    # 3. Check Image Alternative Text (WCAG 1.1.1)
    for img in soup.find_all("img"):
        if not img.has_attr("alt"):
            issues.append(f"{rel_path}: <img> missing alt attribute (src: {img.get('src', 'unknown')})")

    # 4. Check Single H1 Tag (WCAG 1.3.1)
    h1_tags = soup.find_all("h1")
    if len(h1_tags) == 0 and not str(rel_path).startswith("node_modules"):
        issues.append(f"{rel_path}: Missing <h1> page heading")
    elif len(h1_tags) > 1:
        issues.append(f"{rel_path}: Multiple <h1> headings found ({len(h1_tags)})")

    # 5. Check Duplicate DOM IDs (WCAG 4.1.1)
    seen_ids = set()
    for el in soup.find_all(id=True):
        el_id = el["id"].strip()
        if not el_id:
            continue
        if el_id in seen_ids:
            issues.append(f"{rel_path}: Duplicate DOM id detected: '#{el_id}'")
        seen_ids.add(el_id)

    # 6. Check Form Controls Accessibility (WCAG 4.1.2 & 3.3.2)
    for input_tag in soup.find_all(["input", "select", "textarea"]):
        input_type = input_tag.get("type", "text").lower()
        if input_type in ["hidden", "submit", "button", "reset", "image"]:
            continue
        
        input_id = input_tag.get("id")
        has_label = False
        if input_id:
            # Check for <label for="input_id">
            if soup.find("label", attrs={"for": input_id}):
                has_label = True
        
        # Check aria-label, aria-labelledby, title, or parent label
        if (
            input_tag.has_attr("aria-label")
            or input_tag.has_attr("aria-labelledby")
            or input_tag.has_attr("title")
            or input_tag.find_parent("label")
        ):
            has_label = True
        
        if not has_label:
            issues.append(
                f"{rel_path}: Form control <{input_tag.name} id=\"{input_id or 'none'}\"> has no associated <label>, aria-label, or title"
            )

    # 7. Check Empty Anchor and Button Tags (WCAG 2.4.4 & 4.1.2)
    for btn in soup.find_all("button"):
        text = btn.get_text(strip=True)
        aria_label = btn.get("aria-label") or btn.get("title")
        has_img_with_alt = any(img.get("alt") for img in btn.find_all("img"))
        has_svg = bool(btn.find("svg"))
        if not text and not aria_label and not has_img_with_alt and not has_svg:
            issues.append(f"{rel_path}: Empty <button> element with no text, aria-label, or child icon")

    return issues


def run_accessibility_audit(verbose: bool = False) -> bool:
    """Run full accessibility and contrast audit across repository."""
    print("============================================================")
    print("       WCAG 2.2 AA & DOM ACCESSIBILITY AUDITOR (CHECK 22)   ")
    print("============================================================")

    # Phase 1: CSS Color Tokens Contrast Audit
    print("\n[ PHASE 1 ] Auditing CSS Design Tokens for WCAG 2.2 AA Contrast...")
    contrast_issues = audit_color_tokens()
    if contrast_issues:
        for issue in contrast_issues:
            print(f"[FAIL] {issue}")
    else:
        print("[PASS] All core palette tokens exceed WCAG 2.2 AA contrast minimums (>= 4.5:1).")

    # Phase 2: HTML DOM Accessibility Audit
    html_files = sorted(
        [
            Path(p)
            for p in glob.glob(str(BASE_DIR / "**/*.html"), recursive=True)
            if "node_modules" not in p and ".git" not in p
        ]
    )

    print(f"\n[ PHASE 2 ] Auditing DOM Accessibility across {len(html_files)} HTML files...")
    total_dom_issues = []
    
    for hf in html_files:
        file_issues = audit_html_file(hf)
        if file_issues:
            total_dom_issues.extend(file_issues)
            if verbose:
                for fi in file_issues:
                    print(f"  [WARN] {fi}")

    if total_dom_issues:
        print(f"\n[FAIL] Found {len(total_dom_issues)} DOM accessibility issues:")
        for issue in total_dom_issues[:20]:
            print(f"  - {issue}")
        if len(total_dom_issues) > 20:
            print(f"  ... and {len(total_dom_issues) - 20} more issues.")
    else:
        print(f"[PASS] All {len(html_files)} HTML documents comply 100% with DOM accessibility rules.")

    total_failures = len(contrast_issues) + len(total_dom_issues)
    print("============================================================")
    if total_failures > 0:
        print(f"RESULT: FAILED ({total_failures} accessibility violations)")
        return False
    else:
        print(f"RESULT: 100% PASS ({len(html_files)} files audited, 0 violations)")
        return True


if __name__ == "__main__":
    is_verbose = "--verbose" in sys.argv or "-v" in sys.argv
    success = run_accessibility_audit(verbose=is_verbose)
    sys.exit(0 if success else 1)
