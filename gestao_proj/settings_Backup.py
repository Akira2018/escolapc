import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-li1dd3ijq(uutb#ksg*-u++-xqrs8b_h&r3wobp2^v0snk&wha'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#DEBUG = False

#SECURE_SSL_REDIRECT

##ALLOWED_HOSTS = ['*']

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
]


ADMIN_URL = 'admin/'  # Defina o URL do painel de administração
LOGIN_URL = '/accounts/login/'
CSRF_COOKIE_SECURE = False  # Defina como True se estiver usando HTTPS

# hello_django/settings.py

APP_NAME = os.environ.get("FLY_APP_NAME")  # Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',  # Note a vírgula aqui
    'todos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',

]

CORS_ALLOWED_ORIGINS = [
    'http://localhost',  # Incluído o esquema e a porta, se aplicável
]

CSRF_TRUSTED_ORIGINS = ['https://bibliotecaescola.fly.dev']

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

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': False,
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

WSGI_APPLICATION = 'setup.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bdbiblioteca',
        'USER': 'root',
        'PASSWORD': 'Akira2018',
        'HOST': 'localhost',   # Ou endereço do seu servidor MySQL
        'PORT': '3306',        # Porta padrão do MySQL
    }
}


# Restante do seu arquivo settings.py...


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

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

# Adicione estas linhas
DATE_FORMAT = 'dd/mm/YYYY'

DATETIME_FORMAT = 'dd/mm/YYYY H:i:s'

USE_I18N = True

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# Static files (CSS, JavaScript)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/static/'

# Arquivos de Mídia (Imagens)
MEDIA_ROOT = 'D:\\PastaPython\\ProjetosDjango\\ProjetoIntegradorI\\media'
MEDIA_URL = "/media/"

SQLITE3_ROOT = os.path.join(BASE_DIR, 'sqlite3')
SQLITE3_URL = "/venv/"


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
