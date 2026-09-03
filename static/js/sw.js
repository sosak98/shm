/* ==========================================================================
   SHM Shop : Service Worker (mode hors ligne)
   ========================================================================== */
'use strict';

var CACHE = 'shm-shop-v1';

var CORE = [
  '/',
  '/catalogue/',
  '/panier/',
  '/contact/',
  '/static/css/style.css',
  '/static/js/panier.js',
  '/static/js/pwa.js',
  '/static/img/hero.jpg',
  '/static/icons/icon-192.png'
];

/* Installation : pré-cache des pages essentielles */
self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE)
      .then(function (c) { return c.addAll(CORE); })
      .then(function () { return self.skipWaiting(); })
  );
});

/* Activation : nettoyage des anciens caches */
self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys()
      .then(function (keys) {
        return Promise.all(keys.map(function (k) {
          if (k !== CACHE) { return caches.delete(k); }
        }));
      })
      .then(function () { return self.clients.claim(); })
  );
});

/* Interception des requêtes */
self.addEventListener('fetch', function (e) {
  if (e.request.method !== 'GET') { return; }
  var url = new URL(e.request.url);
  if (url.origin !== self.location.origin) { return; }

  /* Pages HTML : réseau d'abord, cache sinon (hors ligne) */
  if (e.request.mode === 'navigate') {
    e.respondWith(
      fetch(e.request).then(function (res) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(e.request, copy); });
        return res;
      }).catch(function () {
        return caches.match(e.request).then(function (m) {
          return m || caches.match('/');
        });
      })
    );
    return;
  }

  /* Fichiers statiques & photos : cache d'abord */
  if (url.pathname.indexOf('/static/') === 0 || url.pathname.indexOf('/media/') === 0) {
    e.respondWith(
      caches.match(e.request).then(function (m) {
        return m || fetch(e.request).then(function (res) {
          var copy = res.clone();
          caches.open(CACHE).then(function (c) { c.put(e.request, copy); });
          return res;
        });
      })
    );
  }
});
