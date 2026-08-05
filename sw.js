/* zyekh.com Service Worker — Cache Strategy */
const CACHE_VERSION = 'v128';
const CACHE_NAME = `zyekh-${CACHE_VERSION}`;

/* Assets to precache on install (minimal core shell) */
const PRECACHE = [
  '/offline.html',
  '/assets/css/shared.css',
  '/assets/js/site-nav.js',
  '/assets/fonts/fonts.css',
  '/assets/fonts/inter-variable-latin.woff2'
];

/* ── Install: precache core shell ── */
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache =>
        Promise.allSettled(
          PRECACHE.map(u => cache.add(u).catch(err =>
            console.warn('[SW] Precache skip:', u, err)
          ))
        )
      )
  );
  self.skipWaiting();
});

/* ── Activate: clean old caches & enable navigation preload ── */
self.addEventListener('activate', event => {
  event.waitUntil(
    Promise.all([
      caches.keys().then(keys =>
        Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
      ),
      self.registration.navigationPreload?.enable() ?? Promise.resolve()
    ])
  );
  self.clients.claim();
});

/* ── Fetch: route by resource type ── */
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  /* Skip non-GET and cross-origin requests */
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;

  /* Static Assets (CSS, JS, Fonts, Images) → Cache-First */
  if (url.pathname.startsWith('/assets/')) {
    event.respondWith(cacheFirst(request));
    return;
  }

  /* HTML navigation → Network-First + Navigation Preload */
  if (request.mode === 'navigate') {
    event.respondWith(networkFirstNav(event));
    return;
  }

  /* Everything else → Cache-First */
  event.respondWith(cacheFirst(request));
});

/* Cache-First: serve from cache, fallback to network then cache */
async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    return new Response('', { status: 408 });
  }
}

/* Network-First with Navigation Preload for HTML */
async function networkFirstNav(event) {
  try {
    const preloadResponse = await event.preloadResponse;
    if (preloadResponse) {
      if (preloadResponse.ok) {
        const cache = await caches.open(CACHE_NAME);
        cache.put(event.request, preloadResponse.clone());
      }
      return preloadResponse;
    }
    const response = await fetch(event.request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(event.request, response.clone());
    }
    return response;
  } catch {
    const cached = await caches.match(event.request);
    return cached || await caches.match('/offline.html');
  }
}
