
import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG
EMAIL_SUBJECT_PREFIX = '[bitakora]'
DEFAULT_FROM_EMAIL = ''

ADMINS = (
     ('Your-name', 'your-email@codesyntax.com'),
)

MANAGERS = ADMINS

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
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
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
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

STATIC_ROOT = '/django/bitakora/static'
MEDIA_ROOT = '/django/bitakora/media'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django_mobile.loader.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination_bootstrap.middleware.PaginationMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
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
    'django_social_share',
    'social.apps.django_app.default',
    'registration',
    'voting',
    'captcha',
    'photologue',
    'sortedm2m',
    'tinymce',
    'haystack',
    'bootstrapform',
    'pagination_bootstrap',
    'contact_form',
    'gunicorn',
    'bitakora',
    'bitakora.accounts',
    'bitakora.base',
    'bitakora.rss',
    'django_mobile',
    'bitakora.photologue_custom',
)

TEMPLATE_CONTEXT_PROCESSORS = (
   "django.contrib.auth.context_processors.auth",
   "django.core.context_processors.debug",
   "django.core.context_processors.i18n",
   "django.core.context_processors.request",
   "django.core.context_processors.media",
   "django.core.context_processors.static",
   "bitakora.context_processors.bitakora_custom",
   "django_mobile.context_processors.flavour",
)

ACCOUNT_ACTIVATION_DAYS = 5

AUTH_USER_MODEL = "accounts.BitakoraUser"

SECRET_KEY = ''

RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
NOCAPTCHA = True

AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'cssocialuser.models.get_user_data',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

ALLOWED_HOSTS = ("127.0.0.1",)

TINYMCE_JS_URL = STATIC_URL + 'js/tinymce/tinymce.min.js'
TINYMCE_JS_ROOT = STATIC_ROOT + 'js/tinymce/tinymce.min.js'

try:
   from tiny_mce_settings import *
except:
   pass

try:
    from server_settings import *
except:
    pass

try:
    from local_settings import *
except:
    pass
