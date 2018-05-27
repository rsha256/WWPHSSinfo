# Development settings
# start devserver by ./runserver.sh

import os
from WWPHSSinfo.settings import BASE_DIR

# SECURITY WARNING: keep the keys used in production secret!
# The following keys are different in production
SECRET_KEY = ')g0y@6p&3@j&1#7t4$9rmyw+9)mn23-mbsafp#%@ba)@_oeee!'
GAUTH_KEY = "732452235079-v9irvkidft14sh1fbkd58o9jp7449knj.apps.googleusercontent.com"
GAUTH_SECRET = "CI9SpGfbUSH92NLe-wepj9Vp"


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'info',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'query_debug.log')
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['file'],
        }
    }
}
