#!/usr/bin/env python3
import os
import sys
import json
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MANIFEST_FILE = DATA_DIR / "social_cards_manifest.json"
OUTPUT_DIR = BASE_DIR / "assets" / "img" / "social-cards"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Font Resolver (Bundled Local Fonts First -> System Fallback)
def get_font(size=40, is_mono=False, is_bold=False):
    bundled_mono = str(BASE_DIR / "assets" / "fonts" / "ttf" / "JetBrainsMono-Regular.ttf")
    bundled_bold = str(BASE_DIR / "assets" / "fonts" / "ttf" / "DejaVuSans-Bold.ttf")
    bundled_sans = str(BASE_DIR / "assets" / "fonts" / "ttf" / "DejaVuSans-Regular.ttf")

    mono_fonts = [
        bundled_mono,
        "/usr/share/fonts/TTF/JetBrainsMonoNerdFontMono-Regular.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
        "/usr/share/fonts/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/noto/NotoSansMono-Regular.ttf"
    ]
    bold_fonts = [
        bundled_bold,
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/noto/NotoSans-Bold.ttf"
    ]
    sans_fonts = [
        bundled_sans,
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/noto/NotoSans-Regular.ttf"
    ]

    candidates = mono_fonts if is_mono else (bold_fonts if is_bold else sans_fonts)
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
    for line in raw_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        if bbox[2] - bbox[0] <= max_w:
            final_lines.append(line)
        else:
            words = line.split(' ')
            curr = ''
            for w in words:
                test = (curr + ' ' + w).strip() if curr else w
                if draw.textbbox((0, 0), test, font=font)[2] - draw.textbbox((0, 0), test, font=font)[0] <= max_w:
                    curr = test
                else:
                    if curr:
                        final_lines.append(curr)
                    curr = '    ' + w
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
        # 1:1 SQUARE INFOGRAPHIC LAYOUT (2400 x 2400)
        # =========================================================================
        title_font_size = 80 if len(raw_title) <= 55 else (70 if len(raw_title) <= 75 else 62)
        font_tag = get_font(size=44, is_mono=True, is_bold=True)
        font_title = get_font(size=title_font_size, is_mono=False, is_bold=True)
        font_desc = get_font(size=38, is_mono=False, is_bold=False)
        font_bar = get_font(size=34, is_mono=True, is_bold=True)
        font_code = get_font(size=33, is_mono=True, is_bold=False)
        font_pillar_head = get_font(size=36, is_mono=True, is_bold=True)
        font_pillar_body = get_font(size=32, is_mono=False, is_bold=False)
        font_meta = get_font(size=34, is_mono=True, is_bold=False)

        # 1. Category Tag
        draw.text((margin + 80, margin + 60), cat_tag, fill=text_muted, font=font_tag)

        # 2. Main Title (Max 3 Lines)
        title_lines = wrap_text(raw_title, font_title, inner_w, draw)[:3]
        curr_y = margin + 130
        line_h = int(title_font_size * 1.32)
        for line in title_lines:
            draw.text((margin + 80, curr_y), line, fill=text_main, font=font_title)
            curr_y += line_h

        # 3. Subtitle / Description (Max 2 Lines)
        desc_text = article_data.get('description', '')
        if desc_text:
            desc_lines = wrap_text(desc_text, font_desc, inner_w, draw)[:2]
            curr_y += 10
            for dl in desc_lines:
                draw.text((margin + 80, curr_y), dl, fill=text_muted, font=font_desc)
                curr_y += 52

        # 4. Terminal Architecture Window
        curr_y += 25
        box_h = 620
        draw.rectangle([margin + 80, curr_y, margin + 80 + inner_w, curr_y + box_h], fill=box_bg, outline=box_border, width=2)
        
        # Terminal Header Bar (76px height)
        bar_h = 76
        draw.rectangle([margin + 80, curr_y, margin + 80 + inner_w, curr_y + bar_h], fill=bar_bg, outline=box_border, width=2)
        
        # 3 Window Control Dots
        dot_y = curr_y + bar_h // 2
        draw.ellipse([margin + 115 - 8, dot_y - 8, margin + 115 + 8, dot_y + 8], fill=dot_red)
        draw.ellipse([margin + 142 - 8, dot_y - 8, margin + 142 + 8, dot_y + 8], fill=dot_yellow)
        draw.ellipse([margin + 169 - 8, dot_y - 8, margin + 169 + 8, dot_y + 8], fill=dot_green)

        # Bar Title (Strictly Centered Inside Bar)
        bar_title = "[ TERMINAL // SUBSYSTEM CONFIGURATION & ARCHITECTURE ]"
        t_bbox = draw.textbbox((0, 0), bar_title, font=font_bar)
        t_h = t_bbox[3] - t_bbox[1]
        bar_text_y = curr_y + (bar_h - t_h) // 2 - 2
        draw.text((margin + 210, bar_text_y), bar_title, fill=text_muted, font=font_bar)

        raw_code = article_data.get('code_snippet', [])
        wrapped_code = wrap_code_lines(raw_code, font_code, max_content_w, 9, draw)

        cy = curr_y + bar_h + 20
        for cl in wrapped_code:
            is_comment = cl.strip().startswith("//") or cl.strip().startswith("#") or cl.strip().startswith("*")
            c_color = text_muted if is_comment else text_main
            draw.text((margin + 110, cy), cl, fill=c_color, font=font_code)
            cy += 52

        # 5. Pillar 1: Architectural Guarantees (Fully Wrapped Bullets)
        curr_y += box_h + 30
        p1_h = 320
        draw.rectangle([margin + 80, curr_y, margin + 80 + inner_w, curr_y + p1_h], fill=card_color, outline=box_border, width=2)
        draw.text((margin + 110, curr_y + 22), "[ ARCHITECTURAL INVARIANTS & SECURITY GUARANTEES ]", fill=text_main, font=font_pillar_head)
        
        invariants = article_data.get('invariants', [])
        py = curr_y + 70
        for t in invariants[:3]:
            clean_t = t if t.startswith("[+]") else f"[+] {t}"
            wrapped_t = wrap_text(clean_t, font_pillar_body, max_content_w, draw)
            for tl in wrapped_t:
                draw.text((margin + 110, py), tl, fill=text_main, font=font_pillar_body)
                py += 46
            py += 6

        # 6. Pillar 2: Production Performance & Verification (Fully Wrapped Metrics)
        curr_y += p1_h + 20
        p2_h = 300
        draw.rectangle([margin + 80, curr_y, margin + 80 + inner_w, curr_y + p2_h], fill=card_color, outline=box_border, width=2)
        draw.text((margin + 110, curr_y + 22), "[ PRODUCTION OPERATIONAL METRICS & VERIFICATION ]", fill=text_main, font=font_pillar_head)
        
        metrics = article_data.get('metrics', [])
        py = curr_y + 70
        for m in metrics[:3]:
            clean_m = m if m.startswith("[*]") else f"[*] {m}"
            wrapped_m = wrap_text(clean_m, font_pillar_body, max_content_w, draw)
            for ml in wrapped_m:
                draw.text((margin + 110, py), ml, fill=text_main, font=font_pillar_body)
                py += 46
            py += 6

        # 7. Footer
        draw.text((margin + 80, height - margin - 55), "Ref: ZYEKH.COM / TECHNICAL BLUEPRINT SPECIFICATION • DECENTRALIZED SYNDICATION 2026", fill=text_muted, font=font_meta)

    else:
        # =========================================================================
        # 16:9 LANDSCAPE OPENGRAPH LAYOUT (2400 x 1260) — HIGH-DENSITY BLUEPRINT
        # =========================================================================
        title_font_size = 72 if len(raw_title) <= 55 else (64 if len(raw_title) <= 75 else 56)
        font_tag = get_font(size=42, is_mono=True, is_bold=True)
        font_title = get_font(size=title_font_size, is_mono=False, is_bold=True)
        font_desc = get_font(size=34, is_mono=False, is_bold=False)
        font_bar = get_font(size=32, is_mono=True, is_bold=True)
        font_code = get_font(size=30, is_mono=True, is_bold=False)
        font_mini_head = get_font(size=30, is_mono=True, is_bold=True)
        font_mini_body = get_font(size=27, is_mono=False, is_bold=False)
        font_meta = get_font(size=32, is_mono=True, is_bold=False)

        # 1. Category Tag
        draw.text((margin + 80, margin + 50), cat_tag, fill=text_muted, font=font_tag)

        # 2. Main Title (Max 2 lines in Landscape)
        title_lines = wrap_text(raw_title, font_title, inner_w, draw)[:2]
        curr_y = margin + 115
        line_h = int(title_font_size * 1.28)
        for line in title_lines:
            draw.text((margin + 80, curr_y), line, fill=text_main, font=font_title)
            curr_y += line_h

        # 3. Subtitle / Description (1-2 lines)
        desc_text = article_data.get('description', '')
        if desc_text:
            desc_lines = wrap_text(desc_text, font_desc, inner_w, draw)[:2]
            curr_y += 6
            for dl in desc_lines:
                draw.text((margin + 80, curr_y), dl, fill=text_muted, font=font_desc)
                curr_y += 46

        # 4. Terminal Box (Balanced Height)
        curr_y += 18
        raw_code = article_data.get('code_snippet', [])
        wrapped_code = wrap_code_lines(raw_code, font_code, max_content_w, 7, draw)
        
        box_h = 420
        draw.rectangle([margin + 80, curr_y, margin + 80 + inner_w, curr_y + box_h], fill=box_bg, outline=box_border, width=2)
        
        # Terminal Header Bar (68px height)
        bar_h = 68
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

        cy = curr_y + bar_h + 16
        for cl in wrapped_code:
            is_comment = cl.strip().startswith("//") or cl.strip().startswith("#") or cl.strip().startswith("*")
            c_color = text_muted if is_comment else text_main
            draw.text((margin + 110, cy), cl, fill=c_color, font=font_code)
            cy += 46

        # 5. Bottom 2-Column Matrix (Zero White Space / Zero Void)
        curr_y += box_h + 18
        bot_h = 165
        col_w = (inner_w - 30) // 2
        left_x = margin + 80
        right_x = left_x + col_w + 30

        # Left Column: Architectural Invariant
        draw.rectangle([left_x, curr_y, left_x + col_w, curr_y + bot_h], fill=box_bg, outline=box_border, width=2)
        draw.text((left_x + 25, curr_y + 18), "[ KEY ARCHITECTURAL INVARIANT ]", fill=text_main, font=font_mini_head)
        invariants = article_data.get('invariants', [])
        if invariants:
            inv_sample = invariants[0]
            clean_inv = inv_sample if inv_sample.startswith("[+]") else f"[+] {inv_sample}"
            wrapped_inv = wrap_text(clean_inv, font_mini_body, col_w - 50, draw)[:2]
            iy = curr_y + 58
            for il in wrapped_inv:
                draw.text((left_x + 25, iy), il, fill=text_muted, font=font_mini_body)
                iy += 38

        # Right Column: Production Operational Metric
        draw.rectangle([right_x, curr_y, right_x + col_w, curr_y + bot_h], fill=box_bg, outline=box_border, width=2)
        draw.text((right_x + 25, curr_y + 18), "[ PRODUCTION OPERATIONAL METRIC ]", fill=text_main, font=font_mini_head)
        metrics = article_data.get('metrics', [])
        if metrics:
            met_sample = metrics[1] if len(metrics) > 1 else metrics[0]
            clean_met = met_sample if met_sample.startswith("[*]") else f"[*] {met_sample}"
            wrapped_met = wrap_text(clean_met, font_mini_body, col_w - 50, draw)[:2]
            my = curr_y + 58
            for ml in wrapped_met:
                draw.text((right_x + 25, my), ml, fill=text_muted, font=font_mini_body)
                my += 38

        # 6. Footer
        draw.text((margin + 80, height - margin - 45), "Ref: ZYEKH.COM / TECHNICAL BLUEPRINT SPECIFICATION • DECENTRALIZED SYNDICATION 2026", fill=text_muted, font=font_meta)


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
