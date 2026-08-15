#!/usr/bin/env python3
import os
import sys
import argparse
import urllib.parse
import urllib.request
import re
import json
import html
import time
import webbrowser
import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent
BLOG_DIR = BASE_DIR / "blog"
BASE_URL = "https://zyekh.com"
MANIFEST_FILE = BASE_DIR / "data" / "social_cards_manifest.json"
HISTORY_FILE = BASE_DIR / "data" / "syndication_history.json"

SUBREDDITS = [
    {"name": "r/netsec", "desc": "Network Security & Cyber Architecture"},
    {"name": "r/linux", "desc": "Linux Kernel & VPS Security Hardening"},
    {"name": "r/programming", "desc": "General Technical & Software Engineering"},
    {"name": "r/SelfHost", "desc": "Self-Hosted & Privacy Infrastructure"},
    {"name": "r/webdev", "desc": "Web Performance, PWA & Frontend Architecture"},
    {"name": "r/devops", "desc": "Cloud Infrastructure & Container Security"}
]

DOMAIN_HASHTAG_MAP = {
    "rust": ["#RustLang", "#MemorySafety", "#SystemsProgramming"],
    "wasm": ["#WebAssembly", "#Wasm", "#ZeroTrust"],
    "ebpf": ["#eBPF", "#LinuxKernel", "#Observability"],
    "xdp": ["#eBPF", "#DDoS", "#Networking"],
    "ssh": ["#ZeroTrust", "#SSH", "#Infosec"],
    "fido2": ["#FIDO2", "#YubiKey", "#HardwareSecurity"],
    "vault": ["#HashiCorpVault", "#Security", "#DevOps"],
    "auditd": ["#DFIR", "#LinuxSecurity", "#Auditd"],
    "vector": ["#Vector", "#ClickHouse", "#LogManagement"],
    "clickhouse": ["#ClickHouse", "#DataEngineering", "#DFIR"],
    "seccomp": ["#Seccomp", "#LinuxSecurity", "#Sandboxing"],
    "landlock": ["#Landlock", "#LSM", "#LinuxSecurity"],
    "systemd": ["#Systemd", "#LinuxHardening", "#DevOps"],
    "ufw": ["#Firewall", "#LinuxSecurity", "#SysAdmin"],
    "fail2ban": ["#Fail2ban", "#IntrusionPrevention", "#Linux"],
    "nginx": ["#Nginx", "#WebSecurity", "#TLS"],
    "http3": ["#QUIC", "#HTTP3", "#WebPerf"],
    "vllm": ["#vLLM", "#LLM", "#AIInference"],
    "dspy": ["#DSPy", "#PromptEngineering", "#GenAI"],
    "moe": ["#MixtureOfExperts", "#PyTorch", "#DeepLearning"],
    "webgpu": ["#WebGPU", "#Inference", "#BrowserAI"],
    "slora": ["#LoRA", "#FineTuning", "#GPU"],
    "rag": ["#RAG", "#ColBERT", "#VectorSearch"],
    "colbert": ["#ColBERT", "#InformationRetrieval", "#RAG"],
    "kubernetes": ["#Kubernetes", "#CloudNative", "#K8sSecurity"],
    "cilium": ["#Cilium", "#Tetragon", "#eBPF"],
    "cosign": ["#Cosign", "#SLSA", "#SupplyChainSecurity"],
    "wireguard": ["#WireGuard", "#VPN", "#MeshNetwork"],
    "faillock": ["#LinuxSecurity", "#PAM", "#AccountSecurity"],
    "csp": ["#AppSec", "#WebSecurity", "#CSP"],
    "omnirouter": ["#AIInfrastructure", "#LLMGateway", "#Fallbacks"],
    "chroot": ["#LinuxNamespaces", "#ContainerSecurity", "#Linux"]
}

def load_dotenv():
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())

    # Dual-File MCP Discovery Protocol fallback
    mcp_paths = [
        Path.home() / ".gemini" / "config" / "mcp_config.json",
        Path.home() / ".gemini" / "config" / "mcp_config_extended.json"
    ]
    for mcp_path in mcp_paths:
        if mcp_path.exists():
            try:
                cfg = json.loads(mcp_path.read_text(encoding='utf-8'))
                for server in cfg.get("mcpServers", {}).values():
                    for k, v in server.get("env", {}).items():
                        if isinstance(v, str):
                            os.environ.setdefault(k, v)
            except Exception:
                pass

