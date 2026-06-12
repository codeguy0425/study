const CACHE_NAME = 'idioms-pwa-v10';
const PRE_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './icon.png',
  './pth/scripts.html',
  './pth/print.html',
  'https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4',
  'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Serif+TC:wght@500;700;900&display=swap'
];

// Pre-cache core files on installation
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRE_CACHE))
      .then(() => self.skipWaiting())
  );
});

// Clean up old caches and claim active clients
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

// Intercept network requests
self.addEventListener('fetch', event => {
  // Only handle GET requests
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);
  const isNavigation = event.request.mode === 'navigate';
  const isHtml = url.pathname.endsWith('.html') || url.pathname === '/' || url.pathname.endsWith('/');

  if (isNavigation || isHtml) {
    // Network-First, Fallback-to-Cache Strategy for HTML/navigation requests
    // This ensures users always get the freshest content when online, while remaining fully offline-capable.
    event.respondWith(
      fetch(event.request)
        .then(networkResponse => {
          return caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, networkResponse.clone());
            return networkResponse;
          });
        })
        .catch(() => {
          return caches.match(event.request);
        })
    );
  } else {
    // Cache-First, Fallback-to-Network Strategy for static assets and CDN resources
    event.respondWith(
      caches.match(event.request).then(cachedResponse => {
        if (cachedResponse) {
          return cachedResponse;
        }

        return fetch(event.request)
          .then(networkResponse => {
            // Dynamically cache external resources (like Google Fonts and CDNs) on demand
            if (
              url.origin === 'https://fonts.googleapis.com' ||
              url.origin === 'https://fonts.gstatic.com' ||
              url.pathname.includes('cdn.jsdelivr.net')
            ) {
              return caches.open(CACHE_NAME).then(cache => {
                cache.put(event.request, networkResponse.clone());
                return networkResponse;
              });
            }
            return networkResponse;
          })
          .catch(() => {
            // Silent catch for offline navigation
          });
      })
    );
  }
});
