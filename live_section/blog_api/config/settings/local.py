import os  # noqa: F401

from .base import *  # noqa: F403

DEBUG = os.getenv("DEBUG", True)

# CORS
# ALLOWED_HOSTS = ['mydomain.com'] # 실제로 배포할 때,
ALLOWED_HOSTS = ["*"]  # 로컬 개발용

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
        "CONN_MAX_AGE": 60,
    }
}
