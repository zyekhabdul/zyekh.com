#!/usr/bin/env python3
import json
import os
import re
import glob
from bs4 import BeautifulSoup

def slugify(text):
    """Convert string to clean URL-friendly slug."""
    text = text.lower().strip()
    slug = re.sub(r'[^a-z0-9]+', '-', text).strip('-')
    return slug or 'section'

def generate_article_html(article_data, current_cache_ver="20260803_v84"):
    """Generate 100% SOP Gold Standard Compliant HTML for a blog article."""
    
    slug = article_data['slug']
    title = article_data['title']
    subtitle = article_data.get('subtitle', '')
    category = article_data.get('category', 'Cyber Security')
    date_pub = article_data.get('date_published', '2026-08-03')
    read_time = article_data.get('read_time_mins', 10)
    word_count = article_data.get('word_count', 1200)
    hero_img = article_data.get('hero_image', 'https://zyekh.com/assets/img/vps-hardening.jpg')
    hero_caption = article_data.get('hero_caption', title)
    exec_summary = article_data.get('exec_summary', [])
    sections = article_data.get('sections', [])
    faqs = article_data.get('faqs', [])
    related_tools = article_data.get('related_tools', [])
    
    canonical_url = f"https://zyekh.com/blog/{slug}.html"
    
    # 1. Build TOC items & Headings with IDs
    toc_items = []
    sections_html = []
    
    for idx, sec in enumerate(sections, 1):
        sec_h2 = sec.get('h2_title', f"Section {idx}")
        sec_id = sec.get('id') or slugify(sec_h2)
        toc_items.append(f'<li><a href="#{sec_id}">{sec_h2}</a></li>')
        
        sec_block = [f'<h2 id="{sec_id}">{sec_h2}</h2>']
        for p in sec.get('content_paragraphs', []):
            sec_block.append(f'<p>{p}</p>')
            
        if sec.get('code_block'):
            lang = sec.get('code_language', 'bash')
            sec_block.append(f'<pre><code class="language-{lang}">{sec["code_block"]}</code></pre>')
            
        sections_html.append("\n".join(sec_block))

    if faqs:
        toc_items.append('<li><a href="#faq">Frequently Asked Questions (FAQ)</a></li>')
        
    toc_html = "\n".join(toc_items)
    sections_rendered = "\n\n".join(sections_html)
    
    # 2. Executive Summary LI elements
    exec_summary_html = "\n".join([f"<li>{item}</li>" for item in exec_summary])
    
    # 3. FAQ elements
    faq_elements = []
    faq_schema_items = []
    for faq in faqs:
        q = faq['question']
        a = faq['answer']
        faq_elements.append(f"""<details>
  <summary>{q}</summary>
  <p style="padding: 1rem 1.25rem; margin: 0; color: var(--text-muted);">{a}</p>
</details>""")
        faq_schema_items.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": a
            }
        })
        
    faq_rendered = "\n".join(faq_elements)
    
    # 4. Related Tools HTML
    tools_links_html = []
    for tool in related_tools:
        tools_links_html.append(f'<a class="blog-badge" href="{tool["url"]}">{tool["name"]}</a>')
    tools_text = " dan ".join(tools_links_html) if tools_links_html else '<a class="blog-badge" href="/tools/password.html">Secure Password Generator</a>'

    # Schema JSON-LD Graph
    schema_graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "TechArticle",
                "headline": title,
                "description": subtitle or title,
                "url": canonical_url,
                "image": hero_img,
                "datePublished": date_pub,
                "dateModified": date_pub,
                "wordCount": word_count,
                "inLanguage": "en-US",
                "author": {
                    "@type": "Person",
                    "name": "Zyekh Abdul Qadir Jailani",
                    "url": "https://zyekh.com/"
                },
                "publisher": {
                    "@type": "Person",
                    "name": "Zyekh Abdul Qadir Jailani",
                    "url": "https://zyekh.com/"
                },
                "mainEntityOfPage": {
                    "@type": "WebPage",
                    "@id": canonical_url
                }
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://zyekh.com/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog & Articles", "item": "https://zyekh.com/blog/"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": canonical_url}
                ]
            }
        ]
    }
    
    if faq_schema_items:
        schema_graph["@graph"].append({
            "@type": "FAQPage",
            "mainEntity": faq_schema_items
        })
        
    schema_json_str = json.dumps(schema_graph, indent=2)

    # Complete 100% SOP Compliant HTML Template
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<link as="font" crossorigin="" href="/assets/fonts/outfit-700-normal.woff2" rel="preload" type="font/woff2"/>
<meta content="#09090b" name="theme-color"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>{title} — zyekh.com</title>
<meta content="{subtitle or title}" name="description"/>
<meta content="Zyekh Abdul Qadir Jailani" name="author"/>
<link href="https://zyekh.com/feed.xml" rel="alternate" title="zyekh.com RSS Feed" type="application/rss+xml"/>
<link href="{canonical_url}" rel="canonical"/>

