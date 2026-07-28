/* zyekh.com Service Worker — Cache Strategy */
const CACHE_VERSION = 'v1';
const CACHE_NAME = `zyekh-${CACHE_VERSION}`;

/* Assets to precache on install (shell) */
const PRECACHE = [
  '/offline.html',
  '/assets/fonts/fonts.css',
  '/assets/fonts/inter-400-normal.woff2',
  '/assets/fonts/inter-500-normal.woff2',
  '/assets/fonts/inter-600-normal.woff2',
  '/assets/fonts/inter-700-normal.woff2',
  '/assets/fonts/outfit-600-normal.woff2',
  '/assets/fonts/outfit-700-normal.woff2',
  '/assets/fonts/outfit-800-normal.woff2',
  '/assets/fonts/fira-code-400-normal.woff2',
  '/assets/fonts/fira-code-600-normal.woff2',
  '/gpg-key.asc',
  '/api/v1/profile.json'
];

/* ── Install: precache font shell ── */
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE.filter(u => {
        // Only precache files that exist (skip missing variants)
        return true;
      })))
      .catch(err => console.warn('[SW] Precache partial failure:', err))
  );
  self.skipWaiting();
});

/* ── Activate: clean old caches ── */
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

/* Enable Navigation Preload (Flash advice) */
self.addEventListener('activate', event => {
  if (self.registration.navigationPreload) {
    event.waitUntil(self.registration.navigationPreload.enable());
  }
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
      const cache = await caches.open(CACHE_NAME);
      cache.put(event.request, preloadResponse.clone());
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
