# GEMINI.md — ZYEKH.COM WORKSPACE RULES

- **CORE THEME**: Code Efficiency & Minimalist Architecture (Zero Over-engineering).
- **PRIMARY GOAL**: High-speed indexing, maximum SEO/GEO performance, and rapid fame on Search Engines & AI Search Engines (Perplexity, ChatGPT, Claude).
- **STRICT NO EMOJI**: All HTML, CSS, JS, and MD files must remain 100% emoji-free. Use clean ASCII / plain text (`[ VERIFIED ]`, `[ NOTE ]`, `[ WARN ]`, `[ INFO ]`, `•`, `->`).
- **ANTI-AI HALLUCINATION**: Always empirically verify data, links, certificates, and repo names against source files before updating code.
- **MAXIMUM EFFICIENCY & MODERN TRENDS**: Prefer native HTML5/CSS/JS features, Baseline 2024+ syntax, and high token efficiency.
- **OBJECTIVE MENTOR PERSONA**: Strip away user coddling and pleasantries. Adopt a direct, objective, professional mentor persona focused strictly on empirical facts and concise solutions.
- **CACHE VERSION BUMP**: Always bump `CACHE_VERSION` in `sw.js` and `?v=...` query strings across all HTML files when modifying CSS/JS.

## HARD-LEARNED LESSONS & BINDING PROTOCOLS (DO NOT REPEAT)
- **Localhost first**: always verify with `python3 -m http.server 8080` before pushing. Localhost has no SW/CDN/cache.
- **CSS centering**: use `top:0;bottom:0;display:flex;align-items:center` for absolute overlays. Never `top:50%;transform:translateY(-50%)`.
- **SW cache issues**: if user sees stale content, it is browser cache — NOT the code. Do NOT modify sw.js activate/fetch logic without explicit approval.
- **One commit per fix**: never bundle HTML + CSS + SW + JS changes when debugging.
- **Cloudflare purge**: always purge after push via API (zone: `1427afa77c5824ee0c34b514260e2e5d`).
- **AI Image Prompts**: Prompts must visually represent the core technical mechanism of the article (e.g. eBPF packet bypass, Wasm memory sandbox). Use rich 3D isometric cyber architecture styling with custom HSL lighting to ensure engaging, informative thumbnails. All images must pass Check 15 MD5 uniqueness audit.
- **MD5 Image Uniqueness**: All article hero images must have 100% unique MD5 hashes. Enforced via `verify_batch.py` (Check 15).
- **DUAL-FILE MCP DISCOVERY PROTOCOL**: Whenever discovering MCP endpoints, tools, or API tokens, AI agents MUST inspect BOTH configuration files (`mcp_config.json` AND `mcp_config_extended.json`) under `~/.gemini/config/`. Never assume configuration is limited to a single file.
- **Social Card Density**: Square cards (2400x2400) must fill canvas height via 4-tier infographic layout (Header + 740px Terminal + 2-Box Invariants/Metrics Matrix + Footer). Zero empty white space.
- **Clean DOM Syndication Parsing**: Always parse `<main class="article-content">` with BeautifulSoup and decompose `.author-card`, `.article-cross-links`, `.exec-summary`, `.article-actions`, `.back-link`, `figure`, `footer`. Never use greedy regex.
- **ATProto 300-Grapheme Limit**: Bluesky posts must not exceed 280 bytes in status text. Use `format_bluesky_post_text()` to truncate gracefully and avoid HTTP 400.
- **Zero Text Slicing (Anti-Dangling Sentences)**: Never slice wrapped text arrays (`[:1]`). Always render all wrapped lines sequentially to prevent sentences cutting off mid-thought.
- **Raw Syntax Code Extraction**: Never use DOM parsers on `<pre>` code if code contains `<generics>`, `<headers.h>`, or `<placeholders>` (DOM parsers delete them as unknown HTML tags). Always extract raw code via regex and unescape HTML entities.
- **High-Contrast Legibility & Multiline Indentation Symmetry**: Always render dark theme card body copy in high-contrast `text_main` (`#f4f4f5`), reserving `text_muted` strictly for metadata headers and comments. Clean redundant double-colon prefixes in takeaways, and align multiline bash continuation lines with 2-space indentation.
- **Authentic Static TTF Anchoring (Protocol 36)**: Never use converted WOFF2s for image generation. Always bind directly to static TrueType binaries (`Outfit-Bold.ttf`, `Inter-Regular.ttf`, `JetBrainsMono-Regular.ttf`).
- **Unbolded Monospace Tags & Headers (Protocol 37)**: Keep tags (`[ CYBERSECURITY...]`) and terminal bar headers in 400 Regular monospace.
- **Full Information Parity (Protocol 38)**: Both 1:1 Square and 16:9 Landscape cards MUST render all 3 Invariants and all 3 Metrics without omission.
- **Dynamic Tight Box Height (Protocol 39)**: Box container heights must be computed dynamically from actual text lines to eliminate internal voids.
- **Compact Cohesive Gaps (Protocol 40)**: Use tight fixed 24px component gaps instead of stretched empty spaces.
- **Collision-Free Footer (Protocol 41)**: Wrap footers in strict collision guards and use neutral technical specification copy.
- **AST-Aware Code Slicing (Protocol 42)**: Multi-line code slices must preserve closing braces `}` and never terminate on trailing `:` or unclosed opening tokens.
- **Headless Geometry Gate (Protocol 43)**: `validate_card_manifest.py` runs headless layout simulation to guarantee $\ge 20\text{px}$ footer clearance and zero border collisions.
- **Persistent Syndication Ledger & Dynamic Domain Mapping (Protocol 44)**: Record all social broadcasts immutably in `data/syndication_history.json`, enforce zero zombie slugs via QA Check 19, route topics to `DOMAIN_HASHTAG_MAP`, and apply polite 2-3s rate-limit throttling in batch sync.

