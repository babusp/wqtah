"""
Django settings for wqtah project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from os.path import join

from dotenv import load_dotenv

from pathlib import Path
from datetime import timedelta


# from decouple import config
# config.encoding = 'cp1251'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
# Define third party apps list
THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "drf_yasg",
    "django_filters",
    "rest_framework_simplejwt.token_blacklist",
    "storages",
    "ckeditor",
]

# local apps list
LOCAL_APPS = [
    "apps.utility",
    "apps.accounts",
    "apps.business",
]

# Add all apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "corsheaders.middleware.CorsPostCsrfMiddleware",
]

ROOT_URLCONF = "wqtah.urls"

PROJECT_TEMPLATES = [
    join(BASE_DIR, "templates"),
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": PROJECT_TEMPLATES,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "wqtah.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASES_NAME"),
        "USER": os.getenv("DATABASES_USER"),
        "PASSWORD": os.getenv("DATABASES_PASSWORD"),
        "HOST": os.getenv("DATABASES_HOST"),
        "PORT": os.getenv("DATABASES_PORT"),
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = "static/"

# the URL for media files
MEDIA_URL = "/media/"
MEDIA_ROOT = "media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# rest framework settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "EXCEPTION_HANDLER": "apps.utility.custom_exception.custom_exception_handler",
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.CoreJSONRenderer",
        "rest_framework_swagger.renderers.SwaggerUIRenderer",
        "rest_framework_swagger.renderers.OpenAPIRenderer",
    ),
}


# SWAGGER-CONFIGURATION
SWAGGER_SETTINGS = {
    "exclude_namespaces": [],
    "api_version": "0.1",
    "api_path": "/",
    "enabled_methods": ["get", "post", "put", "patch", "delete"],
    "api_key": "",
    "is_authenticated": True,
    "is_superuser": False,
    "SECURITY_DEFINITIONS": {
        "api_key": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        },
    },
}

AUTH_USER_MODEL = "accounts.User"

# SMS Configuration for TWILIO account

TWILIO_ACCOUNT_SID = "AC3cf5aba6cbb981eb723ebd6dc1f10741"
TWILIO_AUTH_TOKEN = "88d019fea19082be9dd46e958630c164"
TWILIO_SERVICE_SID = "VA95ebe44d200d769f835b69090592769c"
TWILIO_FROM_CONTACT = +16205688328


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}


CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)
CORS_ALLOW_CREDENTIALS = True


# define SECURE PROXY SSL HEADER
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Azure S3 setup
AZURE_STORAGE_NAME = os.getenv("AZURE_STORAGE_NAME")
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")
DEFAULT_FILE_STORAGE = "apps.utility.storage_backend.CustomFileStorage"


# sendgrid config

# SENDGRID_API_KEY = "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"


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_HOST_USER = "apikey"  # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = os.getenv("SENDGRID_API_KEY")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
