"""
Settings para despliegue en PythonAnywhere (plan gratuito).
Usa SQLite y configura correctamente el proxy HTTPS de PythonAnywhere.
"""
from .base import *
import os

DEBUG = False

# PythonAnywhere gestiona HTTPS via proxy — no redirigir a nivel Django
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

# SQLite para plan gratuito de PythonAnywhere (no incluye PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
