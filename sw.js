/* zyekh.com Service Worker — Cache Strategy */
const CACHE_VERSION = 'v71';
const CACHE_NAME = `zyekh-${CACHE_VERSION}`;

/* Assets to precache on install (shell) */
const PRECACHE = [
  '/offline.html',
  '/assets/css/shared.css',
  '/assets/js/site-nav.js',
  '/assets/fonts/fonts.css',
  '/assets/fonts/inter-variable-latin.woff2',
  '/assets/fonts/outfit-600-normal.woff2',
  '/assets/fonts/outfit-700-normal.woff2',
  '/assets/fonts/outfit-800-normal.woff2',
  '/assets/fonts/fira-code-400-normal.woff2',
  '/assets/fonts/fira-code-600-normal.woff2',
  '/gpg-key.asc',
  '/api/v1/profile.json',
  '/llms-full.txt'
];

/* ── Install: precache font shell ── */
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache =>
        Promise.allSettled(
          PRECACHE.map(u => cache.add(u).catch(err =>
            console.warn('[SW] Precache skip (not found):', u, err)
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

  /* Fonts & icons → Cache-First (immutable assets) */
  if (url.pathname.startsWith('/assets/fonts/') ||
      url.pathname.startsWith('/assets/icons/')) {
    event.respondWith(cacheFirst(request));
    return;
  }

  /* HTML navigation → Network-First + Navigation Preload */
  if (request.mode === 'navigate') {
    event.respondWith(networkFirstNav(event));
    return;
  }

  /* Everything else → Stale-While-Revalidate */
  event.respondWith(staleWhileRevalidate(request));
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

/* Stale-While-Revalidate for CSS, images, etc. */
async function staleWhileRevalidate(request) {
  const cache = await caches.open(CACHE_NAME);
  const cached = await cache.match(request);
  const fetchPromise = fetch(request).then(response => {
    if (response.ok) cache.put(request, response.clone());
    return response;
  }).catch(() => cached);
  return cached || fetchPromise;
}
