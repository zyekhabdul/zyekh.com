#!/usr/bin/env python3
"""
Automated SOP-Compliant Client-Side Tool Scaffolder for zyekh.com
Generates standard Vanilla HTML5/CSS/JS zero-dependency client-side tools with
full Schema.org JSON-LD, OpenGraph, Anti-FOUC, Anti-Clickjacking, and WCAG accessibility.
"""
import os
import sys
import argparse
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def build_tool_html(tool_id: str, title: str, category: str, desc: str, keywords: str = "") -> str:
    if not keywords:
        keywords = f"{tool_id.replace('-', ' ')}, {tool_id}, online tool, client-side utility, zyekh"

    app_category_map = {
        "AI": "AIApplication",
        "Security": "SecurityApplication",
        "Cryptography": "SecurityApplication",
        "Finance": "FinanceApplication",
        "Media": "MultimediaApplication",
        "Developer": "DeveloperApplication",
        "Utility": "UtilitiesApplication"
    }
    app_cat = app_category_map.get(category, "UtilitiesApplication")

    html = f"""<!DOCTYPE html>
<html lang="id-ID">
<head>
<script>var s=localStorage.getItem('theme');if(s)document.documentElement.setAttribute('data-theme',s);else if(window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches)document.documentElement.setAttribute('data-theme','light');</script>
<meta charset="utf-8"/>
<link as="font" crossorigin="" href="/assets/fonts/outfit-700-normal.woff2" rel="preload" type="font/woff2"/>
<meta content="#09090b" name="theme-color"/>
<meta content="width=device-width, initial-scale=1" name="viewport"/>
<title>{title} — Zero-Dependency Client-Side Tool | Zyekh</title>
<meta content="{desc}" name="description"/>
<meta content="{keywords}" name="keywords"/>
<meta content="Zyekh Abdul Qadir Jailani" name="author"/>
<link href="https://zyekh.com/tools/{tool_id}.html" rel="canonical"/>
<!-- Favicons -->
<link href="/assets/icons/favicon.ico" rel="icon" type="image/x-icon"/>
<link href="/assets/icons/favicon-32x32.png" rel="icon" sizes="32x32" type="image/png"/>
<link href="/assets/icons/favicon-16x16.png" rel="icon" sizes="16x16" type="image/png"/>
<link href="/assets/icons/apple-icon-180x180.png" rel="apple-touch-icon" sizes="180x180"/>
<link href="/manifest.json" rel="manifest"/>
<!-- Open Graph -->
<meta content="zyekh.com" property="og:site_name"/>
<meta content="website" property="og:type"/>
<meta content="{title} — Zero-Dependency Client-Side Tool | Zyekh" property="og:title"/>
<meta content="{desc}" property="og:description"/>
<meta content="https://zyekh.com/tools/{tool_id}.html" property="og:url"/>
<meta content="https://zyekh.com/assets/img/social-cards/tool-{tool_id}-dark-landscape.png" property="og:image"/>
<meta content="https://zyekh.com/assets/img/social-cards/tool-{tool_id}-dark-landscape.png" name="twitter:image"/>
<!-- Schema.org JSON-LD -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "WebApplication",
      "@id": "https://zyekh.com/tools/{tool_id}.html#app",
      "name": "{title}",
      "description": "{desc}",
      "url": "https://zyekh.com/tools/{tool_id}.html",
      "applicationCategory": "{app_cat}",
      "operatingSystem": "All",
      "browserRequirements": "Requires JavaScript. Runs entirely client-side.",
      "inLanguage": "id-ID",
      "isAccessibleForFree": true,
      "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "IDR" }},
      "creator": {{
        "@type": "Person",
        "@id": "https://zyekh.com/#person",
        "name": "Zyekh Abdul Qadir Jailani",
        "url": "https://zyekh.com/"
      }},
      "isPartOf": {{ "@type": "WebPage", "@id": "https://zyekh.com/tools/" }}
    }},
    {{
      "@type": "BreadcrumbList",
      "@id": "https://zyekh.com/tools/{tool_id}.html#breadcrumb",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://zyekh.com/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Tools Hub", "item": "https://zyekh.com/tools/" }},
        {{ "@type": "ListItem", "position": 3, "name": "{title}", "item": "https://zyekh.com/tools/{tool_id}.html" }}
      ]
    }}
  ]
}}
</script>
<!-- Self-hosted Fonts & Styles -->
<link as="font" crossorigin="" href="/assets/fonts/inter-variable-latin.woff2" rel="preload" type="font/woff2"/>
<link href="/assets/fonts/fonts.min.css" rel="stylesheet"/>
<link href="/assets/css/shared.css" rel="stylesheet"/>
<style>
  .tool-workspace {{
    display: grid;
    grid-template-columns: 1fr;
    gap: 1.5rem;
    margin-top: 1.5rem;
  }}
  .tool-card {{
    background: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 1.5rem;
  }}
  .form-group {{
    margin-bottom: 1.25rem;
  }}
  .form-group label {{
    display: block;
    font-size: 0.85rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--text-main);
  }}
  .input-field {{
    width: 100%;
    padding: 0.75rem;
    background: var(--bg-dark);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    color: var(--text-main);
    font-family: inherit;
    font-size: 0.9rem;
    box-sizing: border-box;
  }}
  .input-field:focus {{
    outline: none;
    border-color: var(--accent-color, #3b82f6);
  }}
  .output-box {{
    background: var(--bg-dark);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-sm);
    padding: 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    white-space: pre-wrap;
    word-break: break-all;
    min-height: 80px;
    color: var(--text-main);
  }}
  .btn-action {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.65rem 1.25rem;
    background: var(--accent-color, #3b82f6);
    color: #fff;
    border: none;
    border-radius: var(--radius-sm);
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: var(--transition);
  }}
  .btn-action:hover {{
    filter: brightness(1.1);
  }}
</style>
<script>
window.debounceRAF = function(fn, delay) {{
  delay = delay || 60;
  var timer = null;
  return function() {{
    var context = this, args = arguments;
    clearTimeout(timer);
    timer = setTimeout(function() {{
      window.requestAnimationFrame(function() {{
        fn.apply(context, args);
      }});
    }}, delay);
  }};
}};
</script>
<style id="antiClickjack">body{{display:none !important;}}</style>
<script type="text/javascript">if(self===top){{var ac=document.getElementById("antiClickjack");ac.parentNode.removeChild(ac);}}else{{top.location=self.location;}}</script>
</head>
<body>
<site-nav active="tools"></site-nav>
<main class="main-container">
  <header class="page-header">
    <a class="back-link" href="/tools/">[ ARROW ] Kembali ke Tools Hub</a>
    <h1 class="page-title">{title}</h1>
    <p class="page-desc">{desc}</p>
  </header>

  <div class="tool-workspace">
    <div class="tool-card">
      <div class="form-group">
        <label for="primaryInput">Input Data</label>
        <textarea id="primaryInput" class="input-field" rows="4" placeholder="Masukkan input di sini..."></textarea>
      </div>

      <div style="display: flex; gap: 0.75rem; margin-bottom: 1.25rem;">
        <button id="processBtn" class="btn-action" type="button">Proses Eksekusi</button>
        <button id="clearBtn" class="btn-action" style="background: transparent; border: 1px solid var(--border-color); color: var(--text-main);" type="button">Reset</button>
      </div>

      <div class="form-group" style="margin-bottom: 0;">
        <label for="outputResult">Hasil Output (Local In-Browser)</label>
        <div id="outputResult" class="output-box" aria-live="polite">Hasil akan tampil di sini...</div>
      </div>
    </div>
  </div>
</main>

<script>
document.addEventListener('DOMContentLoaded', function() {{
  var inputEl = document.getElementById('primaryInput');
  var outputEl = document.getElementById('outputResult');
  var processBtn = document.getElementById('processBtn');
  var clearBtn = document.getElementById('clearBtn');

  function executeTool() {{
    var val = (inputEl.value || '').trim();
    if (!val) {{
      outputEl.textContent = 'Menunggu input...';
      return;
    }}
    // Execution logic here
    outputEl.textContent = val;
  }}

  inputEl.addEventListener('input', window.debounceRAF(executeTool, 60));
  processBtn.addEventListener('click', executeTool);
  clearBtn.addEventListener('click', function() {{
    inputEl.value = '';
    outputEl.textContent = 'Menunggu input...';
  }});
}});
</script>
<script src="/assets/js/site-nav.js"></script>
</body>
</html>
"""
    return html

