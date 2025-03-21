
import os
from pathlib import Path
import django_heroku
import dj_database_url
from urllib.parse import urlparse
from django.contrib.messages import constants as messages

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-li1dd3ijq(uutb#ksg*-u++-xqrs8b_h&r3wobp2^v0snk&wha'

# Configuração da conexão com o Docker Engine
DOCKER_BASE_URL = 'TCP://127.0.0.1:2375'
DOCKER_API_VERSION = 'auto'

DEBUG = True
ALLOWED_HOSTS = ['192.168.0.203', '127.0.0.1', 'localhost', '.herokuapp.com']

ADMIN_URL = 'admin/'
LOGIN_URL = '/accounts/login/'
CSRF_COOKIE_SECURE = False
CSRF_TRUSTED_ORIGINS = ['https://escolapc.herokuapp.com']

SESSION_COOKIE_AGE = 3600
LOGIN_REDIRECT_URL = '/accounts/profile/'
handler403 = 'django.views.defaults.permission_denied'

AUTH_USER_MODEL = 'gestao.CustomUser'

# Diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

# Static & Media
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'gestao' / 'templates'],
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

# Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'grappelli',
    'gestao.apps.GestaoConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'gestao.middleware.ForeignKeyActivationMiddleware',
]

# Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CORS
CORS_ALLOWED_ORIGINS = ['http://localhost']
CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']
CORS_ALLOW_HEADERS = ['Accept', 'Accept-Language', 'Content-Language', 'Content-Type', 'Authorization']

# Messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}

# Admin interface customizations
SUIT_CONFIG = {
    'ADMIN_NAME': 'Django administration',
    'MENU': (
        'sites',
        {'label': 'Custom', 'icon': 'icon-cog', 'models': ('auth.user', 'auth.group')},
        {'label': 'Blog', 'icon': 'icon-book', 'models': ('blog.category', 'blog.post')},
    )
}

ROOT_URLCONF = 'gestao.urls'
WSGI_APPLICATION = 'gestao_proj.wsgi.application'

# Database (SQLite example)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'Biblioteca.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Localization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = False
USE_TZ = True

# Extras
IMAGEM_LIVROS = MEDIA_ROOT / 'Livros' / 'Imagembiblioteca.jpg'
SQLITE3_ROOT = BASE_DIR / 'sqlite3'
SQLITE3_URL = "/venv/"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Heroku settings
django_heroku.settings(locals())
