import os
from pathlib import Path
import django_heroku
import dj_database_url
from urllib.parse import urlparse

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-li1dd3ijq(uutb#ksg*-u++-xqrs8b_h&r3wobp2^v0snk&wha'

# Configuração da conexão com o Docker Engine
#DOCKER_BASE_URL = 'unix://var/run/docker.sock'  # ou 'tcp://127.0.0.1:2375' para conexão remota
DOCKER_BASE_URL = 'TCP://127.0.0.1:2375' ##para conexão remota
DOCKER_API_VERSION = 'auto'  # para detectar automaticamente a versão da API Docker

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True
ALLOWED_HOSTS = ['192.168.0.203','127.0.0.1', 'localhost','.herokuapp.com']

ADMIN_URL = 'admin/'  # Defina o URL do painel de administração
LOGIN_URL = '/accounts/login/'
CSRF_COOKIE_SECURE = False  # Defina como True se estiver usando HTTPS

CSRF_TRUSTED_ORIGINS = ['https://escolae-255a9c5574fe.herokuapp.com/']

# Define o tempo de expiração da sessão em segundos (por exemplo, 1 hora)
SESSION_COOKIE_AGE = 3600

#APP_NAME = os.environ.get("FLY_APP_NAME")  # Application definition

# settings.py

LOGIN_REDIRECT_URL = '/accounts/profile/'

# settings.py

# Define o template para a página 403
handler403 = 'django.views.defaults.permission_denied'

# settings.py
AUTH_USER_MODEL = 'gestao.User'  # Ajuste 'gestao' para o nome correto do seu app e 'User' para o nome do seu modelo personalizado

# Diretório base do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configurar o diretório dos arquivos estáticos
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Configuração de Logging
# Configuração de Logging
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

# Configure TEMPLATE_DIR
TEMPLATE_DIR = os.path.join(BASE_DIR, 'gestao/templates')

# Configuração dos Templates
import os
from pathlib import Path  # Importe pathlib para lidar com caminhos

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Configure TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'gestao', 'templates')],
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

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'grappelli',
    'gestao.apps.GestaoConfig',  # Mantenha apenas esta linha para evitar duplicidade
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Certifique-se de que esse middleware está presente
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    #'gestao.middleware.AccessibilityMiddleware',
]

# Configurações do Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CORS_ALLOWED_ORIGINS = [
    'http://localhost',  # Incluído o esquema e a porta, se aplicável
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]

CORS_ALLOW_HEADERS = [
    'Accept',
    'Accept-Language',
    'Content-Language',
    'Content-Type',
    'Authorization',
]

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

# Configurações do Banco de Dados

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'Biblioteca.sqlite3'),
        }
}

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'bdbiblia',
#        'USER': 'root',
#        'PASSWORD': 'Bauru2024',
#        'HOST': 'localhost',  # ou o endereço do seu servidor de banco de dados
#        'PORT': '3306',  # a porta padrão do MySQL
#    }
#}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

# Outras configurações
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = False
USE_TZ = True

import os
from pathlib import Path

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Arquivos de Mídia (Imagens)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

IMAGEM_LIVROS = os.path.join(MEDIA_ROOT, 'Livros', 'Imagembiblioteca.jpg')

SQLITE3_ROOT = os.path.join(BASE_DIR, 'sqlite3')
SQLITE3_URL = "/venv/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

django_heroku.settings(locals())
