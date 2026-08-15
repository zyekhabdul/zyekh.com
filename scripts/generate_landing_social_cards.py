#!/usr/bin/env python3
"""
Landing & Root Pages High-Resolution Social Cards Compiler
Renders 2400x1260 Dark Landscape cards for root pages:
- Home (/)
- About (/about/)
- Contact (/contact/)
- Links (/links/)
- Tools Hub (/tools/)
"""
import os
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "assets" / "img" / "social-cards"
FONTS_DIR = BASE_DIR / "assets" / "fonts" / "ttf"

FONT_OUTFIT_BOLD = str(FONTS_DIR / "Outfit-Bold.ttf")
FONT_INTER_REGULAR = str(FONTS_DIR / "Inter-Regular.ttf")
FONT_INTER_BOLD = str(FONTS_DIR / "Inter-Bold.ttf")
FONT_MONO_REGULAR = str(FONTS_DIR / "JetBrainsMono-Regular.ttf")

LANDING_PAGES = {
    "page-home": {
        "tag": "[ PORTAL HUB • SYSTEMS & SECURITY ]",
        "title": "zyekh.com — Systems, Security & AI Engineering",
        "description": "High-performance technical research portal, Linux kernel hardening blueprints, DFIR playbooks, and 46 privacy-first web utilities.",
        "box1_title": "[ CORE ENGINEERING DOMAINS ]",
        "box1_items": [
            ("Linux Kernel Hardening", "eBPF syscall telemetry, LSM Landlock, seccomp filters, and memory-safe abstractions."),
            ("AI Systems Infrastructure", "KV-cache INT4 quantization, S-LoRA multiplexing, and WebGPU browser runtimes."),
            ("Zero-Trust Architecture", "FIDO2 hardware auth, Vault SSH CA short-lived certs, and Wasm sandboxing.")
        ],
        "box2_title": "[ PLATFORM INVARIANTS ]",
        "box2_items": [
            ("Lighthouse Score", "100/100 across Performance, SEO, Best Practices, and Accessibility."),
            ("Client-Side Privacy", "Zero tracking cookies, zero analytics scripts, zero external telemetry."),
            ("Runtime Efficiency", "Vanilla static architecture with sub-10ms browser TTFB globally.")
        ],
        "target_files": ["index.html"]
    },
    "page-about": {
        "tag": "[ RESEARCHER PROFILE • DFIR & KERNEL SEC ]",
        "title": "Zyekh Abdul Qadir Jailani — Security Researcher",
        "description": "Digital Forensics & Incident Response (DFIR) Specialist & Systems Researcher focused on low-level Linux security and AI infrastructure.",
        "box1_title": "[ PRIMARY FOCUS AREAS ]",
        "box1_items": [
            ("Digital Forensics & DFIR", "Kernel event tracing, ClickHouse telemetry pipelines, and threat hunting."),
            ("Kernel Space Security", "eBPF network packet bypass filtering and memory-safe driver design."),
            ("Cryptographic Auth", "Hardware-backed SSH access, FIDO2 WebAuthn, and short-lived CA architectures.")
        ],
        "box2_title": "[ VERIFIED RESEARCH METRICS ]",
        "box2_items": [
            ("PGP Key Fingerprint", "Verified master security identity and secure encrypted communication channel."),
            ("Security Disclosure", "Strict RFC 9116 security.txt compliance and vulnerability reporting policy."),
            ("Open Source Artifacts", "35+ peer-reviewed technical blueprints and 46 interactive utilities.")
        ],
        "target_files": ["about/index.html"]
    },
    "page-contact": {
        "tag": "[ ENCRYPTED INTAKE • VULNERABILITY DISCLOSURE ]",
        "title": "Security Incident Intake & Encrypted Channels",
        "description": "Direct communication gateway for security vulnerability disclosures, DFIR research inquiries, and encrypted technical correspondence.",
        "box1_title": "[ INTAKE & DISCLOSURE CHANNELS ]",
        "box1_items": [
            ("RFC 9116 Policy", "Standardized security.txt protocol for coordinated vulnerability disclosure."),
            ("PGP Master Key", "End-to-end cryptographic encryption for confidential technical inquiries."),
            ("Direct Response SLA", "Prioritized triaging for critical zero-day discoveries and security advisories.")
        ],
        "box2_title": "[ VERIFIED COMMUNICATION MATRIX ]",
        "box2_items": [
            ("Key ID & Fingerprint", "4096-bit RSA / ECC master key identity available at /gpg-key.asc."),
            ("Platform Networks", "Verified contact routes via LinkedIn, GitHub, Discord, and Telegram."),
            ("Zero Logging Policy", "Inbound messages are handled in isolated, encrypted work environments.")
        ],
        "target_files": ["contact/index.html"]
    },
    "page-links": {
        "tag": "[ ECOSYSTEM • VERIFIED PORTFOLIOS & ASSETS ]",
        "title": "Official Ecosystem, Repositories & Resources",
        "description": "Comprehensive index of verified source code repositories, research blueprints, developer tools, and security specifications.",
        "box1_title": "[ ARCHITECTURAL ASSETS ]",
        "box1_items": [
            ("GitHub Repositories", "Open-source Linux hardening scripts, eBPF programs, and AI benchmarks."),
            ("46 Web Utility Tools", "100% client-side privacy-first web utilities with zero telemetry."),
            ("35 Technical Blueprints", "Exhaustive production specifications for modern systems engineering.")
        ],
        "box2_title": "[ FEDERATED IDENTITY & PROFILES ]",
        "box2_items": [
            ("Social Federation", "Verified profiles across Bluesky (ATProto), Mastodon, and Dev.to."),
            ("Domain Identity", "DNSSEC-signed, TLS 1.3 secured root domain at zyekh.com."),
            ("RAG Ingestion", "Complete AI ingestion endpoints at /llms.txt and /llms-full.txt.")
        ],
        "target_files": ["links/index.html"]
    },
    "page-tools": {
        "tag": "[ DEVELOPER UTILITY HUB • 46 BROWSER TOOLS ]",
        "title": "Web Utility Tools Hub — 100% Client-Side Privacy",
        "description": "Collection of 46 fast, offline-capable developer utilities. Cryptography, networking, format conversion, and AI infra calculators.",
        "box1_title": "[ TOOL CATEGORY SUITES ]",
        "box1_items": [
            ("Security & Crypto", "Hash Generator, JWT Inspector, Password Entropy, HMAC, and CSP Digest."),
            ("Systems & Networking", "eBPF Evaluator, Subnet Calculator, Chmod Permissions, and cURL Builder."),
            ("AI & Developer Infra", "LLM VRAM Calculator, AI Token Counter, JSON Validator, and CSS Minifier.")
        ],
        "box2_title": "[ ARCHITECTURAL GUARANTEES ]",
        "box2_items": [
            ("Zero Server Logging", "All computations execute 100% inside your browser's local memory."),
            ("Sub-Millisecond Speed", "Instant reactive UI with zero network latency or round-trips."),
            ("Offline ServiceWorker", "Fully functional PWA caching for offline execution anywhere.")
        ],
        "target_files": ["tools/index.html"]
    }
}