- **AUTONOMOUS INITIATIVE**: Always be highly proactive. Do not wait for the user to point out every problem. If you see a structural, UI/UX, or technical flaw, fix it immediately across all affected files without asking.

- **ZERO COMPLACENCY (ENDLESS OPTIMIZATION)**: Never state that the system is "stable" or "error-free." Declaring finality is an AI anti-pattern. Always assume hidden bugs exist when viewed from a different perspective. Keep innovating, keep analyzing, and never stop auditing.
- **MODERNITY & CUTTING-EDGE METHODS**: Never use legacy or traditional methods (e.g. bash scripts for CI, float-based layouts, var(--x) when native features exist). Always seek and implement the most modern, up-to-date, and optimal solutions (e.g. GitHub Actions, Flexbox/Grid, semantic HTML5, modern Web APIs).
- **RESOURCE EXPANSION & OPPORTUNITY SEEKING**: Never limit solutions strictly to existing configurations (e.g., currently installed MCP servers). Always show initiative by suggesting new possibilities, external integrations, or tool installations that could achieve the goal more effectively (e.g., suggesting a new community MCP server for Reddit/HN instead of immediately rejecting the task).

## AI EDITING ANTI-PATTERNS (ANTI-HALLUCINATION)
- **Destructive Blind Generation**: Never overwrite manually curated markdown files (e.g. llms-full.txt or README.md) using automated loops without verifying if the file contains human-authored metadata. Read the file FIRST.
- **Context-Isolated Updates (Cache Desync)**: Editing CSS/JS without realizing the global impact. An AI MUST NEVER update static assets without bumping the global cache string (sw.js and all HTML files). The `sync_content.py` script now has `bump_cache_version()` to automate this.
- **Double Debouncing (Over-engineering)**: Slapping `setTimeout` wrappers blindly inside functions that are already wrapped by a `requestAnimationFrame` debouncer. Always trace the execution path of input handlers to prevent recursive throttling.
- **Credential Spraying & Lazy Parsing**: Never write regex to blindly harvest tokens from config files and send them to 3rd party APIs. This leaks system secrets. Always parse JSON/YAML structurally.
- **Plaintext Credential Hardcoding**: Never hardcode passwords or keys into automation scripts or temporary `/tmp` files (e.g., `git_askpass.sh`).
- **Passive Ideation Dependency (Reactive Stagnation)**: Never force the user to carry the cognitive load of project management. If an audit yields a valid improvement, build it immediately. Asking "What should I do next?" is strictly forbidden.

## ARCHITECTURAL PARADIGMS
- **The Principle of Collateral Blast Radius**: Whenever modifying a shared global asset, the AI MUST explicitly acknowledge the global blast radius. Never optimize a layout for a blog post if it structurally breaks a tool UI. Always cross-reference changes against at least two distinct page archetypes (e.g., Blog vs Tool) before committing.
- **Systemic Surface Patching**: A security fix is invalid if it is a band-aid on a single node. If an AI identifies and applies a security hardening protocol (e.g., Strict CSP, input sanitization), it MUST proactively execute a global grep/search to enforce the exact same protocol across the entire architectural surface. Think systemically, not locally.
- **Data Integrity in Automation**: When building or modifying build/sync scripts, NEVER use hardcoded 'magic strings' or dummy data for fallbacks. Always route to native, immutable OS metadata (e.g., file modification time / `mtime`) to preserve data integrity and prevent historical corruption during automated loops.
- **Volatility Separation**: Always separate the volatile from the immutable. Whether designing cache layers, DOM rendering loops, or CSS logic, never tightly couple assets that change daily (app logic) with assets that change yearly (heavy media, fonts). This ensures maximum kinetic efficiency and zero bandwidth waste.
- **Decoupled 3-Stage Manifest Compilation**: Never extract text and draw pixels in the same runtime pass. Enforce Stage 1 (Manifest Extraction to JSON) -> Stage 2 (Quality Gate Validation) -> Stage 3 (Deterministic Pillow Compilation).
- **Architectural Surveying Before Construction**: Never build new automation, CI/CD pipelines, or deployment hooks without first performing a comprehensive repository-wide survey to discover existing orchestration scripts. Building redundant automation is an AI anti-pattern that creates conflicting operational layers.

