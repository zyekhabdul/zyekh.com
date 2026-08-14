#!/usr/bin/env python3
import os
import sys
import argparse
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import glob
import re
import json
import html
import webbrowser

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(BASE_DIR, "blog")
BASE_URL = "https://zyekh.com"

SUBREDDITS = [
    {"name": "r/netsec", "desc": "Network Security & Cyber Architecture"},
    {"name": "r/linux", "desc": "Linux Kernel & VPS Security Hardening"},
    {"name": "r/programming", "desc": "General Technical & Software Engineering"},
    {"name": "r/SelfHost", "desc": "Self-Hosted & Privacy Infrastructure"},
    {"name": "r/webdev", "desc": "Web Performance, PWA & Frontend Architecture"},
    {"name": "r/devops", "desc": "Cloud Infrastructure & Container Security"}
]

def load_dotenv():
    env_file = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ[k.strip()] = v.strip()

def parse_article_metadata(filepath):
    content = open(filepath, 'r', encoding='utf-8').read()
    
    # Title
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    title = html.unescape(title_match.group(1).strip()) if title_match else os.path.basename(filepath)
    title = re.sub(r'\s*—\s*zyekh\.com.*', '', title)
    title = re.sub(r'\s*\|\s*zyekh\.com.*', '', title)

    # Description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE | re.DOTALL)
    description = html.unescape(desc_match.group(1).strip()) if desc_match else ""

    # Slug / Relative URL
    rel_path = os.path.relpath(filepath, BASE_DIR)
    url = f"{BASE_URL}/{rel_path}"

    # Exec Summary / TL;DR text
    exec_summary = ""
    summary_match = re.search(r'<div class=["\']exec-summary["\']>(.*?)</div>', content, re.IGNORECASE | re.DOTALL)
    if summary_match:
        clean_text = re.sub(r'<[^>]+>', '', summary_match.group(1)).strip()
        clean_text = ' '.join(clean_text.split())
        exec_summary = html.unescape(clean_text)

    # Article Body Content (Markdown-like summary for Dev.to)
    article_body = ""
    body_match = re.search(r'<article[^>]*>(.*?)</article>', content, re.IGNORECASE | re.DOTALL)
    if body_match:
        clean_body = re.sub(r'<script[^>]*>.*?</script>', '', body_match.group(1), flags=re.DOTALL)
        clean_body = re.sub(r'<style[^>]*>.*?</style>', '', clean_body, flags=re.DOTALL)
        clean_body = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n\n## \1\n\n', clean_body)
        clean_body = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n\n### \1\n\n', clean_body)
        clean_body = re.sub(r'<p[^>]*>(.*?)</p>', r'\n\1\n', clean_body)
        clean_body = re.sub(r'<li[^>]*>(.*?)</li>', r'* \1\n', clean_body)
        clean_body = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', clean_body)
        clean_body = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', r'\n```\n\1\n```\n', clean_body, flags=re.DOTALL)
        clean_body = re.sub(r'<[^>]+>', '', clean_body)
        clean_body = html.unescape(clean_body)
        clean_body = re.sub(r'\n{3,}', '\n\n', clean_body).strip()
        article_body = clean_body

    return {
        'title': title,
        'description': description,
        'url': url,
        'exec_summary': exec_summary,
        'body': article_body,
        'filename': os.path.basename(filepath)
    }

def get_all_articles():
    html_files = sorted(glob.glob(os.path.join(BLOG_DIR, "*.html")))
    articles = []
    for f in html_files:
        if os.path.basename(f) != "index.html":
            articles.append(parse_article_metadata(f))
    return articles

def generate_reddit_intent_url(subreddit, title, url):
    sub = subreddit.replace("r/", "")
    encoded_title = urllib.parse.quote(title)
    encoded_url = urllib.parse.quote(url)
    return f"https://www.reddit.com/r/{sub}/submit?title={encoded_title}&url={encoded_url}"

def generate_hn_intent_url(title, url):
    encoded_title = urllib.parse.quote(title)
    encoded_url = urllib.parse.quote(url)
    return f"https://news.ycombinator.com/submitlink?u={encoded_url}&t={encoded_title}"

def generate_mastodon_intent_url(title, url):
    text = f"{title}\n\n[ Read Full Article -> ] {url}\n\n#Security #Linux #DevOps #Engineering"
    encoded_text = urllib.parse.quote(text)
    return f"https://infosec.exchange/share?text={encoded_text}"

def publish_mastodon(article):
    load_dotenv()
    token = os.environ.get('MASTODON_ACCESS_TOKEN')
    server = os.environ.get('MASTODON_SERVER', 'https://infosec.exchange')
    if not token:
        print("[ WARN ] MASTODON_ACCESS_TOKEN not set in environment or .env file.")
        return False

    status_text = f"{article['title']}\n\n{article['description']}\n\n[ Read Full Article -> ] {article['url']}\n\n#Security #Linux #DevOps #Engineering"
    endpoint = f"{server.rstrip('/')}/api/v1/statuses"
    payload = json.dumps({'status': status_text, 'visibility': 'public'}).encode('utf-8')

    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': 'ZyekhSyndicator/1.0'
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            post_url = data.get('url', data.get('id', 'published'))
            print(f"[ SUCCESS ] Mastodon Post Published: {post_url}")
            return True
    except Exception as e:
        print(f"[ ERROR ] Mastodon Publish Failed: {e}")
        return False

