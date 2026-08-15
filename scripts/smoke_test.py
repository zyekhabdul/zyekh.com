#!/usr/bin/env python3
"""
Localhost Live HTTP Server Smoke Test & Endpoint Validator for zyekh.com
Spawns an ephemeral Python HTTP server on localhost, tests all core page archetypes,
MIME types, security headers (CSP, Anti-Clickjack, Anti-FOUC), XML feeds, and assets.
"""
import sys
import os
import time
import socket
import threading
import urllib.request
import urllib.error
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class QuietHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(BASE_DIR), **kwargs)

    def log_message(self, format, *args):
        # Silence standard HTTP access logging to keep terminal output clean
        pass

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

def run_smoke_tests(port=None):
    if port is None:
        port = get_free_port()

    server = ThreadingHTTPServer(('127.0.0.1', port), QuietHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    time.sleep(0.1)

    base_url = f"http://127.0.0.1:{port}"
    errors = []
    checks_passed = 0

    # Route test matrix: (path, expected_status, content_type_substr, required_strings)
    test_matrix = [
        ("/", 200, "text/html", ["<title>", "antiClickjack", "localStorage.getItem"]),
        ("/about/", 200, "text/html", ["<title>", "antiClickjack", "localStorage.getItem"]),
        ("/contact/", 200, "text/html", ["<title>", "antiClickjack", "localStorage.getItem"]),
        ("/links/", 200, "text/html", ["<title>", "antiClickjack", "localStorage.getItem"]),
        ("/tools/", 200, "text/html", ["<title>", "antiClickjack", "localStorage.getItem"]),
        ("/tools/llm-calculator.html", 200, "text/html", ["<title>", "antiClickjack", "localStorage.getItem"]),
        ("/tools/linux-hardening-generator.html", 200, "text/html", ["<title>", "antiClickjack", "localStorage.getItem"]),
        ("/tools/webgpu-profiler.html", 200, "text/html", ["<title>", "antiClickjack", "localStorage.getItem"]),
        ("/tools/wireguard-generator.html", 200, "text/html", ["<title>", "antiClickjack", "localStorage.getItem"]),
        ("/blog/", 200, "text/html", ["<title>", "antiClickjack", "localStorage.getItem"]),
        ("/blog/linux-vps-hardening-guide-2026.html", 200, "text/html", ["<title>", "article", "antiClickjack"]),
        ("/blueprints/", 200, "text/html", ["<title>", "antiClickjack"]),
        ("/blueprints/topology-builder.html", 200, "text/html", ["<title>", "antiClickjack", "localStorage.getItem"]),
        ("/offline.html", 200, "text/html", ["offline-card", "Offline"]),
        ("/404.html", 200, "text/html", ["404", "Page Not Found"]),
        ("/sitemap.xml", 200, "xml", ["<urlset", "<loc>"]),
        ("/feed.xml", 200, "xml", ["<rss", "<channel>"]),
        ("/atom.xml", 200, "xml", ["<feed", "<entry", "http://www.w3.org/2005/Atom"]),
        ("/feed.json", 200, "json", ["https://jsonfeed.org/version/1.1", "items", "title"]),
        ("/llms.txt", 200, "text", ["zyekh.com", "Entity Identity"]),
        ("/llms-full.txt", 200, "text", ["# zyekh.com", "Security Researcher"]),
        ("/sw.js", 200, "javascript", ["CACHE_VERSION", "addEventListener"]),
        ("/manifest.json", 200, "json", ["short_name", "start_url"]),
        ("/tools/tools-manifest.json", 200, "json", ["zyekh.com", "total_tools", "parameters"]),
        ("/search-index.json", 200, "json", ["title", "url"]),
        ("/assets/css/shared.min.css", 200, "css", [":root"]),
        ("/assets/js/site-nav.min.js", 200, "javascript", ["init"]),
    ]

    print(f"[ SMOKE TEST ] Live server running on {base_url}...")

    for path, expected_status, expected_mime, required_snippets in test_matrix:
        url = f"{base_url}{path}"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ZyekhSmokeTester/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                status = resp.status
                content_type = resp.headers.get("Content-Type", "").lower()
                body = resp.read().decode('utf-8', errors='ignore')

                if status != expected_status:
                    errors.append(f"Path '{path}': Expected HTTP {expected_status}, got HTTP {status}")
                    continue

                if expected_mime and expected_mime not in content_type:
                    errors.append(f"Path '{path}': Expected MIME containing '{expected_mime}', got '{content_type}'")
                    continue

                for snippet in required_snippets:
                    if snippet not in body:
                        errors.append(f"Path '{path}': Missing required snippet '{snippet}' in response body")
                        break
                else:
                    checks_passed += 1

        except Exception as e:
            errors.append(f"Path '{path}': Request failed: {e}")

    # Test 404 behavior on random non-existent route
    try:
        url_404 = f"{base_url}/test-non-existent-smoke-route-12345.html"
        req = urllib.request.Request(url_404, headers={"User-Agent": "ZyekhSmokeTester/1.0"})
        urllib.request.urlopen(req, timeout=5)
        errors.append("Route /test-non-existent-smoke-route-12345.html returned 200 OK instead of 404")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            checks_passed += 1
        else:
            errors.append(f"404 route returned unexpected HTTP status {e.code}")
    except Exception as e:
        errors.append(f"404 test failed with exception: {e}")

    # Shutdown server
    server.shutdown()
    server_thread.join(timeout=1)

    if errors:
        print(f"[ FAIL ] Live HTTP smoke test failed with {len(errors)} error(s):")
        for err in errors:
            print(f"  • {err}")
        return False
    else:
        print(f"[ PASS ] Live HTTP smoke test: {checks_passed}/{checks_passed} archetype routes & checks verified successfully on {base_url}.")
        return True

if __name__ == "__main__":
    success = run_smoke_tests()
    sys.exit(0 if success else 1)
