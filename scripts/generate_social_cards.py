#!/usr/bin/env python3
import os
import sys
import re
import json
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MANIFEST_FILE = DATA_DIR / "social_cards_manifest.json"
OUTPUT_DIR = BASE_DIR / "assets" / "img" / "social-cards"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Font Resolver (Authentic Zyekh.com Typography: Outfit, Inter, JetBrains Mono)
def get_font(size=40, family="sans", is_bold=False):
    ttf_dir = BASE_DIR / "assets" / "fonts" / "ttf"
    
    outfit_bold = str(ttf_dir / "Outfit-Bold.ttf")
    outfit_semibold = str(ttf_dir / "Outfit-SemiBold.ttf")
    inter_reg = str(ttf_dir / "Inter-Regular.ttf")
    inter_bold = str(ttf_dir / "Inter-Bold.ttf")
    mono_reg = str(ttf_dir / "JetBrainsMono-Regular.ttf")

    if family in ["title", "outfit"]:
        candidates = [outfit_bold, outfit_semibold]
    elif family in ["mono", "code"]:
        candidates = [mono_reg]
    else:  # family == "sans" / "inter"
        candidates = [inter_bold] if is_bold else [inter_reg]

    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()




def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        w = bbox[2] - bbox[0]
        if w <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines

def wrap_code_lines(raw_lines, font, max_w, max_total_lines, draw):
    final_lines = []
    
    def get_width(text):
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0]

    for line in raw_lines:
        if get_width(line) <= max_w:
            final_lines.append(line)
        else:
            raw_tokens = line.split(' ')
            tokens = []
            for t in raw_tokens:
                if not t:
                    tokens.append('')
                    continue
                if get_width(t) <= max_w:
                    tokens.append(t)
                else:
                    sub_parts = [p for p in re.split(r'([:;,/])', t) if p]
                    cur_part = ''
                    for p in sub_parts:
                        if get_width(cur_part + p) <= max_w:
                            cur_part += p
                        else:
                            if cur_part:
                                tokens.append(cur_part)
                            if get_width(p) > max_w:
                                for ch in p:
                                    if get_width(cur_part + ch) <= max_w:
                                        cur_part += ch
                                    else:
                                        if cur_part:
                                            tokens.append(cur_part)
                                        cur_part = ch
                            else:
                                cur_part = p
                    if cur_part:
                        tokens.append(cur_part)
            
            curr = ''
            for token in tokens:
                sep = ' ' if curr and not curr.endswith(' ') and token else ''
                test = curr + sep + token if curr else token
                if get_width(test) <= max_w:
                    curr = test
                else:
                    if curr:
                        final_lines.append(curr)
                    indent = '    ' if not token.startswith(' ') else ''
                    test_indented = indent + token
                    if get_width(test_indented) <= max_w:
                        curr = test_indented
                    else:
                        curr = token
            if curr:
                final_lines.append(curr)
        if len(final_lines) >= max_total_lines:
            break
    return final_lines[:max_total_lines]

