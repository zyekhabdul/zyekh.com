#!/usr/bin/env python3
import os
import sys
import re
import html
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = Path(__file__).resolve().parent.parent
BLOG_DIR = BASE_DIR / "blog"
OUTPUT_DIR = BASE_DIR / "assets" / "img" / "social-cards"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Font Resolver
def get_font(size=40, is_mono=False, is_bold=False):
    mono_fonts = [
        "/usr/share/fonts/TTF/JetBrainsMonoNerdFontMono-Regular.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
        "/usr/share/fonts/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/noto/NotoSansMono-Regular.ttf"
    ]
    bold_fonts = [
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/noto/NotoSans-Bold.ttf"
    ]
    sans_fonts = [
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

def determine_category_standard(title, tags, content):
    lower_content = (title + " " + " ".join(tags) + " " + content[:1000]).lower()
    
    if any(k in lower_content for k in ['ebpf', 'xdp', 'network', 'wireguard', 'vpn', 'quic', 'http3', 'cilium']):
        return "B" # Standar B: Network System Flow
    elif any(k in lower_content for k in ['llm', 'vllm', 'dspy', 'kv cache', 'colbert', 'rag', 'moe', 'webgpu']):
        return "C" # Standar C: AI LLM Benchmark Table
    elif any(k in lower_content for k in ['tool', 'utility', 'calculator', 'chmod', 'subnet', 'jwt']):
        return "D" # Standar D: Utility Matrix
    else:
        return "A" # Standar A: Kernel Config Matrix

def generate_social_card(article_data, output_path: Path, theme="dark", mode="landscape"):
    # Dimensions based on mode
    if mode == "square":
        width, height = 2400, 2400
    else:
        width, height = 2400, 1260

    # Theme Tokens
    if theme == "light":
        bg_color = (244, 244, 245)    # #f4f4f5 (Light Main)
        card_color = (255, 255, 255)  # #ffffff (Pure White Card)
        border_color = (212, 212, 216)# #d4d4d8 (Clean Border)
        box_bg = (244, 244, 245)      # #f4f4f5 (Code Box)
        box_border = (212, 212, 216)  # #d4d4d8
        text_main = (9, 9, 11)        # #09090b (Deep Black)
        text_muted = (82, 82, 91)     # #52525b (Dark Gray)
    else:
        bg_color = (9, 9, 11)          # #09090b (Dark Main)
        card_color = (20, 20, 23)      # #141417 (Dark Surface)
        border_color = (39, 39, 42)    # #27272a (Border)
        box_bg = (0, 0, 0)             # #000000 (Code Box)
        box_border = (39, 39, 42)
        text_main = (250, 250, 250)    # #fafafa (White)
        text_muted = (161, 161, 170)   # #a1a1aa (Muted Gray)

    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Outer Card Container (Margin 80px)
    margin = 80
    card_rect = [margin, margin, width - margin, height - margin]
    draw.rectangle(card_rect, fill=card_color, outline=border_color, width=4)

    # Dynamic Title Font Auto-Scaling
    raw_title = article_data['title']
    title_font_size = 64
    if len(raw_title) > 65:
        title_font_size = 50
    elif len(raw_title) > 50:
        title_font_size = 56

    font_tag = get_font(size=36, is_mono=True, is_bold=True)
    font_title = get_font(size=title_font_size, is_mono=False, is_bold=True)
    font_body = get_font(size=40, is_mono=False, is_bold=False)
    font_code = get_font(size=34, is_mono=True, is_bold=False)
    font_meta = get_font(size=32, is_mono=True, is_bold=False)

    tags = article_data.get('tags', ['SECURITY'])
    cat_tag = f"[ {tags[0].upper()} HARDENING ]" if tags else "[ TECHNICAL SPECIFICATION ]"
    
    # 1. Top Category Tag
    draw.text((margin + 70, margin + 70), cat_tag, fill=text_muted, font=font_tag)

    # 2. Main Title (Wrapped max 3 lines)
    title_lines = wrap_text(raw_title, font_title, width - (margin * 2 + 140), draw)
    title_lines = title_lines[:3]
    
    curr_y = margin + 140
    line_h = int(title_font_size * 1.35)
    for line in title_lines:
        draw.text((margin + 70, curr_y), line, fill=text_main, font=font_title)
        curr_y += line_h

    # Determine Standard Layout
    standard = article_data.get('standard') or determine_category_standard(
        article_data['title'], article_data.get('tags', []), article_data.get('body', '')
    )

    curr_y += 30
    inner_w = width - (margin * 2 + 140)

    if standard == "A":
        # Standar A: Kernel Config Matrix
        box_h = 340 if mode == "square" else 300
        box_rect = [margin + 70, curr_y, margin + 70 + inner_w, curr_y + box_h]
        draw.rectangle(box_rect, fill=box_bg, outline=box_border, width=2)
        
        code_lines = [
            "# Kernel Syscall & Sandbox Configuration",
            "ProtectSystem=strict          # Mount /usr, /boot, /etc read-only",
            "ProtectHome=true              # Deny access to /home, /root, /run/user",
            "MemoryDenyWriteExecute=true   # Enforce W^X memory allocation policy"
        ]
        cy = curr_y + 30
        for cl in code_lines:
            c_color = text_muted if cl.startswith("#") else text_main
            draw.text((margin + 100, cy), cl, fill=c_color, font=font_code)
            cy += 64

        curr_y += box_h + 40
        draw.text((margin + 70, curr_y), "Impact: Zero-Trust Process Sandboxing & Syscall Isolation at Kernel Level", fill=text_muted, font=font_body)

    elif standard == "B":
        # Standar B: Network Flow Diagram
        box_h = 340 if mode == "square" else 300
        box_rect = [margin + 70, curr_y, margin + 70 + inner_w, curr_y + box_h]
        draw.rectangle(box_rect, fill=box_bg, outline=box_border, width=2)

        flow_lines = [
            "+-------------------+       +--------------------+       +--------------------+",
            "|  NIC Driver (RX)  | ----> | eBPF XDP Program   | ----> | XDP_DROP (Dropped) |",
            "+-------------------+       +--------------------+       +--------------------+",
            "                                      | (XDP_PASS) -> Linux TCP/IP Stack       "
        ]
        cy = curr_y + 30
        for fl in flow_lines:
            draw.text((margin + 100, cy), fl, fill=text_main, font=font_code)
            cy += 64

        curr_y += box_h + 40
        draw.text((margin + 70, curr_y), "Performance: Line-Rate Packet Filtering with Zero CPU Stack Overhead", fill=text_muted, font=font_body)

    elif standard == "C":
        # Standar C: AI/LLM Benchmark Table
        box_h = 340 if mode == "square" else 300
        box_rect = [margin + 70, curr_y, margin + 70 + inner_w, curr_y + box_h]
        draw.rectangle(box_rect, fill=box_bg, outline=box_border, width=2)

        tbl_lines = [
            "Engine / Strategy        | KV Waste (%) | Max Sequences | Throughput",
            "-------------------------+--------------+---------------+-----------",
            "Standard HuggingFace     | 60%-80%      | 16 seq        | 1.0x      ",
            "vLLM PagedAttention      | < 4%         | 64 seq        | 3.8x Speed"
        ]
        cy = curr_y + 30
        for tl in tbl_lines:
            c_color = text_muted if "Engine" in tl or "---" in tl else text_main
            draw.text((margin + 100, cy), tl, fill=c_color, font=font_code)
            cy += 64

        curr_y += box_h + 40
        draw.text((margin + 70, curr_y), "Key Innovation: Virtual Memory Paging Eliminates Memory Fragmentation", fill=text_muted, font=font_body)

    else:
        # Standar D: Utility Transformation Matrix
        box_h = 340 if mode == "square" else 300
        box_rect = [margin + 70, curr_y, margin + 70 + inner_w, curr_y + box_h]
        draw.rectangle(box_rect, fill=box_bg, outline=box_border, width=2)

        util_lines = [
            "Input Mode  : Octal Notation 4755 (SUID Bit Active)",
            "Binary Mask : 100 111 101 101",
            "Symbolic    : -rwsr-xr-x",
            "Execution   : Executed with file owner (root) effective privilege"
        ]
        cy = curr_y + 30
        for ul in util_lines:
            draw.text((margin + 100, cy), ul, fill=text_main, font=font_code)
            cy += 64

        curr_y += box_h + 40
        draw.text((margin + 70, curr_y), "Transformation Matrix: Local Cryptographic & Octal Permission Evaluation", fill=text_muted, font=font_body)

    # Footer Specification Line (No Brand Logo / No Ad Signal)
    draw.text((margin + 70, height - margin - 70), "Ref: High-Density Technical Reference Specification", fill=text_muted, font=font_meta)

    # Save with File Size Optimization Guard (< 950KB for Bluesky API limit)
    img.save(output_path, "PNG", optimize=True)
    
    file_size_kb = output_path.stat().st_size / 1024
    if file_size_kb > 950:
        # Quantize palette if exceeding 950KB
        q_img = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
        q_img.save(output_path, "PNG", optimize=True)
        file_size_kb = output_path.stat().st_size / 1024

    print(f"[ SUCCESS ] {theme.upper()} {mode.upper()} Social Card Generated ({standard}, {file_size_kb:.1f} KB): {output_path.name}")
    return output_path

def parse_html_for_card(filepath: Path):
    content = filepath.read_text(encoding='utf-8')
    
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    title = html.unescape(title_match.group(1).strip()) if title_match else filepath.name
    title = re.sub(r'\s*—\s*zyekh\.com.*', '', title)
    title = re.sub(r'\s*\|\s*zyekh\.com.*', '', title)

    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE | re.DOTALL)
    description = html.unescape(desc_match.group(1).strip()) if desc_match else ""

    tags = []
    tag_matches = re.findall(r'<span\s+class=["\']meta-tag["\']>\s*#?([\w-]+)\s*</span>', content, re.IGNORECASE)
    if tag_matches:
        for t in tag_matches:
            clean_t = t.lower().strip()
            if clean_t and clean_t not in tags:
                tags.append(clean_t)

    return {
        'title': title,
        'description': description,
        'tags': tags or ['security'],
        'body': content[:1500],
        'slug': filepath.stem
    }

