from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-4%j$!0-vq^x#rvui-fbi$uzoulk43^7(p!e$o6=xmksg%%#anj"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
    },
}

try:
    from .local import *
except ImportError:
    pass
