"""
Django settings for qr_contest project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6(+g79jj$gq%)62dar8qgonl+3l(lfj9+6$q^r13mkv6r9g^e!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['nauryz.odx.kz','185.129.49.151','localhost','127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://nauryz.odx.kz']



# Application definition

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.inlines",  # optional, if special inlines are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "contest",
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

ROOT_URLCONF = 'qr_contest.urls'

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

WSGI_APPLICATION = 'qr_contest.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

from decouple import config
LOGIN_URL = 'login'
# STATIC
ENV = config('ENV', default='dev')  # По умолчанию dev

STATIC_URL = '/static/'

STATIC_ROOT = config('STATIC_ROOT', default='/home/oin/qr_contest/static/')
STATICFILES_DIRS = []

# if ENV == 'prod':
#     STATIC_ROOT = config('STATIC_ROOT', default='/home/oin/qr_contest/static/')
#     STATICFILES_DIRS = []
# else:
#     STATICFILES_DIRS =  [BASE_DIR / 'static']
#     STATIC_ROOT = None  # Django требует None в DEV, иначе collectstatic будет срабатывать

# MEDIA (для загруженных пользователем файлов)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# Базовый URL для генерации QR-кодов
QR_URL = "https://nauryz.odx.kz/"
# QR_URL = "http://127.0.0.1:8000/"
