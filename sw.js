const CACHE_NAME = 'idioms-pwa-v1';
const PRE_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './icon.png',
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

// Intercept network requests with a Cache-First, Fallback-to-Network strategy
self.addEventListener('fetch', event => {
  // Only cache GET requests
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then(cachedResponse => {
      if (cachedResponse) {
        return cachedResponse;
      }

      return fetch(event.request)
        .then(networkResponse => {
          // Dynamically cache external resources (like Google Fonts and CDNs) on demand
          const url = event.request.url;
          if (
            url.startsWith('https://fonts.googleapis.com') ||
            url.startsWith('https://fonts.gstatic.com') ||
            url.includes('cdn.jsdelivr.net')
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
});