<!-- Open Graph / Social Meta Tags -->
<meta content="zyekh.com" property="og:site_name"/>
<meta content="article" property="og:type"/>
<meta content="{title}" property="og:title"/>
<meta content="{subtitle or title}" property="og:description"/>
<meta content="{canonical_url}" property="og:url"/>
<meta content="1280" property="og:image:width"/>
<meta content="720" property="og:image:height"/>
<meta content="https://zyekh.com" property="article:publisher"/>
<meta content="{hero_img}" property="og:image"/>
<meta content="{hero_img}" property="og:image:secure_url"/>
<meta content="image/jpeg" property="og:image:type"/>
<meta content="{title} — zyekh.com" property="og:image:alt"/>
<meta content="{date_pub}T00:00:00Z" property="article:published_time"/>
<meta content="Zyekh Abdul Qadir Jailani" property="article:author"/>
<meta content="@zyekh" name="twitter:creator"/>
<meta content="@zyekh" name="twitter:site"/>
<meta content="summary_large_image" name="twitter:card"/>
<meta content="{title}" name="twitter:title"/>
<meta content="{subtitle or title}" name="twitter:description"/>
<meta content="{hero_img}" name="twitter:image"/>
<meta content="{title} — zyekh.com" name="twitter:image:alt"/>

<!-- Favicons & Manifest -->
<link href="/assets/icons/favicon.ico" rel="icon" type="image/x-icon"/>
<link href="/assets/icons/favicon-32x32.png" rel="icon" sizes="32x32" type="image/png"/>
<link href="/assets/icons/favicon-16x16.png" rel="icon" sizes="16x16" type="image/png"/>
<link href="/assets/icons/apple-icon-180x180.png" rel="apple-touch-icon" sizes="180x180"/>
<link href="/manifest.json" rel="manifest"/>

<!-- Schema.org JSON-LD -->
<script type="application/ld+json">
{schema_json_str}
</script>
<link href="/assets/fonts/fonts.css?v={current_cache_ver}" rel="stylesheet"/>
<link href="/assets/css/shared.css?v={current_cache_ver}" rel="stylesheet"/>
<link href="/assets/css/blog.css?v={current_cache_ver}" rel="stylesheet"/>
<script defer="" src="/assets/js/site-nav.js?v={current_cache_ver}"></script>
</head>
<body>
<!-- Pure CSS Scroll-Driven Reading Progress Bar -->
<div class="reading-progress-bar"></div>

<!-- Header Navigation -->
<site-nav active="blog"></site-nav>

