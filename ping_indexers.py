#!/usr/bin/env python3
import urllib.request
import json
import sys

def ping_indexnow():
    """IndexNow protocol for instant indexing across Bing, Yandex, and Seznam."""
    indexnow_url = "https://api.indexnow.org/indexnow"
    payload = {
        "host": "zyekh.com",
        "key": "zyekh2026indexnowkey",
        "keyLocation": "https://zyekh.com/zyekh2026indexnowkey.txt",
        "urlList": [
            "https://zyekh.com/blog/",
            "https://zyekh.com/blog/linux-vps-hardening-guide-2026.html",
            "https://zyekh.com/blog/minimalist-server-architecture-pure-css-and-static-hosting.html",
            "https://zyekh.com/blog/securing-web-applications-with-strict-content-security-policy.html",
            "https://zyekh.com/blog/understanding-linux-ebpf-security-monitoring.html",
            "https://zyekh.com/",
            "https://zyekh.com/tools/case-converter.html",
            "https://zyekh.com/tools/color.html",
            "https://zyekh.com/tools/converter.html",
            "https://zyekh.com/tools/countdown.html",
            "https://zyekh.com/tools/counter.html",
            "https://zyekh.com/tools/dice.html",
            "https://zyekh.com/tools/diff-checker.html",
            "https://zyekh.com/tools/",
            "https://zyekh.com/tools/kpr.html",
            "https://zyekh.com/tools/lorem.html",
            "https://zyekh.com/tools/markdown.html",
            "https://zyekh.com/tools/password.html",
            "https://zyekh.com/tools/pomodoro.html",
            "https://zyekh.com/tools/pph21.html",
            "https://zyekh.com/tools/qr.html",
            "https://zyekh.com/tools/random-picker.html",
            "https://zyekh.com/tools/split-bill.html",
            "https://zyekh.com/tools/thr.html",
            "https://zyekh.com/tools/tts.html",
            "https://zyekh.com/tools/zakat.html"
        ]
    }
    data = json.dumps(payload).encode('utf-8')
    try:
        req = urllib.request.Request(indexnow_url, data=data, headers={'Content-Type': 'application/json; charset=utf-8'})
        with urllib.request.urlopen(req) as resp:
            print(f"[IndexNow API] Status: {resp.status} (Indexing request submitted successfully)")
    except Exception as e:
        print(f"[IndexNow API] Error: {e}")

if __name__ == "__main__":
    print("Initiating Search Engine IndexNow Ping for zyekh.com...")
    ping_indexnow()
    print("Ping process finished.")
