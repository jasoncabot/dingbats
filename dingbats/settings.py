"""
Django settings for dingbats project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from azure.identity import DefaultAzureCredential
from pathlib import Path
import environ
env = environ.Env(
    # set casting, default value
    ALLOWED_HOSTS=(list, []),
    DEBUG=(bool, False),
    SECRET_KEY=(str, "some-secret-key"),
)
# reading .env file
environ.Env.read_env()

# Get the identity of this application
credential = DefaultAzureCredential()

DATABASE_USER = env('DATABASE_USER', default="")
DATABASE_HOST = env('DATABASE_HOST', default="")
if DATABASE_USER and DATABASE_HOST:
    token = credential.get_token(
        "https://ossrdbms-aad.database.windows.net/.default").token
else:
    token = ""


# False if not in os.environ
DEBUG = env('DEBUG')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Raises django's ImproperlyConfigured exception if SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env('ALLOWED_HOSTS')


# Application definition

INSTALLED_APPS = [
    'game.apps.GameConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'dingbats.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'dingbats.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': DATABASE_USER,
        'PASSWORD': token,
        'HOST': DATABASE_HOST,
        'PORT': '5432',
        'OPTIONS': {'sslmode': 'require'}
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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


# The Debug Toolbar is shown only for the following IP Addresses

INTERNAL_IPS = [
    '127.0.0.1',
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = './public/'

# File Uploads

AZURE_ACCOUNT_NAME = env('AZURE_ACCOUNT_NAME', default="")
AZURE_CONTAINER = env('AZURE_CONTAINER', default="")
AZURE_URL_EXPIRATION_SECS = env('AZURE_URL_EXPIRATION_SECS', default=300)
if AZURE_ACCOUNT_NAME and AZURE_CONTAINER:
    DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
    AZURE_TOKEN_CREDENTIAL = credential.get_token(
        "https://storage.azure.com/.default").token