def wrap_text(text, font, max_w, draw):
    words = text.split()
    lines = []
    curr = []
    for word in words:
        test = " ".join(curr + [word])
        w = draw.textlength(test, font=font)
        if w <= max_w:
            curr.append(word)
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [word]
    if curr:
        lines.append(" ".join(curr))
    return lines

def render_page_card(key, data, out_path):
    w, h = 2400, 1260
    img = Image.new("RGBA", (w, h), (9, 9, 11, 255))
    draw = ImageDraw.Draw(img)

    # Fonts
    f_cat = ImageFont.truetype(FONT_MONO_REGULAR, 26)
    f_title = ImageFont.truetype(FONT_OUTFIT_BOLD, 64)
    f_desc = ImageFont.truetype(FONT_INTER_REGULAR, 32)
    f_box_hdr = ImageFont.truetype(FONT_MONO_REGULAR, 24)
    f_box_title = ImageFont.truetype(FONT_INTER_BOLD, 28)
    f_box_body = ImageFont.truetype(FONT_INTER_REGULAR, 26)
    f_footer = ImageFont.truetype(FONT_MONO_REGULAR, 22)

    # Outer border
    margin = 80
    draw.rectangle([margin, margin, w - margin, h - margin], outline=(39, 39, 42, 255), width=2)

    # Category Tag
    draw.text((margin + 40, margin + 40), data['tag'], font=f_cat, fill=(161, 161, 170, 255))

    # Title
    t_lines = wrap_text(data['title'], f_title, w - (margin * 2) - 80, draw)
    curr_y = margin + 85
    for line in t_lines[:2]:
        draw.text((margin + 40, curr_y), line, font=f_title, fill=(250, 250, 250, 255))
        curr_y += 74

    # Description
    curr_y += 10
    d_lines = wrap_text(data['description'], f_desc, w - (margin * 2) - 80, draw)
    for line in d_lines[:2]:
        draw.text((margin + 40, curr_y), line, font=f_desc, fill=(161, 161, 170, 255))
        curr_y += 42

    # 2 Feature Matrix Boxes
    curr_y += 35
    box_w = (w - (margin * 2) - 80 - 30) // 2
    box_h = 430

    # Box 1
    box1_x = margin + 40
    draw.rectangle([box1_x, curr_y, box1_x + box_w, curr_y + box_h], fill=(20, 20, 23, 255), outline=(39, 39, 42, 255), width=2)
    draw.text((box1_x + 30, curr_y + 25), data['box1_title'], font=f_box_hdr, fill=(161, 161, 170, 255))
    draw.line([box1_x + 30, curr_y + 60, box1_x + box_w - 30, curr_y + 60], fill=(39, 39, 42, 255), width=1)

    item_y = curr_y + 80
    for title, desc in data['box1_items']:
        draw.text((box1_x + 30, item_y), f"• {title}:", font=f_box_title, fill=(250, 250, 250, 255))
        item_y += 36
        wrapped = wrap_text(desc, f_box_body, box_w - 60, draw)
        for wl in wrapped[:2]:
            draw.text((box1_x + 50, item_y), wl, font=f_box_body, fill=(244, 244, 245, 255))
            item_y += 32
        item_y += 10

    # Box 2
    box2_x = box1_x + box_w + 30
    draw.rectangle([box2_x, curr_y, box2_x + box_w, curr_y + box_h], fill=(20, 20, 23, 255), outline=(39, 39, 42, 255), width=2)
    draw.text((box2_x + 30, curr_y + 25), data['box2_title'], font=f_box_hdr, fill=(161, 161, 170, 255))
    draw.line([box2_x + 30, curr_y + 60, box2_x + box_w - 30, curr_y + 60], fill=(39, 39, 42, 255), width=1)

    item_y = curr_y + 80
    for title, desc in data['box2_items']:
        draw.text((box2_x + 30, item_y), f"• {title}:", font=f_box_title, fill=(250, 250, 250, 255))
        item_y += 36
        wrapped = wrap_text(desc, f_box_body, box_w - 60, draw)
        for wl in wrapped[:2]:
            draw.text((box2_x + 50, item_y), wl, font=f_box_body, fill=(244, 244, 245, 255))
            item_y += 32
        item_y += 10

    # Footer
    footer_text = "OPEN TECHNICAL ARCHITECTURE SPECIFICATION • SYSTEMS & SECURITY BLUEPRINT • ZYEKH.COM"
    draw.text((margin + 40, h - margin - 50), footer_text, font=f_footer, fill=(113, 113, 122, 255))

    img.convert("RGB").save(out_path, format="PNG", optimize=True)
    print(f"[ SUCCESS ] Rendered landing card: {out_path.name}")

