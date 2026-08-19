/**
 * site-nav.js — Native Web Component untuk navigasi zyekh.com
 * Usage: <site-nav active="home|tools|blog|about"></site-nav>
 * Zero dependencies. Baseline 2023+.
 */


class SiteNav extends HTMLElement {
  connectedCallback() {
    let active = this.getAttribute('active') || '';

    const links = [
      { href: '/',           label: 'Home',         key: 'home' },
      { href: '/tools/',     label: 'Tools Hub',    key: 'tools' },
      { href: '/blog/',      label: 'Articles',     key: 'blog' },
      { href: '/blueprints/',label: 'Blueprints',   key: 'blueprints' },
      { href: '/links/',     label: 'Link Hub',     key: 'links' },
      { href: 'https://shop.zyekh.com', label: 'Store', key: 'shop', external: true },
      { href: '/about/',     label: 'About & Bio',  key: 'about' },
      { href: '/contact/',   label: 'Contact',      key: 'contact' }
    ];

    const listItems = links.map(l => {
      const cls = ['nav-link',
        l.key === active ? 'active' : ''
      ].filter(Boolean).join(' ');
      const extraAttr = l.external ? ' target="_blank" rel="noopener noreferrer"' : '';
      return `<li><a href="${l.href}" class="${cls}" data-nav="${l.key}"${extraAttr}>${l.label}</a></li>`;
    }).join('');

    this.innerHTML = `
      <header class="header-nav">
        <div class="nav-container">
          <div class="nav-brand-group">
            <a href="/" class="brand-logo">zyekh.com</a>
            <div class="nav-search" id="navSearch"><input type="search" id="navSearchInput" class="nav-search-input" placeholder="Search... (Ctrl+K)" autocomplete="off" role="combobox" aria-autocomplete="list" aria-expanded="false" aria-controls="navSearchResults" aria-label="Search tools and articles">
              <button type="button" class="nav-search-clear" id="navSearchClear" aria-label="Clear search" style="display:none;">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
              <div id="navSearchResults" class="nav-search-dropdown" role="listbox" style="display:none;"></div>
            </div>
          </div>
          <button class="nav-toggle" id="navToggle" aria-label="Toggle navigation menu" aria-expanded="false" aria-controls="navMenu" type="button">
            <span class="hamburger-bar"></span>
            <span class="hamburger-bar"></span>
            <span class="hamburger-bar"></span>
          </button>
          <nav class="nav-menu" id="navMenu">
            <ul class="nav-list">${listItems}</ul>
            <button class="theme-toggle" id="themeToggle" aria-label="Toggle theme" type="button">
              <span class="theme-icon-light">MODE: LIGHT</span>
              <span class="theme-icon-dark">MODE: DARK</span>
            </button>
            <button class="pin-toggle" id="pinToggle" aria-label="Pin Tool" title="Pin this tool to Home" type="button" style="display:none; align-items:center; justify-content:center; background:none; border:none; color:var(--text-main); cursor:pointer; font-size:1.1rem; filter:grayscale(100%); opacity:0.5; transition:transform 0.2s;">
              <span class="pin-icon" style="font-size: 0.75rem; font-weight: bold;">[ PIN ]</span>
            </button>
          </nav>
        </div>
      </header>`;

    this._initNav();
  }

