#!/usr/bin/env python3
"""
manage_articles.py — Unified CLI Content Manager for zyekh.com
Provides CLI commands to list, scaffold, process hero assets, lint, build, and verify blog articles.
Strict Zero-Emoji, Anti-AI Hallucination, and Single Source of Truth architecture.
"""

import sys
import os
import re
import json
import hashlib
import argparse
import subprocess
from pathlib import Path
from PIL import Image

BATCH_DATA_FILE = "batch_data.json"
TOOLS_MANIFEST_FILE = "tools/tools-manifest.json"

def load_articles():
    if not os.path.exists(BATCH_DATA_FILE):
        print(f"[ERROR] {BATCH_DATA_FILE} not found.")
        sys.exit(1)
    with open(BATCH_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_articles(articles):
    with open(BATCH_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"[SUCCESS] Saved {len(articles)} articles to {BATCH_DATA_FILE}.")

def load_tools_manifest():
    if not os.path.exists(TOOLS_MANIFEST_FILE):
        return []
    try:
        data = json.load(open(TOOLS_MANIFEST_FILE, "r", encoding="utf-8"))
        return data.get("tools", [])
    except Exception:
        return []

def find_relevant_tools(keywords, tools_list, max_tools=3):
    """Find existing client-side tools matching keywords to eliminate hallucinated links."""
    scored = []
    kw_tokens = set(re.findall(r'\w+', ' '.join(keywords).lower()))
    
    for t in tools_list:
        score = 0
        name = t.get("name", "").lower()
        desc = t.get("description", "").lower()
        url = t.get("url", "")
        
        for token in kw_tokens:
            if len(token) < 3:
                continue
            if token in name:
                score += 3
            if token in desc:
                score += 1
            if token in url:
                score += 2
                
        if score > 0:
            scored.append((score, {
                "name": t.get("name", "Tool"),
                "url": url,
                "desc": t.get("description", "Interactive security analysis tool.")
            }))
            
    scored.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored[:max_tools]]

def cmd_list(args):
    articles = load_articles()
    print("\n==========================================================================================")
    print(f"                      ZYEKH.COM BLOG ARTICLES DIRECTORY ({len(articles)} Articles)             ")
    print("==========================================================================================")
    print(f"{'#':<3} | {'SLUG':<45} | {'DATE':<10} | {'WORDS':<6} | {'HTML FILE'}")
    print("-" * 90)
    
    for idx, a in enumerate(articles, 1):
        slug = a.get("slug", "unknown")
        date_pub = a.get("date_published", "N/A")
        word_count = a.get("word_count", 0)
        html_path = f"blog/{slug}.html"
        exists = "[OK]" if os.path.exists(html_path) else "[MISSING]"
        print(f"{idx:<3} | {slug:<45} | {date_pub:<10} | {word_count:<6} | {exists} {html_path}")
    print("==========================================================================================\n")

