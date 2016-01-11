
DEBUG = True

DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bitakora',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'CodeSyntax',                  # Not used with sqlite3.
        'HOST': 'mysql.cs',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/var/csmant/django/bitakora/static'
MEDIA_ROOT = '/var/csmant/django/bitakora/media'

BITAKORA_CUSTOM_CSS = STATIC_URL + 'css/blogakeus.css'
BITAKORA_CUSTOM_LOGO = STATIC_URL + 'img/custom/logoa_blogak.gif'
BITAKORA_CUSTOM_MINILOGO = STATIC_URL + 'img/custom/b_bitakora.gif'
BITAKORA_CUSTOM_FAVICON = STATIC_URL + 'img/custom/favicon.ico'
PROFILE_PHOTO_DEFAULT = 'no-profile-photo'

USE_X_FORWARDED_HOST = True


#Twitter API
SOCIAL_AUTH_TWITTER_KEY  = 'CkxrjLUeSbjHzW7E6weeAg'
SOCIAL_AUTH_TWITTER_SECRET = 'zzas9crKEF4KXiPqLzclMkXX49LacZmiUpFvgb9dE'
REQUEST_TOKEN = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN = '1488991-OmNAXMFDdXdLnmeu1QP6YJsIo7KhFgR1XXr0Il2Nd3'
AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'


#Facebook API
SOCIAL_AUTH_FACEBOOK_KEY = '1673433789572685'
SOCIAL_AUTH_FACEBOOK_SECRET = '647c84b17acc7851281201dddf0287'

SOCIAL_AUTH_USER_MODEL = 'accounts.BitakoraUser'