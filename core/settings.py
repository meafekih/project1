"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1y#_#sd(y+=&5#_l83l_!1ro63fkt#@iw=^l+mp9sht-kmhr#s'

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

    'graphene_django',
    'graphql_auth',
    'graphql_jwt.refresh_token.apps.RefreshTokenConfig',
    'django_filters',
    "corsheaders",

    'apps.authentication',
    'apps.crm',
]
AUTH_USER_MODEL = 'authentication.ExtendUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [],
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },

        #'APP_DIRS': True,
    },
]


WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


# Static files settings
STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


GRAPHQL_JWT = {
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ObtainJSONWebToken",
    ],

    'JWT_VERIFY_EXPIRATION': True,
    'JWT_LONG_RUNNING_REFRESH_TOKEN': True,
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
GRAPHENE = {
    'SCHEMA': 'apps.authentication.schema.schema',
    'MIDDLEWARE': [
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
    ],
}

AUTHENTICATION_BACKENDS = [
    #'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
    "graphql_auth.backends.GraphQLAuthBackend",
]

GRAPHQL_AUTH = {
    'LOGIN_ALLOWED_FIELDS': ['email', 'username'],
}

CORS_ORIGIN_ALLOW_ALL = True

""" 
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = (
  'http://127.0.0.1:8000',
)



CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:8000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
]
 """

# Allow requests from any origin (not recommended for production)
CORS_ORIGIN_ALLOW_ALL = True

# Optionally, you can specify a list of allowed origins
# For example:
# CORS_ALLOWED_ORIGINS = [
#     "http://example.com",
#     "https://example.com",
# ]

# Allow credentials (cookies, authorization headers) to be included with cross-origin requests
CORS_ALLOW_CREDENTIALS = True

# Allow specific HTTP methods (e.g., 'GET', 'POST', 'PUT', 'DELETE')
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',  # Include 'OPTIONS' for handling preflight requests
]

# Allow specific HTTP headers
CORS_ALLOW_HEADERS = [
    'Accept',
    'Accept-Language',
    'Content-Type',
    'Authorization',
]

# Set how long the results of a preflight request (OPTIONS) can be cached in the browser
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 hours (in seconds)

GRAPHQL_AUTH_LOGIN_REQUIRED_ERROR_MESSAGE = "Authentication required to access this resource."




#DJANGO_SETTINGS_MODULE = "libreary.settings"
#python_files = ["test_*.py", "*_tests.py", "testing/python/*.py", "*/tests.py"]












