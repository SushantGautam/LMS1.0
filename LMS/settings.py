import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import socket
import subprocess

import django_heroku
import sentry_sdk
from django.contrib.messages import constants as messages
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'x-v$qxhbfy+jse*f)mx7(r_@_h#3rwo-o36t5j#pnhh25%8h*2')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', '210.127.211.100', '103.41.247.44', '192.168.1.29']

# Application definition

INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'crispy_forms',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'corsheaders',
    'django_filters',
    'import_export',
    'WebApp',
    'django.contrib.humanize',
    'forum',
    'quiz',
    'survey',
    'decorator_include',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LMS.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['WebApp/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'forum.context_processors.forum_processor',
            ],
        },
    },
]

# Media related settings are required for avatar uploading to function properly
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Form UI Settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Configure where to link to from the Login and Reg buttons in the forum
forum_LOGIN_URL_NAME = "account:login"
forum_REG_URL_NAME = "account:reg"

# Site Name
forum_SITE_NAME = "A lovely forum"

WSGI_APPLICATION = 'LMS.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'LMS',
#         'USER': 'postgres',
#         'PASSWORD': 'root',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},  # noqa
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},  # noqa
    # {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},  # noqa
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},  # noqa
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

# Channels
# https://channels.readthedocs.io/en/stable/getting-started.html
CHANNEL_LAYERS = {
    "default": {
        "ROUTING": "LMS.routing.channel_routing",

        # Dev Config
        "BACKEND": "asgiref.inmemory.ChannelLayer",

        # Production Config using REDIS
        # "BACKEND": "asgi_redis.RedisChannelLayer",
        # "CONFIG": {
        #    "hosts": [("redis", 6379)],
        # },
    },
}

INSTALLED_APPS += [
    'channels'
]

INSTALLED_APPS += ("django_createsuperuserwithpassword",)

STATICFILES_DIRS = (

    os.path.join(BASE_DIR, 'WebApp/static'),

)  # /opt/soundshelter/soundshelter/soundshelter/static

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

django_heroku.settings(locals())

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'WebApp.MemberInfo'

# Django Messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger'
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
}

# sentry_sdk.init(
#     dsn="https://c929f92bf1284629815c8d96805a4dba@sentry.io/1803012",
#     integrations=[DjangoIntegration(), CeleryIntegration()],
#     release="LMS@1.0-" + str(subprocess.check_output(["git", "describe", "--always"]).strip()),
#     server_name=socket.gethostname(),
#     send_default_pii=True,
#     debug=True,
# )


# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '.cache',
#     }
# }

CORS_ORIGIN_ALLOW_ALL = True

WHITENOISE_MAX_AGE = 43200
