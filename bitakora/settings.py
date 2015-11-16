
import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG
EMAIL_SUBJECT_PREFIX = '[bitakora]'

ADMINS = (
     ('Your-name', 'your-email@codesyntax.com'),
)

MANAGERS = ADMINS

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bitakora',                      # Or path to database file if using sqlite3.
        'USER': 'bitakora_user',                      # Not used with sqlite3.
        'PASSWORD': 'bitakora_pass',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = 'Europe/Madrid'
FIRST_DAY_OF_WEEK = 1
DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'H:i'
DATETIME_FORMAT = 'Y-m-d H:i'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'eu'
LANGUAGES = (
    ('eu', 'Euskara'),
)


SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = '/home/csmant/django/bitakora/static'
MEDIA_ROOT = '/home/csmant/django/bitakora/media'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    )

ROOT_URLCONF = 'bitakora.urls'

TEMPLATE_DIRS = (
	os.path.join(os.path.dirname(__file__), "templates"),
)

my_media_url=os.path.join(os.path.dirname(__file__), "media")


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'photologue',
    'sortedm2m',
    'bitakora',
    'bitakora.accounts',
    'bitakora.base',
    'gunicorn',
)

TEMPLATE_CONTEXT_PROCESSORS = (
   "django.contrib.auth.context_processors.auth",
   "django.core.context_processors.debug",
   "django.core.context_processors.request",
   "django.core.context_processors.media",
   "django.core.context_processors.static",
)


AUTH_USER_MODEL = "accounts.BitakoraUser"

try:
   from tiny_mce_settings import *
except:
   pass


SECRET_KEY = '1569ac8rkf25@10mv*wgkg8n=4m1--rfqm3e+kwbda!xd(m!'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

try:
    from server_settings import *
except:
    pass

try:
    from local_settings import *
except:
    pass
