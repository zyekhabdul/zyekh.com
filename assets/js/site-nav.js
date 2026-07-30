/**
 * site-nav.js — Native Web Component untuk navigasi zyekh.com
 * Usage: <site-nav active="home|tools|blog"></site-nav>
 * Zero dependencies. Baseline 2023+.
 */
class SiteNav extends HTMLElement {
  connectedCallback() {
    const active = this.getAttribute('active') || '';

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
    if (active === 'home' || location.pathname === '/' || location.pathname === '/index.html') {
      this._initScrollSpy();
    }
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
      if (window.innerWidth > 768 && menu.classList.contains('open')) {
        setOpen(false);
      }
    });
  }

  _initScrollSpy() {
    const sections = ['about', 'skills', 'projects', 'contact'];
    const navLinks = this.querySelectorAll('.nav-link[data-nav]');

    const setActive = (key) => {
      navLinks.forEach(link => {
        if (link.dataset.nav === key) {
          link.classList.add('active');
        } else {
          link.classList.remove('active');
        }
      });
    };

    // IntersectionObserver for section scrollspy
    const sectionElements = sections.map(id => document.getElementById(id)).filter(Boolean);
    if (!sectionElements.length) return;

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          setActive(entry.target.id);
        }
      });
    }, {
      rootMargin: '-20% 0px -60% 0px'
    });

    sectionElements.forEach(sec => observer.observe(sec));

    // Top of page (Hero section) -> Home
    window.addEventListener('scroll', () => {
      if (window.scrollY < 200) {
        setActive('home');
      }
    }, { passive: true });
  }
}

customElements.define('site-nav', SiteNav);
