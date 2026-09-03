"""
Paramètres Django pour SHM Shop (boutique catalogue de pagnes).
Développement : SQLite + DEBUG (comportement par défaut).
Production : tout se pilote par variables d'environnement (voir README.md).
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-change-me-in-production')
DEBUG = os.environ.get('DJANGO_DEBUG', '1') == '1'

ALLOWED_HOSTS = ['*'] if DEBUG else [h.strip() for h in os.environ.get('DJANGO_ALLOWED_HOSTS', '.onrender.com,localhost,127.0.0.1').split(',') if h.strip()]

# Aperçu en ligne et domaines autorisés
CSRF_TRUSTED_ORIGINS = [
    'https://*.e2b.app',
    'https://*.onrender.com',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
] + [('https://' + h.lstrip('.')) for h in ALLOWED_HOSTS if h and h != '*']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # fichiers statiques en production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shmshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.shop_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'shmshop.wsgi.application'

# --- Base de données ------------------------------------------------------
# Dev : SQLite. Prod : PostgreSQL via DATABASE_URL (Neon, Render...) (voir README).
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(conn_max_age=600)

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Porto-Novo'
USE_I18N = True
USE_TZ = True

# --- Fichiers statiques & médias -------------------------------------------
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # rempli par « collectstatic » en prod
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Compression + cache longue durée des fichiers statiques en production
if not DEBUG:
    STORAGES = {
        'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
        'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
    }

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# Paramètres SHM Shop
# ---------------------------------------------------------------------------
SHOP_NAME = 'SHM Shop'
# WhatsApp pour les commandes directes (format international sans le +)
SHOP_WHATSAPP = os.environ.get('SHOP_WHATSAPP', '22996437708')
SHOP_WHATSAPP_DISPLAY = '+229 96 43 77 08'

# Numéro pour les appels directs (nouveau format Bénin)
SHOP_PHONE_TEL = '+2290144767524'
SHOP_PHONE_DISPLAY = '+229 01 44 76 75 24'

SHOP_ADDRESS = 'Cotonou, Bénin'
SHOP_HOURS = '24h/24 et 7j/7 (Commandes WhatsApp en continu)'
SHOP_INSTAGRAM = 'https://instagram.com/shmshop'
SHOP_FACEBOOK = 'https://facebook.com/shmshop'