  _initNav() {
    // Centralized Service Worker Registration (Clean & Lightweight)
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(() => {});
      });
    }

    const toggle = this.querySelector('#navToggle');
    const menu   = this.querySelector('#navMenu');
    const themeBtn = this.querySelector('#themeToggle');
    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        const toggleTheme = () => {
          const isLight = document.documentElement.getAttribute('data-theme') === 'light';
          const nextTheme = isLight ? 'dark' : 'light';
          document.documentElement.setAttribute('data-theme', nextTheme);
          localStorage.setItem('theme', nextTheme);
        };

        if (document.startViewTransition) {
          try {
            const transition = document.startViewTransition(toggleTheme);
            if (transition && transition.ready) transition.ready.catch(() => {});
            if (transition && transition.finished) transition.finished.catch(() => {});
          } catch {
            toggleTheme();
          }
        } else {
          toggleTheme();
        }
      });
    }

    const pinBtn = this.querySelector('#pinToggle');
    if (pinBtn) {
      const p = window.location.pathname;
      const isTool = p.startsWith('/tools/') && !p.endsWith('/tools/') && !p.endsWith('index.html');
      
      if (isTool) {
        pinBtn.style.display = 'inline-flex';
        const toolPath = p;
        let toolTitle = document.title.split(' — ')[0];
        
        const getPinned = () => {
          try { return JSON.parse(localStorage.getItem('pinnedTools') || '[]'); } catch { return []; }
        };
        const isPinned = () => getPinned().some(t => t.path === toolPath);
        
        const updatePinUI = () => {
          pinBtn.style.opacity = isPinned() ? '1' : '0.5';
          pinBtn.style.filter = isPinned() ? 'none' : 'grayscale(100%)';
          pinBtn.setAttribute('title', isPinned() ? 'Unpin from Home' : 'Pin to Home');
        };
        updatePinUI();
        
        pinBtn.addEventListener('click', () => {
          let pinned = getPinned();
          if (isPinned()) {
            pinned = pinned.filter(t => t.path !== toolPath);
          } else {
            let cat = 'PINNED TOOL';
            const metaDesc = document.querySelector('meta[name="description"]');
            if (metaDesc && metaDesc.content.toLowerCase().includes('security')) cat = 'SECURITY';
            else if (toolPath.includes('network') || toolPath.includes('ip') || toolPath.includes('subnet')) cat = 'NETWORKING';
            else if (toolPath.includes('json') || toolPath.includes('regex') || toolPath.includes('cron') || toolPath.includes('base64')) cat = 'DEV UTILITY';
            
            pinned.push({ path: toolPath, title: toolTitle, cat: cat });
          }
          localStorage.setItem('pinnedTools', JSON.stringify(pinned));
          updatePinUI();
          pinBtn.style.transform = 'scale(1.3)';
          setTimeout(() => pinBtn.style.transform = 'scale(1)', 200);
        });
      }
    }

    // Hydrate Homepage Pinned Tools
    const grid = document.getElementById('quickToolsGrid');
    if (grid) {
      try {
        const pinned = JSON.parse(localStorage.getItem('pinnedTools') || '[]');
        if (pinned && pinned.length > 0) {
          let newHTML = pinned.map(t => `
            <a href="${t.path}" class="quick-tool-pill" style="border-color:var(--text-main);">
              <span class="quick-tool-cat" style="color:var(--text-main);">[ PIN ] ${t.cat || 'PINNED TOOL'}</span>
              ${t.title}
            </a>
          `).join('');
          newHTML += `
            <button onclick="localStorage.removeItem('pinnedTools'); window.location.reload();" class="quick-tool-pill" style="background:none; cursor:pointer; text-align:left; border-style:dashed;">
              <span class="quick-tool-cat">ACTION</span>
              Clear Pins
            </button>
          `;
          grid.innerHTML = newHTML;
        }
      } catch (e) {}
    }

    if (!toggle || !menu) return;

    // Backdrop
    let backdrop = document.querySelector('.nav-backdrop');
    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.className = 'nav-backdrop';
      backdrop.setAttribute('aria-hidden', 'true');
      document.body.appendChild(backdrop);
    }

    const setOpen = (open) => {
      menu.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', String(open));
      if (open) {
        backdrop.style.display = 'block';
        requestAnimationFrame(() => backdrop.classList.add('active'));
      } else {
        backdrop.classList.remove('active');
        setTimeout(() => { backdrop.style.display = 'none'; }, 300);
      }
    };

    toggle.addEventListener('click', (e) => {
      e.stopPropagation();
      setOpen(!menu.classList.contains('open'));
    });

    menu.addEventListener('click', (e) => {
      if (e.target.closest('.nav-link')) {
        setTimeout(() => setOpen(false), 150);
      }
    });

    backdrop.addEventListener('click', () => setOpen(false));

    this._keydownHandler = (e) => {
      if (!menu.classList.contains('open')) return;
      if (e.key === 'Escape') {
        setOpen(false);
        toggle.focus();
        return;
      }
      if (e.key === 'Tab') {
        const focusable = menu.querySelectorAll('a[href], button, input, textarea, select, details, [tabindex]:not([tabindex="-1"])');
        if (focusable.length === 0) return;
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (e.shiftKey) {
          if (document.activeElement === first || document.activeElement === document.body) {
            e.preventDefault();
            last.focus();
          }
        } else {
          if (document.activeElement === last) {
            e.preventDefault();
            first.focus();
          }
        }
      }
    };
    document.addEventListener('keydown', this._keydownHandler);

    let resizeTicking = false;
    this._resizeHandler = () => {
      if (!resizeTicking) {
        window.requestAnimationFrame(() => {
          if (window.innerWidth > 960 && menu.classList.contains('open')) {
            setOpen(false);
          }
          resizeTicking = false;
        });
        resizeTicking = true;
      }
    };
    window.addEventListener('resize', this._resizeHandler);
  }

  disconnectedCallback() {
    if (this._keydownHandler) document.removeEventListener('keydown', this._keydownHandler);
    if (this._resizeHandler) window.removeEventListener('resize', this._resizeHandler);
  }
}

