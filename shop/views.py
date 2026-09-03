from django.conf import settings
from django.contrib.staticfiles.finders import find
from django.db.models import Q
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from .models import Category, Product

# Filtres de prix du catalogue (?prix=...)
PRIX_FILTRES = {
    '6500': {'label': '6 500 FCFA (ABC & Orientar)', 'min': 6000, 'max': 7000},
    'chiganvy': {'label': '9 000 à 10 000 FCFA (Super Chiganvy)', 'min': 9000, 'max': 10500},
    'moins10': {'label': 'Moins de 10 000 FCFA', 'max': 10000},
    '10plus': {'label': '10 000 FCFA et plus', 'min': 10000},
}


def home(request):
    """Accueil : nouveautés, promotions, catégories et sélection de pagnes."""
    categories = Category.objects.prefetch_related('products').all()
    return render(request, 'shop/home.html', {
        'categories': categories,
        'nouveautes': Product.objects.filter(is_available=True, is_new=True).select_related('category')[:4],
        'promos': Product.objects.filter(is_available=True, is_promo=True).select_related('category')[:4],
        'populaires': Product.objects.filter(is_available=True).select_related('category')[:8],
    })


def catalogue(request):
    """Catalogue complet avec filtres par catégorie, prix, état et recherche."""
    produits = Product.objects.select_related('category').all()
    categories = Category.objects.all()

    filtre = request.GET.get('f', '')
    cat_slug = request.GET.get('cat', '')
    prix = request.GET.get('prix', '')
    q = request.GET.get('q', '').strip()

    # Filtre par catégorie
    selected_cat = None
    if cat_slug:
        produits = produits.filter(category__slug=cat_slug)
        selected_cat = categories.filter(slug=cat_slug).first()

    # Filtre rapide
    if filtre == 'nouveautes':
        produits = produits.filter(is_new=True)
    elif filtre == 'promos':
        produits = produits.filter(is_promo=True)
    elif filtre == 'disponibles':
        produits = produits.filter(is_available=True)

    # Filtre de prix
    if prix in PRIX_FILTRES:
        critere = PRIX_FILTRES[prix]
        if critere.get('min') is not None:
            produits = produits.filter(price__gte=critere['min'])
        if critere.get('max') is not None:
            produits = produits.filter(price__lt=critere['max'])

    # Recherche texte
    if q:
        produits = produits.filter(
            Q(name__icontains=q)
            | Q(reference__icontains=q)
            | Q(description__icontains=q)
            | Q(motif__icontains=q)
            | Q(category__name__icontains=q)
        )

    return render(request, 'shop/catalogue.html', {
        'produits': produits,
        'categories': categories,
        'selected_cat': selected_cat,
        'cat_slug': cat_slug,
        'filtre': filtre,
        'prix': prix,
        'prix_filtres': PRIX_FILTRES,
        'q': q,
    })


def product_detail(request, pk):
    """Page d'un pagne : galerie, catégorie, infos et bouton Commander."""
    produit = get_object_or_404(Product.objects.select_related('category').prefetch_related('images'), pk=pk)
    similaires = (
        Product.objects.filter(is_available=True)
        .select_related('category')
        .exclude(pk=pk)
    )
    if produit.category:
        similaires_cat = similaires.filter(category=produit.category)[:4]
        if similaires_cat.exists():
            similaires = similaires_cat
        else:
            similaires = similaires[:4]
    else:
        similaires = similaires[:4]

    return render(request, 'shop/product_detail.html', {
        'produit': produit,
        'similaires': similaires,
    })


def contact(request):
    """Page contact."""
    return render(request, 'shop/contact.html')


def panier(request):
    """Page panier (contenu géré côté navigateur en localStorage)."""
    return render(request, 'shop/panier.html')


# ---------------------------------------------------------------------------
# PWA : application installable et mode hors ligne
# ---------------------------------------------------------------------------
def manifest_json(request):
    """Manifest servi a la racine (scope '/' obligatoire pour l'installation)."""
    return JsonResponse({
        'name': f'{settings.SHOP_NAME} : Pagnes et Wax de qualite',
        'short_name': settings.SHOP_NAME,
        'description': 'Catalogue de pagnes africains a Cotonou. Commande WhatsApp directe sans paiement en ligne.',
        'start_url': '/',
        'scope': '/',
        'display': 'standalone',
        'background_color': '#1A1615',
        'theme_color': '#C1552E',
        'lang': 'fr',
        'dir': 'ltr',
        'icons': [
            {'src': '/static/icons/icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
            {'src': '/static/icons/icon-512.png', 'sizes': '512x512', 'type': 'image/png',
             'purpose': 'any maskable'},
        ],
    })


def service_worker(request):
    """sw.js servi depuis la racine '/'."""
    path = find('js/sw.js')
    response = FileResponse(open(path, 'rb'), content_type='text/javascript; charset=utf-8')
    response['Service-Worker-Allowed'] = '/'
    response['Cache-Control'] = 'no-cache'
    return response
