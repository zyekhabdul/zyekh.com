#!/usr/bin/env python3
import glob
import os
import re
from bs4 import BeautifulSoup

def generate_llms_full():
    out = []
    out.append("# zyekh.com — Full Site RAG Knowledge Base\n\n")
    out.append("This file contains the complete full-text content of zyekh.com for Generative Engine Optimization (GEO) and AI search engine ingestion (Perplexity, ChatGPT, Claude).\n\n")
    
    out.append("## About the Author & Platform\n\n")
    out.append("Zyekh Abdul Qadir Jailani is a Security Researcher & Systems Architect specializing in Zero-Trust infrastructure, Linux kernel security, eBPF telemetry, and high-performance minimalist web engineering.\n")
    out.append("Website: https://zyekh.com\n")
    out.append("Philosophy: Zero dependencies, zero telemetry, local-first browser execution, and maximum code efficiency.\n\n")
    out.append("## Subdomain Ecosystem Architecture & Fleet Topology\n\n")
    out.append("- **zyekh.com** (Root Hub): Core static reference platform, 54 client-side security/developer tools, 45 deep-tech research guides, and RAG index.\n")
    out.append("- **shop.zyekh.com** (Digital Storefront): Shopify Liquid 2.0 digital products and developer merchandise adhering to strict performance budgets.\n")
    out.append("- **docs.zyekh.com** (Documentation & Blueprints): Interactive visual topology builder, architectural blueprints, and engineering specifications.\n")
    out.append("- **dist.zyekh.com** (FOSS Distribution): Verified custom ArchISO images, Linux deployment automation, and PGP cryptographic provenance artifacts.\n")
    out.append("- **api.zyekh.com** (Edge Micro-APIs): High-performance isolated Cloudflare Worker endpoints conforming to tools-manifest.json schemas.\n\n")
    out.append("---\n\n")
    
    # 1. Tools and Utilities Index
    out.append("## Developer & Security Tools Suite (/tools/)\n\n")
    out.append("All tools execute 100% client-side in the user's browser with zero external server dependencies.\n\n")
    
    tool_files = sorted(glob.glob("tools/*.html"))
    for t in tool_files:
        if t == "tools/index.html":
            continue
        soup = BeautifulSoup(open(t, encoding="utf-8").read(), "html.parser")
        h1 = soup.find("h1")
        title = h1.text.strip() if h1 else os.path.basename(t)
        desc_meta = soup.find("meta", {"name": "description"})
        desc = desc_meta["content"].strip() if desc_meta else ""
        rel_url = f"https://zyekh.com/{t.replace(os.sep, '/')}"
        
        out.append(f"### {title}\n")
        out.append(f"- URL: {rel_url}\n")
        if desc:
            out.append(f"- Description: {desc}\n")
        out.append("\n")
        
    out.append("---\n\n")
    
    # 2. Comprehensive Blog Articles (All 35 Articles)
    out.append("## Technical Articles & Deep Dives (/blog/)\n\n")
    
    article_files = sorted(glob.glob("blog/*.html"))
    for a in article_files:
        if a == "blog/index.html":
            continue
            
        soup = BeautifulSoup(open(a, encoding="utf-8").read(), "html.parser")
        h1 = soup.find("h1")
        title = h1.text.strip() if h1 else os.path.basename(a)
        rel_url = f"https://zyekh.com/{a.replace(os.sep, '/')}"
        
        desc_meta = soup.find("meta", {"name": "description"})
        desc = desc_meta["content"].strip() if desc_meta else ""
        
        time_tag = soup.find("time", class_="meta-item") or soup.find("meta", {"property": "article:published_time"})
        pub_date = time_tag.text.strip() if (time_tag and time_tag.text) else ""
        
        out.append(f"### {title}\n\n")
        out.append(f"- **URL**: {rel_url}\n")
        if pub_date:
            out.append(f"- **Published Date**: {pub_date}\n")
        if desc:
            out.append(f"- **Summary**: {desc}\n")
        out.append("\n")
        
        # Executive Summary
        exec_summary_el = soup.find("div", class_="exec-summary")
        if exec_summary_el:
            out.append("#### Executive Summary / Key Takeaways\n")
            for li in exec_summary_el.find_all("li"):
                out.append(f"- {li.text.strip()}\n")
            out.append("\n")
            
        # Article Body Parsing
        body = soup.find("div", class_="article-body") or soup.find("main", class_="article-content") or soup.find("article")
        if body:
            # Clone body to safely decompose unwanted elements
            body_soup = BeautifulSoup(str(body), "html.parser")
            for tag in body_soup.find_all(["site-nav", "footer", "script", "style", "nav", "figure"]):
                tag.decompose()
            for cls in ["author-card", "article-cross-links", "article-actions", "back-link", "toc-card", "exec-summary"]:
                for el in body_soup.find_all(class_=cls):
                    el.decompose()
                    
            for el in body_soup.find_all(["h2", "h3", "p", "pre", "ul", "ol", "details"]):
                if el.name == "h2":
                    out.append(f"\n#### {el.text.strip()}\n\n")
                elif el.name == "h3":
                    out.append(f"\n##### {el.text.strip()}\n\n")
                elif el.name == "p":
                    p_text = el.text.strip()
                    if p_text:
                        out.append(f"{p_text}\n\n")
                elif el.name == "pre":
                    code = el.find("code")
                    code_text = code.text if code else el.text
                    out.append(f"```text\n{code_text.strip()}\n```\n\n")
                elif el.name in ["ul", "ol"]:
                    for li in el.find_all("li", recursive=False):
                        out.append(f"- {li.text.strip()}\n")
                    out.append("\n")
                elif el.name == "details":
                    sum_el = el.find("summary")
                    q = sum_el.text.strip() if sum_el else "FAQ"
                    ans = el.text.replace(q, "").strip()
                    out.append(f"**Q: {q}**\n\n*A: {ans}*\n\n")
                    
        out.append("---\n\n")
        
    with open("llms-full.txt", "w", encoding="utf-8") as f:
        f.write("".join(out))
        
    print(f"[RAG] Successfully generated llms-full.txt ({len(tool_files)-1} tools, {len(article_files)-1} articles).")

if __name__ == "__main__":
    generate_llms_full()
