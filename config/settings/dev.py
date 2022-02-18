from .base import *

DEBUG = True

SECRET_KEY = 'django-insecure-n3!ccn5(gz!9)($x(#h#_kfj#qm%2)))-z+=lrz6)3&ajr*r57'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vodomat_server',
        'USER': 'vodomat',
        'PASSWORD': 'vodomat',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

AUTH_PASSWORD_VALIDATORS = []
