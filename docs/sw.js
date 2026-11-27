/* Eventually — copia sin conexión.
   - Lo esencial (página, estilos, tipografías, foto del reloj) se guarda al instalar.
   - Con conexión, lo esencial se pide siempre a la red (para ver cambios) y la copia
     solo se usa si la red falla o tarda.
   - Los fotogramas de la película se guardan cuando la página termina de cargarlos
     y después se sirven siempre de la copia. Su dirección lleva la versión de la
     película, así que al rehacerla se descargan de nuevo. */

const CORE = 'eventually-core-v4';
const FRAMES = 'eventually-frames-';
const CORE_FILES = [
  './',
  'index.html',
  'styles.css',
  'app.js',
  'caja.css',
  'caja.js',
  'app.webmanifest',
  'poster.jpg',
  'frames/manifest.json',
  'frames/caja/manifest.json',
  'frames/caja/poster.webp',
  'img/reloj.webp',
  'img/icon-180.png',
  'img/icon-192.png',
  'img/icon-512.png',
  'fonts/instrument-serif.woff2',
  'fonts/instrument-serif-italic.woff2',
  'fonts/instrument-sans.woff2',
  'fonts/reenie-beanie.woff2',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CORE).then((cache) => cache.addAll(CORE_FILES)).then(() => self.skipWaiting())
  );
});

// Al activarse se borran las copias de lo esencial de versiones anteriores.
self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    for (const key of await caches.keys()) {
      if (key.startsWith('eventually-core-') && key !== CORE) await caches.delete(key);
    }
    await self.clients.claim();
  })());
});

const isFrame = (url) => url.pathname.includes('/frames/') && url.pathname.endsWith('.webp');

// Fotogramas: primero la copia; si no está, se pide y se guarda en el momento,
// para que la copia sin conexión no dependa de haber visto la película entera.
async function frameFirst(request, url) {
  const hit = await caches.match(request);
  if (hit) return hit;
  const response = await fetch(request);
  if (response.ok) {
    const cache = await caches.open(FRAMES + (url.searchParams.get('v') || '0'));
    cache.put(request, response.clone());
  }
  return response;
}

// La página se guarda siempre con el mismo nombre, venga con lo que venga detrás
// de la «?»: así sin conexión sale la última que se vio y no una copia vieja.
async function networkFirst(request) {
  const cache = await caches.open(CORE);
  const isPage = request.mode === 'navigate';
  try {
    const response = await Promise.race([
      fetch(request),
      new Promise((_, reject) => setTimeout(() => reject(new Error('lenta')), 4000)),
    ]);
    if (response.ok) cache.put(isPage ? 'index.html' : request, response.clone());
    return response;
  } catch (_) {
    const hit = isPage
      ? await cache.match('index.html')
      : (await cache.match(request)) || (await cache.match(request, { ignoreSearch: true }));
    return hit || fetch(request);
  }
}

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  event.respondWith(isFrame(url) ? frameFirst(request, url) : networkFirst(request));
});

// La página avisa cuando ya tiene todos los fotogramas: se guardan (salen de la
// caché del navegador, sin volver a descargarlos) y se borran los de versiones viejas.
self.addEventListener('message', (event) => {
  const data = event.data || {};
  if (data.type !== 'frames' || !Array.isArray(data.urls)) return;
  event.waitUntil((async () => {
    const name = FRAMES + data.version;
    for (const key of await caches.keys()) {
      if (key.startsWith(FRAMES) && key !== name) await caches.delete(key);
    }
    const cache = await caches.open(name);
    for (const url of data.urls) {
      if (await cache.match(url)) continue;
      try {
        const response = await fetch(url);
        if (response.ok) await cache.put(url, response);
      } catch (_) { /* se reintentará en la próxima visita */ }
    }
  })());
});
