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
Every item in a list or grid must be a fully clickable card.
```html
<!-- Correct Card Architecture -->
<div class="article-item">
  <article class="article-card">
    <a href="/target-url.html" style="display: block; text-decoration: none; color: inherit;">
      <!-- Thumbnail -->
      <div class="card-thumb-wrapper">
         <img src="/assets/img/thumbnail.jpg" alt="Description" class="card-thumb-img" loading="lazy" />
      </div>
      <!-- Meta -->
      <div class="tags-container">
         <span class="meta-tag">#Security</span>
      </div>
      <!-- Content -->
      <h2 class="card-title">Technical Title Goes Here</h2>
      <p class="article-excerpt">A concise, 2-line maximum summary of the content.</p>
    </a>
  </article>
</div>
```

### C. Color & Typography Tokens
- **Backgrounds**: `var(--bg-main)` (body), `var(--bg-card)` (cards/surfaces).
- **Text**: `var(--text-main)` (headings/primary), `var(--text-muted)` (descriptions/meta).
- **Borders**: `var(--border-color)` (idle), `var(--border-hover)` (interactive states).
- **Transitions**: `var(--transition)` (use for all hover effects to ensure smooth scaling/color shifts).

---

**FINAL DIRECTIVE TO AI**: Before generating any new page or UI component, cross-reference your structural plan with this document. If your design mutates an existing pattern or requires excessive scrolling, **you have failed the assignment and must redesign it to be identical to existing patterns.**
