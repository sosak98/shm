/* ==========================================================================
   SHM Shop : PWA (installation et mode hors ligne)
   ========================================================================== */
(function () {
  'use strict';

  /* ---------- Service Worker : le site fonctionne hors ligne ---------- */
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
      navigator.serviceWorker.register('/sw.js').catch(function () { /* silencieux */ });
    });
  }

  /* ---------- Bouton « Installer l'application » ---------- */
  var deferredPrompt = null;
  var chip = document.getElementById('install-chip');

  window.addEventListener('beforeinstallprompt', function (e) {
    e.preventDefault();
    deferredPrompt = e;
    if (chip) { chip.hidden = false; }
  });

  if (chip) {
    chip.addEventListener('click', function () {
      if (!deferredPrompt) { return; }
      deferredPrompt.prompt();
      deferredPrompt.userChoice.finally(function () {
        chip.hidden = true;
        deferredPrompt = null;
      });
    });
  }

  window.addEventListener('appinstalled', function () {
    if (chip) { chip.hidden = true; }
  });

  /* ---------- Apparition douce des éléments au défilement ---------- */
  document.addEventListener('DOMContentLoaded', function () {
    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!('IntersectionObserver' in window) || reduced) { return; }

    var els = document.querySelectorAll(
      '.card, .step, .section-head, .contact-card, .banner-cta, .gallery, .info'
    );
    els.forEach(function (el) { el.classList.add('reveal'); });

    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    els.forEach(function (el) { io.observe(el); });
  });
})();
