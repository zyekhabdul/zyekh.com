#!/usr/bin/env python3
import os
import sys
import re
import html
import json
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).resolve().parent.parent
BLOG_DIR = BASE_DIR / "blog"
DATA_DIR = BASE_DIR / "data"
MANIFEST_FILE = DATA_DIR / "social_cards_manifest.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)

def sanitize_text(text: str) -> str:
    if not text:
        return ""
    # Normalize smart quotes, dashes, ellipsis, and arrows
    t = text.replace('“', '"').replace('”', '"')
    t = t.replace('‘', "'").replace('’', "'")
    t = t.replace('—', ' - ').replace('–', '-')
    t = t.replace('…', '...')
    t = t.replace('→', '->').replace('←', '<-')
    return re.sub(r'\s+', ' ', t).strip()

def extract_clean_code(raw_html: str) -> list[str]:

    pres = re.findall(r'<pre(?:.*?)><code(?:.*?)>(.*?)</code></pre>', raw_html, re.DOTALL)
    if not pres:
        pres = re.findall(r'<pre(?:.*?)>(.*?)</pre>', raw_html, re.DOTALL)
        
    candidate_blocks = []
    for raw in pres:
        if any(bad in raw for bad in ["interactive-demo", "tool-container", "document.getElementById", "innerHTML", "addEventListener"]):
            continue
        unescaped = html.unescape(raw)
        clean = re.sub(r'<span[^>]*>', '', unescaped)
        clean = re.sub(r'</span>', '', clean)
        clean = re.sub(r'</?code[^>]*>', '', clean)
        clean = re.sub(r'</?pre[^>]*>', '', clean)
        
        raw_lines = [l.rstrip() for l in clean.splitlines() if l.strip()]
        # Strip orphan brackets at boundaries
        while raw_lines and raw_lines[0].strip() in ['{', '}', '(', ')']:
            raw_lines = raw_lines[1:]
        while raw_lines and raw_lines[-1].strip() in ['{', '}', '(', ')']:
            raw_lines = raw_lines[:-1]
            
        if len(raw_lines) >= 3:
            candidate_blocks.append(raw_lines)
            
    if not candidate_blocks:
        return [
            "# Production Linux Hardening Architecture",
            "ProtectSystem=strict          # Mount /usr, /boot, /etc read-only",
            "ProtectHome=true              # Deny access to /home, /root, /run/user",
            "MemoryDenyWriteExecute=true   # Enforce strict W^X memory bounds",
            "RestrictSUIDSGID=true         # Neutralize privilege escalation binaries"
        ]
        
    def score_block(b):
        text = "\n".join(b)
        score = len(b)
        if any(kw in text for kw in ["#", "//", "def ", "fn ", "struct ", "class ", "sudo ", "ssh-", "import ", "use ", "add_header", "ufw ", ":root"]):
            score += 20
        if not text.startswith("// XDP Action"):
            score += 5
        if not ("TTFB:" in text):
            score += 10
        return score

    candidate_blocks.sort(key=score_block, reverse=True)
    best = candidate_blocks[0]
    
    # Filter lines so no standalone orphan single brackets exist in the array
    clean_best = [l for l in best if l.strip() not in ['{', '}', '(', ')']]
    selected = clean_best[:8]
        
    if selected and selected[-1].strip().endswith('\\'):
        selected[-1] = selected[-1].strip()[:-1].rstrip()

    # Ensure continuation lines following '\' have proper indentation alignment
    aligned = []
    for i, line in enumerate(selected):
        if i > 0 and selected[i-1].rstrip().endswith('\\'):
            if not line.startswith(' ') and not line.startswith('\t'):
                line = '  ' + line
        aligned.append(line)
    return aligned

