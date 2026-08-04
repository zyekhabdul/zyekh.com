#!/usr/bin/env python3
import glob
import os
import re
import datetime
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def sync_all(bump_version=True):
    print("[SYNC] Starting automated RAG, Sitemap, RSS & Cache Version Synchronization...")

    sw_path = "sw.js"
    sw_ver = "v78"
    
    if os.path.exists(sw_path):
        sw_c = open(sw_path, "r", encoding="utf-8").read()
        m = re.search(r"CACHE_VERSION = 'v(\d+)';", sw_c)
        if m and bump_version:
            curr_v = int(m.group(1))
            next_v = curr_v + 1
            sw_ver = f"v{next_v}"
            sw_c = re.sub(r"CACHE_VERSION = 'v\d+';", f"CACHE_VERSION = '{sw_ver}';", sw_c)
            open(sw_path, "w", encoding="utf-8").write(sw_c)
            print(f"[SYNC] Auto-bumped sw.js CACHE_VERSION: v{curr_v} -> {sw_ver}")
        elif m:
            sw_ver = f"v{m.group(1)}"

    today_str = datetime.date.today().strftime("%Y%m%d")
    new_ver = f"{today_str}_{sw_ver}"
    base_url = "https://zyekh.com"

    # 2. Update HTML query version string across all HTML files
    html_files = sorted(glob.glob("**/*.html", recursive=True))
    for f in html_files:
        c = open(f, "r", encoding="utf-8").read()
        c = re.sub(r"site-nav\.js(\?v=[^\"]*)?", f"site-nav.js?v={new_ver}", c)
        c = re.sub(r"shared\.css(\?v=[^\"]*)?", f"shared.css?v={new_ver}", c)
        c = re.sub(r"blog\.css(\?v=[^\"]*)?", f"blog.css?v={new_ver}", c)
        open(f, "w", encoding="utf-8").write(c)
    print(f"[SYNC] Updated query version ?v={new_ver} across {len(html_files)} HTML files.")

    # 3. Regenerate sitemap.xml dynamically
    urls_data = []
    # Static primary pages
    urls_data.append((f"{base_url}/", "2026-08-03", "weekly", "1.0"))
    urls_data.append((f"{base_url}/about/", "2026-08-03", "weekly", "0.9"))
    urls_data.append((f"{base_url}/tools/", "2026-08-03", "weekly", "0.9"))
    urls_data.append((f"{base_url}/blog/", "2026-08-03", "weekly", "0.9"))

    # Blog Articles
    for b in sorted(glob.glob("blog/*.html")):
        if b == "blog/index.html":
            continue
        rel_path = b.replace("\\", "/")
        urls_data.append((f"{base_url}/{rel_path}", "2026-08-03", "weekly", "0.9"))

    # Tools
    for t in sorted(glob.glob("tools/*.html")):
        if t == "tools/index.html":
            continue
        rel_path = t.replace("\\", "/")
        urls_data.append((f"{base_url}/{rel_path}", "2026-08-03", "weekly", "0.8"))

    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, lastmod, freq, prio in urls_data:
        sitemap_lines.append(f'  <url><loc>{url}</loc><lastmod>{lastmod}</lastmod><changefreq>{freq}</changefreq><priority>{prio}</priority></url>')
    sitemap_lines.append('</urlset>\n')

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_lines))
    print(f"[SYNC] Regenerated sitemap.xml with {len(urls_data)} URLs.")

    # 4. Extract blog articles for RSS feed.xml & llms.txt
    article_meta = []
    for b in sorted(glob.glob("blog/*.html")):
        if b == "blog/index.html":
            continue
        soup = BeautifulSoup(open(b, encoding="utf-8").read(), "html.parser")
        h1 = soup.find("h1")
        title = h1.text.strip() if h1 else b
        desc_meta = soup.find("meta", {"name": "description"})
        desc = desc_meta["content"].strip() if desc_meta else title
        
        time_tag = soup.find("time", class_="meta-item") or soup.find("meta", {"property": "article:published_time"})
        pub_date_str = "Mon, 03 Aug 2026 00:00:00 GMT"
        if time_tag:
            raw_date = time_tag.get("datetime") or time_tag.get("content")
            if raw_date and len(raw_date) >= 10:
                try:
                    dt = datetime.datetime.strptime(raw_date[:10], "%Y-%m-%d")
                    pub_date_str = dt.strftime("%a, %d %b %Y 00:00:00 GMT")
                except ValueError:
                    pass

        rel_url = f"{base_url}/" + b.replace("\\", "/")
        article_meta.append({"title": title, "url": rel_url, "desc": desc, "pub_date": pub_date_str})

    # Update feed.xml
    feed_items = []
    for item in article_meta:
        feed_items.append(f"""    <item>
      <title>{item['title']}</title>
      <link>{item['url']}</link>
      <guid>{item['url']}</guid>
      <description>{item['desc']}</description>
      <pubDate>{item['pub_date']}</pubDate>
    </item>""")

    feed_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2004/08/atom">
  <channel>
    <title>zyekh.com — Technical Articles &amp; Security Insights</title>
    <link>https://zyekh.com/blog/</link>
    <description>Technical articles, Linux kernel news, system hardening guides, and cybersecurity research by Zyekh Abdul Qadir Jailani.</description>
    <language>en-us</language>
    <atom:link href="https://zyekh.com/feed.xml" rel="self" type="application/rss+xml" />
{chr(10).join(feed_items)}
  </channel>