def load_history() -> dict:
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding='utf-8'))
        except Exception:
            pass
    return {}

def record_history(slug: str, platform: str, data: dict):
    history = load_history()
    if slug not in history:
        history[slug] = {}
    history[slug][platform] = data
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    HISTORY_FILE.write_text(json.dumps(history, indent=2), encoding='utf-8')

def load_manifest() -> dict:
    if MANIFEST_FILE.exists():
        try:
            return json.loads(MANIFEST_FILE.read_text(encoding='utf-8'))
        except Exception:
            pass
    return {}

def get_article_takeaways(article: dict, max_items: int = 2) -> list:
    slug = article['slug']
    manifest = load_manifest()
    if slug in manifest:
        invariants = manifest[slug].get('invariants', [])
        if invariants:
            return invariants[:max_items]
    if article.get('exec_summary'):
        return article['exec_summary'][:max_items]
    return []

def get_article_hashtags(article: dict, max_tags: int = 4) -> list:
    slug = article['slug'].lower()
    tags = article.get('tags', [])
    matched_tags = []

    # Map from slug keywords
    for kw, htags in DOMAIN_HASHTAG_MAP.items():
        if kw in slug:
            for ht in htags:
                if ht not in matched_tags:
                    matched_tags.append(ht)

    # Map from article meta tags
    for t in tags:
        t_clean = t.lower()
        if t_clean in DOMAIN_HASHTAG_MAP:
            for ht in DOMAIN_HASHTAG_MAP[t_clean]:
                if ht not in matched_tags:
                    matched_tags.append(ht)
        else:
            fmt = f"#{t.capitalize()}"
            if fmt not in matched_tags:
                matched_tags.append(fmt)

    if not matched_tags:
        matched_tags = ["#Security", "#Linux", "#DevOps", "#Architecture"]

    return matched_tags[:max_tags]

