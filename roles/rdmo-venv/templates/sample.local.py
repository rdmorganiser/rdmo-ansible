# {{ ansible_managed }}
import os
from . import BASE_DIR

DEBUG = False
VENDOR_CDN = False


SECRET_KEY = '{{ rdmo_secret_key }}'
ALLOWED_HOSTS = ['localhost', 'ip6-localhost', '127.0.0.1', '[::1]', '{{ rdmo_canonical_hostname }}']

LANGUAGE_CODE = 'de-de'
TIME_ZONE = 'Europe/Berlin'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ rdmo_user }}',
        'USER': '{{ rdmo_user }}',
        'PASSWORD': '{{ rdmo_postgres_password }}',
        'HOST': '{{ postgres_server }}',
{% if postgres_port != '' %}
        'PORT': '{{ postgres_port }}',
{% endif %}
        #DEBUG: {{ (postgres_disable_tls | bool) }}
        'OPTIONS': {'sslmode': '{{ ((postgres_disable_tls | bool) == True) | ternary('disable', 'verify-full') }}'},
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = '{{ rdmo_mail_server }}'
{% if rdmo_mail_port != '' %}
EMAIL_PORT = '{{ rdmo_mail_port }}'
{% endif %}
{% if rdmo_mail_user != '' %}
EMAIL_HOST_USER = '{{ rdmo_mail_user }}'
{% endif %}
{% if rdmo_mail_pass != '' %}
EMAIL_HOST_PASSWORD = '{{ rdmo_mail_pass }}'
{% endif %}
EMAIL_USE_SSL = '{{ ((rdmo_mail_disable_ssl | bool) == True) | ternary('False', 'True') }}'
EMAIL_USE_TLS = '{{ ((rdmo_mail_disable_tls | bool) == False) | ternary('True', 'False') }}' #fixme
DEFAULT_FROM_EMAIL = '{{ rdmo_mail_address }}'

from rdmo.core.settings import INSTALLED_APPS, AUTHENTICATION_BACKENDS

ACCOUNT = True
SOCIALACCOUNT = True

INSTALLED_APPS += [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.orcid',
]

AUTHENTICATION_BACKENDS.append('allauth.account.auth_backends.AuthenticationBackend')

{% if theme is defined %}

from rdmo.core.settings import INSTALLED_APPS
THEME_DIR = os.path.join(BASE_DIR, 'theme')
INSTALLED_APPS = ['theme'] + INSTALLED_APPS

{% endif %}

from django.utils.translation import ugettext_lazy as _
EXPORT_FORMATS = (
    ('pdf', _('PDF')),
    ('odt', _('Open Office')),
    ('docx', _('Microsoft Office')),
    ('html', _('HTML')),
    ('markdown', _('Markdown')),
    ('tex', _('LaTeX'))
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'rdmo_default'
    },
    'api': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'KEY_PREFIX': 'rdmo_api'
    }
}

LOGGING_DIR = '{{ rdmo_home }}/rdmo-app/log'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s: %(message)s'
        },
        'name': {
            'format': '[%(asctime)s] %(levelname)s %(name)s: %(message)s'
        },
        'console': {
            'format': '[%(asctime)s] %(message)s'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'error_log': {
            'level': 'ERROR',
            'class':'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'error.log'),
            'formatter': 'default'
        },
        'rdmo_log': {
            'level': 'DEBUG',
            'class':'logging.FileHandler',
            'filename': os.path.join(LOGGING_DIR, 'rdmo.log'),
            'formatter': 'name'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins', 'error_log'],
            'level': 'ERROR',
            'propagate': True
        },
        'rdmo': {
            'handlers': ['rdmo_log'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
