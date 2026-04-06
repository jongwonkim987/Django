from config.settings.base import *

DEBUG = True

ALLOWED_HOSTS = []

# Static
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / ".static_root"

# Media
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": SECRET["DB"]["NAME"],
        "USER": SECRET["DB"]["USER"],
        "PASSWORD": SECRET["DB"]["PASSWORD"],
        "HOST": SECRET["DB"]["HOST"],
        "PORT": SECRET["DB"]["PORT"],
    }
}