customElements.define('site-nav', SiteNav);

// Native Zero-Dependency Copy Code Button Injector & Event Delegation
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('pre').forEach(pre => {
    if (pre.querySelector('.copy-code-btn')) return;
    const btn = document.createElement('button');
    btn.className = 'copy-code-btn';
    btn.textContent = 'Copy';
    btn.setAttribute('aria-label', 'Copy code to clipboard');
    btn.style.cssText = 'position:absolute; top:0.5rem; right:0.5rem; background:var(--bg-card); color:var(--text-muted); border:1px solid var(--border-color); font-size:0.75rem; padding:0.2rem 0.55rem; border-radius:4px; cursor:pointer; font-family:sans-serif; transition:all 0.2s; z-index:2;';

    // Wrap pre in a div so button is a sibling (not child) of pre.
    // This prevents button from overlapping code when pre has overflow scroll.
    const wrapper = document.createElement('div');
    wrapper.style.cssText = 'position:relative;';
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);
    wrapper.appendChild(btn);
  });

  // Universal Passive Reading Progress Bar Listener (Throttled via rAF for zero CPU churn)
  const bar = document.querySelector('.reading-progress-bar');
  if (bar) {
    let ticking = false;
    const updateProgress = () => {
      const winScroll = document.documentElement.scrollTop || document.body.scrollTop;
      const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      const scrolled = height > 0 ? (winScroll / height) * 100 : 0;
      bar.style.width = Math.min(100, Math.max(0, scrolled)) + '%';
      ticking = false;
    };
    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(updateProgress);
        ticking = true;
      }
    }, { passive: true });
    updateProgress();
  }

  // Desktop Table of Contents (TOC) Active Scroll-Spy via IntersectionObserver
  const articleHeadings = document.querySelectorAll('.article-body h2[id], .article-body h3[id], .article-content h2[id], .article-content h3[id]');
  const tocLinks = document.querySelectorAll('.toc-card a, .toc-list a, .article-toc a');
  if (articleHeadings.length > 0 && tocLinks.length > 0) {
    const headingMap = new Map();
    tocLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href && href.startsWith('#')) {
        headingMap.set(href.slice(1), link);
      }
    });
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          const activeLink = headingMap.get(id);
          if (activeLink) {
            tocLinks.forEach(l => l.classList.remove('active-toc-item'));
            activeLink.classList.add('active-toc-item');
          }
        }
      });
    }, { rootMargin: '0px 0px -65% 0px', threshold: 0.1 });
    articleHeadings.forEach(h => observer.observe(h));
  }

  // Global Keyboard Productivity Handler: Ctrl+Enter / Cmd+Enter execution in Tool textareas
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
      const activeEl = document.activeElement;
      if (activeEl && (activeEl.tagName === 'TEXTAREA' || activeEl.tagName === 'INPUT')) {
        const container = activeEl.closest('.tool-box, .tool-container, form, main') || document;
        const actionBtn = container.querySelector(
          'button.btn-primary, button[type="submit"], input[type="submit"], ' +
          'button[id*="calc"], button[id*="format"], button[id*="generate"], button[id*="convert"], button[id*="decode"], button[id*="run"], button[id*="eval"], button[id*="btn"]'
        );
        if (actionBtn && typeof actionBtn.click === 'function') {
          e.preventDefault();
          actionBtn.click();
          actionBtn.classList.add('btn-active-flash');
          setTimeout(() => actionBtn.classList.remove('btn-active-flash'), 200);
        }
      }
    }
  });

  // Global Auto-Growing Textarea Elasticity for Utility Tools
  document.addEventListener('input', (e) => {
    if (e.target.tagName === 'TEXTAREA' && (e.target.closest('.tool-box') || e.target.classList.contains('auto-expand') || e.target.closest('.tool-container'))) {
      e.target.style.height = 'auto';
      const nextH = Math.min(e.target.scrollHeight, 480);
      if (nextH > 50) {
        e.target.style.height = nextH + 'px';
      }
    }
  });
});

