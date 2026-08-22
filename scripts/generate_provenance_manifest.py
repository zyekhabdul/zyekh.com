#!/usr/bin/env python3
"""
scripts/generate_provenance_manifest.py
Generates data/provenance-manifest.json containing cryptographic SHA-256 digests
of all platform articles, tools, manifests, and knowledge bases.
Zero dependencies, deterministic output, atomic write.
"""

import os
import glob
import json
import hashlib
from datetime import datetime, timezone

def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def generate_provenance_manifest():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root_dir)

    manifest = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "entity": {
            "name": "Zyekh Abdul Qadir Jailani",
            "url": "https://zyekh.com",
            "pgp_public_key": "https://zyekh.com/gpg-key.asc",
            "license": "MIT"
        },
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hash_algorithm": "SHA-256",
        "artifacts": {
            "core_manifests": {},
            "articles": {},
            "tools": {},
            "blueprints": {}
        }
    }

    # Core system files
    core_files = [
        "llms.txt",
        "llms-full.txt",
        "tools/tools-manifest.json",
        "gpg-key.asc",
        "robots.txt",
        "sitemap.xml",
        "sw.js",
        "manifest.json"
    ]
    for cf in core_files:
        if os.path.exists(cf):
            manifest["artifacts"]["core_manifests"][cf] = {
                "sha256": compute_sha256(cf),
                "size_bytes": os.path.getsize(cf)
            }

    # Articles
    for art in sorted(glob.glob("blog/*.html")):
        if art == "blog/index.html":
            continue
        rel_path = art.replace(os.sep, "/")
        manifest["artifacts"]["articles"][rel_path] = {
            "sha256": compute_sha256(art),
            "size_bytes": os.path.getsize(art)
        }

    # Tools
    for tool in sorted(glob.glob("tools/*.html")):
        if tool == "tools/index.html":
            continue
        rel_path = tool.replace(os.sep, "/")
        manifest["artifacts"]["tools"][rel_path] = {
            "sha256": compute_sha256(tool),
            "size_bytes": os.path.getsize(tool)
        }

    # Blueprints
    for bp in sorted(glob.glob("blueprints/*.html")):
        if bp == "blueprints/index.html":
            continue
        rel_path = bp.replace(os.sep, "/")
        manifest["artifacts"]["blueprints"][rel_path] = {
            "sha256": compute_sha256(bp),
            "size_bytes": os.path.getsize(bp)
        }

    os.makedirs("data", exist_ok=True)
    target_path = os.path.join("data", "provenance-manifest.json")
    tmp_path = target_path + ".tmp"

    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write("\n")

    os.replace(tmp_path, target_path)
    
    total_items = (
        len(manifest["artifacts"]["core_manifests"]) +
        len(manifest["artifacts"]["articles"]) +
        len(manifest["artifacts"]["tools"]) +
        len(manifest["artifacts"]["blueprints"])
    )
    print(f"[PROVENANCE] Successfully generated {target_path} ({total_items} artifacts signed with SHA-256).")

if __name__ == "__main__":
    generate_provenance_manifest()
