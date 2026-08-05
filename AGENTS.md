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
