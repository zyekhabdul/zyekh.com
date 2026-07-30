/**
 * site-nav.js — Native Web Component untuk navigasi zyekh.com
 * Usage: <site-nav active="home|tools|blog"></site-nav>
 * Zero dependencies. Baseline 2023+.
 */
class SiteNav extends HTMLElement {
  connectedCallback() {
    let active = this.getAttribute('active') || '';

    // Check if page loaded with a hash anchor on homepage
    if (location.pathname === '/' || location.pathname === '/index.html' || location.pathname.endsWith('/zyekh.com/')) {
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
      { href: '/tools/',   label: '🧰 Tools Hub', key: 'tools' },
      { href: '/blog/',    label: '📰 Articles',  key: 'blog' },
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
    const toggle = this.querySelector('#navToggle');
    const menu   = this.querySelector('#navMenu');
    if (!toggle || !menu) return;

    // Backdrop
    const backdrop = document.createElement('div');
    backdrop.className = 'nav-backdrop';
    backdrop.setAttribute('aria-hidden', 'true');
    document.body.appendChild(backdrop);

    const setOpen = (open) => {
      menu.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', String(open));
      document.body.style.overflow = open ? 'hidden' : '';
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
          clickTimeout = setTimeout(() => { isClicking = false; }, 900);
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
        clickTimeout = setTimeout(() => { isClicking = false; }, 900);
      }
    });

    // 3. Precision Viewport BoundingRect ScrollSpy for Homepage
    const isHomepage = location.pathname === '/' || location.pathname === '/index.html' || location.pathname.endsWith('/zyekh.com/');
    if (isHomepage) {
      const sectionIds = ['about', 'skills', 'projects', 'contact'];
      const sectionElements = sectionIds
        .map(id => document.getElementById(id))
        .filter(Boolean);

      if (sectionElements.length) {
        const handleScroll = () => {
          if (isClicking) return; // Prevent scroll observer from overwriting explicit user click

          // If at top of page (scrollY < 120) -> Home active
          if (window.scrollY < 120) {
            setActive('home');
            return;
          }

          // Check viewport bounding rect for active section
          let activeSection = null;
          const viewportThreshold = window.innerHeight * 0.35; // 35% from top

          for (const sec of sectionElements) {
            const rect = sec.getBoundingClientRect();
            // Section top is above or near upper viewport threshold, and section bottom is below upper threshold
            if (rect.top <= viewportThreshold && rect.bottom >= 100) {
              activeSection = sec.id;
            }
          }

          if (activeSection) {
            setActive(activeSection);
          } else if (window.scrollY < 300) {
            setActive('home');
          }
        };

        window.addEventListener('scroll', handleScroll, { passive: true });
        handleScroll();
      }
    }
  }
}

customElements.define('site-nav', SiteNav);
