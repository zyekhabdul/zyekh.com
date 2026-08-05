<h1 align="center">
  Zyekh's Zero-Dependency Web Hub
</h1>

<p align="center">
  <strong>42 Local-First, Zero-Dependency Developer & Financial Tools. Built entirely with Vanilla JS/CSS.</strong>
</p>

<p align="center">
  <a href="https://zyekh.com">
    <img src="https://img.shields.io/website?url=https%3A%2F%2Fzyekh.com&up_message=online&up_color=brightgreen&down_message=offline&down_color=red&logo=github&label=Website" alt="Website Status">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT">
  </a>
  <a href="https://zyekh.com/manifest.json">
    <img src="https://img.shields.io/badge/PWA-Supported-blueviolet.svg" alt="PWA Ready">
  </a>
  <a href="https://github.com/zyekhabdul/zyekh.com/actions">
    <img src="https://img.shields.io/badge/CI%2FCD-Google_Indexing_API-success.svg" alt="CI/CD Google Indexing">
  </a>
</p>

---

## [ PHILOSOPHY ] The Philosophy

Modern web development has become bloated. A simple password generator now requires a 200MB Node module folder, a bundler, and connects to 3 different telemetry servers. 

This repository is a counter-movement:
- **Zero Frameworks:** No React, No Vue, No Tailwind. Pure semantic HTML5 and Vanilla CSS variables.
- **Zero Dependencies:** No NPM, no third-party libraries. Everything is written from scratch.
- **Zero Tracking:** No Google Analytics, no telemetry. 
- **100% Local Execution:** Every tool runs purely in your browser. Disconnect from the internet, and they still work via Service Worker caching (PWA).

## [ TOOLS ] The 42 Tools (`/tools/`)

You can view the full suite at [zyekh.com/tools](https://zyekh.com/tools).

**Security & Developer Utilities (Examples):**
- **JSON Validator/Formatter:** Parses locally via AST, no data sent to external servers.
- **Diff Checker:** Strict local character-by-character string comparison.
- **Chmod Calculator:** 4-digit octal notation calculator (SUID, SGID, Sticky).
- **JWT Decoder:** Decodes payload securely in-browser without sending tokens anywhere.
- **Password Generator:** Uses `crypto.getRandomValues()` for cryptographically secure entropy.

**Financial Calculators:**
- Mortgage (KPR), PPh 21 Tax, Zakat, Auto Loan, Salary calculators—all executing math locally.

## [ AI-OPTIMIZED ] AI-Optimized Knowledge Base (`/blog/`)

This site isn't just optimized for human readers and Googlebot; it's optimized for LLMs. 
We strictly implement `.well-known/llms.txt` and `llms-full.txt` routing, allowing Perplexity, ChatGPT, and Claude to instantly ingest the entire repository's knowledge base via Markdown.

## [ ARCHITECTURE ] Technical Architecture & CI/CD

```mermaid
graph TD
    A["Developer (Git Push)"] --> B["GitHub Actions CI"]
    B --> C["Node.js Git Diff Analyzer"]
    C -->|Detects .html changes| D["Google Cloud Indexing API"]
    D --> E["Instant Googlebot Crawl"]
    
    F["Client Browser"] --> G["Cloudflare Edge Cache"]
    G --> H["GitHub Pages"]
    H --> I["Service Worker (Offline Capabilities)"]
```

The repository features a state-of-the-art SEO pipeline. Pushing changes to `main` triggers a GitHub Action that calculates the diff, identifies modified `.html` files, and pings the **Google Indexing API** via a secure Service Account to force a crawl within minutes.

## [ LICENSE ] License

[MIT License](LICENSE) - Feel free to fork, dissect, and steal the code. That's the point of open source.
