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
import webbrowser

BASE_URL = "https://zyekh.com"
BLOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "blog")

SUBREDDITS = [
    {"name": "r/netsec", "desc": "Network Security & Cyber Architecture"},
    {"name": "r/linux", "desc": "Linux Kernel & VPS Security Hardening"},
    {"name": "r/programming", "desc": "General Technical & Software Engineering"},
    {"name": "r/SelfHost", "desc": "Self-Hosted & Privacy Infrastructure"},
    {"name": "r/webdev", "desc": "Web Performance, PWA & Frontend Architecture"},
    {"name": "r/devops", "desc": "Cloud Infrastructure & Container Security"}
]

def parse_article_metadata(filepath):
    content = open(filepath, 'r', encoding='utf-8').read()
    
    import html
    # Title
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
    title = html.unescape(title_match.group(1).strip()) if title_match else os.path.basename(filepath)
    title = re.sub(r'\s*—\s*zyekh\.com.*', '', title)
    title = re.sub(r'\s*\|\s*zyekh\.com.*', '', title)

    # Description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE | re.DOTALL)
    description = html.unescape(desc_match.group(1).strip()) if desc_match else ""

    # Slug / Relative URL
    rel_path = os.path.relpath(filepath, os.path.dirname(BLOG_DIR))
    url = f"{BASE_URL}/{rel_path}"

    # Exec Summary / TL;DR text if present
    exec_summary = ""
    summary_match = re.search(r'<div class=["\']exec-summary["\']>(.*?)</div>', content, re.IGNORECASE | re.DOTALL)
    if summary_match:
        clean_text = re.sub(r'<[^>]+>', '', summary_match.group(1)).strip()
        clean_text = ' '.join(clean_text.split())
        exec_summary = clean_text

    return {
        'title': title,
        'description': description,
        'url': url,
        'exec_summary': exec_summary,
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
        webbrowser.open(intent_urls[0]) # Open first sub e.g. r/netsec or r/linux
        webbrowser.open(hn_url)

def notify_telegram(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = json.dumps({'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        urllib.request.urlopen(req)
        print("[ INFO ] Telegram notification sent.")
    except Exception as e:
        print(f"[ WARN ] Telegram failed: {e}")

def notify_discord(webhook_url, content):
    data = json.dumps({'content': content}).encode('utf-8')
    req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    try:
        urllib.request.urlopen(req)
        print("[ INFO ] Discord notification sent.")
    except Exception as e:
        print(f"[ WARN ] Discord failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Zyekh.com Social Media & Intent Syndicator (Solution A)")
    parser.add_argument("--latest", "-l", action="store_true", help="Syndicate the latest article")
    parser.add_argument("--slug", "-s", type=str, help="Specify article HTML filename or slug")
    parser.add_argument("--open", "-o", action="store_true", help="Auto-open submit tabs in browser")
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
    elif args.latest or len(sys.argv) == 1:
        # Default to latest article (most recent mtime or last in list)
        articles_by_mtime = sorted(articles, key=lambda x: os.path.getmtime(os.path.join(BLOG_DIR, x['filename'])), reverse=True)
        selected_article = articles_by_mtime[0]

    print_syndication_package(selected_article, auto_open=args.open)

    # Optional Telegram & Discord Webhooks if configured
    telegram_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    telegram_chat = os.environ.get('TELEGRAM_CHAT_ID')
    discord_webhook = os.environ.get('DISCORD_WEBHOOK_URL')

    if telegram_token and telegram_chat or discord_webhook:
        msg = f"[ UPDATE ] New Architecture Blueprint Published!\n\n**{selected_article['title']}**\n{selected_article['description']}\n\n[Read Full Article ->]({selected_article['url']})"
        if telegram_token and telegram_chat:
            notify_telegram(telegram_token, telegram_chat, msg)
        if discord_webhook:
            notify_discord(discord_webhook, msg)

if __name__ == "__main__":
    main()
