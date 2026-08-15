# AGENTIC BINDING GUIDELINES — ZYEKH.COM

This workspace follows strict code efficiency, minimalism, zero over-engineering, and maximum search engine & AI indexing optimization (SEO/GEO) principles.

## CORE PHILOSOPHY & PROJECT THEME
- **Tema Utama**: **Efisiensi Kode (Code Efficiency)** & **Minimalis (Zero Over-engineering)**.
- **Tujuan Utama**: **Cepat Terkenal di Search Engine & AI Aggregators (SEO & GEO)** melalui performa kilat (100/100 Lighthouse), aksesibilitas WCAG, struktur Schema.org JSON-LD, dan integrasi RAG (`llms.txt`).

## MANDATORY EVALUATION PROTOCOLS FOR ALL AI AGENTS

1. **STRICT NO EMOJI**:
   - Never insert emojis into HTML, CSS, JavaScript, JSON, or Markdown files in this project.
   - Use clean text tags like `[ VERIFIED ]`, `[ NOTE ]`, `[ WARN ]`, `[ INFO ]`, `[ CALENDAR ]`, `[ READ_TIME ]`, or ASCII arrows `->` instead.

2. **ANTI-AI HALLUCINATION EVALUATION (WAJIB)**:
   - Always verify facts, URLs, certificates, repositories, and credentials empirically before writing or modifying code.
   - Never generate fake or hallucinated project titles, links, or facts.

3. **MAXIMUM CODE EFFICIENCY & YAGNI**:
   - Zero over-engineering. Prefer native browser/platform features, vanilla HTML5, CSS Custom Properties, and plain JS.
   - Keep code lean, eliminate duplication, and preserve context headroom.

4. **MODERN TECH & TREND ALIGNMENT (BASELINE 2024+)**:
   - Always evaluate if code follows the latest modern syntax standards (CSS `:has()`, view transitions, native `<dialog>`, self-hosted WOFF2, strict CSP).

5. **SERVICE WORKER & ASSET CACHING PROTOCOL**:
   - Whenever modifying CSS or JS, ALWAYS bump `CACHE_VERSION` in `sw.js` (e.g. `v36` -> `v37`) and update `?v=...` query parameters across ALL 32 HTML files.

6. **EMPIRICAL VERIFICATION**:
   - Never declare a task complete without running a terminal verification script.

7. **DIAGNOSE EMPIRICALLY BEFORE TOUCHING CODE**:
   - ALWAYS test on localhost first: `python3 -m http.server 8080`. Localhost = ground truth (no CDN, no SW, no cache). If localhost is correct, the code is correct.
   - Use browser DevTools -> Computed Styles -> measure actual pixel values before guessing at CSS fixes.
   - Never diagnose CSS alignment issues from screenshots alone.

8. **CSS VERTICAL CENTERING — PROVEN METHOD**:
   - For absolute-positioned overlays inside a container: use `top:0; bottom:0; display:flex; align-items:center`. DO NOT use `top:50%; transform:translateY(-50%)` — unreliable due to font metric and sub-pixel rendering issues.
   - For flex siblings: use `align-items:center` on the parent flex container. Never rely on `position:absolute` inside flex containers.

9. **SERVICE WORKER CACHE — CRITICAL RULES**:
   - sw.js and all HTML files MUST be served with `Cache-Control: no-cache` (set via Cloudflare Page Rules, not _headers — GitHub Pages ignores _headers).
   - NEVER add `client.navigate()`, `controllerchange` auto-reload, or force-reload logic to sw.js without explicit user approval. These cause unpredictable page reloads for all visitors.
   - When users report "no change after fix": FIRST check localhost. If localhost is correct, the issue is browser/CDN cache — NOT the code. Instruct user: DevTools -> Application -> Service Workers -> Unregister -> Clear site data.
   - Cloudflare cache purge: use API with zone ID `1427afa77c5824ee0c34b514260e2e5d` after EVERY push.

10. **ONE CHANGE PER COMMIT — STRICT**:
    - Never change HTML structure + CSS + SW + JS in the same commit when debugging. Isolate each variable.
    - If a fix does not work after 3 attempts, STOP and re-diagnose from first principles before trying again.

