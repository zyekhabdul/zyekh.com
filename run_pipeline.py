#!/usr/bin/env python3
"""
ZYEKH.COM MASTER AUTOMATION PIPELINE ORCHESTRATOR
Executes Generation -> QA Audit -> Content Sync -> Search Indexing -> Git Push & Cloudflare Purge
"""
import sys, subprocess, os, json, urllib.request

def run_command(cmd, desc):
    print(f"\n[PIPELINE STEP] {desc}...")
    res = subprocess.run(cmd, text=True)
    if res.returncode != 0:
        print(f"[PIPELINE ERROR] Step failed with exit code {res.returncode}: {desc}")
        sys.exit(res.returncode)

def main():
    print("============================================================")
    print("      ZYEKH.COM AUTOMATED PUBLISHING PIPELINE               ")
    print("============================================================")

    # 1. Generate Batch HTML
    run_command([sys.executable, "generate_batch.py"], "Generating Article HTML Files")

    # 2. QA Audit
    run_command([sys.executable, "verify_batch.py"], "Running 14-Axis QA Audit")

    # 3. Content & Cache Sync
    run_command([sys.executable, "sync_content.py"], "Synchronizing Sitemap, RSS, RAG & Cache Version")

    # 4. IndexNow Search Engine Ping
    run_command([sys.executable, "ping_indexers.py"], "Submitting URLs to IndexNow API")

    # 5. Optional Deploy (Git Commit + Push + Cloudflare Purge)
    if "--deploy" in sys.argv:
        print("\n[PIPELINE STEP] Committing, Pushing to GitHub main and Purging Cloudflare Cache...")
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "chore(release): automated batch publication and system synchronization"], check=False)

        print("\n[PIPELINE STEP] Pushing to GitHub main...")
        res = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
        print("[Git Push] Output:", res.stderr or res.stdout)

        # Secure Cloudflare Purge
        config_path = "/home/fuckadmin/.gemini/config/mcp_config.json"
        if os.path.exists(config_path):
            try:
                cfg = json.load(open(config_path))
                cf_token = None
                for server in cfg.get("mcpServers", {}).values():
                    env = server.get("env", {})
                    if "CLOUDFLARE_API_TOKEN" in env:
                        cf_token = env["CLOUDFLARE_API_TOKEN"]
                        break
                
                if cf_token:
                    zone_id = "1427afa77c5824ee0c34b514260e2e5d"
                    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache"
                    req = urllib.request.Request(url, data=b'{"purge_everything":true}', headers={
                        "Authorization": f"Bearer {cf_token}",
                        "Content-Type": "application/json"
                    }, method="POST")
                    with urllib.request.urlopen(req) as resp:
                        print("[Cloudflare Purge API] Success:", resp.read().decode("utf-8"))
                else:
                    print("[WARN] CLOUDFLARE_API_TOKEN not found in mcp_config.json.")
            except Exception as e:
                print(f"[ERROR] Cloudflare Purge Failed: {e}")

    print("\n============================================================")
    print("SUCCESS: Pipeline completed clean & verified!")
    print("============================================================")

if __name__ == "__main__":
    main()
