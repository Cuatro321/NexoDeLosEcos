/* simple progressive service worker */
const CACHE_STATIC = 'nexo-static-v3';
const CORE_ASSETS = [
  '/', '/offline/',
  '/static/css/theme.css',
  '/static/js/app.js',
  '/static/icons/favicon.ico',
  '/static/icons/favicon.svg',
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(CACHE_STATIC).then(c => c.addAll(CORE_ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_STATIC).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Network-first para documentos HTML
async function networkFirst(req) {
  try {
    const fresh = await fetch(req);
    const cache = await caches.open(CACHE_STATIC);
    cache.put(req, fresh.clone());
    return fresh;
  } catch {
    const cached = await caches.match(req);
    if (cached) return cached;
    if (req.mode === 'navigate') return caches.match('/offline/');
    throw new Error('offline');
  }
}

// Stale-while-revalidate para estáticos
async function swr(req) {
  const cache = await caches.open(CACHE_STATIC);
  const cached = await cache.match(req);
  const network = fetch(req).then(res => { cache.put(req, res.clone()); return res; }).catch(() => null);
  return cached || network || Response.error();
}

self.addEventListener('fetch', (e) => {
  const req = e.request;
  const url = new URL(req.url);
  if (req.method !== 'GET') return;

  if (req.headers.get('accept')?.includes('text/html')) {
    e.respondWith(networkFirst(req));
  } else if (url.pathname.startsWith('/static/')) {
    e.respondWith(swr(req));
  }
});
