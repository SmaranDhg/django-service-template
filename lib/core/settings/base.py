import os
from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

SECRET_KEY = "django-insecure-m6f1nia^o1^6a_z4l1+!f@al$%=e-axbhanqn*m63)q_gsvdd0"


DEBUG = True

ALLOWED_HOSTS = ["*"]


# Multitenant Settings
SHARED_APPS = [
    "django_tenants",
    "django.contrib.admin",
    "drf_yasg",
    "lib.shared.authentication",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
TENANT_APPS = [
    "lib.apps.assessment_management",
    "lib.apps.patient_management",
]


DATABASE_ROUTERS = [
    "django_tenants.routers.TenantSyncRouter",
]
TENANT_MODEL = "authentication.Tenant"  # app.Model

TENANT_DOMAIN_MODEL = "authentication.TenantDomain"  # app.Model


PUBLIC_SCHEMA_NAME = "public"


INSTALLED_APPS = SHARED_APPS + TENANT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "lib.core.middleware.TenantMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
AUTH_USER_MODEL = "authentication.User"


ROOT_URLCONF = "lib.core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "lib.core.wsgi.application"


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


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_ROOT = os.path.join(STATIC_BASE_DIR, "static")
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    # os.path.join(STATIC_BASE_DIR, "static"),
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# JWT Settings
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
}


# CORs Settings
CORS_ALLOW_HEADERS = [
    "X-API-Key",
    "X-API-Timestamp",
    "X-API-Signature",
]

# Swagger settings
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "api_key": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
}
