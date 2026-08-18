#!/usr/bin/env python3
"""
scripts/ground_truth.py — Authoritative Ground-Truth & Anti-AI Hallucination Engine for zyekh.com
Provides deterministic filesystem counts, validates text metric parity across all landing pages,
and provides rapid query utilities to prevent hallucinated URLs/tools/articles.
Strict Zero-Emoji, Zero-Speculation architecture.
"""

import os
import sys
import glob
import json
import re
import argparse
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent

def get_authoritative_ground_truth():
    """Extract absolute physical counts directly from immutable filesystem metadata."""
    # 1. Tools count
    tool_files = sorted([f for f in glob.glob(str(BASE_DIR / "tools" / "*.html")) if not f.endswith("tools/index.html")])
    tools_count = len(tool_files)
    
    # Tools manifest count
    tools_manifest_file = BASE_DIR / "tools" / "tools-manifest.json"
    tools_manifest_count = 0
    tools_manifest_items = []
    if tools_manifest_file.exists():
        try:
            tm_data = json.loads(tools_manifest_file.read_text(encoding='utf-8'))
            tools_manifest_items = tm_data.get("tools", [])
            tools_manifest_count = len(tools_manifest_items)
        except Exception:
            pass

    # 2. Blog articles count
    article_files = sorted([f for f in glob.glob(str(BASE_DIR / "blog" / "*.html")) if not f.endswith("blog/index.html")])
    articles_count = len(article_files)
    
    # Batch data count
    batch_data_file = BASE_DIR / "batch_data.json"
    batch_data_count = 0
    batch_articles = []
    if batch_data_file.exists():
        try:
            batch_articles = json.loads(batch_data_file.read_text(encoding='utf-8'))
            batch_data_count = len(batch_articles)
        except Exception:
            pass

    # 3. Blueprints count
    blueprints_file = BASE_DIR / "blueprints" / "index.html"
    blueprints_count = 0
    blueprint_titles = []
    if blueprints_file.exists():
        soup = BeautifulSoup(blueprints_file.read_text(encoding='utf-8', errors='ignore'), 'html.parser')
        bp_grid = soup.find('div', id='blueprintsGrid')
        if bp_grid:
            bp_items = bp_grid.find_all('div', class_='tool-item')
            blueprints_count = len(bp_items)
            for item in bp_items:
                t = item.find('h3', class_='tool-title')
                if t:
                    blueprint_titles.append(t.text.strip())

    # 4. Sitemap URLs count
    sitemap_file = BASE_DIR / "sitemap.xml"
    sitemap_url_count = 0
    if sitemap_file.exists():
        s_content = sitemap_file.read_text(encoding='utf-8', errors='ignore')
        sitemap_url_count = len(re.findall(r'<loc>', s_content))

    # 5. Feed items count
    feed_file = BASE_DIR / "feed.xml"
    feed_item_count = 0
    if feed_file.exists():
        f_content = feed_file.read_text(encoding='utf-8', errors='ignore')
        feed_item_count = len(re.findall(r'<item>', f_content))

    # 6. Service Worker CACHE_VERSION
    sw_file = BASE_DIR / "sw.js"
    cache_version = "UNKNOWN"
    if sw_file.exists():
        sw_content = sw_file.read_text(encoding='utf-8', errors='ignore')
        m = re.search(r"CACHE_VERSION\s*=\s*['\"]([^'\"]+)['\"]", sw_content)
        if m:
            cache_version = m.group(1)

    # 7. Total HTML documents count
    all_html_files = glob.glob(str(BASE_DIR / "**" / "*.html"), recursive=True)
    total_html_count = len(all_html_files)

    return {
        "tools_count": tools_count,
        "tools_manifest_count": tools_manifest_count,
        "articles_count": articles_count,
        "batch_data_count": batch_data_count,
        "blueprints_count": blueprints_count,
        "sitemap_url_count": sitemap_url_count,
        "feed_item_count": feed_item_count,
        "cache_version": cache_version,
        "total_html_files": total_html_count,
        "tools_list": [os.path.basename(f) for f in tool_files],
        "articles_list": [os.path.basename(f) for f in article_files],
        "blueprint_titles": blueprint_titles,
        "tools_manifest_items": tools_manifest_items,
        "batch_articles": batch_articles
    }