def main():
    parser = argparse.ArgumentParser(
        description="Zyekh.com SOP-Compliant Client-Side Tool Scaffolder"
    )
    parser.add_argument("--id", required=True, help="Tool slug identifier (e.g. subnet-calculator)")
    parser.add_argument("--title", required=True, help="Human readable tool title")
    parser.add_argument("--category", required=True, choices=["Developer", "Security", "Cryptography", "Finance", "Media", "AI", "Utility"], help="Tool category")
    parser.add_argument("--desc", required=True, help="Concise technical description")
    parser.add_argument("--keywords", default="", help="Comma separated SEO keywords")
    parser.add_argument("--dry-run", action="store_true", help="Print generated HTML without writing to disk")
    parser.add_argument("--sync", action="store_true", help="Run tools manifest and content sync automatically after scaffolding")

    args = parser.parse_args()

    slug = args.id.lower().strip().replace(' ', '-')
    target_path = BASE_DIR / "tools" / f"{slug}.html"

    if target_path.exists() and not args.dry_run:
        print(f"[ ERROR ] Target file already exists: {target_path}")
        sys.exit(1)

    html_content = build_tool_html(
        tool_id=slug,
        title=args.title,
        category=args.category,
        desc=args.desc,
        keywords=args.keywords
    )

    if args.dry_run:
        print(f"\n[ DRY-RUN ] Generated HTML for tools/{slug}.html:\n")
        print(html_content)
        return

    target_path.write_text(html_content, encoding='utf-8')
    print(f"\n[ SUCCESS ] Created tool file: tools/{slug}.html ({len(html_content)} bytes)")

    if args.sync:
        print("\n[ STEP ] Syncing Tools Manifest & Content Metadata...")
        subprocess.run([sys.executable, str(BASE_DIR / "scripts" / "generate_tools_manifest.py")], cwd=str(BASE_DIR), check=True)
        subprocess.run([sys.executable, str(BASE_DIR / "sync_content.py")], cwd=str(BASE_DIR), check=True)
        print("[ SUCCESS ] Manifest and search registry synchronized!")

if __name__ == "__main__":
    main()