def parse_article_metadata(filepath: Path):
    content = filepath.read_text(encoding='utf-8')
    soup = BeautifulSoup(content, 'html.parser')
    
    # Title
    h1 = soup.find('h1')
    title = h1.get_text().strip() if h1 else filepath.stem
    title = re.sub(r'\s*—\s*zyekh\.com.*', '', title)
    title = re.sub(r'\s*\|\s*zyekh\.com.*', '', title)

    # Description
    desc_meta = soup.find('meta', {'name': 'description'})
    description = desc_meta['content'].strip() if desc_meta and desc_meta.get('content') else ""

    # Dynamic Tags Extraction
    extracted_tags = []
    for tag_elem in soup.find_all('span', class_='meta-tag'):
        t_text = tag_elem.get_text().replace('#', '').strip()
        parts = [p.strip().lower() for p in re.split(r'[•,/|]+', t_text) if p.strip()]
        for p in parts:
            p_clean = re.sub(r'[^a-z0-9-]', '', p)
            if p_clean and p_clean not in extracted_tags:
                extracted_tags.append(p_clean)
    
    if not extracted_tags:
        extracted_tags = ["security", "linux", "devops", "architecture"]

    url = f"{BASE_URL}/blog/{filepath.name}"
    slug = filepath.stem

    # Executive Summary
    exec_summary_items = []
    summary_div = soup.find('div', class_='exec-summary')
    if summary_div:
        for li in summary_div.find_all('li'):
            item_text = li.get_text().strip()
            if item_text:
                exec_summary_items.append(item_text)

    # Clean Article Content Body (Dev.to Markdown extraction)
    main_elem = soup.find('main', class_='article-content')
    clean_markdown = ""
    if main_elem:
        content_soup = BeautifulSoup(str(main_elem), 'html.parser')
        main_root = content_soup.find('main') or content_soup
        
        # Decompose non-content boilerplate elements
        for unwanted in main_root.find_all(['script', 'style', 'figure', 'footer']):
            unwanted.decompose()
        for unwanted in main_root.find_all(class_=['author-card', 'article-cross-links', 'exec-summary', 'article-actions', 'back-link', 'hero-caption', 'heading-reset']):
            unwanted.decompose()

        # Convert FAQ <details> into clean Q&A
        for details in main_root.find_all('details'):
            summary = details.find('summary')
            q_text = summary.get_text().strip() if summary else "FAQ"
            if summary:
                summary.decompose()
            a_text = details.get_text().strip()
            details.replace_with(soup.new_string(f"\n\n**Q: {q_text}**\n\n{a_text}\n\n"))

        md_parts = []
        for elem in main_root.children:
            if not elem.name:
                continue
            if elem.name == 'h2':
                md_parts.append(f"\n\n## {elem.get_text().strip()}\n\n")
            elif elem.name == 'h3':
                md_parts.append(f"\n\n### {elem.get_text().strip()}\n\n")
            elif elem.name == 'h4':
                md_parts.append(f"\n\n#### {elem.get_text().strip()}\n\n")
            elif elem.name == 'pre':
                code_tag = elem.find('code')
                lang = ""
                if code_tag and code_tag.get('class'):
                    for cls in code_tag['class']:
                        if cls.startswith('language-'):
                            lang = cls.replace('language-', '')
                code_text = code_tag.get_text() if code_tag else elem.get_text()
                md_parts.append(f"\n\n```{lang}\n{code_text.strip()}\n```\n\n")
            elif elem.name in ['ul', 'ol']:
                list_str = "\n"
                for idx, li in enumerate(elem.find_all('li'), 1):
                    prefix = f"{idx}." if elem.name == 'ol' else "*"
                    list_str += f"{prefix} {li.get_text().strip()}\n"
                md_parts.append(list_str + "\n")
            elif elem.name == 'p':
                p_text = elem.get_text().strip()
                if p_text:
                    md_parts.append(f"{p_text}\n\n")
            elif elem.name == 'div' and 'faq-section' in elem.get('class', []):
                md_parts.append(f"{elem.get_text().strip()}\n\n")

        raw_md = "".join(md_parts)
        clean_markdown = re.sub(r'\n{3,}', '\n\n', raw_md).strip()

    return {
        'title': title,
        'description': description,
        'url': url,
        'slug': slug,
        'exec_summary': exec_summary_items,
        'body': clean_markdown,
        'tags': extracted_tags,
        'filename': filepath.name
    }

def get_all_articles():
    html_files = sorted(BLOG_DIR.glob("*.html"))
    articles = []
    for f in html_files:
        if f.name != "index.html":
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
    load_dotenv()
    server = os.environ.get('MASTODON_SERVER', 'https://infosec.exchange').rstrip('/')
    text = f"{title}\n\n[ Read Full Article -> ] {url}\n\n#Security #Linux #DevOps #Engineering"
    encoded_text = urllib.parse.quote(text)
    return f"{server}/share?text={encoded_text}"