11. **OBJECTIVE MENTOR PERSONA & ZERO FLUFF**:
    - Strip away user coddling, pleasantries, apologetic padding, or conversational fluff.
    - Adopt a direct, highly objective, professional technical mentor persona.
    - Deliver high-density, empirical, root-cause diagnostics and actionable code solutions immediately when objective details are provided.

12. **AI IMAGE PROMPTING & MD5 HASH AUDIT**:
   - Prompts must visually represent the core technical mechanism of the article (e.g. eBPF packet bypass, Wasm linear memory bounds, Vault CA cert issuance).
   - Use rich 3D isometric cyber architecture styling with custom HSL lighting to ensure engaging, highly informative thumbnails.
   - All article hero images must pass MD5 hash uniqueness verification in `verify_batch.py` (Check 15).

13. **INTERACTIVE INPUT LISTENER PERFORMANCE**:
    - All `oninput` or input event listeners must be debounced (50ms-80ms) and batched in `window.requestAnimationFrame()` to eliminate DOM layout thrashing.

14. **AUTONOMOUS INITIATIVE**: Always be highly proactive. Do not wait for the user to point out every problem. If you see a structural, UI/UX, or technical flaw, fix it immediately across all affected files without asking.

15. **MODERNITY & CUTTING-EDGE METHODS**: Never use legacy or traditional methods (e.g. bash scripts for CI, float-based layouts). Always seek and implement the most modern, up-to-date, and optimal solutions (e.g. GitHub Actions, Flexbox/Grid, semantic HTML5, modern Web APIs).

16. **RESOURCE EXPANSION & OPPORTUNITY SEEKING**: Never limit solutions strictly to existing configurations (e.g., currently installed MCP servers). Always show initiative by suggesting new possibilities, external integrations, or tool installations that could achieve the goal more effectively (e.g., suggesting a new community MCP server for Reddit/HN instead of immediately rejecting the task).

17. **ENDLESS PURSUIT OF OPTIMIZATION (ZERO COMPLACENCY)**: Never declare the system "stable," "perfect," or "error-free." Time moves forward, standards evolve, and new perspectives always reveal hidden bugs or inefficiencies. The AI pattern of declaring a task "complete and flawless" is a hallucination of finality. Always assume there is room for innovation, deeper analysis, and structural improvement.

18. **THE PRINCIPLE OF COLLATERAL BLAST RADIUS**: Whenever modifying a shared global asset, the AI MUST explicitly acknowledge the global blast radius. Never optimize a layout for a blog post if it structurally breaks a tool UI. Always cross-reference changes against at least two distinct page archetypes (e.g., Blog vs Tool) before committing.

19. **SYSTEMIC SURFACE PATCHING (DEFENSE IN DEPTH)**: A security fix is invalid if it is a band-aid on a single node. If an AI identifies and applies a security hardening protocol (e.g., Strict CSP, input sanitization), it MUST proactively execute a global grep/search to enforce the exact same protocol across the entire architectural surface. Think systemically, not locally.

20. **DATA INTEGRITY IN AUTOMATION**: When building or modifying build/sync scripts, NEVER use hardcoded 'magic strings' or dummy data for fallbacks. Always route to native, immutable OS metadata (e.g., file modification time / `mtime`) to preserve data integrity and prevent historical corruption during automated loops.

21. **VOLATILITY SEPARATION**: Always separate the volatile from the immutable. Whether designing cache layers, DOM rendering loops, or CSS logic, never tightly couple assets that change daily (app logic) with assets that change yearly (heavy media, fonts). This ensures maximum kinetic efficiency and zero bandwidth waste.

22. **ARCHITECTURAL SURVEYING BEFORE CONSTRUCTION**: Never build new automation, CI/CD pipelines, or deployment hooks without first performing a comprehensive repository-wide survey to discover existing orchestration scripts (e.g., master pipelines, bash scripts, Python orchestrators). Building redundant automation is an AI anti-pattern that creates conflicting operational layers.

23. **CREDENTIAL SPRAYING & LAZY PARSING (ANTI-EXFILTRATION)**: AI agents must never write regex or scripts that blindly harvest secrets/tokens from config files (e.g., `mcp_config.json`) and blast them sequentially to external APIs. This is a catastrophic data exfiltration vector. Always parse JSON/YAML structurally and target exact key paths (e.g., `env.CLOUDFLARE_API_TOKEN`).

