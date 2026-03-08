from .base import *

DEBUG = True

INSTALLED_APPS += ['django.contrib.admindocs']

# Usar SQLite en desarrollo si no hay PostgreSQL configurado
import os
if os.environ.get('USE_SQLITE', 'True').lower() == 'true':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Permitir devtunnels para pruebas con clientes
CSRF_TRUSTED_ORIGINS = ['https://*.devtunnels.ms', 'https://*.serveousercontent.com']