// Single Event Delegation listener for all copy buttons, share buttons & native lightboxes
document.addEventListener('click', async (e) => {
  // Lightbox Image Delegation
  const img = e.target.closest('.article-body img, .article-content img');
  if (img) {
     let dialog = document.getElementById('nativeLightbox');
     if (!dialog) {
        dialog = document.createElement('dialog');
        dialog.id = 'nativeLightbox';
        dialog.className = 'lightbox-modal';
        dialog.innerHTML = `<img src="" alt="" style="max-height: 90vh; max-width: 90vw; border-radius: var(--radius-md); object-fit: contain;">`;
        document.body.appendChild(dialog);
        dialog.addEventListener('click', (ev) => {
          if (ev.target === dialog) dialog.close();
        });
     }
     const lImg = dialog.querySelector('img');
     lImg.src = img.src;
     lImg.alt = img.alt || '';
     dialog.showModal();
     return;
  }

  // Share Button Delegation
  const shareBtn = e.target.closest('#shareBtn, .btn-share');
  if (shareBtn) {
    const title = document.title;
    const text = document.querySelector('meta[name="description"]')?.content || title;
    const url = window.location.href;
    if (navigator.share) {
      try {
        await navigator.share({ title, text, url });
        return;
      } catch (err) {
        if (err.name === 'AbortError') return;
      }
    }
    try {
      await navigator.clipboard.writeText(url);
      const origText = shareBtn.textContent;
      shareBtn.textContent = 'Link Copied!';
      shareBtn.style.borderColor = 'var(--text-main)';
      setTimeout(() => {
        shareBtn.textContent = origText;
        shareBtn.style.borderColor = 'var(--border-color)';
      }, 2000);
    } catch (err) {}
    return;
  }

  // Copy Code Button & Generic [data-copy-target] Delegation
  const btn = e.target.closest('.copy-code-btn, .btn-copy, [data-copy-target]');
  if (!btn) return;

  let textToCopy = '';
  const targetSel = btn.getAttribute('data-copy-target');
  if (targetSel) {
    const targetEl = document.querySelector(targetSel);
    if (targetEl) {
      textToCopy = targetEl.value || targetEl.innerText || targetEl.textContent || '';
    }
  } else {
    const pre = btn.closest('pre') || btn.parentElement?.querySelector('pre');
    if (pre) {
      const codeElement = pre.querySelector('code');
      textToCopy = codeElement ? codeElement.innerText : pre.innerText;
    } else {
      const card = btn.closest('.hash-result-card, .tool-result, .output-card, tr');
      const valEl = card?.querySelector('.hash-val, .output-val, code');
      if (valEl) textToCopy = valEl.innerText || valEl.textContent || '';
    }
  }

  if (textToCopy && textToCopy.trim() && textToCopy.trim() !== '—') {
    try {
      await navigator.clipboard.writeText(textToCopy.trim());
      const origText = btn.textContent;
      btn.textContent = 'Copied!';
      btn.style.borderColor = 'var(--text-main)';
      btn.style.color = 'var(--text-main)';
      setTimeout(() => {
        btn.textContent = origText || 'Copy';
        btn.style.borderColor = 'var(--border-color)';
        btn.style.color = 'var(--text-muted)';
      }, 1800);
    } catch (err) {
      btn.textContent = 'Failed';
    }
  }
});

