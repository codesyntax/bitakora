#############################
Getting started with Bitakora
#############################

Dependencies
============

- MySQL-python
- Sphinx
- elasticsearch
- lxml
- Pillow
- argparse
- csdjango.contactform
- akismet
- django-photologue
- django-tinymce
- django-pagination-bootstrap
- django-bootstrap-form
- django-recaptcha
- django-registration-redux
- django-voting
- django-haystack
- python-social-auth
- django-social-share
- django-easy-select2
- django-contact-form
- django-mobile
- boto
- django-storages
- cssocialuser
- bitakora
- gunicorn

Installation
============
Create your workbench:
::

    mkdir bitakora
    cd bitakora
    mkdir buildout
    cd buildout
    virtualenv .
    ./bin/pip install zc.buildout

Configuration
=============

- RECAPTCHA_PUBLIC_KEY
- RECAPTCHA_PRIVATE_KEY
- NOCAPTCHA: By default True
- BITAKORA_SEND_MAIL
- BITAKORA_CUSTOM_CSS
- BITAKORA_CUSTOM_LOGO
- BITAKORA_CUSTOM_MINILOGO
- BITAKORA_CUSTOM_FAVICON
- BITAKORA_TWITTER_USER
- BITAKORA_GA
- PROFILE_PHOTO_DEFAULT: By default 'no-profile-photo'
- SOCIAL_AUTH_TWITTER_KEY
- SOCIAL_AUTH_TWITTER_SECRET
- SOCIAL_TWITTER_ACCESS_TOKEN
- SOCIAL_TWITTER_ACCESS_TOKEN_SECRET
- SOCIAL_AUTH_FACEBOOK_KEY
- SOCIAL_AUTH_FACEBOOK_SECRET

Customization
=============

Run Bitakora
============
::

    ./bin/django runserver 0:8080