def cmd_lint(args):
    """Fast pre-flight validator for batch_data.json before generation."""
    articles = load_articles()
    print("\n============================================================")
    print(f"      ZYEKH.COM BATCH DATA LINTER & GEO READINESS ({len(articles)} Articles)  ")
    print("============================================================\n")
    
    errors = []
    warnings = []
    seen_slugs = set()
    
    for idx, a in enumerate(articles, 1):
        slug = a.get("slug", "")
        title = a.get("title", "")
        subtitle = a.get("subtitle", "")
        sections = a.get("sections", [])
        exec_summary = a.get("exec_summary", [])
        faqs = a.get("faqs", [])
        related_tools = a.get("related_tools", [])
        hero_img = a.get("hero_image", "")
        
        # 1. Slug validation
        if not slug or not re.match(r'^[a-z0-9-]+$', slug):
            errors.append(f"Article #{idx}: Invalid or non-URL slug '{slug}'")
        if slug in seen_slugs:
            errors.append(f"Article #{idx}: Duplicate slug '{slug}' detected")
        seen_slugs.add(slug)
        
        # 2. Section count
        if len(sections) < 4:
            errors.append(f"[{slug}] Section depth deficit: {len(sections)} sections (Minimum required: 4)")
            
        # 3. Projected Word count calculation
        total_words = len(re.findall(r'\w+', title)) + len(re.findall(r'\w+', subtitle))
        for ex in exec_summary:
            total_words += len(re.findall(r'\w+', ex))
        for s_idx, sec in enumerate(sections, 1):
            total_words += len(re.findall(r'\w+', sec.get("h2_title", "")))
            for p in sec.get("content_paragraphs", []):
                total_words += len(re.findall(r'\w+', p))
            if sec.get("code_block"):
                code = sec.get("code_block", "")
                total_words += len(re.findall(r'\w+', code))
                open_braces = code.count('{')
                close_braces = code.count('}')
                if open_braces != close_braces:
                    warnings.append(f"[{slug}] Section {s_idx} code block has unbalanced braces: {open_braces} '{{' vs {close_braces} '}}'")
            if sec.get("custom_html"):
                total_words += len(re.findall(r'\w+', sec.get("custom_html", "")))
        for faq in faqs:
            q = faq.get("question") or faq.get("q", "")
            a = faq.get("answer") or faq.get("a", "")
            total_words += len(re.findall(r'\w+', f"{q} {a}"))
            
        # Standard rendered components inside <main class="article-content"> (TOC, author card, related tools)
        total_words += len(re.findall(r'\w+', "Executive Summary Key Security Takeaways Table of Contents Frequently Asked Questions FAQ Written by Zyekh Abdul Qadir Jailani Digital Forensics Incident Response DFIR Specialist Security Researcher Utility Security Tools Related to this Article"))
                    
        if total_words < 800:
            errors.append(f"[{slug}] Word count deficit: {total_words} words (Minimum required: 800 words)")
            
        # 4. Executive summary & FAQs
        if len(exec_summary) < 3:
            warnings.append(f"[{slug}] Executive summary has only {len(exec_summary)} items (Recommended: >= 3)")
        if len(faqs) < 2:
            warnings.append(f"[{slug}] FAQ count deficit: {len(faqs)} items (Recommended: >= 2)")
            
        # 5. Tool link integrity (Anti-AI Hallucination)
        for t in related_tools:
            t_url = t.get("url", "") if isinstance(t, dict) else t
            local_path = t_url.lstrip("/")
            if local_path.startswith("tools/") and not os.path.exists(local_path):
                errors.append(f"[{slug}] Hallucinated related tool URL: '{t_url}' does not exist on disk!")
                
        # 6. Hero image file check
        hero_rel = hero_img.replace("https://zyekh.com/", "").lstrip("/")
        if hero_rel and not os.path.exists(hero_rel):
            warnings.append(f"[{slug}] Hero image file not found on disk: '{hero_rel}'")

    # Print results
    if warnings:
        print(f"[ WARNINGS ] ({len(warnings)} found):")
        for w in warnings:
            print(f"  • [WARN] {w}")
        print()
        
    if errors:
        print(f"[ FAILED ] ({len(errors)} errors detected):")
        for e in errors:
            print(f"  • [FAIL] {e}")
        print("============================================================\n")
        sys.exit(1)
    else:
        print(f"[ PASS ] All {len(articles)} articles in batch_data.json passed pre-flight linting with 0 errors!")
        print("============================================================\n")

