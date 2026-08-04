# PROGRAMMATIC ARTICLE GENERATION PIPELINE — STANDARD OPERATING PROCEDURE (SOP)

This document defines the permanent, binding blueprint for programmatically generating, verifying, synchronizing, and publishing high-quality technical article batches on `zyekh.com`.

---

## 1. PIPELINE CORE ARCHITECTURE

The pipeline consists of 5 modular components orchestrated by a master runner:

```
[ batch_data.json ] 
        |
        v
[ generate_batch.py ] -----> Produces 100% SOP-compliant HTML files in /blog/
        |
        v
[ verify_batch.py ] -------> Runs 14-axis QA audit (Word count >=800, H2 >=4, Schema, Meta, Image, IDs, No-Emoji)
        |
        v
[ sync_content.py ] -------> Renders blog/index.html cards, auto-bumps sw.js CACHE_VERSION, updates sitemap, feed.xml, llms.txt
        |
        v
[ ping_indexers.py ] ------> Pings IndexNow API (Status 200 OK) + Git Push + Cloudflare Purge
```

Master Orchestration Command:
```bash
python3 run_pipeline.py --deploy
```

---

## 2. THE 14 GOLD STANDARD QA AUDIT REQUIREMENTS

Every generated `.html` file inside `/blog/` MUST implement all 14 components:

1. **Meta & Social Media Tags**: Canonical URL, Meta Description, Author, RSS (`feed.xml`), Favicons, OpenGraph (`og:image:secure_url`, `og:image:alt`), Twitter Cards (`twitter:creator`, `twitter:site`).
2. **Schema.org JSON-LD**: Multi-graph containing `@type: TechArticle`, `@type: BreadcrumbList`, and `@type: FAQPage`.
3. **Header Navigation**: Custom element `<site-nav active="blog"></site-nav>`.
4. **Article Header & Meta Bar**: `<span class="meta-tag">`, `<h1 class="article-title">`, Author, `<time datetime="...">`, Reading time, `#shareBtn` (Native Web Share API).
5. **Featured Hero Image**: `<figure class="article-hero-wrapper"><picture>` with WebP + JPG fallback, `width="1280" height="720"`, `loading="lazy"`, `decoding="async"`, and `<figcaption>`.
6. **Executive Summary Box**: `<div class="exec-summary">` containing key takeaways.
7. **Table of Contents (ToC)**: `<nav class="toc-card"><ol class="toc-list">` linking to `#heading-id`.
8. **Article Sections**: Every `<h2>` MUST have a unique, slugified `id="..."` and code snippets wrapped in `<pre><code class="language-bash">`.
9. **FAQ Section**: `<div class="faq-section"><h2 id="faq">` with `<details><summary>`.
10. **Author Bio & Cross-Links**: `<div class="author-card">` (EEAT/DFIR branding) and `<div class="article-cross-links callout-card">` (valid links to `/tools/*.html`).
11. **Element ID Uniqueness**: 0 duplicate IDs allowed across document DOM trees.
12. **Single Navigation Script Tag**: Exactly 1 `<script src="site-nav.js">` per page.
13. **Minimum Technical Depth Threshold**: Word count MUST be >= 800 words (Target: 1,200 - 1,600+ words).
14. **Minimum Section Depth**: Section H2 count MUST be >= 4 sections.

---

## 3. JSON INPUT DATA SCHEMA (`batch_data.json` & `batch_data_template.json`)

To prepare Batch 2 or any future article batch, copy [`batch_data_template.json`](file:///home/fuckadmin/.git-clone/zyekh.com/batch_data_template.json) to `batch_data.json` and fill in the structured array:

```json
[
  {
    "slug": "article-url-slug",
    "title": "Full Article Title Blueprint for 2026",
    "subtitle": "Comprehensive meta description and subtitle for search engines.",
    "category": "Topic Category • Sub-Category",
    "tags": ["#TopicCategory", "#SubCategory"],
    "date_published": "YYYY-MM-DD",
    "read_time_mins": 12,
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
- All WebP images must be compressed under 100 KB target payload.

---

## 5. MASTER AUTOMATED VERIFICATION & PUBLISHING PIPELINE

Execute all pipeline stages, audits, syncs, indexer pings, git push, and Cloudflare purge using a single command:

```bash
python3 run_pipeline.py --deploy
```

---

## 6. ZERO EMOJI POLICY & CACHE SOP

- **Strict No Emoji**: Never insert emojis in HTML, CSS, JS, JSON, or Markdown. Use text tags like `[ VERIFIED ]`, `[ NOTE ]`, `[ WARN ]`, `[ INFO ]`, `•`, `->`.
- **Cache Version Bump**: Always bump `CACHE_VERSION` in `sw.js` and query strings `?v=...` across all HTML files upon modifying CSS/JS/HTML.
