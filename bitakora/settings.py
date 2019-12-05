import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG
EMAIL_SUBJECT_PREFIX = "[bitakora]"
DEFAULT_FROM_EMAIL = ""

ADMINS = (("Your-name", "your-email@codesyntax.com"),)

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        "NAME": "",  # Or path to database file if using sqlite3.
        "USER": "",  # Not used with sqlite3.
        "PASSWORD": "",  # Not used with sqlite3.
        "HOST": "",  # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",  # Set to empty string for default. Not used with sqlite3.
    }
}

TIME_ZONE = "Europe/Madrid"
FIRST_DAY_OF_WEEK = 1
DATE_FORMAT = "Y-m-d"
TIME_FORMAT = "H:i"
DATETIME_FORMAT = "Y-m-d H:i"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"
LANGUAGES = (("en", "English"),)

SITE_ID = 2

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATIC_ROOT = "/django/bitakora/static"
MEDIA_ROOT = "/django/bitakora/media"


MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "pagination_bootstrap.middleware.PaginationMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
]

ROOT_URLCONF = "bitakora.urls"


INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.contrib.flatpages",
    "django.contrib.humanize",
    "django.contrib.admin",
    "django_social_share",
    "sortedm2m",
    "photologue",
    "voting",
    "captcha",
    "tinymce",
    "haystack",
    "bootstrapform",
    "pagination_bootstrap",
    "contact_form",
    "gunicorn",
    "django_user_agents",
    "bitakora",
    "bitakora.accounts",
    "bitakora.base",
    "bitakora.rss",
    "bitakora.photologue_custom",
    "bitakora.contact",
    "bitakora.ikasbloga",
    "registration",
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'bitakora.context_processors.bitakora_custom',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                # insert your TEMPLATE_LOADERS here
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ]
        },
    },
]

ACCOUNT_ACTIVATION_DAYS = 5

AUTH_USER_MODEL = "accounts.BitakoraUser"

REGISTRATION_FORM = "bitakora.accounts.forms.RegistrationForm"
INCLUDE_REGISTER_URL = False

SECRET_KEY = "+ajg=l4%nzc&via@*qbb3@oi^awf+6*qc_*4yo##$&*mez#7wu"

RECAPTCHA_PUBLIC_KEY = ""
RECAPTCHA_PRIVATE_KEY = ""
NOCAPTCHA = True

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
)

HAYSTACK_CONNECTIONS = {
    "default": {"ENGINE": "haystack.backends.simple_backend.SimpleEngine"}
}

SESSION_COOKIE_AGE = 63000000

ALLOWED_HOSTS = ("127.0.0.1", "beta.blogak.eus", "blogak.eus", "www.blogak.eus")
AKISMET_API_KEY = ""

try:
    from .tiny_mce_settings import *
except:
    pass

try:
    from .server_settings import *
except:
    pass

try:
    from bitakora.s3storage.settings_s3boto import *
except:
    pass

try:
    from .local_settings import *
except:
    pass

TINYMCE_JS_URL = STATIC_URL + "js/tinymce/tinymce.min.js"
TINYMCE_JS_ROOT = STATIC_ROOT + "js/tinymce/tinymce.min.js"