def cmd_scaffold(args):
    """Scaffolds a 100% SOP-compliant article skeleton in batch_data.json."""
    articles = load_articles()
    existing_slugs = {a.get("slug") for a in articles}
    
    slug = args.slug or input("Article Slug (e.g. eBPF-packet-filtering): ").strip().lower()
    slug = re.sub(r'[^a-z0-9-]+', '-', slug).strip('-')
    if slug in existing_slugs:
        print(f"[ERROR] Slug '{slug}' already exists in batch_data.json.")
        sys.exit(1)
        
    title = args.title or input("Article Title: ").strip()
    subtitle = args.subtitle or input("Subtitle / Description: ").strip()
    category = args.category or input("Category (default: Cyber Security • Systems Hardening): ").strip() or "Cyber Security • Systems Hardening"
    date_pub = args.date or input("Publish Date (YYYY-MM-DD): ").strip()
    
    # Semantic tool discovery
    tools_list = load_tools_manifest()
    matched_tools = find_relevant_tools([title, subtitle, category], tools_list, max_tools=3)
    
    hero_clean = slug.replace("-", "_")
    
    skeleton = {
        "slug": slug,
        "title": title,
        "subtitle": subtitle,
        "category": category,
        "tags": [f"#{t.strip()}" for t in category.split("•") if t.strip()],
        "date_published": date_pub,
        "read_time_mins": 12,
        "word_count": 1400,
        "hero_image": f"https://zyekh.com/assets/img/{hero_clean}.jpg",
        "hero_caption": f"Technical Architecture & Threat Model for {title}",
        "exec_summary": [
            f"Core Mechanism: Primary engineering concept underlying {title}.",
            "Security Invariant: Critical defensive constraint preventing exploitation.",
            "Production Impact: Operational benchmark and resilience outcome in high-load clusters."
        ],
        "sections": [
            {
                "id": "architectural-overview",
                "h2_title": "1. Architectural Overview & Core Threat Landscape",
                "content_paragraphs": [
                    "Technical background and threat model analyzing system boundary vulnerabilities.",
                    "Detailed decomposition of failure modes and memory/packet routing vectors.",
                    "Establishing defense-in-depth isolation parameters."
                ],
                "code_block": "# Core implementation or configuration baseline\nsysctl -p",
                "code_language": "bash"
            },
            {
                "id": "internals-and-execution-flow",
                "h2_title": "2. Low-Level Mechanics & Execution Pipeline",
                "content_paragraphs": [
                    "Detailed analysis of kernel tracepoints, bytecode execution, or cryptographic primitives.",
                    "Step-by-step trace through memory layouts and validation gates.",
                    "Performance implications under high-concurrency production workloads."
                ],
                "code_block": "// Low-level runtime implementation\nvoid execute_invariant_check() {\n    // Invariant logic\n}",
                "code_language": "c"
            },
            {
                "id": "defensive-hardening",
                "h2_title": "3. Hardening Blueprint & Invariant Enforcement",
                "content_paragraphs": [
                    "Comprehensive mitigation strategies eliminating attack vectors.",
                    "Formal verification rules and automated continuous testing checks.",
                    "Production policy enforcement and rollback triggers."
                ],
                "code_block": "# Hardening policy deployment\nsudo systemctl restart daemon",
                "code_language": "bash"
            },
            {
                "id": "operational-verification",
                "h2_title": "4. Telemetry, Monitoring & Verification Playbook",
                "content_paragraphs": [
                    "Real-time observability metrics and forensic audit logging.",
                    "Incident response triggers and automated remediation playbooks.",
                    "Empirical verification protocols to certify compliance."
                ],
                "code_block": "# Verification check command\nauditctl -l",
                "code_language": "bash"
            }
        ],
        "faqs": [
            {
                "question": f"What is the primary operational advantage of {title}?",
                "answer": "Provides deterministic security guarantees and eliminates attack surface with zero runtime performance overhead."
            },
            {
                "question": "How do you verify configuration correctness in production?",
                "answer": "Utilize automated linting gates, kernel audit logs, and continuous smoke testing verification."
            }
        ],
        "related_tools": matched_tools
    }
    
    articles.append(skeleton)
    save_articles(articles)
    print(f"\n[SUCCESS] Scaffolded new article '{slug}' in batch_data.json.")
    print(f"  • Matched Tools: {len(matched_tools)} tools bound from manifest ({', '.join(t['name'] for t in matched_tools) if matched_tools else 'None'})")
    print(f"  • Sections: {len(skeleton['sections'])} structured chapters")