def main():
    parser = argparse.ArgumentParser(description="Zyekh.com Dual-Theme & Multi-Ratio Social Share Card Generator")
    parser.add_argument("--latest", action="store_true", help="Generate cards for the latest blog article")
    parser.add_argument("--all", action="store_true", help="Generate cards for all blog articles")
    parser.add_argument("--slug", type=str, help="Generate cards for a specific article slug")
    args = parser.parse_args()

    articles = sorted(BLOG_DIR.glob("*.html"))
    articles = [a for a in articles if a.name != "index.html"]

    if not articles:
        print("[ WARN ] No blog articles found.")
        sys.exit(1)

    targets = []
    if args.slug:
        for a in articles:
            if args.slug in a.name:
                targets.append(a)
                break
    elif args.all:
        targets = articles
    else:
        articles_by_mtime = sorted(articles, key=lambda x: x.stat().st_mtime, reverse=True)
        targets = [articles_by_mtime[0]]

    print(f"[ BATCH DUAL-THEME MULTI-RATIO ] Processing {len(targets)} articles...")
    for a in targets:
        data = parse_html_for_card(a)
        
        # 1. Dark Landscape (2400x1260) -> For OpenGraph & Mastodon
        out_dark_land = OUTPUT_DIR / f"{data['slug']}-dark-landscape.png"
        generate_social_card(data, out_dark_land, theme="dark", mode="landscape")
        
        # 2. Light Square (2400x2400) -> For Bluesky Mobile Feed Breakout
        out_light_sq = OUTPUT_DIR / f"{data['slug']}-light-square.png"
        generate_social_card(data, out_light_sq, theme="light", mode="square")

if __name__ == "__main__":
    main()
