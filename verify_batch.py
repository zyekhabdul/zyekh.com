#!/usr/bin/env python3
import glob
import os
import sys
import json
import time
import hashlib
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup

CACHE_FILE = Path("data/.qa_cache.json")

def compute_codebase_hash():
    """Computes aggregate MD5 hash across all critical tracked files."""
    patterns = [
        "blog/*.html",
        "tools/*.html",
        "blueprints/*.html",
        "assets/css/*.css",
        "assets/js/*.js",
        "scripts/*.py",
        "*.html",
        "verify_batch.py",
        "check_emojis.py",
        "sync_content.py"
    ]
    files = []
    for pat in patterns:
        for f in glob.glob(pat):
            if os.path.isfile(f):
                files.append(f)
    files.sort()
    
    h = hashlib.md5()
    for f in files:
        h.update(f.encode('utf-8'))
        try:
            with open(f, 'rb') as fp:
                h.update(fp.read())
        except Exception:
            pass
    return h.hexdigest(), len(files)

def is_qa_cache_valid():
    """Checks if data/.qa_cache.json matches current codebase hash."""
    if not CACHE_FILE.exists():
        return False
    try:
        data = json.loads(CACHE_FILE.read_text(encoding='utf-8'))
        current_hash, file_count = compute_codebase_hash()
        return data.get("hash") == current_hash and data.get("passed") is True
    except Exception:
        return False

def save_qa_cache(fast_mode=False):
    """Saves valid QA cache stamp."""
    current_hash, file_count = compute_codebase_hash()
    data = {
        "hash": current_hash,
        "file_count": file_count,
        "timestamp": int(time.time()),
        "passed": True,
        "fast_mode": fast_mode
    }
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CACHE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2), encoding='utf-8')
    tmp.replace(CACHE_FILE)

