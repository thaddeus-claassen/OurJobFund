"""
Django settings for ourjobfund project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os;
from .debug import DEBUG;

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)));

if DEBUG:
    ALLOWED_HOSTS = [];
    SECURE_SSL_REDIRECT = False;
    SESSION_COOKIE_SECURE = False;
    CSRF_COOKIE_SECURE = False;
else:
    ALLOWED_HOSTS = ['.ourjobfund.com', '54.173.90.146'];
    SECURE_SSL_REDIRECT = True;
    SESSION_COOKIE_SECURE = True;
    CSRF_COOKIE_SECURE = True;


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = open(os.path.join(BASE_DIR, '.django/secret_key.txt'), 'r').read();

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'job',
    'user',
    'jobuser',
    'update',
    'filter',
    'notification',
    'about',
    'contact',
    'privacy',
    'terms_of_service',
    'django_static_jquery',
    'bootstrap3',
    'rest_framework',
    'annoying',
    'pinax.stripe',
]

SITE_ID = 1;

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
};

if (DEBUG):
    REST_FRAMEWORK['DATETIME_FORMAT'] = '%B %#d, %Y';
else:
    REST_FRAMEWORK['DATETIME_FORMAT']  = '%B %-d, %Y';
    
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ourjobfund.urls';

USER_TZ = True;

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'templates')),],
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

WSGI_APPLICATION = 'ourjobfund.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'ourjobfund',
            'USER': 'root',
            'PASSWORD': open(os.path.join(BASE_DIR, '.django/database_password.txt'), 'r').read().rstrip(),
            'HOST': 'localhost',
            'POST': '',
        }
    }

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us';

TIME_ZONE = 'UTC';

USE_I18N = True;

USE_L10N = True;

USE_TZ = True;

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/';

STATIC_ROOT = os.path.join(BASE_DIR, 'static');

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'base/static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media');

MEDIA_URL = '/media/';

LOGOUT_URL = '/log_out/'

LOGIN_URL = '/sign_up/';

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda u: '/user/%s/' % u.username,
}

if not DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple' : {
                'format' : '%(asctime)s' '%(message)s'
            }
        },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'ourjobfund.log'),
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }
   
STRIPE_TEST_PUBLIC_KEY = open(os.path.join(BASE_DIR, '.stripe/stripe_public_test_key.txt'), 'r').read().rstrip();
STRIPE_TEST_SECRET_KEY = open(os.path.join(BASE_DIR, '.stripe/stripe_secret_test_key.txt'), 'r').read().rstrip();
STRIPE_LIVE_PUBLIC_KEY = open(os.path.join(BASE_DIR, '.stripe/stripe_public_key.txt'), 'r').read().rstrip();
STRIPE_LIVE_SECRET_KEY = open(os.path.join(BASE_DIR, '.stripe/stripe_secret_key.txt'), 'r').read().rstrip();

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend';
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend';
    EMAIL_HOST = 'smtp.zoho.com';
    EMAIL_HOST_USER = open(os.path.join(BASE_DIR, '.zoho/zoho_username.txt'), 'r').read().rstrip();
    EMAIL_HOST_PASSWORD = open(os.path.join(BASE_DIR, '.zoho/zoho_password.txt'), 'r').read().rstrip();
    EMAIL_PORT = 587;
    EMAIL_USE_TLS = True;
    DEFAULT_FROM_EMAIL = 'admin@ourjobfund.com';