def publish_devto(article):
    load_dotenv()
    api_key = os.environ.get('DEVTO_API_KEY')
    if not api_key:
        print("[ WARN ] DEVTO_API_KEY not set in environment or .env file.")
        return False

    body_content = f"# {article['title']}\n\n> {article['description']}\n\n"
    if article['exec_summary']:
        body_content += f"## Executive Summary\n{article['exec_summary']}\n\n"
    
    if article['body']:
        body_content += article['body'] + "\n\n"
    
    body_content += f"---\n*Originally published at [{article['url']}]({article['url']})*"

    endpoint = "https://dev.to/api/articles"
    payload = json.dumps({
        "article": {
            "title": article['title'],
            "published": True,
            "body_markdown": body_content,
            "tags": ["security", "linux", "devops", "architecture"],
            "canonical_url": article['url'],
            "description": article['description']
        }
    }).encode('utf-8')

    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={
            'api-key': api_key,
            'Content-Type': 'application/json',
            'User-Agent': 'ZyekhSyndicator/1.0'
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            url = data.get('url', 'published')
            print(f"[ SUCCESS ] Dev.to Article Published: {url}")
            return True
    except Exception as e:
        print(f"[ ERROR ] Dev.to Publish Failed: {e}")
        return False

def print_syndication_package(article, auto_open=False):
    print("=" * 70)
    print(f"[ ARTICLE ] {article['title']}")
    print(f"[ URL ] {article['url']}")
    print("=" * 70)

    print("\n[ REDDIT INTENT SUBMIT URLS (1-CLICK AUTO-FILL) ]")
    print("-" * 70)
    intent_urls = []
    for sub in SUBREDDITS:
        intent = generate_reddit_intent_url(sub['name'], article['title'], article['url'])
        intent_urls.append(intent)
        print(f"• {sub['name']} ({sub['desc']}):")
        print(f"  {intent}\n")

    hn_url = generate_hn_intent_url(article['title'], article['url'])
    masto_url = generate_mastodon_intent_url(article['title'], article['url'])

    print("[ HACKER NEWS SUBMIT URL ]")
    print(f"• {hn_url}\n")

    print("[ MASTODON SHARE URL ]")
    print(f"• {masto_url}\n")

    print("[ DEV.TO / HASHNODE CROSSPOST MARKDOWN HEADER ]")
    print("-" * 70)
    print("---")
    print(f"title: '{article['title']}'")
    print(f"published: true")
    print(f"canonical_url: {article['url']}")
    print(f"description: '{article['description']}'")
    print("tags: linux, security, devops, architecture")
    print("---\n")

    print("[ REDDIT DRAFT POST SNIPPET (COPY-PASTE) ]")
    print("-" * 70)
    print(f"**Title**: {article['title']}")
    if article['exec_summary']:
        print(f"\n**TL;DR / Key Takeaways**:\n{article['exec_summary']}\n")
    else:
        print(f"\n**Summary**:\n{article['description']}\n")
    print(f"Full technical breakdown & commands: [{article['url']}]({article['url']})")
    print("-" * 70)

    if auto_open:
        print("\n[ ACTION ] Opening Reddit & Hacker News submission tabs in browser...")
        webbrowser.open(intent_urls[0])
        webbrowser.open(hn_url)

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Zyekh.com Social Media & Intent Syndicator")
    parser.add_argument("--latest", "-l", action="store_true", help="Syndicate the latest article")
    parser.add_argument("--slug", "-s", type=str, help="Specify article HTML filename or slug")
    parser.add_argument("--open", "-o", action="store_true", help="Auto-open submit tabs in browser")
    parser.add_argument("--publish-mastodon", action="store_true", help="Auto-publish status to Mastodon API")
    parser.add_argument("--publish-devto", action="store_true", help="Auto-publish article to Dev.to API")
    parser.add_argument("--publish", "-p", action="store_true", help="Auto-publish to both Mastodon and Dev.to APIs")
    args = parser.parse_args()

    articles = get_all_articles()
    if not articles:
        print("[ WARN ] No articles found in blog/ directory.")
        sys.exit(1)

    selected_article = None
    if args.slug:
        for a in articles:
            if args.slug in a['filename'] or args.slug in a['url']:
                selected_article = a
                break
        if not selected_article:
            print(f"[ WARN ] Article matching '{args.slug}' not found.")
            sys.exit(1)
    else:
        articles_by_mtime = sorted(articles, key=lambda x: os.path.getmtime(os.path.join(BLOG_DIR, x['filename'])), reverse=True)
        selected_article = articles_by_mtime[0]

    print_syndication_package(selected_article, auto_open=args.open)

    if args.publish or args.publish_mastodon:
        print("\n[ API PUBLISH ] Broadcasting to Mastodon...")
        publish_mastodon(selected_article)

    if args.publish or args.publish_devto:
        print("\n[ API PUBLISH ] Broadcasting to Dev.to...")
        publish_devto(selected_article)

if __name__ == "__main__":
    main()