// Native Zero-Dependency Inline Header Search Engine (Ctrl+K & Dynamic Dropdown)
(function () {
  let searchData = null;
  let selectedIndex = -1;

  function escapeHTML(str) {
    return String(str || '').replace(/[&<>"']/g, m => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
    }[m]));
  }

  function preloadSearchData() {
    if (searchData) return Promise.resolve(searchData);
    return fetch('/search-index.json')
      .then(r => r.json())
      .then(data => {
        searchData = data;
        return data;
      })
      .catch(() => []);
  }

  // Preload on idle or after short timeout
  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => preloadSearchData());
  } else {
    setTimeout(preloadSearchData, 1000);
  }

  function initInlineSearch() {
    const searchContainer = document.getElementById('navSearch');
    const input = document.getElementById('navSearchInput');
    const dropdown = document.getElementById('navSearchResults');
    const clearBtn = document.getElementById('navSearchClear');
    if (!input || !dropdown) return;

    function syncClearButton() {
      if (clearBtn) {
        clearBtn.style.display = input.value.trim().length > 0 ? 'inline-flex' : 'none';
      }
    }

    if (clearBtn) {
      clearBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        input.value = '';
        syncClearButton();
        closeDropdown();
        input.focus();
      });
    }

    function closeDropdown() {
      dropdown.style.display = 'none';
      dropdown.innerHTML = '';
      input.setAttribute('aria-expanded', 'false');
      input.removeAttribute('aria-activedescendant');
      selectedIndex = -1;
    }

    function updateSelection() {
      const allItems = dropdown.querySelectorAll('.nav-search-item');
      allItems.forEach((el, idx) => {
        if (idx === selectedIndex) {
          el.classList.add('selected');
          el.setAttribute('aria-selected', 'true');
          input.setAttribute('aria-activedescendant', el.id || `nav-opt-${idx}`);
          el.scrollIntoView({ block: 'nearest' });
        } else {
          el.classList.remove('selected');
          el.setAttribute('aria-selected', 'false');
        }
      });
    }

    function highlightTokens(text, tokens) {
      let escaped = escapeHTML(text);
      if (!tokens || tokens.length === 0) return escaped;
      tokens.forEach(t => {
        if (!t || t.length < 2) return;
        const reg = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
        escaped = escaped.replace(reg, '<mark class="search-match">$1</mark>');
      });
      return escaped;
    }

    function renderDropdown(items, sectionTitle, tokens, rawQuery) {
      if (!items || items.length === 0) {
        const safeQuery = escapeHTML(rawQuery || input.value.trim());
        dropdown.innerHTML = `
          <div class="nav-search-empty">
            <div class="nav-search-empty-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                <line x1="8" y1="11" x2="14" y2="11"></line>
              </svg>
            </div>
            <div class="nav-search-empty-title">No results found</div>
            <div class="nav-search-empty-desc">No tools or articles matching "<strong>${safeQuery}</strong>"</div>
          </div>`;
        dropdown.style.display = 'block';
        input.setAttribute('aria-expanded', 'true');
        input.removeAttribute('aria-activedescendant');
        selectedIndex = -1;
        return;
      }

      let html = '';
      if (sectionTitle) {
        html += `<div class="nav-search-section">[ ${escapeHTML(sectionTitle)} ]</div>`;
      }
      html += items.map((item, idx) => `
        <a href="${escapeHTML(item.url)}" id="nav-opt-${idx}" class="nav-search-item" role="option" aria-selected="false">
          <span class="nav-search-type">${escapeHTML((item.type || 'PAGE').toUpperCase())}</span>
          <div class="nav-search-text">
            <strong class="nav-search-title">${highlightTokens(item.title, tokens)}</strong>
            <small class="nav-search-desc">${highlightTokens(item.desc || '', tokens)}</small>
          </div>
        </a>
      `).join('');

      dropdown.innerHTML = html;
      dropdown.style.display = 'block';
      input.setAttribute('aria-expanded', 'true');
      selectedIndex = 0;
      updateSelection();
    }

    let debounceTimer;
    async function filterAndRender(query) {
      const q = query.toLowerCase().trim();
      if (!q) {
        closeDropdown();
        return;
      }
      const data = await preloadSearchData();
      const tokens = q.split(/\s+/).filter(Boolean);
      const filtered = (data || []).filter(item => {
        const corpus = `${item.title} ${item.desc || ''} ${item.type || ''}`.toLowerCase();
        return tokens.every(t => corpus.includes(t));
      }).slice(0, 8);

      renderDropdown(filtered, 'Search Results', tokens, q);
    }

    input.addEventListener('focus', () => {
      const q = input.value.trim();
      if (q) filterAndRender(q);
    });

    input.addEventListener('keydown', (ev) => {
      const items = dropdown.querySelectorAll('.nav-search-item');
      if (ev.key === 'ArrowDown') {
        ev.preventDefault();
        if (items.length > 0) {
          selectedIndex = (selectedIndex + 1) % items.length;
          updateSelection();
        }
      } else if (ev.key === 'ArrowUp') {
        ev.preventDefault();
        if (items.length > 0) {
          selectedIndex = (selectedIndex - 1 + items.length) % items.length;
          updateSelection();
        }
      } else if (ev.key === 'Enter') {
        if (selectedIndex >= 0 && items[selectedIndex]) {
          ev.preventDefault();
          items[selectedIndex].click();
        } else if (items.length > 0) {
          ev.preventDefault();
          items[0].click();
        }
      } else if (ev.key === 'Escape') {
        ev.preventDefault();
        closeDropdown();
        input.blur();
      }
    });

    input.addEventListener('input', (ev) => {
      syncClearButton();
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        filterAndRender(ev.target.value);
      }, 50);
    });

    dropdown.addEventListener('click', (ev) => {
      const item = ev.target.closest('.nav-search-item');
      if (item) {
        closeDropdown();
      }
    });

    document.addEventListener('click', (ev) => {
      if (searchContainer && !searchContainer.contains(ev.target)) {
        closeDropdown();
      }
    });
  }

  function focusSearch() {
    const input = document.getElementById('navSearchInput');
    if (input) {
      if (document.activeElement === input) {
        input.blur();
        const dropdown = document.getElementById('navSearchResults');
        if (dropdown) {
          dropdown.style.display = 'none';
          dropdown.innerHTML = '';
        }
      } else {
        input.focus();
        input.select();
        const q = input.value.trim();
        if (q) {
          const ev = new Event('input', { bubbles: true });
          input.dispatchEvent(ev);
        }
      }
    }
  }

  window.openCmdPalette = focusSearch;
  window.focusNavSearch = focusSearch;

  // Global Ctrl+K / Cmd+K binding
  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      focusSearch();
    }
  });

  // Global search trigger delegation
  document.addEventListener('click', (e) => {
    if (e.target.closest('[data-action="open-search"]')) {
      e.preventDefault();
      focusSearch();
    }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initInlineSearch);
  } else {
    initInlineSearch();
  }
})();