</rss>
"""
    with open("feed.xml", "w", encoding="utf-8") as f:
        f.write(feed_xml)
    print(f"[SYNC] Updated feed.xml with {len(article_meta)} articles.")

    # Update llms.txt & llms-full.txt RAG Knowledge Base
    llms_txt = """# zyekh.com — LLM RAG Knowledge Base

> Official portfolio, technical articles, Linux security blueprints, and 42+ client-side web utility tools by Zyekh Abdul Qadir Jailani (Full Stack Developer & Security Researcher).

## Technical Blog & Security Guides
"""
    for a in article_meta:
        llms_txt += f"- [{a['title']}]({a['url']}): {a['desc']}\n"

    llms_txt += """
## Privacy-First Client-Side Web Utilities (/tools/)
- 42+ Client-Side Tools: Zakat, PPh 21, THR, KPR, JHT, JKP, Pesangon, Password Generator, QR Code Generator, Hash Generator, HMAC, Subnet Calculator, SQL Formatter, Diff Checker, AI Token Estimator, Regex Tester, Base64, JSON Formatter, etc.
- All tools execute 100% in-browser with zero server data collection.
"""
    with open("llms.txt", "w", encoding="utf-8") as f:
        f.write(llms_txt)
    print("[SYNC] Updated llms.txt RAG knowledge base.")

    # 5. Harmonize blog/index.html card category hashtags from article sources
    index_path = "blog/index.html"
    if os.path.exists(index_path):
        soup_index = BeautifulSoup(open(index_path, "r", encoding="utf-8").read(), "html.parser")
        updated = False
        for card in soup_index.find_all("article", class_="article-card"):
            link = card.find("a", href=True)
            if not link:
                continue
            href = link["href"].lstrip("/")
            if not os.path.exists(href):
                continue
            art_soup = BeautifulSoup(open(href, "r", encoding="utf-8").read(), "html.parser")
            meta_span = art_soup.find("span", class_="meta-tag")
            if not meta_span:
                continue
            cat_text = meta_span.text.strip()
            parts = [p.strip() for p in re.split(r'[•,/|]+', cat_text) if p.strip()]
            hashtags = [f"#{re.sub(r'[^a-zA-Z0-9]', '', p)}" for p in parts if p]
            tags_div = card.find("div", class_="tags-container")
            if tags_div and hashtags:
                new_tags_html = "\n".join([f'<span class="meta-tag">{h}</span>' for h in hashtags])
                tags_div.clear()
                for h in hashtags:
                    tag_span = soup_index.new_tag("span", attrs={"class": "meta-tag"})
                    tag_span.string = h
                    tags_div.append(tag_span)
                updated = True
        if updated:
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(str(soup_index))
            print(f"[SYNC] Harmonized category hashtags in {index_path} from article sources.")

    print("[SYNC] Synchronization completed successfully!")

if __name__ == "__main__":
    sync_all()
