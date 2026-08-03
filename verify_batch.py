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
            
        if errors:
            failures += 1
            print(f"[FAIL] {filename}:")
            for err in errors:
                print(f"       - {err}")
        else:
            print(f"[PASS] {filename} (100% SOP Compliant)")
            
    print("\n============================================================")
    if failures > 0:
        print(f"FAILED: {failures}/{len(articles)} articles did not pass QA audit.")
        sys.exit(1)
    else:
        print(f"SUCCESS: All {len(articles)} articles passed 100% QA audit!")
        print("============================================================")

if __name__ == "__main__":
    verify_all_articles()