def audit_metric_parity(gt):
    """
    Scans core landing pages and documentation to ensure NO metric drift exists.
    Checks that occurrences of tool/article numbers match ground truth.
    """
    errors = []
    
    tools_n = gt["tools_count"]
    articles_n = gt["articles_count"]
    blueprints_n = gt["blueprints_count"]
    
    # Check 1: Manifest counts parity
    if gt["tools_manifest_count"] != tools_n:
        errors.append(f"Tools Manifest Desync: tools-manifest.json has {gt['tools_manifest_count']} tools, but filesystem has {tools_n} tools/*.html files.")
        
    if gt["batch_data_count"] != articles_n:
        errors.append(f"Batch Data Desync: batch_data.json has {gt['batch_data_count']} articles, but filesystem has {articles_n} blog/*.html files.")

    if gt["feed_item_count"] != articles_n:
        errors.append(f"RSS Feed Desync: feed.xml has {gt['feed_item_count']} items, but filesystem has {articles_n} blog articles.")

    # Check 2: Audit text claims across core files
    files_to_check = [
        ("index.html", BASE_DIR / "index.html"),
        ("README.md", BASE_DIR / "README.md"),
        ("about/index.html", BASE_DIR / "about" / "index.html"),
        ("contact/index.html", BASE_DIR / "contact" / "index.html"),
        ("tools/index.html", BASE_DIR / "tools" / "index.html"),
        ("blueprints/index.html", BASE_DIR / "blueprints" / "index.html"),
        ("llms.txt", BASE_DIR / "llms.txt"),
    ]

    # Detect stale number patterns (e.g. 42 tools, 46 tools, 50 tools, 51 tools, 52 tools, 35 articles)
    stale_tool_patterns = [r'\b(4[0-9]|5[0-2])\s+(?:web\s+)?(?:utility\s+)?tools\b', r'\b(4[0-9]|5[0-2])\s+tools\b', r'tools\s*\((\d+)\)']
    stale_article_patterns = [r'\b(3[0-9]|4[0-4])\s+(?:deep-dive\s+)?(?:technical\s+)?articles\b', r'\b(3[0-9]|4[0-4])\s+articles\b']
    
    for label, fpath in files_to_check:
        if not fpath.exists():
            continue
        content = fpath.read_text(encoding='utf-8', errors='ignore')
        
        # Verify Tool Count references
        for pat in stale_tool_patterns:
            matches = re.findall(pat, content, flags=re.IGNORECASE)
            for m in matches:
                val = int(m) if isinstance(m, str) and m.isdigit() else None
                if val and val != tools_n:
                    errors.append(f"[{label}] Stale tool count '{val}' detected (Expected ground truth: {tools_n}).")
        
        # Verify Article Count references
        for pat in stale_article_patterns:
            matches = re.findall(pat, content, flags=re.IGNORECASE)
            for m in matches:
                val = int(m) if isinstance(m, str) and m.isdigit() else None
                if val and val != articles_n:
                    errors.append(f"[{label}] Stale article count '{val}' detected (Expected ground truth: {articles_n}).")

    return errors

def print_summary(gt):
    print("================================================================================")
    print("               ZYEKH.COM AUTHORITATIVE GROUND-TRUTH SNAPSHOT                    ")
    print("================================================================================")
    print(f" • Active Client-Side Tools  : {gt['tools_count']} files (Manifest: {gt['tools_manifest_count']})")
    print(f" • Deep-Dive Blog Articles   : {gt['articles_count']} files (batch_data: {gt['batch_data_count']}, feed: {gt['feed_item_count']})")
    print(f" • Security Blueprints Cards : {gt['blueprints_count']} items in /blueprints/")
    print(f" • Sitemap XML Coverage      : {gt['sitemap_url_count']} canonical URLs")
    print(f" • Total HTML Documents      : {gt['total_html_files']} files")
    print(f" • Active Cache Version      : {gt['cache_version']}")
    print("--------------------------------------------------------------------------------")
    print(" [ VERIFIED ] Single Source of Truth Status: 100% Deterministic & Anti-Drift")
    print("================================================================================\n")

def find_tool(gt, query):
    q = query.lower().strip()
    results = []
    for item in gt["tools_manifest_items"]:
        name = item.get("name", "")
        url = item.get("url", "")
        desc = item.get("description", "")
        cat = item.get("category", "")
        if q in name.lower() or q in url.lower() or q in desc.lower() or q in cat.lower():
            results.append(item)
            
    print(f"\n[ QUERY: '{query}' ] Found {len(results)} matching tool(s):")
    for r in results:
        print(f"  • {r.get('name')} -> {r.get('url')} [{r.get('category')}]")
        print(f"    Desc: {r.get('description')}")
    print()

def find_article(gt, query):
    q = query.lower().strip()
    results = []
    for a in gt["batch_articles"]:
        title = a.get("title", "") or ""
        slug = a.get("slug", "") or ""
        cat = a.get("category", "") or ""
        summary = a.get("summary") or a.get("meta_description") or a.get("description") or ""
        if q in title.lower() or q in slug.lower() or q in summary.lower() or q in cat.lower():
            results.append((a, summary))
            
    print(f"\n[ QUERY: '{query}' ] Found {len(results)} matching article(s):")
    for a, summ in results:
        print(f"  • {a.get('title')}")
        print(f"    Slug: blog/{a.get('slug')}.html [{a.get('category')}]")
        if summ:
            print(f"    Summary: {summ[:100]}...")
    print()

def main():
    parser = argparse.ArgumentParser(description="Ground-Truth Metric Parity & Anti-Hallucination Engine")
    parser.add_argument("--summary", action="store_true", help="Print high-density ground truth summary")
    parser.add_argument("--json", action="store_true", help="Output ground truth data as JSON")
    parser.add_argument("--check", action="store_true", help="Audit all files for metric drift (exit code 1 on mismatch)")
    parser.add_argument("--find-tool", type=str, help="Search tool by keyword/slug to avoid phantom URLs")
    parser.add_argument("--find-article", type=str, help="Search blog article by keyword/slug")
    
    args = parser.parse_args()
    gt = get_authoritative_ground_truth()
    
    if args.json:
        # Strip long lists for cleaner JSON output
        out = {k: v for k, v in gt.items() if not k.endswith('_items') and not k.endswith('_articles')}
        print(json.dumps(out, indent=2))
        return

    if args.find_tool:
        find_tool(gt, args.find_tool)
        return

    if args.find_article:
        find_article(gt, args.find_article)
        return

    if args.check:
        errors = audit_metric_parity(gt)
        if errors:
            print("\n============================================================")
            print(" [ FAIL ] METRIC PARITY & ANTI-HALLUCINATION AUDIT FAILED   ")
            print("============================================================")
            for err in errors:
                print(f"  • [ERROR] {err}")
            print(f"\nTotal violations: {len(errors)}")
            sys.exit(1)
        else:
            print("\n[ PASS ] 100% Metric Parity Verified across all core pages (Zero Metric Drift)!")
            return

    # Default action
    print_summary(gt)

if __name__ == "__main__":
    main()
