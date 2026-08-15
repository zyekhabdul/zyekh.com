#!/usr/bin/env python3
"""
Web AI Agent Tool Manifest Generator for zyekh.com
Extracts structured JSON schema for all 43 client-side tools (parameters, execution model, categories)
to enable direct tool-calling and semantic discovery by Browser AI Agents (Claude, ChatGPT, Gemini).
"""
import os
import sys
import glob
import json
import datetime
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent

CATEGORY_MAP = {
    "ai": "AI & LLM Inference",
    "llm": "AI & LLM Inference",
    "token": "AI & LLM Inference",
    "speculative": "AI & LLM Inference",
    "ebpf": "Security & Linux Systems",
    "chmod": "Security & Linux Systems",
    "linux-hardening": "Security & Linux Systems",
    "hardening": "Security & Linux Systems",
    "subnet": "Security & Linux Systems",
    "curl": "Security & Linux Systems",
    "hash": "Cryptography & Encoding",
    "hmac": "Cryptography & Encoding",
    "jwt": "Cryptography & Encoding",
    "base64": "Cryptography & Encoding",
    "uuid": "Cryptography & Encoding",
    "password": "Cryptography & Encoding",
    "pesangon": "Indonesian Finance & Employment",
    "jht": "Indonesian Finance & Employment",
    "jkp": "Indonesian Finance & Employment",
    "pph21": "Indonesian Finance & Employment",
    "kpr": "Indonesian Finance & Employment",
    "thr": "Indonesian Finance & Employment",
    "zakat": "Indonesian Finance & Employment",
    "split-bill": "Indonesian Finance & Employment",
    "regex": "Developer & Web Utilities",
    "json": "Developer & Web Utilities",
    "csv-json": "Developer & Web Utilities",
    "sql": "Developer & Web Utilities",
    "cron": "Developer & Web Utilities",
    "diff-checker": "Developer & Web Utilities",
    "markdown": "Developer & Web Utilities",
    "css-minifier": "Developer & Web Utilities",
    "html-entity": "Developer & Web Utilities",
    "url": "Developer & Web Utilities",
    "image-converter": "Media & Canvas Utilities",
    "svg-converter": "Media & Canvas Utilities",
    "color": "Media & Canvas Utilities",
    "qr": "Media & Canvas Utilities",
    "tts": "Media & Canvas Utilities",
    "pomodoro": "Productivity & Time",
    "countdown": "Productivity & Time",
    "epoch": "Productivity & Time",
    "counter": "Productivity & Time",
    "dice": "Productivity & Time",
    "random-picker": "Productivity & Time",
    "case-converter": "Developer & Web Utilities",
    "lorem": "Developer & Web Utilities",
    "converter": "Developer & Web Utilities",
    "env": "Developer & Web Utilities",
}

def determine_category(slug: str) -> str:
    for key, cat in CATEGORY_MAP.items():
        if key in slug.lower():
            return cat
    return "General Utility"

def generate_tools_manifest(output_path: str = "tools/tools-manifest.json", dry_run: bool = False) -> dict:
    tools_glob = sorted(glob.glob(str(BASE_DIR / "tools" / "*.html")))
    tool_entries = []

    for t_file in tools_glob:
        if t_file.endswith("index.html"):
            continue

        slug = os.path.splitext(os.path.basename(t_file))[0]
        content = open(t_file, "r", encoding="utf-8", errors="ignore").read()
        soup = BeautifulSoup(content, "html.parser")

        h1 = soup.find("h1")
        title = h1.text.strip() if h1 else slug.replace("-", " ").title()
        
        desc_meta = soup.find("meta", {"name": "description"})
        desc = desc_meta["content"].strip() if desc_meta else title

        # Extract input parameters from DOM
        parameters = []
        for inp in soup.find_all(["input", "select", "textarea"]):
            inp_id = inp.get("id") or inp.get("name")
            if not inp_id or inp_id.startswith("search") or inp_id == "themeToggle":
                continue
            
            inp_type = inp.get("type", "text") if inp.name == "input" else inp.name
            if inp_type in ["hidden", "submit", "button"]:
                continue

            placeholder = inp.get("placeholder", "")
            
            # Find associated label if available
            label_text = ""
            if inp.get("id"):
                lbl = soup.find("label", {"for": inp["id"]})
                if lbl:
                    label_text = lbl.text.strip()

            param_desc = label_text or placeholder or inp_id.replace("-", " ").replace("_", " ").title()

            param_entry = {
                "name": inp_id,
                "type": "number" if inp_type == "number" else "string",
                "input_element": inp_type,
                "description": param_desc
            }
            if inp.name == "select":
                opts = [opt.get("value", opt.text.strip()) for opt in inp.find_all("option") if opt.get("value") is not None]
                if opts:
                    param_entry["enum"] = opts[:10]

            parameters.append(param_entry)

        entry = {
            "id": slug,
            "name": title,
            "description": desc,
            "category": determine_category(slug),
            "url": f"https://zyekh.com/tools/{slug}.html",
            "execution": {
                "type": "client_side_javascript",
                "telemetry": "none",
                "offline_ready": True,
                "storage": "local_memory_or_localstorage"
            },
            "parameters": parameters
        }
        tool_entries.append(entry)

    manifest_data = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "name": "zyekh.com Client-Side Web Tools Manifest",
        "version": "1.0.0",
        "description": "Structured machine-readable tool catalog and parameter schemas for Browser AI Agents & LLMs.",
        "platform": "https://zyekh.com",
        "total_tools": len(tool_entries),
        "updated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tools": tool_entries
    }

    target_file = BASE_DIR / output_path
    target_file.parent.mkdir(parents=True, exist_ok=True)
    
    if not dry_run:
        tmp_file = str(target_file) + ".tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2)
        os.replace(tmp_file, str(target_file))
        print(f"[MANIFEST] Generated {target_file} with {len(tool_entries)} tools.")
    else:
        print(f"[DRY-RUN] Would generate {target_file} with {len(tool_entries)} tools.")

    return manifest_data

if __name__ == "__main__":
    is_dry = "--dry-run" in sys.argv
    generate_tools_manifest(dry_run=is_dry)
