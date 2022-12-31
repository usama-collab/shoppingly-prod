import os
from pathlib import Path
from decouple import config
# for postgresql
# import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# from django.core.management.utils import get_random_secret_key
# SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", get_random_secret_key())
SECRET_KEY = config("SECRET_KEY")

DEBUG = config('DEBUG', cast=bool, default=True)
# if not DEBUG:
#     ALLOWED_HOSTS += os.getenv("DJANGO_ALLOWED_HOSTS",
#                                "127.0.0.1,localhost").split(",")
# ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(" ")
ALLOWED_HOSTS = ["*"]


# Application definition


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'app.apps.AppConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shoppingly.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'shoppingly.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    # 'Postgresql': {
    #     # 'ENGINE': 'django.db.backends.postgresql',
    #     # or
    #     'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #     'NAME': 'storefront2',
    #     'HOST': 'localhost',
    #     'USER': os.getenv('DEV_DB_USER'),
    #     'PASSWORD': os.getenv('DEV_DB_PASSWORD')
    # },
    # 'mysql': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'storefront2',
    #     # 'HOST': 'mysql',
    #     'HOST': 'localhost',
    #     'USER': os.getenv('DEV_DB_USER'),
    #     'PASSWORD': os.getenv('DEV_DB_PASSWORD')
    # },
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


# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
from .cdn.storage_conf import *  # noqa

from .email.email_conf import *  # noqa
