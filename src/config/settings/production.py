from .base import *

DEBUG = False

CSRF_TRUSTED_ORIGINS = ['https://admin.roganska.com']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{os.getenv("REDIS_HOST")}:{os.getenv("REDIS_PORT")}',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'database' / 'db.sqlite3',
    },
    'vodomat_server': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}

REDIS_HOST = os.getenv('REDIS_HOST')

AUTH_PASSWORD_VALIDATORS = []
