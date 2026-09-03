/* ==========================================================================
   SHM Shop : Panier cote navigateur (localStorage)
   Aucune base de donnees, aucun compte client : la commande complete
   part en un seul message WhatsApp pre-rempli.
   ========================================================================== */
(function () {
  'use strict';

  var KEY = 'shmshop_cart';
  var WA = (window.SHM && window.SHM.wa) || '22996437708';
  var SHOP = (window.SHM && window.SHM.name) || 'SHM Shop';

  /* ---------- Stockage ---------- */
  function getCart() {
    try { return JSON.parse(localStorage.getItem(KEY)) || []; }
    catch (e) { return []; }
  }
  function saveCart(cart) {
    localStorage.setItem(KEY, JSON.stringify(cart));
    updateBadge();
  }

  /* ---------- Format FCFA : 12500 -> "12 500 FCFA" ---------- */
  function fcfa(n) {
    return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ' ') + ' FCFA';
  }

  /* ---------- Badge du header ---------- */
  function updateBadge() {
    var total = getCart().reduce(function (s, i) { return s + i.qty; }, 0);
    document.querySelectorAll('.cart-count').forEach(function (b) {
      b.textContent = total;
      b.hidden = total === 0;
    });
  }

  /* ---------- Ajout d'un pagne ---------- */
  function addToCart(data) {
    var cart = getCart();
    var item = cart.find(function (i) { return i.ref === data.ref; });
    if (item) { item.qty += 1; }
    else {
      cart.push({
        ref: data.ref, name: data.name, price: parseInt(data.price, 10),
        qty: 1, url: data.url, img: data.img
      });
    }
    saveCart(cart);
    /* petit « pop » sur le compteur du menu */
    document.querySelectorAll('.cart-count').forEach(function (b) {
      b.classList.remove('bump');
      void b.offsetWidth; /* relance l'animation */
      b.classList.add('bump');
    });
    toast('✅ « ' + data.name + ' » ajouté au panier');
  }

  /* ---------- Notification ---------- */
  function toast(msg) {
    var t = document.getElementById('shm-toast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'shm-toast';
      t.className = 'toast';
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(t._hide);
    t._hide = setTimeout(function () { t.classList.remove('show'); }, 2300);
  }

  /* ---------- Lien WhatsApp de la commande complète ---------- */
  function buildOrderLink() {
    var cart = getCart();
    if (!cart.length) { return '#'; }
    var lines = cart.map(function (i) {
      return '• Ref ' + i.ref + ' (' + i.name + ') : ' + fcfa(i.price) + ' x ' + i.qty + ' = ' + fcfa(i.price * i.qty);
    });
    var total = cart.reduce(function (s, i) { return s + i.price * i.qty; }, 0);
    var message =
      'Bonjour ' + SHOP + ' 👋🏽, je souhaite commander :\n\n' +
      lines.join('\n') +
      '\n\n🧺 Total : ' + fcfa(total) +
      '\n\nCes pagnes sont-ils toujours disponibles ?';
    return 'https://wa.me/' + WA + '?text=' + encodeURIComponent(message);
  }

  /* ---------- Rendu de la page panier ---------- */
  function renderCart() {
    var root = document.getElementById('cart-items');
    if (!root) { return; }               // on n'est pas sur la page panier

    var cart = getCart();
    var empty = document.getElementById('cart-empty');
    var layout = document.getElementById('cart-layout');

    if (!cart.length) {
      if (empty) { empty.hidden = false; }
      if (layout) { layout.hidden = true; }
      updateBadge();
      return;
    }
    if (empty) { empty.hidden = true; }
    if (layout) { layout.hidden = false; }

    root.innerHTML = cart.map(function (i) {
      return '' +
        '<div class="cart-row" data-ref="' + i.ref + '">' +
          '<a class="cart-thumb" href="' + i.url + '"><img src="' + i.img + '" alt="' + i.name + '"></a>' +
          '<div class="cart-info">' +
            '<span class="card-ref">Réf. ' + i.ref + '</span>' +
            '<a class="cart-name" href="' + i.url + '">' + i.name + '</a>' +
            '<span class="cart-unit">' + fcfa(i.price) + ' / pièce</span>' +
          '</div>' +
          '<div class="qty">' +
            '<button type="button" class="qty-btn" data-act="dec" aria-label="Diminuer">−</button>' +
            '<span class="qty-val">' + i.qty + '</span>' +
            '<button type="button" class="qty-btn" data-act="inc" aria-label="Augmenter">+</button>' +
          '</div>' +
          '<div class="cart-line-total">' + fcfa(i.price * i.qty) + '</div>' +
          '<button type="button" class="cart-remove" title="Retirer du panier" aria-label="Retirer">✕</button>' +
        '</div>';
    }).join('');

    var total = cart.reduce(function (s, i) { return s + i.price * i.qty; }, 0);
    document.getElementById('cart-total').textContent = fcfa(total);
    document.getElementById('cart-order').href = buildOrderLink();
    updateBadge();
  }

  /* ---------- Interactions (délégation d'événements) ---------- */
  document.addEventListener('click', function (e) {
    // Bouton « Ajouter au panier » (cartes + page produit)
    var addBtn = e.target.closest && e.target.closest('.btn-add-cart');
    if (addBtn) { addToCart(addBtn.dataset); return; }

    // Lignes du panier
    var row = e.target.closest && e.target.closest('.cart-row');
    if (row) {
      var ref = row.dataset.ref;
      var cart = getCart();
      var item = cart.find(function (i) { return i.ref === ref; });

      if (e.target.closest('.cart-remove')) {
        cart = cart.filter(function (i) { return i.ref !== ref; });
        saveCart(cart); renderCart();
        return;
      }
      var qtyBtn = e.target.closest('.qty-btn');
      if (qtyBtn && item) {
        if (qtyBtn.dataset.act === 'inc') { item.qty += 1; }
        else { item.qty = Math.max(1, item.qty - 1); }
        saveCart(cart); renderCart();
        return;
      }
    }

    // Vider le panier
    if (e.target.closest && e.target.closest('#cart-clear')) {
      localStorage.removeItem(KEY);
      renderCart();
      toast('🗑️ Panier vidé');
    }
  });

  /* ---------- Menu Mobile (Tiroir Hamburger) ---------- */
  function initMobileMenu() {
    var menuBtn = document.getElementById('menu-toggle');
    var drawer = document.getElementById('mobile-drawer');
    var backdrop = document.getElementById('drawer-backdrop');
    var closeBtn = document.getElementById('drawer-close');

    if (!menuBtn || !drawer || !backdrop) { return; }

    function openMenu() {
      drawer.classList.add('is-open');
      backdrop.classList.add('is-open');
      menuBtn.classList.add('is-active');
      menuBtn.setAttribute('aria-expanded', 'true');
      drawer.setAttribute('aria-hidden', 'false');
      backdrop.setAttribute('aria-hidden', 'false');
      document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
      drawer.classList.remove('is-open');
      backdrop.classList.remove('is-open');
      menuBtn.classList.remove('is-active');
      menuBtn.setAttribute('aria-expanded', 'false');
      drawer.setAttribute('aria-hidden', 'true');
      backdrop.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }

    menuBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      if (drawer.classList.contains('is-open')) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    if (closeBtn) {
      closeBtn.addEventListener('click', function (e) {
        e.stopPropagation();
        closeMenu();
      });
    }

    backdrop.addEventListener('click', closeMenu);

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) {
        closeMenu();
      }
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    updateBadge();
    renderCart();
    initMobileMenu();
  });
})();