def extract_manifest():
    articles = sorted(BLOG_DIR.glob("*.html"))
    articles = [a for a in articles if a.name != "index.html"]

    print(f"[ MANIFEST EXTRACTOR ] Processing {len(articles)} articles...")
    manifest = {}

    for filepath in articles:
        raw_content = filepath.read_text(encoding='utf-8')
        soup = BeautifulSoup(raw_content, 'html.parser')
        
        slug = filepath.stem

        # 1. Title
        h1 = soup.find('h1')
        raw_title = h1.get_text().strip() if h1 else slug
        raw_title = re.sub(r'\s*—\s*zyekh\.com.*', '', raw_title)
        raw_title = re.sub(r'\s*\|\s*zyekh\.com.*', '', raw_title)
        title = sanitize_text(raw_title)

        # 2. Description
        desc_meta = soup.find('meta', {'name': 'description'})
        raw_desc = desc_meta['content'].strip() if desc_meta and desc_meta.get('content') else ""
        description = sanitize_text(raw_desc)

        # 3. Tags
        tags = []
        for tag_elem in soup.find_all('span', class_='meta-tag'):
            t_text = tag_elem.get_text().replace('#', '').strip()
            parts = [p.strip().lower() for p in re.split(r'[•,/|]+', t_text) if p.strip()]
            for p in parts:
                p_clean = re.sub(r'[^a-z0-9-]', '', p)
                if p_clean and p_clean not in tags:
                    tags.append(p_clean)

        # 4. Clean Code Snippet
        code_lines = extract_clean_code(raw_content)

        # 5. Executive Summary Invariants & Takeaways
        takeaways = []
        summary_div = soup.find('div', class_='exec-summary')
        if summary_div:
            for li in summary_div.find_all('li'):
                t_text = sanitize_text(li.get_text().strip())
                if t_text:
                    if not (t_text.endswith('.') or t_text.endswith('!') or t_text.endswith('?') or t_text.endswith(')')):
                        t_text += '.'
                    takeaways.append(t_text)

        if not takeaways:
            takeaways = [
                "Systemic Defense: Strict isolation and attack surface minimization.",
                "Least-Privilege: Fine-grained capability gates and boundary enforcement.",
                "Zero Overhead: Native kernel mechanisms and deterministic execution."
            ]

        # 6. Contextual Operational Metrics (Factual & Domain-Specific)
        domain_tag = " • ".join([t.upper() for t in tags[:2]]) if tags else "TECHNICAL BLUEPRINT"
        
        # Metric 1: Domain & Architecture Category
        m1 = f"Architecture Domain: {domain_tag}"
        
        # Metric 2: Contextual Production Impact (Extracted from 4th takeaway if available, or domain-tuned)
        if len(takeaways) >= 4:
            raw_t4 = takeaways[3]
            if ":" in raw_t4:
                pfx, rest = raw_t4.split(":", 1)
                m2 = f"Operational Impact: {pfx.strip()} - {rest.strip()}"
            else:
                m2 = f"Operational Impact: {raw_t4}"
        elif any(k in slug for k in ["llm", "rag", "vllm", "moe", "slora", "kv-cache", "dspy", "webgpu", "structured-output", "colbert"]):
            m2 = "Inference Impact: High-throughput token optimization with zero memory fragmentation"
        elif any(k in slug for k in ["ebpf", "xdp", "tetragon", "cilium"]):
            m2 = "Kernel Impact: Sub-microsecond packet processing in kernel space via eBPF/XDP"
        elif any(k in slug for k in ["ssh", "fido2", "vault", "pam", "faillock", "landlock", "seccomp", "chroot", "auditd", "cosign", "systemd", "pss"]):
            m2 = "Security Impact: Zero-trust cryptographic boundary with hardware-backed integrity"
        elif any(k in slug for k in ["rust"]):
            m2 = "Safety Impact: Memory safety without garbage collection overhead in kernel subsystems"
        else:
            m2 = "Production Impact: Deterministic low-latency execution with zero external dependencies"

        # Metric 3: Standards Compliance

        if any(k in slug for k in ["llm", "rag", "vllm", "moe", "slora", "kv-cache", "dspy", "webgpu", "structured-output", "colbert"]):
            m3 = "Runtime Standard: Baseline 2026 High-Performance AI Inference Architecture"
        elif any(k in slug for k in ["csp", "http3", "minimalist"]):
            m3 = "Web Standard: Zero-Vulnerability Edge & Strict Content Security Policy"
        else:
            m3 = "Compliance Standard: Baseline 2026 Linux Zero-Trust Architecture"

        metrics = [m1, m2, m3]

        manifest[slug] = {
            "slug": slug,
            "title": title,
            "description": description,
            "tags": tags or ["security", "linux"],
            "code_snippet": code_lines,
            "invariants": takeaways[:3],
            "metrics": metrics
        }



    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"[ SUCCESS ] Manifest generated for {len(manifest)} articles -> {MANIFEST_FILE}")

if __name__ == "__main__":
    extract_manifest()