def generate_social_card(article_data, output_path: Path, theme="dark", mode="landscape"):
    if mode == "square":
        width, height = 2400, 2400
    else:
        width, height = 2400, 1260

    # Theme Tokens
    if theme == "light":
        bg_color = (244, 244, 245)      # #f4f4f5 (Light Canvas)
        card_color = (255, 255, 255)    # #ffffff (Pure White Surface)
        border_color = (203, 213, 225)  # #cbd5e1 (Clean Slate Border)
        box_bg = (248, 250, 252)        # #f8fafc (Terminal/Box Light)
        bar_bg = (226, 232, 240)        # #e2e8f0 (Terminal Header Bar)
        box_border = (203, 213, 225)
        text_main = (15, 23, 42)        # #0f172a (Slate 900)
        text_muted = (100, 116, 139)    # #64748b (Slate 500)
        dot_red = (239, 68, 68)
        dot_yellow = (234, 179, 8)
        dot_green = (34, 197, 94)
    else:
        bg_color = (9, 9, 11)           # #09090b (Dark Canvas)
        card_color = (18, 18, 22)       # #121216 (Dark Surface)
        border_color = (39, 39, 42)     # #27272a (Border)
        box_bg = (0, 0, 0)              # #000000 (Terminal Box)
        bar_bg = (28, 28, 32)           # #1c1c20 (Terminal Header Bar)
        box_border = (45, 45, 50)       # #2d2d32
        text_main = (250, 250, 250)     # #fafafa (White)
        text_muted = (161, 161, 170)    # #a1a1aa (Muted Gray)
        dot_red = (239, 68, 68)
        dot_yellow = (234, 179, 8)
        dot_green = (34, 197, 94)

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    margin = 90 if mode == "square" else 80
    card_rect = [margin, margin, width - margin, height - margin]
    draw.rectangle(card_rect, fill=card_color, outline=border_color, width=4)

    raw_title = article_data['title']
    tags = article_data.get('tags', ['SECURITY'])
    tag_str = " • ".join([t.upper() for t in tags[:3]])
    cat_tag = f"[ {tag_str} ]" if tag_str else "[ TECHNICAL SPECIFICATION ]"

    inner_w = width - (margin * 2 + 160)
    max_content_w = inner_w - 60

    if mode == "square":

        # =========================================================================
        # 1:1 SQUARE INFOGRAPHIC LAYOUT (2400 x 2400) — STANDARD TYPOGRAPHY
        # =========================================================================
        title_font_size, title_line_h = 76, 100
        desc_font_size, desc_line_h = 38, 52
        code_font_size, code_line_h = 34, 48
        inv_font_size, inv_line_h = 34, 46
        met_font_size, met_line_h = 34, 46

        font_tag = get_font(size=42, family="mono", is_bold=False)
        font_title = get_font(size=title_font_size, family="outfit", is_bold=True)
        font_desc = get_font(size=desc_font_size, family="sans", is_bold=False)
        font_bar = get_font(size=34, family="mono", is_bold=False)
        font_code = get_font(size=code_font_size, family="mono", is_bold=False)
        font_pillar_head = get_font(size=34, family="mono", is_bold=False)
        font_inv_body = get_font(size=inv_font_size, family="sans", is_bold=False)
        font_met_body = get_font(size=met_font_size, family="sans", is_bold=False)
        font_meta = get_font(size=34, family="mono", is_bold=False)

        raw_code = article_data.get('code_snippet', [])
        invariants = article_data.get('invariants', [])[:3]
        metrics = article_data.get('metrics', [])[:3]

        # --- DRAWING PASS ---
        # A. Category Tag
        draw.text((margin + 80, margin + 55), cat_tag, fill=text_muted, font=font_tag)

        # B. Main Title
        title_lines = wrap_text(raw_title, font_title, inner_w, draw)[:3]
        curr_y = margin + 125
        for line in title_lines:
            draw.text((margin + 80, curr_y), line, fill=text_main, font=font_title)
            curr_y += title_line_h

        # C. Subtitle / Description
        desc_text = article_data.get('description', '')
        if desc_text:
            desc_lines = wrap_text(desc_text, font_desc, inner_w, draw)[:2]
            curr_y += 8
            for dl in desc_lines:
                draw.text((margin + 80, curr_y), dl, fill=text_muted, font=font_desc)
                curr_y += desc_line_h

        # --- DYNAMIC CONTENT-DRIVEN BOX HEIGHTS ---
        # 1. Pre-calculate wrapped content
        wrapped_code = wrap_code_lines(raw_code, font_code, max_content_w, 9, draw)
        inv_wrapped_list = [wrap_text(t if t.startswith("[+]") else f"[+] {t}", font_inv_body, max_content_w, draw) for t in invariants]
        met_wrapped_list = [wrap_text(m if m.startswith("[*]") else f"[*] {m}", font_met_body, max_content_w, draw) for m in metrics]

        total_inv_lines = sum(len(lines) for lines in inv_wrapped_list)
        total_met_lines = sum(len(lines) for lines in met_wrapped_list)

        bar_h = 76
        box_h = bar_h + 20 + (len(wrapped_code) * code_line_h) + 20
        p1_h = 68 + (total_inv_lines * inv_line_h) + (len(invariants) * 8) + 18
        p2_h = 68 + (total_met_lines * met_line_h) + (len(metrics) * 8) + 18

        gap_between_boxes = 24



        # D. Terminal Architecture Window
        curr_y += 20
        draw.rectangle([margin + 80, curr_y, margin + 80 + inner_w, curr_y + box_h], fill=box_bg, outline=box_border, width=2)
        draw.rectangle([margin + 80, curr_y, margin + 80 + inner_w, curr_y + bar_h], fill=bar_bg, outline=box_border, width=2)

        # Control Dots
        dot_y = curr_y + bar_h // 2
        draw.ellipse([margin + 115 - 8, dot_y - 8, margin + 115 + 8, dot_y + 8], fill=dot_red)
        draw.ellipse([margin + 142 - 8, dot_y - 8, margin + 142 + 8, dot_y + 8], fill=dot_yellow)
        draw.ellipse([margin + 169 - 8, dot_y - 8, margin + 169 + 8, dot_y + 8], fill=dot_green)

        # Bar Title
        bar_title = "[ TERMINAL // SUBSYSTEM CONFIGURATION & ARCHITECTURE ]"
        t_bbox = draw.textbbox((0, 0), bar_title, font=font_bar)
        t_h = t_bbox[3] - t_bbox[1]
        bar_text_y = curr_y + (bar_h - t_h) // 2 - 2
        draw.text((margin + 210, bar_text_y), bar_title, fill=text_muted, font=font_bar)

        cy = curr_y + bar_h + 20
        for cl in wrapped_code:
            is_comment = cl.strip().startswith("//") or cl.strip().startswith("#") or cl.strip().startswith("*")
            c_color = text_muted if is_comment else text_main
            draw.text((margin + 110, cy), cl, fill=c_color, font=font_code)
            cy += code_line_h

        # E. Pillar 1: Architectural Guarantees
        curr_y += box_h + gap_between_boxes
        draw.rectangle([margin + 80, curr_y, margin + 80 + inner_w, curr_y + p1_h], fill=card_color, outline=box_border, width=2)
        draw.text((margin + 110, curr_y + 22), "[ ARCHITECTURAL INVARIANTS & SECURITY GUARANTEES ]", fill=text_main, font=font_pillar_head)
        
        py = curr_y + 70
        for wrapped_t in inv_wrapped_list:
            for tl in wrapped_t:
                draw.text((margin + 110, py), tl, fill=text_main, font=font_inv_body)
                py += inv_line_h
            py += 8

        # F. Pillar 2: Production Performance & Verification
        curr_y += p1_h + gap_between_boxes
        draw.rectangle([margin + 80, curr_y, margin + 80 + inner_w, curr_y + p2_h], fill=card_color, outline=box_border, width=2)
        draw.text((margin + 110, curr_y + 22), "[ PRODUCTION OPERATIONAL METRICS & VERIFICATION ]", fill=text_main, font=font_pillar_head)
        
        py = curr_y + 70
        for wrapped_m in met_wrapped_list:
            for ml in wrapped_m:
                draw.text((margin + 110, py), ml, fill=text_main, font=font_met_body)
                py += met_line_h
            py += 8

        # G. Cohesive Footer (Directly below Pillar 2)
        footer_y = curr_y + p2_h + 40
        if footer_y + 40 <= height - margin:
            draw.text((margin + 80, footer_y), "OPEN TECHNICAL ARCHITECTURE SPECIFICATION • SYSTEMS & SECURITY BLUEPRINT 2026", fill=text_muted, font=font_meta)



    else:
        # =========================================================================
        # 16:9 LANDSCAPE OPENGRAPH LAYOUT (2400 x 1260) — STANDARD TYPOGRAPHY
        # =========================================================================
        title_font_size, title_line_h = 60, 76
        desc_font_size, desc_line_h = 30, 42
        code_font_size, code_lh = 30, 38

        font_tag = get_font(size=38, family="mono", is_bold=False)
        font_title = get_font(size=title_font_size, family="outfit", is_bold=True)
        font_desc = get_font(size=desc_font_size, family="sans", is_bold=False)
        font_bar = get_font(size=30, family="mono", is_bold=False)
        font_code = get_font(size=code_font_size, family="mono", is_bold=False)
        font_matrix_head = get_font(size=25, family="mono", is_bold=False)
        font_matrix_body = get_font(size=22, family="sans", is_bold=False)
        font_meta = get_font(size=32, family="mono", is_bold=False)

        raw_code = article_data.get('code_snippet', [])
        desc_text = article_data.get('description', '')

        # 1. Category Tag
        draw.text((margin + 80, margin + 45), cat_tag, fill=text_muted, font=font_tag)

        # 2. Main Title (Max 2 lines in Landscape)
        title_lines = wrap_text(raw_title, font_title, inner_w, draw)[:2]
        curr_y = margin + 105
        for line in title_lines:
            draw.text((margin + 80, curr_y), line, fill=text_main, font=font_title)
            curr_y += title_line_h

        # 3. Subtitle / Description (1-2 lines)
        if desc_text:
            desc_lines = wrap_text(desc_text, font_desc, inner_w, draw)[:2]
            curr_y += 6
            for dl in desc_lines:
                draw.text((margin + 80, curr_y), dl, fill=text_muted, font=font_desc)
                curr_y += desc_line_h

        # 4. Terminal Box (Dynamic Tight Height)
        curr_y += 14
        wrapped_code = wrap_code_lines(raw_code, font_code, max_content_w, 7, draw)
        
        bar_h = 56
        box_h = bar_h + 14 + (len(wrapped_code) * code_lh) + 14
        draw.rectangle([margin + 80, curr_y, margin + 80 + inner_w, curr_y + box_h], fill=box_bg, outline=box_border, width=2)
        draw.rectangle([margin + 80, curr_y, margin + 80 + inner_w, curr_y + bar_h], fill=bar_bg, outline=box_border, width=2)
        
        # 3 Window Control Dots
        dot_y = curr_y + bar_h // 2
        draw.ellipse([margin + 110 - 7, dot_y - 7, margin + 110 + 7, dot_y + 7], fill=dot_red)
        draw.ellipse([margin + 135 - 7, dot_y - 7, margin + 135 + 7, dot_y + 7], fill=dot_yellow)
        draw.ellipse([margin + 160 - 7, dot_y - 7, margin + 160 + 7, dot_y + 7], fill=dot_green)

        # Bar Title (Strictly Centered Inside Bar)
        bar_title = "[ TERMINAL // CONFIGURATION & CODE SPECIFICATION ]"
        t_bbox = draw.textbbox((0, 0), bar_title, font=font_bar)
        t_h = t_bbox[3] - t_bbox[1]
        bar_text_y = curr_y + (bar_h - t_h) // 2 - 2
        draw.text((margin + 200, bar_text_y), bar_title, fill=text_muted, font=font_bar)

        cy = curr_y + bar_h + 14
        for cl in wrapped_code:
            is_comment = cl.strip().startswith("//") or cl.strip().startswith("#") or cl.strip().startswith("*")
            c_color = text_muted if is_comment else text_main
            draw.text((margin + 110, cy), cl, fill=c_color, font=font_code)
            cy += code_lh

        # 5. Bottom 2-Column Matrix (Full Parity: Dynamic Tight Box Height)
        curr_y += box_h + 14
        col_w = (inner_w - 30) // 2
        left_x = margin + 80
        right_x = left_x + col_w + 30
        matrix_lh = 28

        # Pre-wrap to calculate exact content height without awkward inner space
        invariants = article_data.get('invariants', [])[:3]
        metrics = article_data.get('metrics', [])[:3]

        wrapped_invs = [wrap_text(inv if inv.startswith("[+]") else f"[+] {inv}", font_matrix_body, col_w - 44, draw) for inv in invariants]
        wrapped_mets = [wrap_text(met if met.startswith("[*]") else f"[*] {met}", font_matrix_body, col_w - 44, draw) for met in metrics]

        total_inv_lines = sum(len(w) for w in wrapped_invs)
        total_met_lines = sum(len(w) for w in wrapped_mets)
        max_lines = max(total_inv_lines, total_met_lines)

        # Dynamic box height: header + content lines + item gaps + bottom padding
        bot_h = 48 + (max_lines * matrix_lh) + (max(len(invariants), len(metrics)) * 6) + 14

        # Left Column: All Architectural Invariants
        draw.rectangle([left_x, curr_y, left_x + col_w, curr_y + bot_h], fill=box_bg, outline=box_border, width=2)
        draw.text((left_x + 22, curr_y + 14), "[ ARCHITECTURAL INVARIANTS & SECURITY GUARANTEES ]", fill=text_main, font=font_matrix_head)
        iy = curr_y + 48
        for w_inv in wrapped_invs:
            for il in w_inv:
                draw.text((left_x + 22, iy), il, fill=text_main, font=font_matrix_body)
                iy += matrix_lh
            iy += 6

        # Right Column: All Production Operational Metrics
        draw.rectangle([right_x, curr_y, right_x + col_w, curr_y + bot_h], fill=box_bg, outline=box_border, width=2)
        draw.text((right_x + 22, curr_y + 14), "[ PRODUCTION OPERATIONAL METRICS & VERIFICATION ]", fill=text_main, font=font_matrix_head)
        my = curr_y + 48
        for w_met in wrapped_mets:
            for ml in w_met:
                draw.text((right_x + 22, my), ml, fill=text_main, font=font_matrix_body)
                my += matrix_lh
            my += 6

        # 6. Collision-Free Footer (Only rendered if there is ample vertical breathing room)
        footer_y = height - margin - 50
        if curr_y + bot_h + 20 <= footer_y:
            draw.text((margin + 80, footer_y), "OPEN TECHNICAL ARCHITECTURE SPECIFICATION • SYSTEMS & SECURITY BLUEPRINT 2026", fill=text_muted, font=font_meta)




    # Save with File Size Optimization (< 950KB for API limit)

    img.save(output_path, "PNG", optimize=True)
    file_size_kb = output_path.stat().st_size / 1024
    if file_size_kb > 950:
        q_img = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
        q_img.save(output_path, "PNG", optimize=True)
        file_size_kb = output_path.stat().st_size / 1024

    print(f"[ SUCCESS ] {theme.upper()} {mode.upper()} Social Card Generated ({file_size_kb:.1f} KB): {output_path.name}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Zyekh.com Manifest-Driven Social Share Card Compiler")
    parser.add_argument("--latest", action="store_true", help="Generate cards for the latest blog article")
    parser.add_argument("--all", action="store_true", help="Generate cards for all blog articles")
    parser.add_argument("--slug", type=str, help="Generate cards for a specific article slug")
    args = parser.parse_args()

    if not MANIFEST_FILE.exists():
        print(f"[ ERROR ] Manifest file not found: {MANIFEST_FILE}. Run scripts/extract_card_manifest.py first.")
        sys.exit(1)

    manifest = json.loads(MANIFEST_FILE.read_text(encoding='utf-8'))
    print(f"[ MANIFEST-DRIVEN COMPILER ] Loaded {len(manifest)} articles from manifest.")

    targets = []
    if args.slug:
        if args.slug in manifest:
            targets.append(manifest[args.slug])
        else:
            print(f"[ ERROR ] Slug '{args.slug}' not found in manifest.")
            sys.exit(1)
    elif args.all:
        targets = list(manifest.values())
    else:
        # Default: pick first entry
        targets = [list(manifest.values())[0]]

    print(f"[ COMPILER ] Compiling {len(targets)} articles into social share cards...")
    for data in targets:
        # 1. Dark Landscape (2400x1260) -> For OpenGraph & Mastodon
        out_dark_land = OUTPUT_DIR / f"{data['slug']}-dark-landscape.png"
        generate_social_card(data, out_dark_land, theme="dark", mode="landscape")
        
        # 2. Light Square (2400x2400) -> For Bluesky Mobile Feed Breakout
        out_light_sq = OUTPUT_DIR / f"{data['slug']}-light-square.png"
        generate_social_card(data, out_light_sq, theme="light", mode="square")

if __name__ == "__main__":
    main()
