/**
 * site-nav.js — Native Web Component untuk navigasi zyekh.com
 * Usage: <site-nav active="home|tools|blog"></site-nav>
 * Zero dependencies. Baseline 2023+.
 */
class SiteNav extends HTMLElement {
  connectedCallback() {
    let active = this.getAttribute('active') || '';

    // Check if page loaded with a hash anchor on homepage
    const isHomepage = location.pathname === '/' || 
                       location.pathname.endsWith('/index.html') || 
                       location.pathname.endsWith('/zyekh.com/');

    if (isHomepage) {
      const hashKey = location.hash.replace('#', '');
      if (['about', 'skills', 'projects', 'contact'].includes(hashKey)) {
        active = hashKey;
      }
    }

    const links = [
      { href: '/',         label: 'Home',         key: 'home' },
      { href: '/#about',   label: 'About',        key: 'about' },
      { href: '/#skills',  label: 'Skills',       key: 'skills' },
      { href: '/#projects',label: 'Projects',     key: 'projects' },
      { href: '/tools/',   label: 'Tools Hub', key: 'tools' },
      { href: '/blog/',    label: 'Articles',  key: 'blog' },
      { href: '/#contact', label: 'Contact',      key: 'contact' },
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
          </nav>
        </div>
      </header>`;

    this._initNav();
    this._initActiveTracker(active);
  }

  _initNav() {
    // Centralized Service Worker Registration
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').then(reg => reg.update()).catch(() => {});
      });
    }

    // Centralized Speculation Rules API Injection (Chrome 109+)
    if (typeof HTMLScriptElement !== 'undefined' && HTMLScriptElement.supports && HTMLScriptElement.supports('speculationrules')) {
      if (!document.querySelector('script[type="speculationrules"]')) {
        const specScript = document.createElement('script');
        specScript.type = 'speculationrules';
        specScript.textContent = JSON.stringify({
          prerender: [{
            source: 'document',
            where: {
              and: [
                { href_matches: '/*' },
                { not: { href_matches: '/assets/*' } }
              ]
            },
            eagerness: 'moderate'
          }]
        });
        document.head.appendChild(specScript);
      }
    }

    const toggle = this.querySelector('#navToggle');
    const menu   = this.querySelector('#navMenu');
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

  _initActiveTracker(initialActive) {
    const navLinks = this.querySelectorAll('.nav-link[data-nav]');
    let isClicking = false;
    let clickTimeout = null;

    const setActive = (key) => {
      if (!key) return;
      navLinks.forEach(link => {
        if (link.dataset.nav === key) {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      });
    };

    // 1. Instant Active Highlight on Link Click
    navLinks.forEach(link => {
      link.addEventListener('click', () => {
        const key = link.dataset.nav;
        if (key) {
          setActive(key);
          isClicking = true;
          clearTimeout(clickTimeout);
          clickTimeout = setTimeout(() => { isClicking = false; }, 1000);
        }
      });
    });

    // 2. Hashchange Listener (direct visits / anchor navigation)
    window.addEventListener('hashchange', () => {
      const hashKey = location.hash.replace('#', '');
      if (hashKey && ['about', 'skills', 'projects', 'contact'].includes(hashKey)) {
        setActive(hashKey);
        isClicking = true;
        clearTimeout(clickTimeout);
        clickTimeout = setTimeout(() => { isClicking = false; }, 1000);
      }
    });

    // 3. Gapless Precision Viewport BoundingRect ScrollSpy for Homepage
    const isHomepage = location.pathname === '/' || 
                       location.pathname.endsWith('/index.html') || 
                       location.pathname.endsWith('/zyekh.com/');

    if (isHomepage) {
      const sectionNavMap = {
        'about': 'about',
        'console': 'about',
        'skills': 'skills',
        'projects': 'projects',
        'credentials': 'projects',
        'contact': 'contact'
      };

      const sectionIds = Object.keys(sectionNavMap);
      const sectionElements = sectionIds
        .map(id => document.getElementById(id))
        .filter(Boolean);

      if (sectionElements.length) {
        const handleScroll = () => {
          if (isClicking) return; // Prevent scroll observer from overwriting explicit user click

          // Bottom of page check -> Contact active
          const isAtBottom = (window.innerHeight + window.scrollY) >= (document.documentElement.scrollHeight - 60);
          if (isAtBottom) {
            setActive('contact');
            return;
          }

          // Top of page (scrollY < 120) -> Home active
          if (window.scrollY < 120) {
            setActive('home');
            return;
          }

          // Check viewport bounding rect for active section
          let activeKey = null;
          const viewportThreshold = window.innerHeight * 0.35; // 35% from top

          for (const sec of sectionElements) {
            const rect = sec.getBoundingClientRect();
            if (rect.top <= viewportThreshold && rect.bottom >= 50) {
              activeKey = sectionNavMap[sec.id];
            }
          }

          if (activeKey) {
            setActive(activeKey);
          } else if (window.scrollY < 300) {
            setActive('home');
          }
        };

        window.addEventListener('scroll', handleScroll, { passive: true });

        // Initial check if scroll position > 120
        if (window.scrollY > 120) {
          handleScroll();
        }
      }
    }
  }
}

customElements.define('site-nav', SiteNav);
