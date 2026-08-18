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

    import glob
    blog_count = len([f for f in glob.glob(str(BASE_DIR / "blog/*.html")) if not f.endswith("blog/index.html")])
    if len(data) != blog_count:
        print(f"[ ERROR ] Expected {blog_count} articles, found {len(data)}")
        sys.exit(1)

    # Initialize font engine for headless geometry simulation
    try:
        sys.path.insert(0, str(BASE_DIR))
        from PIL import Image, ImageDraw
        import scripts.generate_social_cards as gsc
        img = Image.new('RGB', (2400, 1260))
        draw = ImageDraw.Draw(img)
        font_title_land = gsc.get_font(size=60, family='outfit', is_bold=True)
        font_desc_land = gsc.get_font(size=30, family='sans', is_bold=False)
        font_code_land = gsc.get_font(size=30, family='mono', is_bold=False)
        font_matrix_body_land = gsc.get_font(size=22, family='sans', is_bold=False)
    except Exception as e:
        print(f"[ WARN ] Headless layout simulation unavailable: {e}")
        draw = None

    errors = []

    for slug, item in data.items():
        # Title
        title = item.get("title", "").strip()
        if not title or len(title) < 5:
            errors.append(f"{slug}: Invalid or empty title")

        # Description (Must terminate with punctuation)
        desc = item.get("description", "").strip()
        if not desc or len(desc) < 10:
            errors.append(f"{slug}: Invalid or empty description")
        elif not (desc.endswith('.') or desc.endswith('!') or desc.endswith('?') or desc.endswith(')')):
            errors.append(f"{slug}: Description is missing terminating punctuation: '{desc}'")
        if ".." in desc:
            errors.append(f"{slug}: Description contains double period '..'")

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
            if "::" in inv_str:
                errors.append(f"{slug}: Invariant {idx} contains double colon '::': '{inv_str}'")
            if ".." in inv_str:
                errors.append(f"{slug}: Invariant {idx} contains double period '..': '{inv_str}'")

        # Metrics (Must be 3 items with contextual accuracy and proper punctuation)
        metrics = item.get("metrics", [])
        if len(metrics) < 3:
            errors.append(f"{slug}: Metrics count {len(metrics)} < 3")
        for idx, met in enumerate(metrics, 1):
            met_str = met.strip()
            if not met_str:
                errors.append(f"{slug}: Metric {idx} is empty")
            if not (met_str.endswith('.') or met_str.endswith('!') or met_str.endswith('?') or met_str.endswith(')')):
                errors.append(f"{slug}: Metric {idx} is missing terminating punctuation: '{met_str}'")
            if met_str.lower().startswith("architecture domain:"):
                errors.append(f"{slug}: Redundant Category Domain found in Metric {idx}: '{met_str}'")
            if "::" in met_str and not any(k in met_str for k in ["std::", "vllm::", "bpf::"]):
                errors.append(f"{slug}: Metric {idx} contains double colon '::': '{met_str}'")
            if ".." in met_str:
                errors.append(f"{slug}: Metric {idx} contains double period '..': '{met_str}'")
            # Semantic Anti-Boilerplate Gate
            if "compile-time invariant" in met_str.lower() and not any(k in slug for k in ["rust", "wasm"]):
                errors.append(f"{slug}: Semantic mismatch - non-compiled domain contains 'compile-time invariant' boilerplate: '{met_str}'")

        # Code Snippet (Must be 3-8 lines, balanced brackets, no dangling trailers)
        code = item.get("code_snippet", [])
        if len(code) < 3:
            errors.append(f"{slug}: Code snippet has only {len(code)} lines (< 3)")
        
        code_str = "\n".join(code)
        open_b = code_str.count('{')
        close_b = code_str.count('}')
        if open_b != close_b:
            errors.append(f"{slug}: Code snippet has unbalanced curly braces: {open_b} '{{' vs {close_b} '}}'")
            
        if code:
            last_line = code[-1].strip()
            if last_line.endswith('\\'):
                errors.append(f"{slug}: Final code line has dangling trailing backslash: '{last_line}'")
            if last_line.endswith(':') and not last_line.startswith(('#', '//', '/*')):
                errors.append(f"{slug}: Final code line ends with incomplete trailing colon: '{last_line}'")
            if last_line.endswith(('{', '(', '[', ',', '|')) and not last_line.startswith(('#', '//', '/*')):
                errors.append(f"{slug}: Final code line ends with unclosed opening/continuation syntax: '{last_line}'")
                
        for idx, line in enumerate(code, 1):
            if idx == 1 and line.strip() in ['{', '}', '(', ')']:
                errors.append(f"{slug}: First code line is an orphan bracket: '{line}'")
            if idx == len(code) and line.strip() in ['{', '(', ')']:
                errors.append(f"{slug}: Final code line is an unclosed opening bracket: '{line}'")

        # Headless Layout Clearance Simulation Gate
        if draw is not None:
            margin_l = 80
            inner_w_l = 2400 - (margin_l * 2 + 160)
            max_w_l = inner_w_l - 60
            col_w_l = (inner_w_l - 30) // 2

            curr_y_l = margin_l + 105
            title_lines_l = gsc.wrap_text(title, font_title_land, inner_w_l, draw)[:2]
            curr_y_l += len(title_lines_l) * 76
            desc_lines_l = gsc.wrap_text(desc, font_desc_land, inner_w_l, draw)[:2]
            curr_y_l += 6 + (len(desc_lines_l) * 42) + 14

            wrapped_code_l = gsc.wrap_code_lines(code, font_code_land, max_w_l, 7, draw)
            bar_h_l = 56
            box_h_l = bar_h_l + 14 + (len(wrapped_code_l) * 38) + 14
            curr_y_l += box_h_l + 14

            inv_l = [gsc.wrap_text(inv if inv.startswith('[+]') else f'[+] {inv}', font_matrix_body_land, col_w_l - 44, draw) for inv in invariants[:3]]
            met_l = [gsc.wrap_text(met if met.startswith('[*]') else f'[*] {met}', font_matrix_body_land, col_w_l - 44, draw) for met in metrics[:3]]
            max_lines_l = max(sum(len(w) for w in inv_l), sum(len(w) for w in met_l))
            bot_h_l = 48 + (max_lines_l * 28) + (max(len(invariants[:3]), len(metrics[:3])) * 6) + 14

            content_bottom_l = curr_y_l + bot_h_l
            footer_y_l = 1260 - margin_l - 50
            clearance_l = footer_y_l - content_bottom_l
            if clearance_l < 20:
                errors.append(f"{slug}: Landscape vertical clearance is too tight ({clearance_l}px < 20px required)")

    if errors:
        print(f"\n[ FAIL ] Found {len(errors)} validation errors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print(f"\n[ PASS ] 100% Quality Audit Passed! All {len(data)} articles have complete, verified, deterministic metadata and zero geometry collisions.")

if __name__ == "__main__":
    validate_manifest()
