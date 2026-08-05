/**
 * site-nav.js — Native Web Component untuk navigasi zyekh.com
 * Usage: <site-nav active="home|tools|blog|about"></site-nav>
 * Zero dependencies. Baseline 2023+.
 */
// Immediate Theme Init to avoid UI flash
(function() {
  var saved = localStorage.getItem('theme');
  if (saved) {
    document.documentElement.setAttribute('data-theme', saved);
  } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
    document.documentElement.setAttribute('data-theme', 'light');
  }
})();

class SiteNav extends HTMLElement {
  connectedCallback() {
    let active = this.getAttribute('active') || '';

    const links = [
      { href: '/',           label: 'Home',         key: 'home' },
      { href: '/tools/',     label: 'Tools Hub',    key: 'tools' },
      { href: '/blog/',      label: 'Articles',     key: 'blog' },
      { href: '/blueprints/',label: 'Blueprints',   key: 'blueprints' },
      { href: '/about/',     label: 'About & Bio',  key: 'about' }
    ];

    const listItems = links.map(l => {
      const cls = ['nav-link',
        l.key === active ? 'active' : ''
      ].filter(Boolean).join(' ');
      return `<li><a href="${l.href}" class="${cls}" data-nav="${l.key}">${l.label}</a></li>`;
    }).join('');

    this.innerHTML = `
      <header class="header-nav">
        <div class="nav-container">
          <a href="/" class="brand-logo">zyekh.com</a>
          <button class="nav-toggle" id="navToggle" aria-label="Toggle navigation" aria-expanded="false">
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
        const isLight = document.documentElement.getAttribute('data-theme') === 'light';
        const nextTheme = isLight ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', nextTheme);
        localStorage.setItem('theme', nextTheme);
      });
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

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && menu.classList.contains('open')) {
        setOpen(false);
        toggle.focus();
      }
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 960 && menu.classList.contains('open')) {
        setOpen(false);
      }
    });
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
    
    pre.style.position = 'relative';
    pre.appendChild(btn);
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
});

// Single Event Delegation listener for all copy buttons & native share buttons
document.addEventListener('click', async (e) => {
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

  // Copy Code Button Delegation
  const btn = e.target.closest('.copy-code-btn');
  if (!btn) return;
  const pre = btn.closest('pre');
  if (!pre) return;

  const codeElement = pre.querySelector('code');
  const codeText = codeElement ? codeElement.innerText : pre.innerText;
  try {
    await navigator.clipboard.writeText(codeText.trim());
    btn.textContent = 'Copied!';
    btn.style.borderColor = 'var(--text-main)';
    btn.style.color = 'var(--text-main)';
    setTimeout(() => {
      btn.textContent = 'Copy';
      btn.style.borderColor = 'var(--border-color)';
      btn.style.color = 'var(--text-muted)';
    }, 1800);
  } catch (err) {
    btn.textContent = 'Failed';
  }
});
