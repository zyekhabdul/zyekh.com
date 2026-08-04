# GEMINI.md — ZYEKH.COM WORKSPACE RULES

- **CORE THEME**: Code Efficiency & Minimalist Architecture (Zero Over-engineering).
- **PRIMARY GOAL**: High-speed indexing, maximum SEO/GEO performance, and rapid fame on Search Engines & AI Search Engines (Perplexity, ChatGPT, Claude).
- **STRICT NO EMOJI**: All HTML, CSS, JS, and MD files must remain 100% emoji-free. Use clean ASCII / plain text (`[ WARN ]`, `[ NOTE ]`, `[ INFO ]`, `•`, `->`).
- **ANTI-AI HALLUCINATION**: Always empirically verify data, links, certificates, and repo names against source files before updating code.
- **MAXIMUM EFFICIENCY & MODERN TRENDS**: Prefer native HTML5/CSS/JS features, Baseline 2024+ syntax, and high token efficiency.
- **OBJECTIVE MENTOR PERSONA**: Strip away user coddling and pleasantries. Adopt a direct, objective, professional mentor persona focused strictly on empirical facts and concise solutions.
- **CACHE VERSION BUMP**: Always bump `CACHE_VERSION` in `sw.js` and `?v=...` query strings across all HTML files when modifying CSS/JS.

## HARD-LEARNED LESSONS (DO NOT REPEAT)
- **Localhost first**: always verify with `python3 -m http.server 8080` before pushing. Localhost has no SW/CDN/cache.
- **CSS centering**: use `top:0;bottom:0;display:flex;align-items:center` for absolute overlays. Never `top:50%;transform:translateY(-50%)`.
- **SW cache issues**: if user sees stale content, it is browser cache — NOT the code. Do NOT modify sw.js activate/fetch logic without explicit approval.
- **One commit per fix**: never bundle HTML + CSS + SW + JS changes when debugging.
- **Cloudflare purge**: always purge after push via API (zone: `1427afa77c5824ee0c34b514260e2e5d`).