def update_landing_html(manifest):
    for key, data in manifest.items():
        card_filename = f"{key}-dark-landscape.png"
        og_url = f"https://zyekh.com/assets/img/social-cards/{card_filename}"

        for tf in data["target_files"]:
            target_path = BASE_DIR / tf
            if not target_path.exists():
                continue
            content = target_path.read_text(encoding="utf-8")
            soup = BeautifulSoup(content, "html.parser")
            head = soup.find("head")
            if not head:
                continue

            # Update or insert og:image
            og_tag = soup.find("meta", property="og:image")
            if og_tag:
                og_tag["content"] = og_url
            else:
                new_tag = soup.new_tag("meta", property="og:image", content=og_url)
                head.append(new_tag)

            # Update or insert twitter:image
            tw_tag = soup.find("meta", attrs={"name": "twitter:image"})
            if tw_tag:
                tw_tag["content"] = og_url
            else:
                new_tag = soup.new_tag("meta", attrs={"name": "twitter:image", "content": og_url})
                head.append(new_tag)

            target_path.write_text(str(soup), encoding="utf-8")
            print(f"[ SUCCESS ] Updated OG/Twitter social tags in {tf} -> {card_filename}")

def main():
    print("============================================================")
    print("    LANDING PAGES SOCIAL SHARE CARDS COMPILER               ")
    print("============================================================")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for key, data in LANDING_PAGES.items():
        out_path = OUTPUT_DIR / f"{key}-dark-landscape.png"
        render_page_card(key, data, out_path)

    update_landing_html(LANDING_PAGES)
    print("\n[ SUCCESS ] All 5 landing page social share cards compiled successfully.")

if __name__ == "__main__":
    main()
