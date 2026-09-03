from urllib.parse import quote

from django import template
from django.conf import settings

register = template.Library()


def _fcfa_int(value):
    """12500 -> '12 500'"""
    return f'{int(value):,}'.replace(',', ' ')


@register.filter
def fcfa(value):
    """12500 -> '12 500 FCFA'"""
    try:
        return _fcfa_int(value) + ' FCFA'
    except (TypeError, ValueError):
        return value


@register.simple_tag
def whatsapp_link(product=None):
    """Lien wa.me avec message pré-rempli (produit précis ou message générique)."""
    number = getattr(settings, 'SHOP_WHATSAPP', '22900000000')
    shop = getattr(settings, 'SHOP_NAME', 'SHM Shop')
    if product is not None:
        message = (
            f'Bonjour {shop} 👋🏽, je suis intéressé(e) par le pagne '
            f'Réf. {product.reference} ({product.name}) '
            f'au prix de {_fcfa_int(product.price)} FCFA. '
            f'Est-il toujours disponible ?'
        )
    else:
        message = (
            f"Bonjour {shop} 👋🏽, j'aimerais avoir plus d'informations "
            f'sur vos pagnes.'
        )
    return f'https://wa.me/{number}?text={quote(message)}'
