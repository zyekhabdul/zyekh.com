#!/usr/bin/env python3
import glob
import os
import sys
from bs4 import BeautifulSoup

def verify_all_articles():
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
    if not os.path.exists(manifest_path):
        print(f"[FAIL] Manifest file missing: {manifest_path}")
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

    print("\n============================================================")
    if failures > 0:
        print(f"FAILED: {failures} QA audit violations detected across articles/images.")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {len(articles)} articles passed 100% QA audit (Checks 1-16)!")
        print("============================================================")

if __name__ == "__main__":
    verify_all_articles()

