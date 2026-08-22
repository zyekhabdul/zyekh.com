# SUBDOMAIN ARCHITECTURAL STANDARDS & INTEGRATION CONTRACT — ZYEKH.COM
> Authoritative Single Source of Truth (SSOT) for all subdomains under `*.zyekh.com`.

---

## 1. CORE PHILOSOPHY & RUNTIME ARCHITECTURE

All subdomains in the `*.zyekh.com` ecosystem must strictly implement and maintain the following core architectural standards:

1. **Zero-Dependency & Zero-Framework**:
   - Do not import client-side frameworks (React, Vue, Angular, Tailwind CSS, Bootstrap) or heavy runtime libraries for standard components.
   - Standard runtime is native Semantic HTML5, CSS Custom Properties, Vanilla JavaScript, and native Web APIs (`Web Crypto API`, `Canvas API`, `Web Speech API`, `Web Workers`).
2. **100% Local-First Execution & Zero Telemetry**:
   - Computation, data parsing, cryptographic operations, and rendering must execute directly in the client's browser.
   - Telemetry scripts, ad trackers (Google Analytics, Meta Pixel, Hotjar), and third-party profiling are strictly prohibited.
3. **Self-Hosted Static Binary Assets**:
   - Zero external CDN links for stylesheets or fonts (e.g. Google Fonts, cdnjs, unpkg are banned).
   - Fonts must be self-hosted WOFF2 binaries located in `/assets/fonts/` with `font-display: swap;`.

---

## 2. DESIGN SYSTEM & DESIGN TOKENS (DS-SSOT)

All subdomains must use the unified monochrome design system tokens:

### A. CSS Custom Properties (Tokens)

```css
/* Core Monochrome Token Definition */
:root {
  color-scheme: dark;
  --bg-dark:            #09090b;
  --bg-main:            #09090b;
  --bg-card:            #141417;
  --bg-secondary:       #18181b;
  --border-color:       #27272a;
  --border-color-hover: #52525b;
  --border-hover:       #52525b;
  --text-main:          #fafafa;
  --text-muted:         #a1a1aa;
  --accent-white:       #ffffff;
  --accent:             #ffffff;
  --accent-glow:        rgba(255, 255, 255, 0.1);
  --code-bg:            #000000;

  /* Spacing */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2.5rem;

  /* Radius */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;

  /* Transitions — Spring Curve */
  --transition: 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

[data-theme="light"] {
  color-scheme: light;
  --bg-dark:            #f0f0f3;
  --bg-main:            #ffffff;
  --bg-card:            #ffffff;
  --bg-secondary:       #f4f4f5;
  --border-color:       #d4d4d8;
  --border-color-hover: #71717a;
  --border-hover:       #71717a;
  --text-main:          #09090b;
  --text-muted:         #27272a;
  --accent-white:       #09090b;
  --accent:             #09090b;
  --accent-glow:        rgba(0, 0, 0, 0.05);
  --code-bg:            #e4e4e7;
}
```

### B. Typography Stack
- **Headings / Brand**: `Outfit`, system-ui, -apple-system, sans-serif (700 Bold).
- **Body Text**: `Inter`, system-ui, -apple-system, sans-serif (400 Regular, 600 Semi-Bold).
- **Monospace / Code / Tags**: `JetBrains Mono`, 'Fira Code', ui-monospace, monospace (400 Regular).

### C. Layout Invariants
- **Max Container Width**: Uniform `max-width: 1280px; margin: 0 auto; padding: 0 1.5rem;` across all pages.
- **Off-Canvas Mobile Drawer Breakpoint**: Fixed at `@media (max-width: 960px)`.
- **Clickable Box Pattern**: All list and grid cards must wrap the entire interactive surface in an anchor tag `<a>`.
- **Anti-FOUC (Flash of Unstyled Content)**: Every HTML `<head>` must include the blocking theme script:
  ```html
  <script>
    (function(){
      var t = localStorage.getItem('zyekh_theme') || (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');
      document.documentElement.setAttribute('data-theme', t);
    })();
  </script>
  ```

---

## 3. SECURITY HEADERS & PERMISSION POLICIES

All subdomains served through Cloudflare Pages or Edge reverse proxies must set these HTTP response headers:

```http
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin-when-cross-origin
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Permissions-Policy: accelerometer=(), camera=(), geolocation=(), gyroscope=(), magnetometer=(), microphone=(), payment=(), usb=(), interest-cohort=(), browsing-topics=(), run-ad-auction=(), join-ad-interest-group=()
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; font-src 'self'; img-src 'self' data: https:; connect-src 'self' https://api.zyekh.com https://chat.zyekh.com https://shop.zyekh.com https://docs.zyekh.com https://dist.zyekh.com; frame-ancestors 'none'; base-uri 'self';
```

---

## 4. CACHING & SERVICE WORKER SYNCHRONIZATION

1. **HTML Documents**: `Cache-Control: public, no-cache, must-revalidate`.
2. **Service Worker (`/sw.js`)**: `Cache-Control: no-cache, no-store, must-revalidate`.
3. **Static Assets (`/assets/*`)**: `Cache-Control: public, max-age=31536000, immutable` with asset cache-busting query strings (`?v=VERSION`).
4. **Cache Version Bumping**: Whenever CSS or JS files are updated, the `CACHE_VERSION` in `sw.js` must be incremented, and query version strings across all HTML files must be updated atomically.

---

## 5. MACHINE-INGESTION & GEO STANDARDS

1. **RAG Discovery**: Each subdomain must support or link to `.well-known/llms.txt` and `/llms-full.txt`.
2. **Schema.org Structured Data**: All pages must embed JSON-LD (`WebSite`, `Organization`, `WebApplication`, `TechArticle`, or `Product`).
3. **Tools Manifest**: Web utilities must expose structured parameter schemas conforming to `tools-manifest.json`.

---

## 6. PRE-DEPLOYMENT QA GATE CHECKLIST

Before deploying any new page or subdomain service, the following checks must pass:
1. `[ QA 1 ]` Zero emoji characters in code or content (verified by `check_emojis.py`).
2. `[ QA 2 ]` WCAG 2.2 AA Contrast Compliance (>= 4.5:1 ratio).
3. `[ QA 3 ]` Self-hosted WOFF2 fonts with `font-display: swap`.
4. `[ QA 4 ]` Anti-FOUC theme script present in `<head>`.
5. `[ QA 5 ]` Responsive viewport verification at 360px, 768px, 960px, 1280px, and 1920px.
6. `[ QA 6 ]` Live HTTP Smoke Test 200 OK on all routes without CSP errors.
7. `[ QA 7 ]` Valid Schema.org JSON-LD without duplicate `@id` conflicts.
