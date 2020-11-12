const cacheName = 'lms-v1';
const staticAssets = [
  '/',
  '/static/vendors/bundle.css',
  '/static/PWA/manifest.json',
  '/static/vendors/slick/slick.css',
  '/static/vendors/slick/slick-theme.css',
  '/static/vendors/datepicker/daterangepicker.css',
  '/static/vendors/dataTable/datatables.min.css',
  '/static/css/app.min.css',
  '/static/css/custom.css',
  '/static/vendors/select2/css/select2.min.css',
  '/static/vendors/bundle.js',
  '/static/vendors/charts/apex/apexcharts.min.js',
  '/static/vendors/datepicker/daterangepicker.js',
  '/static/media/image/logo/large-logo.png'
];

self.addEventListener('install', async e => {
  const cache = await caches.open(cacheName);
  await cache.addAll(staticAssets);
  return self.skipWaiting();
});

self.addEventListener('activate', e => {
  self.clients.claim();
});

self.addEventListener('fetch', async e => {
  const req = e.request;
  const url = new URL(req.url);

  if (url.origin === location.origin) {
    e.respondWith(cacheFirst(req));
  } else {
    e.respondWith(networkAndCache(req));
  }
});

async function cacheFirst(req) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(req);
  return cached || fetch(req);
}

async function networkAndCache(req) {
  const cache = await caches.open(cacheName);
  try {
    const fresh = await fetch(req);
    await cache.put(req, fresh.clone());
    return fresh;
  } catch (e) {
    const cached = await cache.match(req);
    return cached;
  }
}