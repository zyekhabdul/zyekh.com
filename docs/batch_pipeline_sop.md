# PROGRAMMATIC ARTICLE GENERATION PIPELINE — STANDARD OPERATING PROCEDURE (SOP)

This document defines the permanent, binding blueprint for programmatically generating, verifying, synchronizing, and publishing high-quality technical article batches on `zyekh.com`.

---

## 1. PIPELINE CORE ARCHITECTURE

The pipeline consists of 5 modular components:

```
[ batch_data.json ] 
        |
        v
[ generate_batch.py ] -----> Produces 100% SOP-compliant HTML files in /blog/
        |
        v
[ verify_batch.py ] -------> Runs 10-axis QA audit (Schema, Meta, Image, IDs, No-Emoji)
        |
        v
[ sync_content.py ] -------> Auto-bumps sw.js CACHE_VERSION, updates sitemap.xml, feed.xml, llms.txt
        |
        v
[ ping_indexers.py ] ------> Pings IndexNow API (Status 200 OK) + Git Push + Cloudflare Purge
```

---

## 2. THE 10 GOLD STANDARD HTML REQUIREMENTS

Every generated `.html` file inside `/blog/` MUST implement all 10 components:

1. **Meta & Social Media Tags**: Canonical URL, Meta Description, Author, RSS (`feed.xml`), Favicons, OpenGraph (`og:image:secure_url`, `og:image:alt`), Twitter Cards (`twitter:creator`, `twitter:site`).
2. **Schema.org JSON-LD**: Multi-graph containing `@type: TechArticle`, `@type: BreadcrumbList`, and `@type: FAQPage`.
3. **Header Navigation**: Custom element `<site-nav active="blog"></site-nav>`.
4. **Article Header & Meta Bar**: `<span class="meta-tag">`, `<h1 class="article-title">`, Author, `<time datetime="...">`, Reading time, `#shareBtn` (Native Web Share API).
5. **Featured Hero Image**: `<figure class="article-hero-wrapper"><picture>` with WebP + JPG fallback, `width="1280" height="720"`, `loading="lazy"`, `decoding="async"`, and `<figcaption>`.
6. **Executive Summary Box**: `<div class="exec-summary">` containing key takeaways.
7. **Table of Contents (ToC)**: `<nav class="toc-card"><ol class="toc-list">` linking to `#heading-id`.
8. **Article Sections**: Every `<h2>` MUST have a unique, slugified `id="..."` and code snippets wrapped in `<pre><code class="language-bash">`.
9. **FAQ Section**: `<div class="faq-section" id="faq"><h2 id="faq">` with `<details><summary>`.
10. **Author Bio & Cross-Links**: `<div class="author-card">` (EEAT/DFIR branding) and `<div class="article-cross-links callout-card">` (valid links to `/tools/*.html`).

---

## 3. JSON INPUT DATA SCHEMA (`batch_data.json`)

```json
[
  {
    "slug": "article-url-slug",
    "title": "Full Article Title Blueprint for 2026",
    "subtitle": "Comprehensive meta description and subtitle for search engines.",
    "category": "Topic Category • Sub-Category",
    "date_published": "YYYY-MM-DD",
    "read_time_mins": 10,
    "word_count": 1400,
    "hero_image": "https://zyekh.com/assets/img/article-hero.jpg",
    "hero_caption": "Caption describing the hero image",
    "exec_summary": [
      "Key Takeaway 1",
      "Key Takeaway 2"
    ],
    "sections": [
      {
        "id": "section-id-slug",
        "h2_title": "1. Section Heading Title",
        "content_paragraphs": [
          "Paragraph content..."
        ],
        "code_block": "command or code snippet",
        "code_language": "bash"
      }
    ],
    "faqs": [
      {
        "question": "Frequently asked question text?",
        "answer": "Detailed answer text."
      }
    ],
    "related_tools": [
      {"name": "Tool Name", "url": "/tools/tool-name.html"}
    ]
  }
]
```

---

## 4. THUMBNAIL IMAGE GENERATION POLICY

- Each article MUST have a unique 16:9 banner image in `assets/img/` (`.jpg` and `.webp`).
- If API capacity is unavailable, generate high-resolution banners locally using Pillow (`python3 -c "... create_tech_banner ..."`).

---

## 5. AUTOMATED VERIFICATION & PUBLISHING COMMANDS

```bash
# 1. Generate HTML files from batch_data.json
python3 generate_batch.py

# 2. Run QA verification script
python3 verify_batch.py

# 3. Synchronize sitemap, feed.xml, llms.txt, sw.js CACHE_VERSION, and HTML query strings
python3 sync_content.py

# 4. Trigger IndexNow API
python3 ping_indexers.py
```

---

## 6. ZERO EMOJI POLICY & CACHE SOP

- **Strict No Emoji**: Never insert emojis in HTML, CSS, JS, JSON, or Markdown. Use text tags like `[ VERIFIED ]`, `[ NOTE ]`, `[ WARN ]`, `[ INFO ]`, `•`, `->`.
- **Cache Version Bump**: Always bump `CACHE_VERSION` in `sw.js` and query strings `?v=...` across all HTML files upon modifying CSS/JS/HTML.
