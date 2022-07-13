from .base import *
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': '123456789',
        'HOST': 'localhost',
        'PORT': '',
    }
}
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1"]
MIDDLEWARE += [
    "silk.middleware.SilkyMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INSTALLED_APPS += [
    "silk",
    "debug_toolbar",
]
INTERNAL_IPS = [
    "127.0.0.1",
]

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": config("DB_NAME"),
#         "USER": config("DB_USER"),
#         "PASSWORD": config("DB_PASSWORD"),
#         "HOST": config("DB_HOST"),
#     }
# }
