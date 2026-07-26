#!/usr/bin/env python3
import urllib.request
import urllib.parse
import json
import sys

SITEMAP_URL = "https://zyekh.com/sitemap.xml"
SITE_URL = "https://zyekh.com/"

def ping_google():
    url = f"https://www.google.com/ping?sitemap={urllib.parse.quote(SITEMAP_URL)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            print(f"[Google Ping] Status: {resp.status}")
    except Exception as e:
        print(f"[Google Ping] Notice: {e}")

def ping_bing():
    url = f"https://www.bing.com/ping?sitemap={urllib.parse.quote(SITEMAP_URL)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            print(f"[Bing Ping] Status: {resp.status}")
    except Exception as e:
        print(f"[Bing Ping] Notice: {e}")

def ping_indexnow():
    # IndexNow API endpoint for Bing, Yandex, Seznam
    indexnow_url = "https://api.indexnow.org/indexnow"
    payload = {
        "host": "zyekh.com",
        "key": "zyekh2026indexnowkey",
        "keyLocation": "https://zyekh.com/zyekh2026indexnowkey.txt",
        "urlList": [
            "https://zyekh.com/",
            "https://zyekh.com/tools/",
            "https://zyekh.com/blog/",
            "https://zyekh.com/tools/zakat.html",
            "https://zyekh.com/tools/pph21.html",
            "https://zyekh.com/tools/kpr.html",
            "https://zyekh.com/tools/thr.html",
            "https://zyekh.com/tools/split-bill.html",
            "https://zyekh.com/tools/password.html"
        ]
    }
    data = json.dumps(payload).encode('utf-8')
    try:
        req = urllib.request.Request(indexnow_url, data=data, headers={'Content-Type': 'application/json; charset=utf-8'})
        with urllib.request.urlopen(req) as resp:
            print(f"[IndexNow] Status: {resp.status}")
    except Exception as e:
        print(f"[IndexNow] Notice: {e}")

if __name__ == "__main__":
    print("Initiating Search Engine Indexer Ping for zyekh.com...")
    ping_google()
    ping_bing()
    ping_indexnow()
    print("Ping process finished.")
