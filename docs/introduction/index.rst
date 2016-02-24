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

Customization
=============

Run Bitakora
============
::
    ./bin/django runserver 0:8080
