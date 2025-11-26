from django.http import HttpResponse
from django.views.generic import TemplateView
import json

class HomeView(TemplateView):
    template_name = 'core/home.html'

class OfflineView(TemplateView):
    template_name = 'core/offline.html'

class ManifestView(TemplateView):
    content_type = 'application/manifest+json'

    def get(self, request, *args, **kwargs):
        manifest = {
            "name": "El Nexo de los Ecos",
            "short_name": "NexoEcos",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#0b0f14",
            "theme_color": "#0b0f14",
            "icons": [
                {"src": "/static/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
                {"src": "/static/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
                {"src": "/static/icons/maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
            ]
        }
        return HttpResponse(json.dumps(manifest), content_type=self.content_type)


class ServiceWorkerView(TemplateView):
    content_type = 'application/javascript'

    def get(self, request, *args, **kwargs):
        js = r"""
// ========= Nexo SW v4 =========
// - Cachea páginas HTML que visitas (Inicio, Códex, etc.)
// - Si se cae la red: primero usa la copia en caché, si no existe muestra /offline/
// ===============================

const STATIC_CACHE = 'nexo-static-v4';
const PAGES_CACHE  = 'nexo-pages-v1';
const OFFLINE_URL  = '/offline/';

// Recursos estáticos mínimos para que la app arranque y la pantalla offline
const STATIC_ASSETS = [
  '/',
  '/offline/',
  '/static/css/theme.css',
  '/static/js/app.js'
];

// -------- INSTALL: precache básico --------
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(STATIC_CACHE).then(cache => cache.addAll(STATIC_ASSETS))
  );
  self.skipWaiting();
});

// -------- ACTIVATE: limpia versiones viejas --------
self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys
        .filter(k => ![STATIC_CACHE, PAGES_CACHE].includes(k))
        .map(k => caches.delete(k))
    );

    // navigationPreload = un pequeño boost en navegaciones
    if ('navigationPreload' in self.registration) {
      await self.registration.navigationPreload.enable();
    }

    await self.clients.claim();
  })());
});

// -------- FETCH --------
self.addEventListener('fetch', event => {
  const req = event.request;

  // 1) Navegaciones de páginas HTML
  if (req.mode === 'navigate') {
    event.respondWith(handleNavigation(event));
    return;
  }

  // 2) Archivos estáticos (CSS, JS, imágenes…)
  if (req.url.includes('/static/')) {
    event.respondWith(cacheFirst(req));
  }
});

// ===== Estrategias =====

// Navegaciones: network-first → cache → offline
async function handleNavigation(event) {
  const req = event.request;
  const pagesCache = await caches.open(PAGES_CACHE);

  try {
    // a) Si hay navigationPreload, úsalo
    const preload = await event.preloadResponse;
    if (preload) {
      pagesCache.put(req, preload.clone());
      return preload;
    }

    // b) Petición normal a red
    const networkResp = await fetch(req);
    pagesCache.put(req, networkResp.clone()); // guardamos la copia para el futuro
    return networkResp;

  } catch (err) {
    // c) Sin red: intentamos servir la versión cacheada de ESA ruta
    const cached = await pagesCache.match(req);
    if (cached) return cached;

    // d) Último recurso: pantalla offline
    const staticCache = await caches.open(STATIC_CACHE);
    const offline = await staticCache.match(OFFLINE_URL);
    return offline || new Response('Sin conexión', {
      status: 503,
      statusText: 'Offline'
    });
  }
}

// Estáticos: cache-first con actualización en segundo plano
async function cacheFirst(req) {
  const cache = await caches.open(STATIC_CACHE);
  const cached = await cache.match(req);
  if (cached) {
    // Intento de refresco silencioso en background
    fetch(req).then(resp => cache.put(req, resp.clone())).catch(() => {});
    return cached;
  }

  const networkResp = await fetch(req);
  cache.put(req, networkResp.clone());
  return networkResp;
}
"""
        return HttpResponse(js, content_type=self.content_type)