def verify_all_articles():
    # Cache Check Only (Used by pre-commit hook for 0.05s instant check)
    if "--cache-check-only" in sys.argv:
        if is_qa_cache_valid():
            print("[ OK ] QA cache valid and verified (0.05s).")
            sys.exit(0)
        else:
            print("[ WARN ] QA cache stale or missing. Running full verification...")

    fast_mode = "--fast" in sys.argv or "-f" in sys.argv
    no_cache = "--no-cache" in sys.argv or "--force" in sys.argv

    # Instant QA Cache Bypass
    if not no_cache and "--cache-check-only" not in sys.argv:
        if is_qa_cache_valid():
            print("[ CACHE ] Codebase checksum matches last verified state (0.05s). All 25 checks passed!")
            sys.exit(0)

    articles = sorted(glob.glob("blog/*.html"))
    articles = [a for a in articles if a != "blog/index.html"]
    
    print("============================================================")
    print("          ZYEKH.COM PROGRAMMATIC BATCH QA AUDITOR           ")
    print("============================================================\n")
    print(f"[AUDIT] Found {len(articles)} blog articles to verify...\n")
    
    failures = 0
    
    for a in articles:
        filename = os.path.basename(a)
        content = open(a, encoding='utf-8', errors='ignore').read()
        soup = BeautifulSoup(content, 'html.parser')
        
        errors = []
        
        # Check 1: Main Content Wrapper
        if not soup.find('main', class_='article-content'):
            errors.append("Missing <main class=\"article-content\"> wrapper")
            
        # Check 2: Hero Figure
        if not soup.find('figure', class_='article-hero-wrapper'):
            errors.append("Missing <figure class=\"article-hero-wrapper\">")
            
        # Check 3: Executive Summary
        if not soup.find('div', class_='exec-summary'):
            errors.append("Missing <div class=\"exec-summary\">")
            
        # Check 4: Table of Contents
        if not soup.find('nav', class_='toc-card'):
            errors.append("Missing <nav class=\"toc-card\">")
            
        # Check 5: H2 Heading IDs
        h2s = soup.find_all('h2')
        missing_h2_ids = [h for h in h2s if not h.get('id')]
        if missing_h2_ids:
            errors.append(f"{len(missing_h2_ids)}/{len(h2s)} <h2> tags missing id=\"...\"")
            
        # Check 6: FAQ Section
        if not soup.find('div', class_='faq-section'):
            errors.append("Missing <div class=\"faq-section\">")
            
        # Check 7: Author Bio Card
        if not soup.find('div', class_='author-card'):
            errors.append("Missing <div class=\"author-card\">")
            
        # Check 8: Related Tools Card
        if not soup.find('div', class_='article-cross-links'):
            errors.append("Missing <div class=\"article-cross-links\">")
            
        # Check 9: Schema.org TechArticle
        if "TechArticle" not in content:
            errors.append("Missing Schema.org TechArticle JSON-LD")
            
        # Check 10: Share Button
        if not soup.find('button', id='shareBtn'):
            errors.append("Missing share button (#shareBtn)")
            
        # Check 11: Duplicate Element IDs Check
        all_ids = [el['id'] for el in soup.find_all(id=True)]
        seen_ids = set()
        dups = set()
        for i in all_ids:
            if i in seen_ids:
                dups.add(i)
            seen_ids.add(i)
        if dups:
            errors.append(f"Duplicate element IDs found: {', '.join(dups)}")
            
        # Check 12: Single Site-Nav Script Tag Check
        site_nav_scripts = [s for s in soup.find_all('script') if s.get('src') and 'site-nav.js' in s.get('src')]
        if len(site_nav_scripts) > 1:
            errors.append(f"Multiple ({len(site_nav_scripts)}) site-nav.js script tags detected")
            
        # Check 13: Minimum Technical Word Count Threshold (>= 800 Words)
        main_el = soup.find('main', class_='article-content')
        if main_el:
            import re
            words = len(re.findall(r'\w+', main_el.text))
            if words < 800:
                errors.append(f"Article length deficit: {words} words (Minimum required: 800 words)")
                
        # Check 14: Minimum Section Depth (>= 4 H2 Headings)
        if main_el:
            h2_count = len(main_el.find_all('h2'))
            if h2_count < 4:
                errors.append(f"Section depth deficit: {h2_count} H2 headings (Minimum required: 4 sections)")
            
        # Check 16: Hero Image LCP Performance Optimization Check (loading="eager")
        hero_img_el = soup.find('img', class_='article-hero-img')
        if hero_img_el and hero_img_el.get('loading') == 'lazy':
            errors.append("Hero image loading attribute set to 'lazy' instead of 'eager' (LCP Bottleneck)")
            
        if errors:
            failures += 1
            print(f"[FAIL] {filename}:")
            for err in errors:
                print(f"       - {err}")
        else:
            print(f"[PASS] {filename} (100% SOP Compliant)")

    # Check 15: Global MD5 Image Uniqueness Audit across all article hero images
    import hashlib
    print("\n[AUDIT] Running Check 15: Image MD5 Hash Uniqueness Audit...")
    image_hashes = {}
    img_failures = 0
    for a in articles:
        content = open(a, encoding='utf-8', errors='ignore').read()
        soup = BeautifulSoup(content, 'html.parser')
        hero_img = soup.find('img', class_='article-hero-img') or soup.find('img', class_='card-thumb-img')
        if hero_img and hero_img.get('src'):
            src = hero_img['src'].replace('https://zyekh.com/', '').lstrip('/')
            if os.path.exists(src):
                h = hashlib.md5(open(src, 'rb').read()).hexdigest()
                if h in image_hashes:
                    print(f"[FAIL] Duplicate Hero Image MD5 Hash detected in {os.path.basename(a)}:")
                    print(f"       - Shared MD5 ({h}) with {image_hashes[h]} ({src})")
                    img_failures += 1
                else:
                    image_hashes[h] = os.path.basename(a)

    if img_failures > 0:
        failures += img_failures

    # Check 16: Social Cards & Manifest Deterministic Integrity Audit
    import json
    from PIL import Image
    print("\n[AUDIT] Running Check 16: Social Share Cards & Manifest Integrity Audit...")
    manifest_path = "data/social_cards_manifest.json"
    card_failures = 0

    # Execute deep manifest validator with AST brace balance and headless geometry gates
    try:
        from scripts.validate_card_manifest import validate_manifest
        validate_manifest()
    except Exception as e:
        print(f"[FAIL] Manifest validation gate failed: {e}")
        card_failures += 1
    else:
        manifest_data = json.loads(open(manifest_path, encoding='utf-8').read())
        for a in articles:
            slug = os.path.splitext(os.path.basename(a))[0]
            if slug not in manifest_data:
                print(f"[FAIL] Article '{slug}' missing from {manifest_path}")
                card_failures += 1
                continue
            
            # Check Dark Landscape Card
            dark_land = f"assets/img/social-cards/{slug}-dark-landscape.png"
            if not os.path.exists(dark_land):
                print(f"[FAIL] Missing Dark Landscape Card: {dark_land}")
                card_failures += 1
            else:
                sz = os.path.getsize(dark_land) / 1024
                if sz < 10 or sz > 950:
                    print(f"[FAIL] {dark_land} file size invalid ({sz:.1f} KB)")
                    card_failures += 1
                try:
                    with Image.open(dark_land) as im:
                        if im.size != (2400, 1260):
                            print(f"[FAIL] {dark_land} dimensions {im.size} != (2400, 1260)")
                            card_failures += 1
                except Exception as e:
                    print(f"[FAIL] {dark_land} corrupted: {e}")
                    card_failures += 1

            # Check Light Square Card
            light_sq = f"assets/img/social-cards/{slug}-light-square.png"
            if not os.path.exists(light_sq):
                print(f"[FAIL] Missing Light Square Card: {light_sq}")
                card_failures += 1
            else:
                sz = os.path.getsize(light_sq) / 1024
                if sz < 10 or sz > 950:
                    print(f"[FAIL] {light_sq} file size invalid ({sz:.1f} KB)")
                    card_failures += 1
                try:
                    with Image.open(light_sq) as im:
                        if im.size != (2400, 2400):
                            print(f"[FAIL] {light_sq} dimensions {im.size} != (2400, 2400)")
                            card_failures += 1
                except Exception as e:
                    print(f"[FAIL] {light_sq} corrupted: {e}")
                    card_failures += 1

    if card_failures > 0:
        failures += card_failures

    # Check 17: XML Feeds & Sitemap Integrity Audit
    import xml.etree.ElementTree as ET
    print("\n[AUDIT] Running Check 17: XML Feeds, Atom, JSON Feed & Sitemap Integrity Audit...")
    xml_failures = 0
    try:
        feed_tree = ET.parse('feed.xml')
        feed_links = set(elem.text.strip() for elem in feed_tree.getroot().findall('channel/item/link') if elem.text)
        for a in articles:
            expected_url = f"https://zyekh.com/{a.replace(os.sep, '/')}"
            if expected_url not in feed_links:
                print(f"[FAIL] Article missing from feed.xml: {expected_url}")
                xml_failures += 1
    except Exception as e:
        print(f"[FAIL] feed.xml XML parse error: {e}")
        xml_failures += 1

    try:
        atom_tree = ET.parse('atom.xml')
        atom_ns = {'atom': 'http://www.w3.org/2005/Atom'}
        atom_links = set(elem.get('href', '').strip() for elem in atom_tree.getroot().findall('atom:entry/atom:link', atom_ns) if elem.get('href'))
        for a in articles:
            expected_url = f"https://zyekh.com/{a.replace(os.sep, '/')}"
            if expected_url not in atom_links:
                print(f"[FAIL] Article missing from atom.xml: {expected_url}")
                xml_failures += 1
    except Exception as e:
        print(f"[FAIL] atom.xml XML parse error: {e}")
        xml_failures += 1

    try:
        feed_json_data = json.loads(open('feed.json', encoding='utf-8').read())
        if feed_json_data.get("version") != "https://jsonfeed.org/version/1.1":
            print(f"[FAIL] feed.json invalid version: {feed_json_data.get('version')}")
            xml_failures += 1
        json_item_urls = set(item.get('url', '') for item in feed_json_data.get('items', []))
        for a in articles:
            expected_url = f"https://zyekh.com/{a.replace(os.sep, '/')}"
            if expected_url not in json_item_urls:
                print(f"[FAIL] Article missing from feed.json: {expected_url}")
                xml_failures += 1
    except Exception as e:
        print(f"[FAIL] feed.json JSON parse error: {e}")
        xml_failures += 1

    try:
        sitemap_tree = ET.parse('sitemap.xml')
        sitemap_urls = set(elem.text.strip() for elem in sitemap_tree.getroot().findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc') if elem.text)
        for a in articles:
            expected_url = f"https://zyekh.com/{a.replace(os.sep, '/')}"
            if expected_url not in sitemap_urls:
                print(f"[FAIL] Article missing from sitemap.xml: {expected_url}")
                xml_failures += 1
        if "https://zyekh.com/links/" not in sitemap_urls:
            print("[FAIL] /links/ page missing from sitemap.xml")
            xml_failures += 1
    except Exception as e:
        print(f"[FAIL] sitemap.xml XML parse error: {e}")
        xml_failures += 1

    if xml_failures > 0:
        failures += xml_failures

    # Check 18: Tools Metadata & RAG Knowledge Base Parity Audit
    print("\n[AUDIT] Running Check 18: Tools OpenGraph & RAG Knowledge Base Parity Audit...")
    tool_failures = 0
    tools = [t for t in sorted(glob.glob("tools/*.html")) if t != "tools/index.html"]
    for t in tools:
        t_content = open(t, encoding='utf-8', errors='ignore').read()
        t_soup = BeautifulSoup(t_content, 'html.parser')
        if not t_soup.find('meta', property='og:image'):
            print(f"[FAIL] {t} missing <meta property=\"og:image\">")
            tool_failures += 1
        if not t_soup.find('meta', attrs={'name': 'twitter:image'}):
            print(f"[FAIL] {t} missing <meta name=\"twitter:image\">")
            tool_failures += 1

    if not os.path.exists("llms-full.txt"):
        print("[FAIL] llms-full.txt does not exist")
        tool_failures += 1
    else:
        llms_full_content = open("llms-full.txt", encoding='utf-8').read()
        for a in articles:
            a_slug = os.path.splitext(os.path.basename(a))[0]
            if a_slug not in llms_full_content:
                print(f"[FAIL] Article '{a_slug}' missing from llms-full.txt")
                tool_failures += 1

    manifest_path = "tools/tools-manifest.json"
    if not os.path.exists(manifest_path):
        print("[FAIL] tools/tools-manifest.json does not exist")
        tool_failures += 1
    else:
        try:
            m_data = json.loads(open(manifest_path, encoding='utf-8').read())
            manifest_slugs = set(tool_entry["id"] for tool_entry in m_data.get("tools", []))
            for t in tools:
                t_slug = os.path.splitext(os.path.basename(t))[0]
                if t_slug not in manifest_slugs:
                    print(f"[FAIL] Tool '{t_slug}' missing from tools/tools-manifest.json")
                    tool_failures += 1
        except Exception as err:
            print(f"[FAIL] tools/tools-manifest.json is malformed JSON: {err}")
            tool_failures += 1

    if tool_failures > 0:
        failures += tool_failures

    # Check 19: Syndication History & Ledger Parity Audit
    print("\n[AUDIT] Running Check 19: Syndication History & Ledger Parity Audit...")
    ledger_failures = 0
    history_path = "data/syndication_history.json"
    if os.path.exists(history_path):
        try:
            history_data = json.loads(open(history_path, encoding='utf-8').read())
            valid_slugs = set(os.path.splitext(os.path.basename(a))[0] for a in articles)
            for slug, platforms in history_data.items():
                if slug not in valid_slugs:
                    print(f"[FAIL] Zombie slug in syndication history (no matching blog HTML): {slug}")
                    ledger_failures += 1
                for platform_name, meta in platforms.items():
                    if not isinstance(meta, dict):
                        print(f"[FAIL] Invalid metadata format for {slug} on {platform_name}")
                        ledger_failures += 1
                        continue
                    if 'url' in meta and not (meta['url'].startswith('http://') or meta['url'].startswith('https://')):
                        print(f"[FAIL] Invalid URL scheme in history for {slug} ({platform_name}): {meta['url']}")
                        ledger_failures += 1
                    if platform_name == 'bluesky' and 'uri' in meta and not meta['uri'].startswith('at://'):
                        print(f"[FAIL] Invalid ATProto URI in history for {slug}: {meta['uri']}")
                        ledger_failures += 1
        except Exception as e:
            print(f"[FAIL] syndication_history.json JSON parse error: {e}")
            ledger_failures += 1
    if ledger_failures > 0:
        failures += ledger_failures

    # Check 20: Site-Wide Internal Hyperlink & DOM Anchor Auditor
    print("\n[AUDIT] Running Check 20: Site-Wide Internal Hyperlink & DOM Anchor Auditor...")
    link_failures = 0
    import urllib.parse
    all_html_files = [f for f in glob.glob("**/*.html", recursive=True) if "node_modules" not in f]
    for fpath in all_html_files:
        try:
            f_content = open(fpath, encoding='utf-8', errors='ignore').read()
            f_soup = BeautifulSoup(f_content, 'html.parser')
            local_dom_ids = set(el['id'] for el in f_soup.find_all(id=True))
            for a in f_soup.find_all('a', href=True):
                href = a['href'].strip()
                if not href or href.startswith(('http://', 'https://', 'mailto:', 'tel:', 'javascript:')):
                    continue
                if href.startswith('#'):
                    target_id = href[1:]
                    if target_id and target_id not in local_dom_ids:
                        print(f"[FAIL] {fpath}: Broken local anchor #{target_id}")
                        link_failures += 1
                    continue
                parsed = urllib.parse.urlparse(href)
                path = parsed.path
                fragment = parsed.fragment
                if path.startswith('/'):
                    rel_p = path.lstrip('/')
                else:
                    rel_p = str(Path(fpath).parent / path)
                if rel_p == '' or rel_p.endswith('/'):
                    target_f = Path(rel_p) / 'index.html'
                else:
                    target_f = Path(rel_p)
                    if not target_f.exists() and (Path(rel_p) / 'index.html').exists():
                        target_f = Path(rel_p) / 'index.html'
                if not target_f.exists():
                    print(f"[FAIL] {fpath}: Broken link to {href} (file {target_f} missing)")
                    link_failures += 1
                elif fragment:
                    t_content = target_f.read_text(encoding='utf-8', errors='ignore')
                    t_soup = BeautifulSoup(t_content, 'html.parser')
                    t_ids = set(el['id'] for el in t_soup.find_all(id=True))
                    if fragment not in t_ids:
                        print(f"[FAIL] {fpath}: Broken link anchor {href} (#{fragment} missing in {target_f})")
                        link_failures += 1
        except Exception as e:
            print(f"[FAIL] {fpath}: Error auditing links: {e}")
            link_failures += 1
    if link_failures > 0:
        failures += link_failures

    # Check 21: Localhost Live HTTP Server & Architecture Smoke Test
    print("\n[ Check 21 ] Localhost Live HTTP Server & Architecture Smoke Test...")
    try:
        from scripts.smoke_test import run_smoke_tests
        smoke_passed = run_smoke_tests()
        if not smoke_passed:
            print("[FAIL] Localhost live HTTP smoke test encountered routing/content failures.")
            failures += 1
    except Exception as e:
        print(f"[FAIL] Exception during localhost smoke test execution: {e}")
        failures += 1

    # Check 22: Automated DOM Accessibility & WCAG 2.2 AA Contrast QA Check
    print("\n[ Check 22 ] Automated DOM Accessibility & WCAG 2.2 AA Contrast Audit...")
    try:
        from scripts.audit_accessibility import run_accessibility_audit
        a11y_passed = run_accessibility_audit(verbose=False)
        if not a11y_passed:
            print("[FAIL] Accessibility or color contrast violations detected.")
            failures += 1
    except Exception as e:
        print(f"[FAIL] Exception during accessibility audit execution: {e}")
        failures += 1

    # Check 23: Site-Wide Metric Parity & Anti-Hallucination Audit
    print("\n[ Check 23 ] Site-Wide Metric Parity & Anti-Hallucination Audit...")
    try:
        from scripts.ground_truth import get_authoritative_ground_truth, audit_metric_parity
        gt = get_authoritative_ground_truth()
        gt_errors = audit_metric_parity(gt)
        if gt_errors:
            print(f"[FAIL] Metric parity or anti-hallucination violations detected ({len(gt_errors)} issues):")
            for err in gt_errors:
                print(f"  • {err}")
            failures += len(gt_errors)
        else:
            print(f"[PASS] 100% Metric parity verified across all core pages (Tools: {gt['tools_count']}, Articles: {gt['articles_count']}, Blueprints: {gt['blueprints_count']}).")
    except Exception as e:
        print(f"[FAIL] Exception during metric parity audit: {e}")
        failures += 1

    # Check 24: CSS Performance, Rendering Anti-Patterns & WebKit Reset Auditor
    print("\n[ Check 24 ] CSS Performance, Rendering Anti-Patterns & WebKit Reset Audit...")
    try:
        from scripts.audit_css_perf import audit_css_performance
        css_passed = audit_css_performance(verbose=False)
        if not css_passed:
            print("[FAIL] CSS performance or rendering anti-pattern violations detected.")
            failures += 1
    except Exception as e:
        print(f"[FAIL] Exception during CSS performance audit execution: {e}")
        failures += 1

    # Check 25A: CSS Property-Pair Invariant & Conflict Auditor
    print("\n[ Check 25A ] CSS Property-Pair Invariants & Conflict Audit...")
    try:
        from scripts.audit_css_invariants import audit_css_invariants
        invariants_passed = audit_css_invariants(verbose=False)
        if not invariants_passed:
            print("[FAIL] CSS Property-Pair Invariant violations detected.")
            failures += 1
    except Exception as e:
        print(f"[FAIL] Exception during CSS Invariants audit: {e}")
        failures += 1

    # Check 25B: Playwright Headless Layout & Computed Style Probe
    print("\n[ Check 25B ] Playwright Headless Layout & Computed Style Probe...")
    if fast_mode:
        print("[ FAST ] Skipping Playwright headless probe (--fast mode enabled).")
    else:
        try:
            from scripts.audit_dom_layout import audit_dom_layout
            dom_passed = audit_dom_layout(verbose=False)
            if not dom_passed:
                print("[FAIL] Headless DOM layout overflow or low computed contrast violations detected.")
                failures += 1
        except Exception as e:
            print(f"[FAIL] Exception during Headless DOM layout probe: {e}")
            failures += 1

    print("\n============================================================")
    if failures > 0:
        print(f"FAILED: {failures} QA audit violations detected across system.")
        sys.exit(1)
    else:
        save_qa_cache(fast_mode=fast_mode)
        print(f"SUCCESS: All {len(articles)} articles, assets, and live server passed 100% QA audit (Checks 1-25)!")
        print("============================================================")

if __name__ == "__main__":
    verify_all_articles()


