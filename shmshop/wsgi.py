"""
WSGI config for shmshop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shmshop.settings')

application = get_wsgi_application()

# Distribution instantanée des photos média et statiques en production
media_dir = str(settings.MEDIA_ROOT)
if os.path.exists(media_dir):
    try:
        application = WhiteNoise(application, root=str(settings.STATIC_ROOT), prefix='/static/')
        application.add_files(media_dir, prefix='/media/')
    except Exception:
        pass
