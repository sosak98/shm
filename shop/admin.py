from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    """Photos supplementaires de la galerie produit."""
    model = ProductImage
    extra = 1
    fields = ('image', 'alt')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('icon', 'name', 'slug', 'nb_produits', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description='Nombre de pagnes')
    def nb_produits(self, obj):
        count = obj.products.count()
        return f'{count} pagne{"s" if count > 1 else ""}'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'photo_miniature',
        'reference',
        'name',
        'category',
        'prix_affiche',
        'disponibilite_badge',
        'is_new',
        'is_promo',
        'created_at',
    )
    list_display_links = ('photo_miniature', 'reference', 'name')
    list_editable = ('category', 'is_new', 'is_promo')
    list_filter = ('category', 'is_available', 'is_new', 'is_promo')
    search_fields = ('reference', 'name', 'description', 'motif', 'category__name')
    inlines = [ProductImageInline]
    save_on_top = True
    list_per_page = 25

    fieldsets = (
        ('🏷️ Informations du Pagne', {
            'fields': (('name', 'reference'), ('category', 'price', 'old_price')),
            'description': 'Renseignez le nom, la référence unique, la catégorie et le prix de vente en FCFA.'
        }),
        ('🎨 Motif et Description', {
            'fields': ('motif', 'description'),
            'description': 'Description du tissu, couleurs dominantes et style.'
        }),
        ('📸 Photo Principale', {
            'fields': ('image',),
            'description': 'Photo principale qui apparaîtra sur les cartes du catalogue et les aperçus.'
        }),
        ('⚙️ Disponibilité et Badges', {
            'fields': (('is_available', 'is_new', 'is_promo'),),
            'description': 'Cochez Disponible pour le mettre en vente, Nouveauté ou Promotion pour les badges.'
        }),
    )

    @admin.display(description='Aperçu')
    def photo_miniature(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="width: 48px; height: 48px; object-fit: cover; border-radius: 8px; border: 1px solid #E6DCD1; box-shadow: 0 2px 4px rgba(0,0,0,0.06);" />'
            )
        return '-'

    @admin.display(description='Prix', ordering='price')
    def prix_affiche(self, obj):
        val = f'{obj.price:,} FCFA'.replace(',', ' ')
        if obj.old_price and obj.old_price > obj.price:
            old = f'{obj.old_price:,} FCFA'.replace(',', ' ')
            return mark_safe(
                f'<span style="font-weight: 700; color: #C1552E;">{val}</span> <span style="text-decoration: line-through; color: #8C7E74; font-size: 0.85em; margin-left: 4px;">{old}</span>'
            )
        return mark_safe(f'<span style="font-weight: 700; color: #C1552E;">{val}</span>')

    @admin.display(description='Disponibilité', ordering='is_available')
    def disponibilite_badge(self, obj):
        if obj.is_available:
            return mark_safe('<span style="background: #E6F4EA; color: #137333; padding: 4px 10px; border-radius: 12px; font-weight: 700; font-size: 0.78rem; display: inline-block;">En stock</span>')
        return mark_safe('<span style="background: #EFE8E1; color: #5A4D41; padding: 4px 10px; border-radius: 12px; font-weight: 700; font-size: 0.78rem; display: inline-block;">Épuisé</span>')


# Personnalisation des titres
admin.site.site_header = 'SHM Shop : Espace Gestion'
admin.site.site_title = 'SHM Shop Administration'
admin.site.index_title = 'Tableau de bord et Catalogue'

# Injection des statistiques et du tableau de bord sur l'accueil admin
original_admin_index = admin.site.index


def custom_admin_index(request, extra_context=None):
    extra_context = extra_context or {}
    total = Product.objects.count()
    available = Product.objects.filter(is_available=True).count()
    out_of_stock = total - available
    promos = Product.objects.filter(is_promo=True).count()
    new_items = Product.objects.filter(is_new=True).count()
    categories_count = Category.objects.count()
    recents = Product.objects.all().select_related('category').order_by('-created_at')[:8]

    extra_context.update({
        'total_products': total,
        'available_count': available,
        'out_of_stock_count': out_of_stock,
        'promos_count': promos,
        'new_count': new_items,
        'categories_count': categories_count,
        'recents': recents,
        'shop_name': getattr(settings, 'SHOP_NAME', 'SHM Shop'),
        'shop_whatsapp': getattr(settings, 'SHOP_WHATSAPP', '22996437708'),
        'shop_whatsapp_display': getattr(settings, 'SHOP_WHATSAPP_DISPLAY', '+229 96 43 77 08'),
        'shop_phone_display': getattr(settings, 'SHOP_PHONE_DISPLAY', '+229 01 44 76 75 24'),
        'shop_hours': getattr(settings, 'SHOP_HOURS', 'Lundi au Samedi : 9h à 19h'),
        'shop_address': getattr(settings, 'SHOP_ADDRESS', 'Cotonou, Bénin'),
    })
    return original_admin_index(request, extra_context=extra_context)


admin.site.index = custom_admin_index
