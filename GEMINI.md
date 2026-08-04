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
- **AI Image Prompts**: Never specify object details, visual metaphors, or lighting schemes (e.g. no "shield inside core", no "laser lighting"). Use standardized theme keywords (`3D cyber architecture visual representing [TOPIC], dark background, clean developer aesthetic, 8k render --ar 16:9`) and state ONLY the topic to prevent repetitive composition patterns.
- **MD5 Image Uniqueness**: All article hero images must have 100% unique MD5 hashes. Enforced via `verify_batch.py` (Check 15).
- **Input Listener Debouncing**: Always debounce `oninput` handlers (50ms-80ms) and batch DOM writes in `window.requestAnimationFrame()` to eliminate layout thrashing and typing lag.