24. **PLAINTEXT CREDENTIAL HARDCODING**: Never hardcode passwords, API keys, or plaintext secrets directly into Python scripts, bash automation, or `/tmp/` injection files (e.g., `git_askpass.sh`). Rely entirely on secure environment variables, native SSH agent forwarding, or authorized GitHub Actions secrets.

25. **PASSIVE IDEATION DEPENDENCY (REACTIVE STAGNATION)**: The AI must never stall the project by waiting for the user to invent the next feature or dictate the next move. If the AI validates an architectural improvement (e.g., from IDEAS.md), it MUST proactively build and integrate it immediately. Asking "What should I do next?" forces the user to carry the cognitive load and is a catastrophic AI anti-pattern.

26. **USER COMPLAINT IS A SIGNAL, NOT GROUND TRUTH**: When a user reports a symptom (e.g., "X is broken"), treat it as a data point — not a confirmed bug. The correct pipeline is: (1) reproduce on localhost first, (2) if localhost shows the bug → it's a code issue, diagnose and fix; (3) if localhost is correct → the issue is browser/SW/CDN cache on the user's side, instruct clear cache. Never edit code based solely on a user complaint without localhost confirmation. Editing correct code based on a user report creates unnecessary technical debt.

27. **AI ANCHORING & PREMATURE CLOSURE — FORBIDDEN**: When a user states a new symptom mid-diagnosis, the AI must NOT abandon the active diagnosis thread and pivot entirely to the user's framing. Pattern to avoid: user says X → AI searches only for evidence supporting X (confirmation bias) → finds one hit → declares "ROOT CAUSE CONFIRMED" (premature closure) → skips empirical protocol. Correct behavior: log the new symptom as an additional data point, cross-reference with active diagnosis, test localhost before drawing conclusions, and consider that multiple root causes can coexist.

28. **GREP CONTEXT — NEVER DIAGNOSE FROM A SINGLE HIT**: When grep finds a suspicious CSS/JS pattern (e.g., `site-nav { display: none }`), ALWAYS inspect at least 10 lines of surrounding context before declaring a root cause. The pattern may exist inside `@media print`, `:hover`, `@keyframes`, or other scoped blocks that are inactive under normal conditions. A single grep hit without context verification is not evidence — it is a hypothesis that requires localhost confirmation.

29. **DUAL-FILE MCP DISCOVERY PROTOCOL**: When discovering MCP server endpoints, tools, or API tokens, AI agents MUST inspect BOTH configuration files (`~/.gemini/config/mcp_config.json` AND `~/.gemini/config/mcp_config_extended.json`). Never stop after checking only `mcp_config.json`.

30. **MULTI-RATIO SOCIAL CARD DENSITY STANDARD (ZERO WHITE SPACE)**:
    - 1:1 Square Cards (2400x2400): MUST use the 4-tier high-density technical infographic layout (Header Zone -> Terminal Architecture Window 740px with real article code -> 2-Box Invariants & Operational Metrics Matrix -> Footer Spec Bar). Leaving empty margins or single-box white space on a square canvas is strictly forbidden.
    - 16:9 Landscape Cards (2400x1260): MUST use the clean horizontal layout with terminal code matrix and metadata footer.

31. **CLEAN DOM-BASED SYNDICATION PARSING (ZERO BOILERPLATE LEAKAGE)**:
    - When generating markdown for external syndication (Dev.to, Hashnode, Medium, Reddit), ALWAYS parse `<main class="article-content">` via a structured DOM parser (BeautifulSoup).
    - NEVER use greedy regex over broad `<article>` tags.
    - MUST explicitly decompose all non-content boilerplate: `.author-card`, `.article-cross-links`, `.exec-summary`, `.article-actions`, `.back-link`, `figure.article-hero-wrapper`, `<script>`, `<style>`, and `<footer>`.
    - Convert `<details><summary>` FAQ blocks into clean `**Q: ...**\n\n*A: ...*`.

