#!/usr/bin/env python3
import urllib.request
import json
import os
import glob
import xml.etree.ElementTree as ET

def get_all_urls():
    """Extract all valid site URLs dynamically from sitemap.xml or html files."""
    urls = set()
    sitemap_path = os.path.join(os.path.dirname(__file__), "sitemap.xml")
    
    if os.path.exists(sitemap_path):
        try:
            tree = ET.parse(sitemap_path)
            root = tree.getroot()
            # Namespace handling for sitemap.xml
            ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            for loc in root.findall('.//sm:loc', ns):
                if loc.text:
                    urls.add(loc.text.strip())
        except Exception as e:
            print(f"[Warn] Could not parse sitemap.xml: {e}")
            
    if not urls:
        # Fallback: scan local html files
        base_url = "https://zyekh.com/"
        for filepath in glob.glob("**/*.html", recursive=True):
            if "offline.html" in filepath or "404.html" in filepath:
                continue
            clean_path = filepath.replace("\\", "/")
            if clean_path == "index.html":
                urls.add(base_url)
            elif clean_path.endswith("/index.html"):
                urls.add(base_url + clean_path[:-10])
            else:
                urls.add(base_url + clean_path)
                
    return sorted(list(urls))

def ping_indexnow():
    """IndexNow protocol for instant indexing across Bing, Yandex, and Seznam."""
    indexnow_url = "https://api.indexnow.org/indexnow"
    url_list = get_all_urls()
    print(f"Extracted {len(url_list)} URLs for IndexNow submission.")
    
    payload = {
        "host": "zyekh.com",
        "key": "zyekh2026indexnowkey",
        "keyLocation": "https://zyekh.com/zyekh2026indexnowkey.txt",
        "urlList": url_list
    }
    data = json.dumps(payload).encode('utf-8')
    try:
        req = urllib.request.Request(
            indexnow_url, 
            data=data, 
            headers={'Content-Type': 'application/json; charset=utf-8'}
        )
        with urllib.request.urlopen(req) as resp:
            print(f"[IndexNow API] Status: {resp.status} (Indexing request submitted successfully for {len(url_list)} URLs)")
    except Exception as e:
        print(f"[IndexNow API] Error: {e}")

if __name__ == "__main__":
    print("Initiating Search Engine IndexNow Ping for zyekh.com...")
    ping_indexnow()
    print("Ping process finished.")
