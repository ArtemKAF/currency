from os import environ
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = environ.get("SECRET_KEY", "default")

DEBUG = environ.get("DEBUG", "FALSE").upper() == "TRUE"

ALLOWED_HOSTS = environ.get("ALLOWED_HOSTS", "localhost").split(",")


INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "currency.apps.CurrencyConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

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

ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = "config.wsgi.application"

if environ.get("USE_SQLITE", "FALSE").upper() == "TRUE":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": environ.get("POSTGRES_DB", "default"),
            "USER": environ.get("POSTGRES_USER", "default"),
            "PASSWORD": environ.get("POSTGRES_PASSWORD", "default"),
            "HOST": environ.get("POSTGRES_HOST", "localhost"),
            "PORT": environ.get("POSTGRES_PORT", 5432),
        }
    }


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


LANGUAGE_CODE = "ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static/",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REDIS_URI = environ.get("REDIS_URI", "redis://localhost:6379")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [{"address": REDIS_URI}],
        },
    },
}

CURRENCY_API_URL = environ.get("CURRENCY_API_URL", "http://localhost/")
CURRENCY_API_KEY = environ.get("CURRENCY_API_KEY", "")
CURRENCY_API_PARAMETERS = environ.get("CURRENCY_API_PARAMETERS", "")
CURRENCY_API_COMPLITE_URL = (
    f"{CURRENCY_API_URL}?{CURRENCY_API_PARAMETERS}&key={CURRENCY_API_KEY}"
)

CELERY_BROKER_URL = REDIS_URI
CELERY_RESULT_BACKEND = REDIS_URI
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BEAT_SCHEDULE = {
    "get_currency_rate_task": {
        "task": "currency.tasks.get_currency_task",
        "args": (CURRENCY_API_COMPLITE_URL,),
        "schedule": 30.0,
        "options": {
            "expires": 25.0,
        },
    },
}
