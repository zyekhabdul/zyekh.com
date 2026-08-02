# AGENTIC BINDING GUIDELINES — ZYEKH.COM

This workspace follows strict code efficiency, minimalism, and token preservation principles.

## MANDATORY RULES FOR ALL AI AGENTS

1. **STRICT NO EMOJI**:
   - Never insert emojis into HTML, CSS, JavaScript, JSON, or Markdown files in this project.
   - Use clean text tags like `[ VERIFIED ]`, `[ NOTE ]`, `[ WARN ]`, `[ INFO ]`, `[ CALENDAR ]`, `[ READ_TIME ]`, or ASCII arrows `->` instead.

2. **SERVICE WORKER & ASSET CACHING**:
   - Whenever modifying CSS or JS, ALWAYS bump `CACHE_VERSION` in `sw.js` (e.g. `v36` -> `v37`) and update `?v=...` query parameters across ALL 32 HTML files.

3. **EMPIRICAL VERIFICATION**:
   - Never declare a task complete without running a terminal verification script.

4. **YAGNI & MINIMALISM**:
   - Zero over-engineering. Prefer native platform features and vanilla HTML5/CSS/JS.
