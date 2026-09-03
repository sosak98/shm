from django.conf import settings

from .models import Category


def shop_info(request):
    """Rend les infos de la boutique et les catégories disponibles partout."""
    return {
        'SHOP_NAME': settings.SHOP_NAME,
        'SHOP_WHATSAPP': settings.SHOP_WHATSAPP,
        'SHOP_WHATSAPP_DISPLAY': getattr(settings, 'SHOP_WHATSAPP_DISPLAY', '+229 96 43 77 08'),
        'SHOP_PHONE_DISPLAY': settings.SHOP_PHONE_DISPLAY,
        'SHOP_PHONE_TEL': settings.SHOP_PHONE_TEL,
        'SHOP_ADDRESS': settings.SHOP_ADDRESS,
        'SHOP_HOURS': settings.SHOP_HOURS,
        'SHOP_INSTAGRAM': settings.SHOP_INSTAGRAM,
        'SHOP_FACEBOOK': settings.SHOP_FACEBOOK,
        'ALL_CATEGORIES': Category.objects.all(),
    }
