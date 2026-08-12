#!/usr/bin/env python3
"""
manage_articles.py — Unified CLI Content Manager for zyekh.com
Provides CLI commands to list, add, build, verify, and manage blog articles.
"""

import sys
import os
import json
import argparse
import subprocess

BATCH_DATA_FILE = "batch_data.json"

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

def cmd_list(args):
    articles = load_articles()
    print(f"\n==========================================================================================")
    print(f"                      ZYEKH.COM BLOG ARTICLES DIRECTORY ({len(articles)} Articles)             ")
    print(f"==========================================================================================")
    print(f"{'#':<3} | {'SLUG':<45} | {'DATE':<10} | {'WORDS':<6} | {'HTML FILE'}")
    print(f"-" * 90)
    
    for idx, a in enumerate(articles, 1):
        slug = a.get("slug", "unknown")
        date_pub = a.get("date_published", "N/A")
        word_count = a.get("word_count", 0)
        html_path = f"blog/{slug}.html"
        exists = "[OK]" if os.path.exists(html_path) else "[MISSING]"
        print(f"{idx:<3} | {slug:<45} | {date_pub:<10} | {word_count:<6} | {exists} {html_path}")
    print(f"==========================================================================================\n")

def cmd_build(args):
    print("[BUILD] Running unified article build pipeline...")
    cmd = "python3 generate_batch.py && python3 sync_content.py && python3 generate_llms_full.py"
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

def cmd_add(args):
    articles = load_articles()
    existing_slugs = {a.get("slug") for a in articles}
    
    slug = args.slug or input("Article Slug (e.g. eBPF-security-guide): ").strip().lower()
    if slug in existing_slugs:
        print(f"[ERROR] Slug '{slug}' already exists in batch_data.json.")
        sys.exit(1)
        
    title = args.title or input("Article Title: ").strip()
    subtitle = args.subtitle or input("Subtitle: ").strip()
    category = args.category or input("Category (default: Cyber Security • Hardening): ").strip() or "Cyber Security • Hardening"
    date_pub = args.date or input("Publish Date (YYYY-MM-DD): ").strip()
    
    new_article = {
        "slug": slug,
        "title": title,
        "subtitle": subtitle,
        "category": category,
        "tags": [f"#{t.strip()}" for t in category.split("•") if t.strip()],
        "date_published": date_pub,
        "read_time_mins": 12,
        "word_count": 1400,
        "hero_image": f"https://zyekh.com/assets/img/{slug.replace('-', '_')}_hero.jpg",
        "hero_caption": f"3D Isometric Model of {title}",
        "exec_summary": [
            "Executive Key Takeaway 1",
            "Executive Key Takeaway 2",
            "Executive Key Takeaway 3"
        ],
        "sections": [
            {
                "id": "introduction",
                "h2_title": "1. Architectural Overview & Foundations",
                "content_paragraphs": [
                    "Detailed technical introduction paragraph explaining the core problem and solution space."
                ]
            }
        ],
        "faqs": [
            {
                "question": "What is the primary technical takeaway?",
                "answer": "Detailed answer explaining technical implementation details."
            }
        ],
        "related_tools": []
    }
    
    articles.append(new_article)
    save_articles(articles)
    print(f"[SUCCESS] Article '{slug}' added to batch_data.json.")
    if args.auto_build:
        cmd_build(args)

def main():
    parser = argparse.ArgumentParser(description="Unified CLI Content Manager for zyekh.com")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    parser_list = subparsers.add_parser("list", help="List all articles in batch_data.json")
    parser_list.set_defaults(func=cmd_list)
    
    # Build command
    parser_build = subparsers.add_parser("build", help="Run full article compilation & sync pipeline")
    parser_build.set_defaults(func=cmd_build)
    
    # Verify command
    parser_verify = subparsers.add_parser("verify", help="Run QA audit & emoji checks")
    parser_verify.set_defaults(func=cmd_verify)
    
    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new article entry to batch_data.json")
    parser_add.add_argument("--slug", help="Article URL slug")
    parser_add.add_argument("--title", help="Article Title")
    parser_add.add_argument("--subtitle", help="Article Subtitle")
    parser_add.add_argument("--category", help="Article Category")
    parser_add.add_argument("--date", help="Publish Date (YYYY-MM-DD)")
    parser_add.add_argument("--auto-build", action="store_true", help="Automatically run build pipeline after adding")
    parser_add.set_defaults(func=cmd_add)
    
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    args.func(args)

if __name__ == "__main__":
    main()
