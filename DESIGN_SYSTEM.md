# ZYEKH.COM — UI/UX & DESIGN SYSTEM GUIDELINES

This document serves as the absolute source of truth for all frontend architecture, UI/UX patterns, and design decisions on `zyekh.com`. AI agents must read and adhere to these principles before creating or modifying any HTML/CSS files.

---

## 1. THE "BAD AI UX" ANTI-PATTERN (STRICTLY PROHIBITED)

When tasked with building UIs, AI models predictably fall into toxic UX anti-patterns: **Oversizing elements** and **Inconsistent mutations**. AIs tend to generate massive paddings, giant fonts, single-column vertical layouts, and randomly change the structure of components across different pages. 

**Why this fails:** It wastes screen real estate, forces the user into endless scrolling, causes cognitive overload, and destroys the site's professional consistency.

**Prohibited AI Habits:**
- 🚫 **Oversized Elements**: Do not use giant paddings (e.g., `padding: 3rem`) or huge fonts for standard cards.
- 🚫 **Single-Column Lists for Data**: Never stack 10+ items vertically if they can be placed in a grid.
- 🚫 **Ad-Hoc CSS Injection**: Do not inject custom `<style>` blocks into HTML headers to create new, disconnected UI components.
- 🚫 **Unclickable Areas**: Never make just the text/title clickable. The entire bounded box (card) must be a clickable anchor `<a>`.
- 🚫 **Design Mutation**: Never invent a new layout for a component (like a Footer, Header, or Card) if that component already exists on another page.

---

## 2. STRICT CROSS-PAGE CONSISTENCY (NO MUTATION)

This is an absolute mandate: **If Part A is designed a certain way originally, all other pages MUST follow exactly that same design.** 

- **Example 1 (Cards)**: If an `.article-card` contains a `div.card-thumb-wrapper`, `div.tags-container`, `h2.card-title`, and `p.article-excerpt`, you must replicate this EXACT DOM structure across all pages that display articles. Do not suddenly remove the tags container or change the `h2` to an `h3` unless globally dictated.
- **Example 2 (Footers)**: The `<footer class="footer">` must be 100% identical across `/blog/`, `/tools/`, and `/blueprints/`. Do not spontaneously create a dark footer for one page and a light footer for another.
- **Actionable Rule**: Before building any component, **analyze the current live pages** (e.g., `tools/index.html` or `blog/index.html`). Identify the existing pattern and **clone it**. Do not get creative with structural layouts if a template already exists.

---

## 3. THE ZYEKH.COM PHILOSOPHY: HIGH DENSITY & EFFORTLESS EXPLORATION

The core UX goal of this project is **Effortless Scanning**. Users are technical professionals who want to parse maximum information with minimum friction.

- **Compact & Scaled Down**: Close the gaps. Scale down elements. Use tighter margins/paddings so that more content fits natively into the user's viewport without scrolling.
- **Grid-First Architecture**: Always display collections (articles, tools, cheatsheets) using CSS Grids to utilize horizontal space effectively.
- **Information Density**: Group related meta-information tightly. Use muted colors `var(--text-muted)` for secondary info to guide the eye directly to the primary titles `var(--text-main)`.

---

## 4. COMPONENT STANDARDIZATION (REUSABILITY)

Do not invent new classes. Always construct pages using the existing standardized classes found in `assets/css/shared.css` and `assets/css/blog.css`.

### A. Layout & Grids
- `.grid-2`: Responsive 2-column grid for articles/blueprints.
- `.grid-3`: Responsive 3-column grid for smaller items/tools.
- `.container-blog`: The standard max-width wrapper for readable content.

### B. Interactive Cards (The "Clickable Box")
Every item in a list or grid must be a fully clickable card. There are only **TWO** acceptable layouts. Do not mix them. Do not create a third layout.

#### Standard A: With Image (Mirrors `/blog/index.html`)
Use this for articles or rich media.
```html
<div class="article-item">
  <article class="article-card">
    <a href="/target-url.html" style="display: flex; flex-direction: column; height: 100%; text-decoration: none; color: inherit;">
      <div class="card-thumb-wrapper">
         <picture>
           <img src="/assets/img/thumbnail.jpg" alt="Description" class="card-thumb-img" loading="lazy" />
         </picture>
      </div>
      <div class="tags-container">
         <span class="meta-tag">#Security</span>
      </div>
      <h2 class="card-title">Technical Title Goes Here</h2>
      <p class="article-excerpt">A concise, 2-line maximum summary of the content.</p>
    </a>
  </article>
</div>
```

#### Standard B: Without Image (Mirrors `/tools/index.html`)
Use this for data items, tools, cheatsheets, and text-heavy lists.
```html
<div class="tool-item">
  <a href="/target-url.html" class="tool-card">
    <div>
      <span class="tool-category">CATEGORY NAME</span>
      <h3 class="tool-title">Utility Title</h3>
      <p class="tool-desc">A concise, 2-line maximum explanation.</p>
    </div>
    <span class="tool-badge">Open Tool →</span>
  </a>
</div>
```

### C. Color & Typography Tokens
- **Backgrounds**: `var(--bg-main)` (body), `var(--bg-card)` (cards/surfaces).
- **Text**: `var(--text-main)` (headings/primary), `var(--text-muted)` (descriptions/meta).
- **Borders**: `var(--border-color)` (idle), `var(--border-hover)` (interactive states).
- **Transitions**: `var(--transition)` (use for all hover effects to ensure smooth scaling/color shifts).

