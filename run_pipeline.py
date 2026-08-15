#!/usr/bin/env python3
"""
ZYEKH.COM MASTER AUTOMATION PIPELINE ORCHESTRATOR
Executes Generation -> QA Audit -> Content Sync -> Search Indexing -> Social Syndication -> Git Deploy & Cloudflare Purge
"""
import sys
import subprocess
import os
import json
import re
import urllib.request
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def sanitize_secret_log(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    text = re.sub(r'Bearer\s+[a-zA-Z0-9_\-\.]{10,}', 'Bearer [REDACTED_TOKEN]', text, flags=re.IGNORECASE)
    text = re.sub(r'token\s*[:=]\s*["\']?[a-zA-Z0-9_\-\.]{10,}["\']?', 'token=[REDACTED]', text, flags=re.IGNORECASE)
    text = re.sub(r'api[-_]?key\s*[:=]\s*["\']?[a-zA-Z0-9_\-\.]{10,}["\']?', 'api_key=[REDACTED]', text, flags=re.IGNORECASE)
    text = re.sub(r'password\s*[:=]\s*["\']?[^"\'\s,]{6,}["\']?', 'password=[REDACTED]', text, flags=re.IGNORECASE)
    return text

def run_command(cmd, desc):
    print(f"\n[ PIPELINE STEP ] {desc}...")
    res = subprocess.run(cmd, cwd=str(BASE_DIR), text=True)
    if res.returncode != 0:
        print(f"[ PIPELINE ERROR ] Step failed with exit code {res.returncode}: {desc}")
        sys.exit(res.returncode)

def purge_cloudflare_cache():
    print("\n[ PIPELINE STEP ] Purging Cloudflare CDN Edge Cache...")
    config_paths = [
        Path.home() / ".gemini" / "config" / "mcp_config.json",
        Path.home() / ".gemini" / "config" / "mcp_config_extended.json",
        BASE_DIR / ".env"
    ]
    cf_token = os.environ.get("CLOUDFLARE_API_TOKEN")

    if not cf_token:
        # Check .env first
        env_file = BASE_DIR / ".env"
        if env_file.exists():
            with open(env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and 'CLOUDFLARE_API_TOKEN=' in line:
                        cf_token = line.split('=', 1)[1].strip()
                        break

    if not cf_token:
        # Check MCP configs structurally
        for cfg_path in config_paths[:2]:
            if cfg_path.exists():
                try:
                    cfg = json.loads(cfg_path.read_text(encoding='utf-8'))
                    for server in cfg.get("mcpServers", {}).values():
                        env = server.get("env", {})
                        if "CLOUDFLARE_API_TOKEN" in env:
                            cf_token = env["CLOUDFLARE_API_TOKEN"]
                            break
                    if cf_token:
                        break
                except Exception:
                    pass

    if not cf_token:
        print("[ WARN ] CLOUDFLARE_API_TOKEN not found in environment, .env, or MCP configs.")
        return

    zone_id = "1427afa77c5824ee0c34b514260e2e5d"
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache"
    req = urllib.request.Request(
        url,
        data=b'{"purge_everything":true}',
        headers={
            "Authorization": f"Bearer {cf_token}",
            "Content-Type": "application/json",
            "User-Agent": "ZyekhPipeline/1.0"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("success"):
                print("[ SUCCESS ] Cloudflare Cache Purged Successfully (Zone: " + zone_id + ")")
            else:
                print("[ WARN ] Cloudflare Purge Response:", data)
    except Exception as e:
        print(f"[ ERROR ] Cloudflare Purge API Call Failed: {sanitize_secret_log(e)}")

def run_syndication(slug=None, generate_cards=False, sync_unposted=False):
    syndicate_script = BASE_DIR / "scripts" / "syndicate.py"
    if not syndicate_script.exists():
        print("[ WARN ] scripts/syndicate.py not found. Skipping social syndication.")
        return

    if generate_cards:
        extract_script = BASE_DIR / "scripts" / "extract_card_manifest.py"
        validate_script = BASE_DIR / "scripts" / "validate_card_manifest.py"
        cards_script = BASE_DIR / "scripts" / "generate_social_cards.py"

        print("\n[ PIPELINE STEP ] Executing Decoupled 3-Stage Social Asset Pipeline...")
        if extract_script.exists():
            subprocess.run([sys.executable, str(extract_script)], cwd=str(BASE_DIR), check=True)
        if validate_script.exists():
            subprocess.run([sys.executable, str(validate_script)], cwd=str(BASE_DIR), check=True)
        if cards_script.exists():
            cards_cmd = [sys.executable, str(cards_script)]
            if slug:
                cards_cmd.extend(["--slug", slug])
            else:
                cards_cmd.append("--all")
            subprocess.run(cards_cmd, cwd=str(BASE_DIR), check=True)

    print("\n[ PIPELINE STEP ] Broadcasting to Social APIs & Generating Intents...")
    if sync_unposted:
        cmd = [sys.executable, str(syndicate_script), "--sync-unposted"]
    elif slug:
        cmd = [sys.executable, str(syndicate_script), "--publish", "--slug", slug]
    else:
        cmd = [sys.executable, str(syndicate_script), "--publish", "--latest"]

    subprocess.run(cmd, cwd=str(BASE_DIR), check=False)

def main():
    parser = argparse.ArgumentParser(
        description="Zyekh.com Master Publishing & Automation Pipeline Orchestrator"
    )
    parser.add_argument(
        "--skip-generate",
        action="store_true",
        help="Skip batch article HTML generation (generate_batch.py)"
    )
    parser.add_argument(
        "--skip-qa",
        action="store_true",
        help="Skip QA audit step (verify_batch.py)"
    )
    parser.add_argument(
        "--skip-indexnow",
        action="store_true",
        help="Skip IndexNow search engine ping (ping_indexers.py)"
    )
    parser.add_argument(
        "--syndicate",
        action="store_true",
        help="Broadcast article to social channels (Mastodon, Dev.to, Bluesky) via scripts/syndicate.py"
    )
    parser.add_argument(
        "--sync-unposted",
        action="store_true",
        help="Broadcast all unposted articles to social channels with rate-limiting"
    )
    parser.add_argument(
        "--social-cards",
        action="store_true",
        help="Pre-generate dual-theme social cards before syndication"
    )
    parser.add_argument(
        "--slug",
        type=str,
        help="Specify target article slug for selective syndication or card generation"
    )
    parser.add_argument(
        "--purge-cf",
        action="store_true",
        help="Execute standalone Cloudflare CDN edge cache purge"
    )
    parser.add_argument(
        "--deploy",
        action="store_true",
        help="Commit changes locally and purge Cloudflare cache"
    )

    args = parser.parse_args()

    print("============================================================")
    print("      ZYEKH.COM AUTOMATED PUBLISHING PIPELINE               ")
    print("============================================================")

    # Standalone Cloudflare Purge mode
    if args.purge_cf and not any([not args.skip_generate, not args.skip_qa, args.syndicate, args.sync_unposted]):
        purge_cloudflare_cache()
        print("\n[ SUCCESS ] Standalone Cloudflare purge completed.")
        return

    # 1. Generate Batch HTML
    if not args.skip_generate:
        run_command([sys.executable, "generate_batch.py"], "Generating Article HTML Files")

    # 2. QA Audit (Strict 21-axis verification)
    if not args.skip_qa:
        run_command([sys.executable, "verify_batch.py"], "Running 21-Axis QA Audit")

    # 3. Content & Cache Sync
    run_command([sys.executable, "sync_content.py"], "Synchronizing Sitemap, RSS, RAG & Cache Version")

    # 4. Generate llms-full.txt
    run_command([sys.executable, "generate_llms_full.py"], "Generating llms-full.txt for GEO")

    # 5. IndexNow Search Engine Ping
    if not args.skip_indexnow:
        run_command([sys.executable, "ping_indexers.py"], "Submitting URLs to IndexNow API")

    # 6. Multi-Channel Social Syndication
    if args.syndicate or args.sync_unposted:
        run_syndication(slug=args.slug, generate_cards=args.social_cards, sync_unposted=args.sync_unposted)

    # 7. Deployment / Cloudflare Purge
    if args.deploy or args.purge_cf:
        print("\n[ PIPELINE STEP ] Creating Local Git Commit Checkpoint...")
        subprocess.run(["git", "add", "."], check=False)
        subprocess.run(
            ["git", "commit", "-m", "chore(release): automated batch publication and system synchronization"],
            check=False
        )
        purge_cloudflare_cache()

    print("\n============================================================")
    print("[ SUCCESS ] Master Pipeline Execution Completed Cleanly!")
    print("============================================================")

if __name__ == "__main__":
    main()
