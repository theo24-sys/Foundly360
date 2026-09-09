from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = [host.strip().removeprefix("https://").removeprefix("http://").rstrip("/") for host in os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if host.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "django_filters",
    "rest_framework",
    "apps.core",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"

database_url = os.getenv("DATABASE_URL")
if not DEBUG and not database_url:
    raise RuntimeError("DATABASE_URL must be configured when DJANGO_DEBUG=0.")

DATABASES = {"default": dj_database_url.config(
    default=database_url or f"postgresql://{os.getenv('POSTGRES_USER', 'foundry360')}:{os.getenv('POSTGRES_PASSWORD', 'foundry360')}@{os.getenv('POSTGRES_HOST', 'localhost')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'foundry360')}",
    conn_max_age=600,
    ssl_require=not DEBUG,
)}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Nairobi"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CORS_ALLOWED_ORIGINS = [origin.strip().rstrip("/") for origin in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",") if origin.strip()]
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.redis.RedisCache", "LOCATION": os.getenv("REDIS_URL", "redis://127.0.0.1:6379/1")}}
CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CSRF_TRUSTED_ORIGINS = [origin.strip().rstrip("/") for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",") if origin.strip()]

R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT_URL", "")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME", "")
AWS_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY", "")
AWS_S3_ENDPOINT_URL = R2_ENDPOINT_URL
AWS_STORAGE_BUCKET_NAME = R2_BUCKET_NAME
AWS_S3_REGION_NAME = "auto"
AWS_QUERYSTRING_AUTH = True
AWS_QUERYSTRING_EXPIRE = 900