---

## 5. THE FIVE UNWRITTEN LAWS OF ARCHITECTURE

To prevent rogue AI mutations, the following structural components are strictly codified. Do not reinvent these wheels.

### Law 1: Macro Layout Wrappers
You must strictly separate Grid/Hub pages from Reading/Prose pages.
- **Index/Hub Pages (Grid-heavy)**: Must be wrapped in `<main class="main-container">` and use `<header class="page-header">` (containing `.page-title` and `.page-subtitle`).
- **Reading/Prose Pages (Text-heavy)**: Must be wrapped in `<div class="container-blog">` -> `<article class="article-wrapper">` -> `<div class="article-body">`. 

### Law 2: The Navigation Component
Never build a manual `<nav>` tag or unordered list `<ul>` for the top navigation bar. 
- You must always inject the native Web Component: `<site-nav active="page_name"></site-nav>`.

### Law 3: Search & Filter Architecture
If a page requires a category filter system, you must clone the exact layout used in `/tools/index.html`.
- Use `<div class="filter-bar">` containing `<button class="filter-btn">`.

### Law 4: Prose Callouts & Alerts
When writing technical articles or cheatsheets, do not invent custom inline styles for warnings or summaries.
- **TL;DR / Executive Summary** at the top: `<div class="exec-summary">`.
- **Inline Warnings / Notes**: `<div class="callout">`.

### Law 5: Code Block Presentation
Never apply custom background colors or inline styles to terminal outputs or code snippets. 
- All code blocks must simply be wrapped in `<pre><code>`. The `blog.css` handles the `Fira Code` typography, overflow scroll, and Dark Mode syntax coloring automatically.

### Law 6: CSS Grid Children Containing `<pre>` — Grid Blowout Prevention
**Problem**: CSS Grid columns default to `min-width: auto`. When a `.tool-item` (grid child) contains a `<pre>` block with long lines, the `<pre>` forces the column to expand beyond its `1fr` boundary, blowing past the `.main-container` margin.

**Root cause**: `max-width: 100%` on `<pre>` is calculated relative to the grid child's actual size — which has already expanded. The chain breaks at the grid child level, not the `<pre>` level.

**Standard fix** (already codified in `shared.css`):
```css
.tool-item { display: flex; flex-direction: column; min-width: 0; }
```
`min-width: 0` overrides CSS Grid's `min-width: auto` default, allowing the column to shrink to the `1fr` constraint. The `<pre>` then correctly scrolls horizontally within its bounded container.

**Rule**: Any new grid child class (e.g. `.article-item`, `.blueprint-item`) that may contain `<pre>` or `<code>` blocks MUST include `min-width: 0`. Do NOT solve this by adding `overflow: hidden` on the card — that clips the horizontal scroll of the code block.

**AI Anti-pattern to avoid**: Proposing ad-hoc solutions (e.g. custom wrapper divs, inline `overflow: hidden`, JS resize observers) before checking if `min-width: 0` on the grid child resolves it.

### Law 7: Copy Button & `<pre>` Wrap in Cards
**Problem**: A dynamically injected absolute "Copy" button inside a `<pre>` block will overlap the code text if the text is long, because the text flows to the 100% width of the container.
**Standard fix**: 
1. The Copy button must be injected as a **sibling** to the `<pre>` (inside a `position: relative` wrapper div), never as a child of `<pre>`.
2. The `<pre>` block within grid cards (e.g., `.tool-card pre`) must have `padding-right: 3.5rem` to reserve permanent blank space for the absolute Copy button.
3. Grid card `<pre>` blocks should use `white-space: pre-wrap; overflow-y: auto;` to wrap long lines instead of horizontal scrolling, keeping the UI compact.

### Law 8: Inline Code `<code>` Styling
When writing inline code within paragraphs or list items (outside of a `<pre>`), do not use plain text or bold text. 
**Standard fix**: Inline `<code>` must be enclosed in a distinct "box" (background color with border and padding) mirroring the `/blueprints` design. This is already handled globally in `shared.css`. Just wrap the text in `<code>` and the CSS will apply `background: var(--code-bg); padding: 0.15rem 0.3rem; border: 1px solid var(--border-color); border-radius: 4px;`.

### Law 9: Theme Initialization Protocol (Anti-FOUC)
**Problem**: Reading `localStorage` to initialize dark/light mode from within a deferred Web Component (like `site-nav.js`) causes a Flash of Unstyled Content (FOUC), where the page flashes white before turning dark.
**Standard fix**: 
Theme initialization must be executed synchronously before the `<body>` is rendered. This is handled globally by injecting a blocking `<script>` tag directly into the `<head>` of all HTML files. 
- Do **NOT** put `localStorage.getItem('theme')` initialization logic in `site-nav.js`.
- The `sync_content.py` build script automatically injects the anti-FOUC script into all HTML files.
- `site-nav.js` should only contain the click event listener for the toggle button.

---

**FINAL DIRECTIVE TO AI**: Before generating any new page or UI component, cross-reference your structural plan with this document. If your design mutates an existing pattern, mixes up the wrapper classes, or requires excessive scrolling, **you have failed the assignment and must redesign it to be identical to existing patterns.**
