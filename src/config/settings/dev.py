from .base import *

DEBUG = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{os.getenv("REDIS_HOST_TEST")}:{os.getenv("REDIS_PORT_TEST")}',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / '..' / 'database' / 'db.sqlite3',
    },
    'vodomat_server': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME_TEST'),
        'USER': os.getenv('DATABASE_USER_TEST'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD_TEST'),
        'HOST': os.getenv('DATABASE_HOST_TEST'),
        'PORT': os.getenv('DATABASE_PORT_TEST'),
    }
}

REDIS_HOST = os.getenv('REDIS_HOST_TEST')

AUTH_PASSWORD_VALIDATORS = []