<article class="container-article" itemscope="" itemtype="https://schema.org/TechArticle">
  <!-- Back to Blog -->
  <a class="back-link" href="/blog/">← Back to Articles</a>

  <!-- Article Header -->
  <header class="article-header">
    <span class="meta-tag">{category}</span>
    <h1 class="article-title">{title}</h1>
    <div class="article-meta">
      <span>By Zyekh Abdul Qadir Jailani</span>
      <time class="meta-item" datetime="{date_pub}T00:00:00Z">Published: {date_pub}</time>
      <span>{read_time} min read ({word_count}+ Words)</span>
      <button class="btn-share" id="shareBtn" style="background: transparent; border: 1px solid var(--border-color); color: var(--text-main); font-size: 0.75rem; padding: 0.15rem 0.6rem; border-radius: 4px; cursor: pointer; margin-left: auto; transition: all var(--transition);" type="button">[ SHARE ARTICLE ]</button>
    </div>
  </header>

  <!-- Article Body Content -->
  <main class="article-content">
    <!-- Featured Hero Image -->
    <figure class="article-hero-wrapper">
      <picture>
        <source srcset="{hero_img.replace('.jpg', '.webp')}" type="image/webp"/>
        <img alt="{title}" class="article-hero-img" decoding="async" height="720" itemprop="image" loading="lazy" src="{hero_img}" width="1280"/>
      </picture>
      <figcaption class="hero-caption">{hero_caption}</figcaption>
    </figure>

    <!-- Executive Summary / Takeaways Box -->
    <div class="exec-summary">
      <div class="exec-summary-title">Executive Summary &amp; Key Security Takeaways</div>
      <ul>
{exec_summary_html}
      </ul>
    </div>

    <!-- Table of Contents -->
    <nav class="toc-card">
      <div class="toc-title">Table of Contents</div>
      <ol class="toc-list">
{toc_html}
      </ol>
    </nav>

{sections_rendered}

    <!-- FAQ Section -->
    <div class="faq-section" id="faq">
      <h2 id="faq">Frequently Asked Questions (FAQ)</h2>
{faq_rendered}
    </div>

    <!-- Author Bio Card (EEAT & DFIR Branding) -->
    <div class="author-card">
      <img alt="Zyekh Abdul Qadir Jailani" class="author-avatar" decoding="async" height="60" loading="lazy" src="/assets/img/profile.webp" width="60"/>
      <div class="author-info">
        <h4>Written by Zyekh Abdul Qadir Jailani</h4>
        <p>Digital Forensics &amp; Incident Response (DFIR) Specialist &amp; Security Researcher specializing in Linux kernel hardening, threat hunting, and system security research.</p>
        <div class="author-social-links" style="margin-top:0.4rem; font-size:0.85rem; color:var(--text-muted);">
          <a href="https://www.linkedin.com/in/zyekh-abdul-qadir-jailani/" rel="noopener" style="font-weight:600" target="_blank">LinkedIn</a> •
          <a href="https://github.com/zyekhabdul" rel="noopener" style="font-weight:600" target="_blank">GitHub</a> •
          <a href="https://discord.gg/jDmerBugvu" rel="noopener" style="font-weight:600" target="_blank">Discord</a> •
          <a href="mailto:zyekhabdulqadirjailani@gmail.com" style="font-weight:600">Email</a> •
          <a href="/gpg-key.asc" style="font-weight:600" target="_blank">PGP Key</a>
        </div>
      </div>
    </div>

    <!-- Related Tools Recommendation -->
    <div class="article-cross-links callout-card">
      <h4 class="heading-reset">Utility Security Tools Related to this Article:</h4>
      <p class="note-sm">
        Gunakan {tools_text} untuk membantu alur kerja konfigurasi keamanan Anda secara privasi di browser.
      </p>
    </div>
  </main>

  <!-- Footer -->
  <footer class="footer">
    <p>© 2026 <strong>zyekh.com</strong> — Zyekh Abdul Qadir Jailani. All rights reserved.</p>
  </footer>
</article>
<script defer="" src="/assets/js/site-nav.js?v={current_cache_ver}"></script>
</body>
</html>"""
    
    output_path = os.path.join("blog", f"{slug}.html")
    with open(output_path, "w", encoding="utf-8") as out:
        out.write(full_html)
        
    print(f"[GENERATOR] Successfully created {output_path}")

def process_batch(json_file):
    if not os.path.exists(json_file):
        print(f"[Error] Input JSON file {json_file} not found!")
        return
        
    data = json.load(open(json_file, encoding='utf-8'))
    articles = data if isinstance(data, list) else [data]
    
    print(f"[GENERATOR] Processing batch of {len(articles)} articles from {json_file}...")
    for art in articles:
        generate_article_html(art)
        
    print(f"[GENERATOR] Batch processing completed for {len(articles)} articles.")

if __name__ == "__main__":
    process_batch("batch_data.json")
