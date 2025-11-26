"""
Django settings for nexoecos project.
"""
from pathlib import Path
import os

# ================== RUTAS BÁSICAS ==================
BASE_DIR = Path(__file__).resolve().parent.parent

# === Seguridad / Debug ===
SECRET_KEY = 'django-insecure-01z^h7ls4&p-29vhy&q5mkzd3jfb1imfrn@f5=^!8uh4_6%*i6'
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# ================== APPS ==================
INSTALLED_APPS = [
    # Núcleo Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # App Codex con configuración (para cargar señales)
    'codex.apps.CodexConfig',

    # Utilidades
    'django_htmx',
    'rest_framework',
    'django.contrib.humanize',
    'widget_tweaks',

    # Apps del proyecto
    'core',
    'accounts',
    'community',
    'news',
]

# ================== MIDDLEWARE ==================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # estáticos en prod
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nexoecos.urls'

# ================== TEMPLATES ==================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # admin personalizado + vistas del sitio
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nexoecos.wsgi.application'

# ================== BASE DE DATOS ==================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ================== ARCHIVOS ESTÁTICOS / MEDIA ==================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']   # assets en desarrollo
STATIC_ROOT = BASE_DIR / 'staticfiles'     # destino collectstatic

# URL absoluta del sitio para construir URLs completas de media
SITE_URL = "http://127.0.0.1:8000"  # para desarrollo

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Django 4.2+ STORAGES (evita InvalidStorageError)
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": MEDIA_ROOT,
            "base_url": MEDIA_URL,
        },
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ================== AUTENTICACIÓN / REDIRECTS ==================
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'core:home'
LOGOUT_REDIRECT_URL = 'core:home'

# ================== FIREBASE ==================
# Clave de servicio de Firebase Admin
FIREBASE_SERVICE_ACCOUNT = BASE_DIR / "config" / "firebase-service-account.json"
FIREBASE_PROJECT_ID = "integradora-300c3"

# ================== SEGURIDAD EXTRA ==================
CSRF_TRUSTED_ORIGINS = [
    'https://*.pythonanywhere.com',
]

# ================== PASSWORD VALIDATORS ==================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ================== IDIOMA / ZONA HORARIA ==================
LANGUAGE_CODE = "es"

LANGUAGES = [
    ("es", "Español"),
    ("en", "English"),
]

LOCALE_PATHS = [BASE_DIR / "locale"]

TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ================== VARIOS ==================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