def cmd_process_hero(args):
    """Resizes, converts to WebP, audits MD5 hash, and registers hero images."""
    if not os.path.exists(args.image):
        print(f"[ERROR] Input image file not found: {args.image}")
        sys.exit(1)
        
    slug = args.slug.strip().lower()
    clean_slug = slug.replace("-", "_")
    target_jpg = f"assets/img/{clean_slug}.jpg"
    target_webp = f"assets/img/{clean_slug}.webp"
    
    # 1. Open and resize to 1280x720 (16:9)
    try:
        im = Image.open(args.image)
        if im.mode != "RGB":
            im = im.convert("RGB")
            
        # Target dimensions
        target_w, target_h = 1280, 720
        im_ratio = im.width / im.height
        target_ratio = target_w / target_h
        
        if im_ratio > target_ratio:
            # Image is wider: crop sides
            new_w = int(im.height * target_ratio)
            left = (im.width - new_w) // 2
            im = im.crop((left, 0, left + new_w, im.height))
        elif im_ratio < target_ratio:
            # Image is taller: crop top/bottom
            new_h = int(im.width / target_ratio)
            top = (im.height - new_h) // 2
            im = im.crop((0, top, im.width, top + new_h))
            
        im = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
        
        # Save JPG
        im.save(target_jpg, "JPEG", quality=88, optimize=True)
        # Save WebP
        im.save(target_webp, "WEBP", quality=85)
        
        # 2. Compute MD5 Hash
        with open(target_jpg, "rb") as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
            
        print(f"[OK] Processed hero image for '{slug}':")
        print(f"  • JPG  -> {target_jpg} (1280x720, MD5: {file_hash})")
        print(f"  • WebP -> {target_webp} (1280x720)")
        
        # 3. Audit MD5 Hash Uniqueness across all existing images
        all_imgs = [f for f in os.listdir("assets/img") if f.endswith(".jpg") and f != os.path.basename(target_jpg)]
        duplicates = []
        for other in all_imgs:
            other_path = os.path.join("assets/img", other)
            with open(other_path, "rb") as f:
                other_hash = hashlib.md5(f.read()).hexdigest()
                if other_hash == file_hash:
                    duplicates.append(other)
                    
        if duplicates:
            print(f"[WARN] Image MD5 hash collision detected with: {', '.join(duplicates)}! Regenerate image.")
        else:
            print("[PASS] Image MD5 hash is 100% unique across assets/img/.")
            
        # 4. Update batch_data.json if slug exists
        articles = load_articles()
        updated = False
        for a in articles:
            if a.get("slug") == slug:
                a["hero_image"] = f"https://zyekh.com/{target_jpg}"
                updated = True
                break
        if updated:
            save_articles(articles)
            print(f"[SUCCESS] Updated hero_image path in batch_data.json for '{slug}'.")
            
    except Exception as e:
        print(f"[ERROR] Failed to process hero image: {e}")
        sys.exit(1)

def cmd_build(args):
    print("[BUILD] Running unified article build pipeline...")
    cmd = "python3 generate_batch.py && python3 scripts/extract_card_manifest.py && python3 scripts/validate_card_manifest.py && python3 sync_content.py && python3 generate_llms_full.py"
    res = subprocess.run(cmd, shell=True)
    if res.returncode == 0:
        print("[SUCCESS] Build completed successfully.")
    else:
        print("[ERROR] Build pipeline failed.")
        sys.exit(res.returncode)

def cmd_verify(args):
    print("[VERIFY] Running QA verification audit...")
    cmd = "python3 verify_batch.py && python3 check_emojis.py"
    res = subprocess.run(cmd, shell=True)
    if res.returncode == 0:
        print("[SUCCESS] Verification passed with 0 errors!")
    else:
        print("[ERROR] Verification audit failed.")
        sys.exit(res.returncode)

def main():
    parser = argparse.ArgumentParser(description="Unified CLI Content Manager for zyekh.com")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # 1. List command
    p_list = subparsers.add_parser("list", help="List all articles in batch_data.json")
    p_list.set_defaults(func=cmd_list)
    
    # 2. Lint command
    p_lint = subparsers.add_parser("lint", help="Lint batch_data.json for GEO/RAG compliance & zero hallucinations")
    p_lint.set_defaults(func=cmd_lint)
    
    # 3. Scaffold command
    p_scaffold = subparsers.add_parser("scaffold", help="Scaffold a 100%% SOP-compliant article skeleton with auto tool matching")
    p_scaffold.add_argument("--slug", help="Article URL slug")
    p_scaffold.add_argument("--title", help="Article Title")
    p_scaffold.add_argument("--subtitle", help="Article Subtitle")
    p_scaffold.add_argument("--category", help="Article Category")
    p_scaffold.add_argument("--date", help="Publish Date (YYYY-MM-DD)")
    p_scaffold.set_defaults(func=cmd_scaffold)
    
    # 4. Process Hero command
    p_hero = subparsers.add_parser("process-hero", help="Crop/resize 16:9 hero image, generate WebP, audit MD5 hash, and bind to batch_data.json")
    p_hero.add_argument("--image", required=True, help="Path to input raw image (JPG/PNG)")
    p_hero.add_argument("--slug", required=True, help="Article slug")
    p_hero.set_defaults(func=cmd_process_hero)
    
    # 5. Build command
    p_build = subparsers.add_parser("build", help="Run full article compilation & sync pipeline")
    p_build.set_defaults(func=cmd_build)
    
    # 6. Verify command
    p_verify = subparsers.add_parser("verify", help="Run 22-axis QA audit & emoji checks")
    p_verify.set_defaults(func=cmd_verify)
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    args.func(args)

if __name__ == "__main__":
    main()
