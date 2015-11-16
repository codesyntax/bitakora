
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

STATIC_ROOT = '/var/csmant/django/blogak/static'
MEDIA_ROOT = '/var/csmant/django/blogak/media'

USE_X_FORWARDED_HOST = True