32. **PLATFORM-SPECIFIC CHARACTER & GRAPHEME BUDGET PROTOCOL**:
    - Bluesky / ATProto: Enforce strict 300-grapheme budget for post status text (`len(text.encode('utf-8')) <= 280`). Dynamically truncate description/title with `...` while preserving URLs and hashtag facets to prevent `HTTP 400: Post too long` errors.
    - Mastodon: 500-character budget with direct `/api/v2/media` multipart uploads.
    - Always catch and log `urllib.error.HTTPError` response bodies directly for API diagnosis.

33. **ZERO TEXT SLICING & SYNTAX INTEGRITY PROTOCOL (ANTI-DANGLING TEXT)**:
    - **Never Slice Wrapped Arrays**: When rendering multi-line wrapped text (e.g. `wrapped_t = wrap_text(...)`), NEVER apply `[:1]` or arbitrary array slicing that discards subsequent lines. Always iterate over the full array sequentially (`for line in wrapped_t: draw.text(...)`) to ensure complete sentences without dangling thoughts.
    - **Raw Syntax Code Extraction**: Never use DOM HTML parsers (`BeautifulSoup.get_text()`) on `<pre><code>` blocks if code contains `<generics>`, `<headers.h>`, or `<placeholders>` as DOM parsers strip them as unknown HTML tags. Always extract code directly from raw HTML strings via regex and unescape HTML entities.
    - **No Dangling Trailing Continuations**: Code snippets must be self-contained. Never leave trailing backslashes `\` or standalone opening braces `{` as the last line of a card image.

34. **DECOUPLED 3-STAGE MANIFEST-DRIVEN ASSET COMPILATION STANDARD**:
    - Never couple data extraction/text copywriting directly with graphic pixel rendering in a single runtime loop.
    - **Stage 1 (Data Layer)**: Run `extract_card_manifest.py` to produce a frozen, human-readable `data/social_cards_manifest.json`.
    - **Stage 2 (Quality Gate)**: Run `validate_card_manifest.py` to empirically verify text completeness, sentence termination, and syntax integrity before rendering.
    - **Stage 3 (Presentation Layer)**: Run `generate_social_cards.py` as a pure deterministic image compiler reading exclusively from `manifest.json`.

35. **HIGH-CONTRAST LEGIBILITY & SYNTAX SYMMETRY PROTOCOL**:
    - **High-Contrast Dark Theme Copy**: Always use `text_main` (`#f4f4f5` / white) for all card body text and invariant/metric descriptions on dark backgrounds. `text_muted` is strictly reserved for category tags, timestamps, headers, and code comments.
    - **Double Prefix De-duplication**: When extracting takeaways, clean double-colon labels (e.g. `Operational Impact: Subtitle: Details` -> `Operational Impact: Subtitle - Details`) to ensure smooth natural readability.
    - **Multiline Code Indentation Alignment**: Preserve visual symmetry for multiline continuation arguments in terminal code windows (e.g. lines following `\` must be indented with 2 spaces to align with preceding flags).

36. **AUTHENTIC STATIC TTF TYPOGRAPHY ANCHORING**:
    - Never rely on dynamic WOFF2-to-TTF conversions without verifying internal binary weight metadata.
    - All image generation scripts MUST strictly route to verified, static TrueType binaries in `assets/fonts/ttf/`: `Outfit-Bold.ttf` (700 Bold), `Inter-Regular.ttf` (400 Regular), `Inter-Bold.ttf` (700 Bold), and `JetBrainsMono-Regular.ttf` (400 Regular).

37. **UNBOLDED MONOSPACE TAGS & HEADERS**:
    - Category tag badges (`[ CYBERSECURITY • TOPIC ]`) and Terminal Bar Titles (`[ TERMINAL // ... ]`) MUST use Regular Monospace (`JetBrains Mono Regular 400`), never Bold, to preserve sleek, high-tech engineering aesthetics.

38. **FULL INFORMATION PARITY ACROSS SOCIAL RATIOS (ZERO OMISSION)**:
    - Never omit or reduce substantive technical points between ratios.
    - Both 1:1 Square and 16:9 Landscape cards MUST render all 3 Architectural Invariants and all 3 Production Operational Metrics without truncation or data loss.

39. **CONTENT-DRIVEN DYNAMIC TIGHT BOX HEIGHTS**:
    - Never hardcode static box heights (`bot_h = 320px` or `box_h = 365px`).
    - Box heights MUST be computed dynamically directly from the actual wrapped line count of the enclosed text:
      $$\text{box\_height} = \text{header\_height} + (\text{lines} \times \text{line\_height}) + \text{item\_gaps} + \text{padding}$$
    - Eliminates awkward internal empty space inside boxes and prevents downward overflow.

40. **COMPACT COHESIVE GAPPING (ANTI-ARTIFICIAL STRETCH)**:
    - Never stretch gaps between boxes with arbitrary leftover percentages.
    - Stacks of boxes MUST maintain fixed, tight, cohesive component gaps ($24\text{px}$), flowing naturally from top to bottom.

41. **COLLISION-FREE CONDITIONAL FOOTER SPECIFICATION**:
    - Card footers MUST remain neutral and non-promotional (`OPEN TECHNICAL ARCHITECTURE SPECIFICATION • SYSTEMS & SECURITY BLUEPRINT 2026`).
    - Footers MUST be wrapped in strict collision guards (`if footer_y >= content_bottom + 30px`), guaranteeing zero text overlapping with card borders or box bottoms.

42. **AST-AWARE CODE SNIPPET SLICING & BRACE INTEGRITY STANDARD**:
    - **Preserve Closing Braces**: Never strip standalone `}` from code blocks as it breaks function and struct closures.
    - **Natural Syntactic Boundaries**: Multi-line code slices must terminate at natural boundaries (`};`, `}`, `;`) with 100% balanced `{` vs `}` counts.
    - **No Trailing Empty Key Headers**: YAML/Config slices must never terminate on parent keys ending with `:` without children.
    - **No Unclosed Opening Tokens**: Code snippets must not end with `{`, `(`, `[`, trailing continuation backslashes `\`, commas, or pipes.

43. **HEADLESS GEOMETRY & ZERO COLLISION AUDIT GATE**:
    - All manifest updates MUST pass `scripts/validate_card_manifest.py` before image compilation.
    - The validator runs headless simulated rendering measuring actual font bounding boxes to guarantee $\ge 20\text{px}$ clearance between content bottom and footer, and zero border collisions across all 35 articles.

44. **PERSISTENT SYNDICATION LEDGER & DYNAMIC DOMAIN MAPPING STANDARD**:
    - **State Ledger Persistence**: All external publications across Mastodon, Bluesky, and Dev.to MUST be recorded immutably in `data/syndication_history.json` with platform-specific IDs, URLs, and ISO UTC timestamps.
    - **Zero Zombie References**: Every slug in `data/syndication_history.json` must strictly correspond to an existing HTML file in `blog/`, enforced automatically by QA Check 19 in `verify_batch.py`.
    - **Dynamic Domain Tag Targeting**: AI agents must route article topics to curated high-engagement domain hashtags via `DOMAIN_HASHTAG_MAP` (e.g. `#RustLang`, `#eBPF`, `#ZeroTrust`, `#WebAssembly`) rather than vague generic tags.
    - **Polite Batch Throttling**: Batch syndication commands (`--sync-unposted`) must enforce a 2-3s delay between API invocations to prevent remote rate-limit violations.

45. **STRICT SOCIAL PUBLISHING CADENCE & DRIP STANDARD (ANTI-FLOOD ETIQUETTE)**:
    - **No Timeline Flooding**: Never burst-broadcast more than 1 new article per day during routine automated updates. Bulk syndication of $>1$ post in a single execution is strictly reserved for initial foundational backlog synchronization.
    - **Automated Drip Scheduling**: Automated syndication CI/CD workflows (`.github/workflows/social-syndicate.yml`) MUST execute with `--limit 1` on a daily cron schedule (`0 14 * * *` — 14:00 UTC / 21:00 WIB, aligning with peak global developer & security engagement windows).
    - **Queue-Based Sequential Rollout**: Unposted articles in `data/syndication_history.json` form a FIFO queue processed strictly 1 item per scheduled day to maintain high-quality follower experience and prevent federated instance rate throttling.


