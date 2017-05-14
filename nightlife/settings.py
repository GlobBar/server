"""
Django settings for nightlife project.

Generated by 'django-admin startproject' using Django 1.9.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')rnhb2+*n2h#f*xvwujo@ih7v8tedh0n&zzt$-fv*626h0f5y&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'imagekit',
    # auth
    'oauth2_provider',
    'social.apps.django_app.default',
    'rest_framework_social_oauth2',
    # apps
    'places',
    'apiusers',
    'files',
    'report',
    'city',
    'friends',
    'points',
    'notification',
    # push
    'djcelery',
    'pushy',
    'user_messages.apps.UserMessagesConfig',
    'socapp',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nightlife.urls'

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
                'social.apps.django_app.context_processors.backends',
                'social.apps.django_app.context_processors.login_redirect',
                'django.core.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'nightlife.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nightlife',
        'USER': 'root',
        'PASSWORD': '218bae4f22133d56',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = "/var/www/html/nightlife/nightlife/static/"
#STATIC_ROOT = "/var/www/html/globbar-staging/globbar_server/nightlife/static/"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAdminUser',
    ),
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # OAuth
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

AUTHENTICATION_BACKENDS = (

    # Others auth providers (e.g. Google, OpenId, etc)
    'social.backends.instagram.InstagramOAuth2',

    # Facebook OAuth2
    'social.backends.facebook.FacebookAppOAuth2',
    'social.backends.facebook.FacebookOAuth2',

    # django-rest-framework-social-oauth2
    'rest_framework_social_oauth2.backends.DjangoOAuth2',

    # Django
    'django.contrib.auth.backends.ModelBackend',

)

OAUTH2_PROVIDER = {
    # Expire after a year
    'ACCESS_TOKEN_EXPIRE_SECONDS': 31104000,
}

# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = '1061144060574069'
SOCIAL_AUTH_FACEBOOK_SECRET = '2081762679ce68e3f9b6f6e2f39f186f'

# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from facebook.
# Email is not sent by default, to get it, you must request the email permission:
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_INSTAGRAM_SCOPE = ['email']

# Instagram configuration
SOCIAL_AUTH_INSTAGRAM_KEY = '18794d594ced45b8b9e68dd61bb5d95d'
SOCIAL_AUTH_INSTAGRAM_SECRET = '2a1b998d7e3747ee88ce619c20667676'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
SITE_DOMAIN = 'http://127.0.0.1:8000'
IMAGEKIT_CACHEFILE_DIR = os.path.join(BASE_DIR, 'media')

# PUSH
# Android
PUSHY_GCM_API_KEY = 'YOUR_API_KEY_HERE'  # not using

# Send JSON or plaintext payload to GCM server (default is JSON)
PUSHY_GCM_JSON_PAYLOAD = True  # not using

# iOS
PUSHY_APNS_SANDBOX = True  # True or False   # not using
PUSHY_APNS_KEY_FILE = 'NightLife_tes_keyt.pem'  # not using
PUSHY_APNS_CERTIFICATE_FILE = 'NightLife_test_cert.pem'  # not using

PUSHY_QUEUE_DEFAULT_NAME = 'default'   # not using
PUSHY_DEVICE_KEY_LIMIT = 1000  # not using

# Actual data for push Notifications
# DEV
# PEM_KEY_DIR = os.path.join(BASE_DIR, 'notification/test.pem')
# SSL_HOST = 'gateway.sandbox.push.apple.com'

# PROD
PEM_KEY_DIR = os.path.join(BASE_DIR, 'notification/prod.pem')
SSL_HOST = 'gateway.push.apple.com'

VIDEO_TEST = '/report/2016/04/07/SampleVideo_1280x720_1mb.mp4'

# Email
SEND_GRID_API_KEY = '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'