def upload_mastodon_media(token, server, image_path, description=""):
    import uuid
    boundary = f"----WebKitFormBoundary{uuid.uuid4().hex}"
    endpoint = f"{server.rstrip('/')}/api/v2/media"
    
    with open(image_path, "rb") as f:
        file_bytes = f.read()
    
    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode('utf-8'))
    body.extend(f'Content-Disposition: form-data; name="file"; filename="{os.path.basename(image_path)}"\r\n'.encode('utf-8'))
    body.extend(b"Content-Type: image/png\r\n\r\n")
    body.extend(file_bytes)
    body.extend(b"\r\n")
    
    if description:
        body.extend(f"--{boundary}\r\n".encode('utf-8'))
        body.extend(f'Content-Disposition: form-data; name="description"\r\n\r\n'.encode('utf-8'))
        body.extend(f"{description}\r\n".encode('utf-8'))
        
    body.extend(f"--{boundary}--\r\n".encode('utf-8'))
    
    req = urllib.request.Request(
        endpoint,
        data=bytes(body),
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'User-Agent': 'ZyekhSyndicator/1.0'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('id')
    except Exception as err:
        print(f"[ WARN ] Mastodon Media Upload Failed: {err}")
        return None

def format_mastodon_status(article: dict) -> str:
    takeaways = get_article_takeaways(article, max_items=2)
    tags = get_article_hashtags(article, max_tags=4)
    tags_str = ' '.join(tags)

    status = f"{article['title']}\n\n{article['description']}"
    if takeaways:
        status += "\n\nKey Architecture:\n" + "\n".join([f"• {t}" for t in takeaways])
    
    status += f"\n\n[ Read Full Article -> ] {article['url']}\n\n{tags_str}"
    
    # 500 char safety truncate
    if len(status) > 495:
        # Fallback to lean description
        status = f"{article['title']}\n\n{article['description']}\n\n[ Read Full Article -> ] {article['url']}\n\n{tags_str}"
    return status

def publish_mastodon(article):
    load_dotenv()
    token = os.environ.get('MASTODON_ACCESS_TOKEN')
    server = os.environ.get('MASTODON_SERVER', 'https://infosec.exchange')
    if not token:
        print("[ WARN ] MASTODON_ACCESS_TOKEN not set in environment or .env file.")
        return False

    status_text = format_mastodon_status(article)
    
    media_ids = []
    card_path = BASE_DIR / "assets" / "img" / "social-cards" / f"{article['slug']}-dark-landscape.png"
    if card_path.exists():
        media_id = upload_mastodon_media(token, server, card_path, description=article['title'])
        if media_id:
            media_ids.append(media_id)
            print(f"[ SUCCESS ] Mastodon Dark Landscape Social Card Attached: {card_path.name}")

    endpoint = f"{server.rstrip('/')}/api/v1/statuses"
    payload_dict = {'status': status_text, 'visibility': 'public'}
    if media_ids:
        payload_dict['media_ids'] = media_ids
    payload = json.dumps(payload_dict).encode('utf-8')

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
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            post_url = data.get('url', data.get('id', 'published'))
            post_id = data.get('id')
            record_history(article['slug'], 'mastodon', {
                'id': post_id,
                'url': post_url,
                'posted_at': datetime.datetime.now(datetime.timezone.utc).isoformat()
            })
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
        body_content += "## Executive Summary & Key Takeaways\n\n"
        for item in article['exec_summary']:
            body_content += f"* {item}\n"
        body_content += "\n---\n\n"
    
    if article['body']:
        body_content += article['body'] + "\n\n"
    
    body_content += f"---\n\n*Originally published at [{article['url']}]({article['url']})*"

    # Check if existing article ID is known
    history = load_history()
    existing_devto_id = history.get(article['slug'], {}).get('devto', {}).get('id')
    
    method = 'POST'
    endpoint = "https://dev.to/api/articles"
    if existing_devto_id:
        endpoint = f"https://dev.to/api/articles/{existing_devto_id}"
        method = 'PUT'

    payload = json.dumps({
        "article": {
            "title": article['title'],
            "published": True,
            "body_markdown": body_content,
            "tags": article['tags'][:4],
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
        },
        method=method
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            url = data.get('url', 'published')
            article_id = data.get('id')
            record_history(article['slug'], 'devto', {
                'id': article_id,
                'url': url,
                'updated_at': datetime.datetime.now(datetime.timezone.utc).isoformat()
            })
            action_label = "Updated" if method == 'PUT' else "Published"
            print(f"[ SUCCESS ] Dev.to Article {action_label}: {url}")
            return True
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8')
        if e.code == 429:
            print(f"[ WARN ] Dev.to Rate limited (429). Sleeping 32s before automatic retry...")
            time.sleep(32)
            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    resp_data = json.loads(resp.read().decode('utf-8'))
                    article_id = resp_data.get('id')
                    url = resp_data.get('url', f"https://dev.to/zyekh/{article['slug']}")
                    record_history(article['slug'], 'devto', {
                        'id': article_id,
                        'url': url,
                        'updated_at': datetime.datetime.now(datetime.timezone.utc).isoformat()
                    })
                    action_label = "Updated" if method == 'PUT' else "Published"
                    print(f"[ SUCCESS ] Dev.to Article {action_label} (Post-Retry): {url}")
                    return True
            except Exception as retry_err:
                print(f"[ ERROR ] Dev.to Retry Failed: {retry_err}")
                return False
        print(f"[ ERROR ] Dev.to Publish Failed ({e.code}): {err_msg}")
        return False
    except Exception as e:
        print(f"[ ERROR ] Dev.to Publish Failed: {e}")
        return False

def resolve_bluesky_pds(handle_or_did):
    did = handle_or_did
    if not handle_or_did.startswith("did:"):
        try:
            url = f"https://bsky.social/xrpc/com.atproto.identity.resolveHandle?handle={handle_or_did}"
            with urllib.request.urlopen(url, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                did = data.get("did", handle_or_did)
        except Exception:
            pass
    if did.startswith("did:plc:"):
        try:
            url = f"https://plc.directory/{did}"
            with urllib.request.urlopen(url, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                for svc in data.get("service", []):
                    if svc.get("type") == "AtprotoPersonalDataServer":
                        return svc.get("serviceEndpoint", "https://bsky.social"), did
        except Exception:
            pass
    return "https://bsky.social", did

def extract_bsky_facets(text):
    facets = []
    url_regex = re.compile(r'https?://[^\s)]+')
    for m in url_regex.finditer(text):
        uri = m.group(0)
        byte_start = len(text[:m.start()].encode('utf-8'))
        byte_end = len(text[:m.end()].encode('utf-8'))
        facets.append({
            "index": {"byteStart": byte_start, "byteEnd": byte_end},
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": uri}]
        })
    tag_regex = re.compile(r'#([A-Za-z0-9_]+)')
    for m in tag_regex.finditer(text):
        tag = m.group(1)
        byte_start = len(text[:m.start()].encode('utf-8'))
        byte_end = len(text[:m.end()].encode('utf-8'))
        facets.append({
            "index": {"byteStart": byte_start, "byteEnd": byte_end},
            "features": [{"$type": "app.bsky.richtext.facet#tag", "tag": tag}]
        })
    return facets

def format_bluesky_post_text(title, description, url, tags, takeaways=None):
    tags_str = ' '.join(tags[:2])
    suffix = f'\n\n[ Read Full Article -> ] {url}'
    if tags_str:
        suffix += f'\n\n{tags_str}'
    suffix = suffix.strip()
    fixed_len = len(suffix.encode('utf-8'))
    
    budget = 280 - fixed_len

    # Try high-density bullet format if budget permits
    if takeaways and len(takeaways) > 0:
        bullet = f"• {takeaways[0]}"
        combined = f"{title}\n\n{bullet}"
        if len(combined.encode('utf-8')) <= budget - 4:
            return f"{combined}\n\n{suffix}"

    title_len = len(title.encode('utf-8'))
    if title_len >= budget - 20:
        clean_title = title[:budget - 3].rstrip() + '...'
        return f'{clean_title}\n\n{suffix}'
    
    desc_budget = budget - title_len - 2
    if desc_budget > 30 and description:
        clean_desc = description
        if len(clean_desc.encode('utf-8')) > desc_budget:
            clean_desc = clean_desc[:desc_budget - 3].rstrip() + '...'
        return f'{title}\n\n{clean_desc}\n\n{suffix}'
    else:
        return f'{title}\n\n{suffix}'

def publish_bluesky(article):
    load_dotenv()
    handle = os.environ.get('BSKY_HANDLE')
    password = os.environ.get('BSKY_APP_PASSWORD')

    if not handle or not password:
        print("[ WARN ] BSKY_HANDLE or BSKY_APP_PASSWORD not set in environment or .env file.")
        return False

    pds_server, did = resolve_bluesky_pds(handle)

    # 1. Create Session
    session_endpoint = f"{pds_server.rstrip('/')}/xrpc/com.atproto.server.createSession"
    session_payload = json.dumps({"identifier": handle, "password": password}).encode('utf-8')

    req = urllib.request.Request(
        session_endpoint,
        data=session_payload,
        headers={'Content-Type': 'application/json', 'User-Agent': 'ZyekhSyndicator/1.0'}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            session_data = json.loads(resp.read().decode('utf-8'))
            access_jwt = session_data.get('accessJwt')
            did = session_data.get('did', did)
    except Exception as e:
        print(f"[ ERROR ] Bluesky Auth Failed: {e}")
        return False

    # 2. Check/Generate Light Square Social Card Attachment for Bluesky Mobile Feed Breakout
    card_path = BASE_DIR / "assets" / "img" / "social-cards" / f"{article['slug']}-light-square.png"
    if not card_path.exists():
        try:
            from scripts.generate_social_cards import generate_social_card
            generate_social_card(article, card_path, theme="light", mode="square")
        except Exception as err:
            print(f"[ WARN ] Social Card auto-generation skipped: {err}")

    blob_ref = None
    if card_path.exists():
        upload_endpoint = f"{pds_server.rstrip('/')}/xrpc/com.atproto.repo.uploadBlob"
        card_bytes = card_path.read_bytes()
        blob_req = urllib.request.Request(
            upload_endpoint,
            data=card_bytes,
            headers={
                'Authorization': f'Bearer {access_jwt}',
                'Content-Type': 'image/png',
                'User-Agent': 'ZyekhSyndicator/1.0'
            }
        )
        try:
            with urllib.request.urlopen(blob_req, timeout=15) as b_resp:
                b_data = json.loads(b_resp.read().decode('utf-8'))
                blob_ref = b_data.get('blob')
                print(f"[ SUCCESS ] Bluesky Category Social Card Attached: {card_path.name}")
        except Exception as e:
            print(f"[ WARN ] Bluesky Blob Upload Failed: {e}")

    # 3. Post Record with Embed
    post_endpoint = f"{pds_server.rstrip('/')}/xrpc/com.atproto.repo.createRecord"
    takeaways = get_article_takeaways(article, max_items=1)
    tags = get_article_hashtags(article, max_tags=2)
    status_text = format_bluesky_post_text(article['title'], article.get('description', ''), article['url'], tags, takeaways)
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

    record_obj = {
        "$type": "app.bsky.feed.post",
        "text": status_text,
        "createdAt": now_iso
    }
    facets = extract_bsky_facets(status_text)
    if facets:
        record_obj["facets"] = facets

    if blob_ref:
        record_obj["embed"] = {
            "$type": "app.bsky.embed.images",
            "images": [{
                "alt": article['title'],
                "image": blob_ref
            }]
        }

    post_req = urllib.request.Request(
        post_endpoint,
        data=json.dumps({"repo": did, "collection": "app.bsky.feed.post", "record": record_obj}).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {access_jwt}',
            'Content-Type': 'application/json',
            'User-Agent': 'ZyekhSyndicator/1.0'
        }
    )
    try:
        with urllib.request.urlopen(post_req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            uri = data.get('uri', 'published')
            record_history(article['slug'], 'bluesky', {
                'uri': uri,
                'cid': data.get('cid'),
                'posted_at': datetime.datetime.now(datetime.timezone.utc).isoformat()
            })
            print(f"[ SUCCESS ] Bluesky Post Published: {uri}")
            return True
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode('utf-8')
        print(f"[ ERROR ] Bluesky Post Failed ({e.code}): {err_msg}")
        return False
    except Exception as e:
        print(f"[ ERROR ] Bluesky Post Failed: {e}")
        return False

def print_status_table():
    articles = get_all_articles()
    history = load_history()
    
    print("\n" + "=" * 90)
    print(f"{'ARTICLE SLUG':<45} | {'DEV.TO':<10} | {'BLUESKY':<10} | {'MASTODON':<10}")
    print("=" * 90)

    total = len(articles)
    devto_count = 0
    bsky_count = 0
    masto_count = 0

    for a in articles:
        slug = a['slug']
        h = history.get(slug, {})
        
        has_devto = "[ DONE ]" if 'devto' in h else "[  --  ]"
        has_bsky = "[ DONE ]" if 'bluesky' in h else "[  --  ]"
        has_masto = "[ DONE ]" if 'mastodon' in h else "[  --  ]"
        
        if 'devto' in h: devto_count += 1
        if 'bluesky' in h: bsky_count += 1
        if 'mastodon' in h: masto_count += 1

        slug_trunc = slug[:43] + ".." if len(slug) > 45 else slug
        print(f"{slug_trunc:<45} | {has_devto:<10} | {has_bsky:<10} | {has_masto:<10}")

    print("=" * 90)
    print(f"SYNDICATION TOTALS ({total} Articles):")
    print(f"  • Dev.to:   {devto_count}/{total} published")
    print(f"  • Bluesky:  {bsky_count}/{total} published")
    print(f"  • Mastodon: {masto_count}/{total} published")
    print("=" * 90 + "\n")

def print_syndication_package(article, auto_open=False):
    tags = get_article_hashtags(article, max_tags=4)
    takeaways = get_article_takeaways(article, max_items=2)

    print("=" * 70)
    print(f"[ ARTICLE ] {article['title']}")
    print(f"[ URL ] {article['url']}")
    print(f"[ HASHTAGS ] {' '.join(tags)}")
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
    print(f"tags: {', '.join(article['tags'][:4])}")
    print("---\n")

    print("[ REDDIT DRAFT POST SNIPPET (HIGH-DENSITY COPY) ]")
    print("-" * 70)
    print(f"**Title**: {article['title']}\n")
    if takeaways:
        print("**Key Architecture / Highlights**:")
        for t in takeaways:
            print(f"* {t}")
        print()
    else:
        print(f"**Summary**: {article['description']}\n")
    print(f"Full technical breakdown & benchmark commands: [{article['url']}]({article['url']})")
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
    parser.add_argument("--status", action="store_true", help="Display syndication status overview table")
    parser.add_argument("--sync-unposted", action="store_true", help="Auto-publish unposted articles to all social APIs with rate limiting")
    parser.add_argument("--limit", "-n", type=int, default=0, help="Limit number of unposted articles to process in this run (e.g. --limit 1 for daily drip)")
    parser.add_argument("--open", "-o", action="store_true", help="Auto-open submit tabs in browser")
    parser.add_argument("--publish-mastodon", action="store_true", help="Auto-publish status to Mastodon API")
    parser.add_argument("--publish-devto", action="store_true", help="Auto-publish article to Dev.to API")
    parser.add_argument("--publish-bsky", action="store_true", help="Auto-publish status to Bluesky API")
    parser.add_argument("--publish", "-p", action="store_true", help="Auto-publish to all social APIs (Mastodon, Dev.to, Bluesky)")
    args = parser.parse_args()

    if args.status:
        print_status_table()
        sys.exit(0)

    articles = get_all_articles()
    if not articles:
        print("[ WARN ] No articles found in blog/ directory.")
        sys.exit(1)

    if args.sync_unposted:
        history = load_history()
        unposted = []
        for a in articles:
            h = history.get(a['slug'], {})
            if 'mastodon' not in h or 'bluesky' not in h or 'devto' not in h:
                unposted.append(a)

        if args.limit and args.limit > 0:
            unposted = unposted[:args.limit]

        print(f"\n[ BATCH SYNC ] Processing {len(unposted)} unposted/partially-posted article(s) (limit={args.limit or 'all'}).")
        for idx, a in enumerate(unposted, 1):
            h = history.get(a['slug'], {})
            print(f"\n[{idx}/{len(unposted)}] Broadcasting: {a['slug']}")
            
            if 'mastodon' not in h:
                publish_mastodon(a)
                time.sleep(2)
            if 'bluesky' not in h:
                publish_bluesky(a)
                time.sleep(2)
            if 'devto' not in h:
                publish_devto(a)
                time.sleep(2)
            
            time.sleep(1)

        print("\n✨ [ BATCH SYNC COMPLETE ] ✨\n")
        print_status_table()
        sys.exit(0)

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
        articles_by_mtime = sorted(articles, key=lambda x: (BLOG_DIR / x['filename']).stat().st_mtime, reverse=True)
        selected_article = articles_by_mtime[0]

    print_syndication_package(selected_article, auto_open=args.open)

    # Parallel API Execution via ThreadPoolExecutor
    publish_tasks = []
    if args.publish or args.publish_mastodon:
        publish_tasks.append(("Mastodon", publish_mastodon))

    if args.publish or args.publish_devto:
        publish_tasks.append(("Dev.to", publish_devto))

    if args.publish or args.publish_bsky:
        publish_tasks.append(("Bluesky", publish_bluesky))

    if publish_tasks:
        print("\n[ API PARALLEL PUBLISH ] Broadcasting to social APIs concurrently...")
        with ThreadPoolExecutor(max_workers=len(publish_tasks)) as executor:
            futures = [executor.submit(func, selected_article) for name, func in publish_tasks]
            for future in futures:
                future.result()

if __name__ == "__main__":
    main()
